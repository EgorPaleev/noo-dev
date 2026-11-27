#!/bin/sh
set -eu

fail() {
    printf '%s\n' "$1" >&2
    exit 1
}

[ "$#" -eq 1 ] || fail 'Использование: prepare-run-storage.sh <id-запуска>'
case "$1" in
    [!a-z0-9]*|*[!a-z0-9-]*|'') fail 'Некорректный ID запуска.' ;;
esac
[ "${#1}" -le 64 ] || fail 'Некорректный ID запуска.'

root=$(git rev-parse --show-toplevel)
cd "$root"
run_dir=".noorules/runs/$1"
tracked=$(git ls-files -- "$run_dir")
[ -z "$tracked" ] || fail "В $run_dir уже есть файлы в индексе Git. Выбери другой ID запуска."

if git check-ignore -q -- "$run_dir/run.json" && git check-ignore -q -- "$run_dir/"; then
    printf '%s\n' "$run_dir"
    exit 0
fi

exclude=$(git rev-parse --git-path info/exclude)
pattern='/.noorules/runs/'
if [ ! -f "$exclude" ] || ! grep -Fqx -- "$pattern" "$exclude"; then
    mkdir -p "$(dirname "$exclude")"
    printf '\n%s\n' "$pattern" >> "$exclude"
fi
git check-ignore -q -- "$run_dir/run.json" && git check-ignore -q -- "$run_dir/" ||
    fail "Git не исключает $run_dir. Проверь действующие правила игнорирования."
printf '%s\n' "$run_dir"
