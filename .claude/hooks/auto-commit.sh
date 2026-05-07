#!/bin/bash
# Auto-commit hook for Claude Code PostToolUse event.
# Fires after Edit/Write/NotebookEdit tool calls to automatically commit changes.
#
# Input: JSON object from stdin
#   { "tool_name": "Edit", "tool_input": { "file_path": "..." } }
#   { "tool_name": "NotebookEdit", "tool_input": { "notebook_path": "..." } }

INPUT=$(cat)

# Extract file path and tool name via python (cross-platform, no jq dependency)
eval "$(echo "$INPUT" | python -c "
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

# Stage the file (handles adds, modifications, and deletions)
git add "$FILE_PATH" 2>/dev/null

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
