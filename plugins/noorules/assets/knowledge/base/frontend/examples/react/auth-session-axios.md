# React SPA Axios Auth Session Reference

## Purpose

Show cookie-only and memory-access Axios transports with single-flight refresh,
bounded replay and a stable React provider lifecycle.

## Applies when

Apply when `axios` and React are installed, the project selected
`react-auth-session-reference`, and the browser calls the API directly without
a BFF.

## Does not apply when

Do not copy this reference into a BFF, use it to invent backend routes or error
contracts, or use memory-access when the API authenticates with cookies.

## Reference

The helpers below recognize only the project's explicit expired-access signal
and require unsafe requests to opt into replay.

```ts
import axios, {
  AxiosError,
  type AxiosInstance,
  type InternalAxiosRequestConfig,
} from "axios";

type AuthRequestConfig = InternalAxiosRequestConfig & {
  authRetry?: boolean;
  replayAfterRefresh?: boolean;
};

type ApiError = { code?: string };
type AccessResponse = { accessToken: string };
type SessionHooks = { onSessionLost: () => void };

const sessionPaths = new Set([
  "/session/login",
  "/session/refresh",
  "/session/logout",
]);
const safeMethods = new Set(["get", "head", "options"]);

const isExpiredAccess = (error: unknown): error is AxiosError<ApiError> =>
  axios.isAxiosError<ApiError>(error) &&
  error.response?.status === 401 &&
  error.response.data?.code === "access_expired";

const canReplay = (config: AuthRequestConfig) => {
  const method = config.method?.toLowerCase();
  return Boolean(
    method &&
      !sessionPaths.has(config.url ?? "") &&
      (safeMethods.has(method) || config.replayAfterRefresh === true),
  );
};

const csrfHeaders = (readCsrfToken: () => string) => ({
  "X-CSRF-Token": readCsrfToken(),
});

function installRefreshInterceptor(args: {
  api: AxiosInstance;
  refreshOnce: () => Promise<void>;
}) {
  const { api, refreshOnce } = args;

  api.interceptors.response.use(undefined, async (error: unknown) => {
    if (!isExpiredAccess(error) || !error.config) throw error;

    const original = error.config as AuthRequestConfig;
    if (original.authRetry || !canReplay(original)) throw error;

    original.authRetry = true;
    await refreshOnce();
    return api.request(original);
  });
}

function singleFlight(args: {
  refresh: () => Promise<void>;
  onSessionLost: () => void;
}) {
  let pending: Promise<void> | null = null;

  return () => {
    if (!pending) {
      pending = args
        .refresh()
        .catch((error: unknown) => {
          args.onSessionLost();
          throw error;
        })
        .finally(() => {
          pending = null;
        });
    }
    return pending;
  };
}
```

In cookie-only mode both tokens are server-set `HttpOnly` cookies. The client
never reads a token or creates an `Authorization` header.

```ts
export function createCookieSessionClient(args: {
  baseURL: string;
  readCsrfToken: () => string;
  hooks: SessionHooks;
}) {
  const api = axios.create({ baseURL: args.baseURL, withCredentials: true });
  const sessionApi = axios.create({
    baseURL: args.baseURL,
    withCredentials: true,
  });

  api.interceptors.request.use((config) => {
    if (!safeMethods.has(config.method?.toLowerCase() ?? "")) {
      Object.assign(config.headers, csrfHeaders(args.readCsrfToken));
    }
    return config;
  });

  const refreshOnce = singleFlight({
    refresh: async () => {
      await sessionApi.post(
        "/session/refresh",
        undefined,
        { headers: csrfHeaders(args.readCsrfToken) },
      );
    },
    onSessionLost: args.hooks.onSessionLost,
  });

  installRefreshInterceptor({ api, refreshOnce });

  return {
    api,
    bootstrap: async () => {
      await sessionApi.get("/session/csrf");
      return api.get("/session");
    },
    login: (credentials: { login: string; password: string }) =>
      sessionApi.post("/session/login", credentials, {
        headers: csrfHeaders(args.readCsrfToken),
      }),
    logout: async () => {
      try {
        await sessionApi.post("/session/logout", undefined, {
          headers: csrfHeaders(args.readCsrfToken),
        });
      } finally {
        args.hooks.onSessionLost();
      }
    },
  };
}
```

