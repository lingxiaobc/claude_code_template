#!/bin/bash
# Auto-commit hook for Claude Code PostToolUse event.
# Fires after Edit/Write/NotebookEdit tool calls to automatically commit changes.
#
# Input: JSON object from stdin
#   { "tool_name": "Edit", "tool_input": { "file_path": "..." } }
#   { "tool_name": "NotebookEdit", "tool_input": { "notebook_path": "..." } }

INPUT=$(cat)

# Extract file path and tool name via python (cross-platform, no jq dependency)
# Try python3 first, fall back to python
PY_CMD=""
python3 -c "pass" 2>/dev/null && PY_CMD=python3 || PY_CMD=python

eval "$(echo "$INPUT" | $PY_CMD -c "
import sys, json
try:
    data = json.load(sys.stdin)
    ti = data.get('tool_input', {})
    fp = ti.get('file_path', '') or ti.get('notebook_path', '')
    tn = data.get('tool_name', '')
    print(f'FILE_PATH={repr(fp)}')
    print(f'TOOL_NAME={repr(tn)}')
except:
    print('FILE_PATH=\"\"')
    print('TOOL_NAME=\"\"')
" 2>/dev/null)"

# Skip if no file path
[ -z "$FILE_PATH" ] && exit 0

# Must be inside a git repo
git rev-parse --git-dir > /dev/null 2>&1 || exit 0

# Skip files inside .git/ or .claude/settings.local.json
case "$FILE_PATH" in
  *.git/*|.git/*) exit 0 ;;
  */settings.local.json|settings.local.json) exit 0 ;;
esac

# Convert Windows-style paths to POSIX format for Git
case "$FILE_PATH" in
  [A-Za-z]:*)
    # Windows absolute path (e.g. P:\path) → convert via cygpath or manual
    POSIX_PATH=$(cygpath -u "$FILE_PATH" 2>/dev/null) || {
      # Fallback: convert drive letter manually (P:\ → /p/)
      DRIVE=$(echo "$FILE_PATH" | sed 's/^\([A-Za-z]\):.*/\1/' | tr '[:upper:]' '[:lower:]')
      REST=$(echo "$FILE_PATH" | sed 's/^[A-Za-z]:[\\\/]//')
      POSIX_PATH="/$DRIVE/${REST}\\"
    }
    FILE_PATH="$POSIX_PATH"
    ;;
esac

# Skip large files (>10MB)
if [ -f "$FILE_PATH" ] 2>/dev/null; then
  FILE_SIZE=$(stat -c%s "$FILE_PATH" 2>/dev/null || stat -f%z "$FILE_PATH" 2>/dev/null || echo 0)
  [ "$FILE_SIZE" -gt 10485760 ] 2>/dev/null && exit 0
fi

# Stage the file (handles adds, modifications, and deletions)
git add "$FILE_PATH" 2>/dev/null || {
  # Log staging failure but don't block the workflow
  echo "[auto-commit] Failed to stage: $FILE_PATH" >> .claude/hooks.log 2>/dev/null
  exit 0
}

# Check if there are actually staged changes
# For initial repo (no HEAD), just check if staged files exist
if git rev-parse HEAD > /dev/null 2>&1; then
  git diff --cached --quiet 2>/dev/null && exit 0
else
  [ -z "$(git diff --cached --name-only 2>/dev/null)" ] && exit 0
fi

# Build commit message based on tool type
BASENAME=$(basename "$FILE_PATH")
case "$TOOL_NAME" in
  Edit)         ACTION="update" ;;
  Write)        ACTION="create" ;;
  NotebookEdit) ACTION="update notebook" ;;
  *)            ACTION="modify" ;;
esac

git commit -m "auto: $ACTION $BASENAME" 2>/dev/null

exit 0
