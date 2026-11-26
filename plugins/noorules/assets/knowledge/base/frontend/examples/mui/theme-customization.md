# MUI Theme Customization Reference

## Purpose

Illustrate a typed Material UI theme assembled from project design tokens,
custom type augmentation and reusable component overrides.

## Applies when

Apply when the `mui` preset is selected and the project needs to create or
change its Material UI theme from an approved design contract.

## Does not apply when

Do not copy the placeholder token names or values, add custom variants without
a design requirement, or replace an existing project theme organization.

## Reference

Define only custom keys that the project design system actually needs:

```ts
// theme-contract.d.ts
import type { CSSProperties } from "react";

declare module "@mui/material/styles" {
  interface Palette {
    brandAccent: Palette["primary"];
  }

  interface PaletteOptions {
    brandAccent?: PaletteOptions["primary"];
  }

  interface TypeBackground {
    surfaceMuted: string;
  }

  interface TypographyVariants {
    labelLarge: CSSProperties;
  }

  interface TypographyVariantsOptions {
    labelLarge?: CSSProperties;
  }
}

declare module "@mui/material/Typography" {
  interface TypographyPropsVariantOverrides {
    labelLarge: true;
  }
}

declare module "@mui/material/Button" {
  interface ButtonPropsSizeOverrides {
    compact: true;
  }
}

export {};
```

Keep token groups typed and independently reviewable:

```ts
// theme/options.ts
import type {
  PaletteOptions,
  TypographyVariantsOptions,
} from "@mui/material/styles";

export const palette = {
  primary: {
    main: "#1D4ED8",
    contrastText: "#FFFFFF",
  },
  brandAccent: {
    main: "#7C3AED",
    contrastText: "#FFFFFF",
  },
  background: {
    default: "#F8FAFC",
    paper: "#FFFFFF",
    surfaceMuted: "#F1F5F9",
  },
  text: {
    primary: "#0F172A",
    secondary: "#475569",
  },
} satisfies PaletteOptions;

export const typography = {
  fontFamily: 'Inter, system-ui, -apple-system, "Segoe UI", sans-serif',
  h1: {
    fontSize: "2.5rem",
    fontWeight: 700,
    lineHeight: 1.2,
  },
  body1: {
    fontSize: "1rem",
    lineHeight: 1.5,
  },
  labelLarge: {
    fontSize: "0.875rem",
    fontWeight: 600,
    lineHeight: 1.25,
  },
} satisfies TypographyVariantsOptions;
```

Type reusable component configuration against the installed MUI contract:

```ts
// theme/components/button.ts
import type { Components } from "@mui/material/styles";

export const MuiButton = {
  defaultProps: {
    disableElevation: true,
  },
  variants: [
    {
      props: { size: "compact" },
      style: {
        minHeight: 32,
        paddingInline: 12,
      },
    },
  ],
  styleOverrides: {
    root: ({ theme }) => ({
      ...theme.typography.labelLarge,
      borderRadius: theme.shape.borderRadius,
      textTransform: "none",
    }),
  },
} satisfies Components["MuiButton"];
```

Compose the theme once at the application provider boundary:

```ts
// theme/theme.ts
import { createTheme } from "@mui/material/styles";
import { MuiButton } from "./components/button";
import { palette, typography } from "./options";

export const theme = createTheme({
  palette,
  typography,
  shape: {
    borderRadius: 12,
  },
  components: {
    MuiButton,
  },
});
```

```tsx
// AppThemeProvider.tsx
import CssBaseline from "@mui/material/CssBaseline";
import { ThemeProvider } from "@mui/material/styles";
import type { PropsWithChildren } from "react";
import { theme } from "./theme/theme";

export function AppThemeProvider({ children }: PropsWithChildren) {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      {children}
    </ThemeProvider>
  );
}
```

## Adaptation notes

- Replace placeholder colors, typography and sizing only from the approved
  design source, and verify contrast and interaction states after mapping them.
- Preserve the consuming project's provider location, module boundaries,
  naming and existing component override files.
- Add CSS custom properties only when non-MUI consumers need the same semantic
  tokens or highly dynamic values require them.
- Add dark mode or MUI color schemes only when the product owns a corresponding
  design contract, and verify the installed major-version API first.
- Keep router adapters, modal providers and other application integrations
  outside the reusable theme example.

## Checklist

- [ ] Custom theme keys are declared through module augmentation.
- [ ] Palette and typography options retain their installed MUI types.
- [ ] Component overrides use semantic tokens and typed public slots.
- [ ] The theme is created at a stable provider boundary.
- [ ] Placeholder values and structure were adapted to project context.
