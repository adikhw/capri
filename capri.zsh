# Source this file from ~/.zshrc:
#   source /path/to/capri.zsh

# Resolved at source time, so it points to the folder containing this file
typeset -g CAPRI_SCRIPT="${0:A:h}/capri.py"

capri() {
    local result code

    # stdout is captured, stderr stays visible in the terminal
    result="$(python3 "$CAPRI_SCRIPT" "$@")"
    code=$?

    if [[ $code -eq 0 && -n "$result" && -d "$result" ]]; then
        cd "$result"
    else
        return $code
    fi
}