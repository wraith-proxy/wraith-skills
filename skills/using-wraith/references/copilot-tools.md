# Copilot CLI Tool Notes

| Action | Copilot CLI tool |
|---|---|
| Run a shell command | `bash` (Windows: `powershell`) |
| Read a file | `view` |
| Edit a file | `apply_patch` |
| Find files | `glob` |
| Search text | `rg` |
| Dispatch an agent | `task` |

## Built-in agents

`explore`, `task`, `code-review`, `general-purpose`, `research`.

## Skills and agents

- Skills load when relevant or through `/skills`.
- Custom agents are listed with `/agent`.
- Claude tool names in agent files map to Copilot aliases.
