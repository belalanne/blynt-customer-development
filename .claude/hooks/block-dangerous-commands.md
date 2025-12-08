---
event: PreToolUse
matchTools:
  - Bash
---

# Block Dangerous Commands

Check if the bash command is safe to execute.

**BLOCK these patterns:**
- `rm -rf /` or any recursive delete on root
- `sudo` commands
- Commands that modify system files
- Commands that could expose credentials
- `curl | bash` or `wget | bash` patterns

**ALLOW these patterns:**
- `pip install` / `pip3 install`
- `python` / `python3` commands
- `git` commands
- `npm` / `node` commands
- File listing (`ls`, `find`, `tree`)
- Environment checks (`env`, `which`, `whereis`)

If the command is dangerous, respond with:
```
BLOCK: This command could be harmful: [brief reason]
```

If the command is safe, respond with:
```
ALLOW
```
