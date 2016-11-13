# Bash Script that checks for dependencies required by DigiDash
command -v libsdl2-dev >/dev/null 2>&1 || { echo >&2 "libsdl2-dev required. Abort."; exit 1; }