In memory-access mode only the refresh token is a server-set `HttpOnly` cookie.
The returned access token exists in the transport closure until reload or
session loss.

```ts
export function createMemoryAccessClient(args: {
  baseURL: string;
  readCsrfToken: () => string;
  hooks: SessionHooks;
}) {
  let accessToken: string | null = null;
  const api = axios.create({ baseURL: args.baseURL });
  const sessionApi = axios.create({
    baseURL: args.baseURL,
    withCredentials: true,
  });

  api.interceptors.request.use((config) => {
    if (accessToken) config.headers.Authorization = `Bearer ${accessToken}`;
    return config;
  });

  const loseSession = () => {
    accessToken = null;
    args.hooks.onSessionLost();
  };
  const refreshOnce = singleFlight({
    refresh: async () => {
      const response = await sessionApi.post<AccessResponse>(
        "/session/refresh",
        undefined,
        { headers: csrfHeaders(args.readCsrfToken) },
      );
      accessToken = response.data.accessToken;
    },
    onSessionLost: loseSession,
  });

  installRefreshInterceptor({ api, refreshOnce });

  return {
    api,
    bootstrap: async () => {
      await sessionApi.get("/session/csrf");
      return refreshOnce();
    },
    login: async (credentials: { login: string; password: string }) => {
      const response = await sessionApi.post<AccessResponse>(
        "/session/login",
        credentials,
        { headers: csrfHeaders(args.readCsrfToken) },
      );
      accessToken = response.data.accessToken;
    },
    logout: async () => {
      try {
        await sessionApi.post(
          "/session/logout",
          undefined,
          { headers: csrfHeaders(args.readCsrfToken) },
        );
      } finally {
        loseSession();
      }
    },
  };
}
```

Create the selected client once per application provider lifecycle. Bootstrap
before protected routes are considered authenticated, and centralize private
cache cleanup in the session-loss hook.

```tsx
function AuthProvider(props: { children: React.ReactNode }) {
  const [status, setStatus] = React.useState<
    "loading" | "authenticated" | "unauthenticated"
  >("loading");
  const queryClient = useQueryClient();
  const [client] = React.useState(() =>
    createCookieSessionClient({
      baseURL: apiBaseUrl,
      readCsrfToken,
      hooks: {
        onSessionLost: () => {
          queryClient.clear();
          setStatus("unauthenticated");
        },
      },
    }),
  );

  React.useEffect(() => {
    let active = true;
    client.bootstrap().then(
      () => active && setStatus("authenticated"),
      () => active && setStatus("unauthenticated"),
    );
    return () => {
      active = false;
    };
  }, [client]);

  return <AuthContext.Provider value={{ client, status }}>{props.children}</AuthContext.Provider>;
}
```

## Adaptation notes

- Replace routes, credentials, response schemas, CSRF transport and
  `access_expired` with the project-owned API contract.
- The CSRF bootstrap operation must establish a browser-readable CSRF value,
  never a JavaScript-readable access or refresh token.
- Validate login, refresh and session responses at runtime before changing
  authentication state.
- Mark an unsafe request `replayAfterRefresh: true` only after documenting
  reusable body semantics and the server's no-side-effect rejection guarantee.
- Add best-effort cross-tab coordination only with a server rotation design
  that remains safe when browser coordination fails.
- Test success, an expired-request burst, an ordinary `401`, refresh and replay
  failures, login, logout, reload bootstrap, a cross-tab rotation race and each
  explicitly replayable unsafe request.
- Replace `queryClient.clear()` with the project's precise user-scoped cache
  cleanup when public cache data should survive logout.
- Read the selected [React SPA auth-session rule](../../rules/stacks/react/auth-session.md)
  before adapting this example; it remains the owner of storage, CSRF,
  refresh and replay invariants.

## Checklist

- [ ] `axios` is installed and the chosen profile matches the API contract.
- [ ] The session client cannot invoke the protected-client interceptor.
- [ ] Concurrent expired requests share one refresh attempt.
- [ ] Ordinary `401` and repeated failures do not refresh recursively.
- [ ] Unsafe replay is explicit and justified.
- [ ] Reload bootstrap and final cache cleanup match route behavior.
