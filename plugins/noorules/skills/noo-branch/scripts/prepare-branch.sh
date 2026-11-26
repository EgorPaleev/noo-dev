#!/bin/sh
set -eu

fail() {
    printf '%s\n' "$1" >&2
    exit 1
}

if [ "$#" -lt 2 ] || [ "$#" -gt 3 ]; then
    fail 'Использование: prepare-branch.sh <рабочая-ветка> <remote> [<базовая-ветка>]'
fi

branch=$1
remote=$2
base=${3-}

git check-ref-format --branch "$branch" >/dev/null
git remote get-url -- "$remote" >/dev/null
changes=$(git status --porcelain=v1 --untracked-files=no --ignore-submodules=none)
[ -z "$changes" ] || fail 'В рабочей копии есть незакоммиченные изменения отслеживаемых файлов.'

if git show-ref --verify --quiet "refs/heads/$branch"; then
    fail "Рабочая ветка $branch уже существует."
fi

if [ -z "$base" ]; then
    remote_head=$(git ls-remote --exit-code --symref -- "$remote" HEAD)
    base=$(printf '%s\n' "$remote_head" | awk '$1 == "ref:" && $2 ~ /^refs\/heads\// && $3 == "HEAD" { sub(/^refs\/heads\//, "", $2); print $2 }')
    [ -n "$base" ] || fail "Основная ветка remote $remote не определена. Укажи базовую ветку явно."
fi

base_ref="refs/heads/$base"
tracking_ref="refs/remotes/$remote/$base"
git check-ref-format "$base_ref"
git check-ref-format "$tracking_ref"
git fetch --no-tags --no-write-fetch-head -- "$remote" "+$base_ref:$tracking_ref"
base_commit=$(git rev-parse --verify "${tracking_ref}^{commit}")
git switch --no-track --no-overwrite-ignore -c "$branch" "$base_commit"
printf 'branch=%s\nremote=%s\nbase=%s\nbase_commit=%s\n' "$branch" "$remote" "$base" "$base_commit"
