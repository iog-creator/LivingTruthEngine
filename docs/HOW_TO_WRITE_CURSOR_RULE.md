# How to Write a Cursor Rule (`.mdc`)

Cursor rules use YAML frontmatter + Markdown body. The only frontmatter Cursor needs is:

```yaml
---
description: <short, human description>   # required
globs: "src/**/*.ts"                      # optional; list or string — implies Auto-Attached
alwaysApply: true                         # optional; true implies Always
---
```

- **Always** → `alwaysApply: true`
- **Auto-Attached** → `globs:` present
- **Agent-Requested** → neither of the above; must include `description`

## Special case: `00-global.mdc`
- Must set `alwaysApply: true`
- `globs` is unnecessary

> This follows Cursor “Rules for AI” conventions where rule type is controlled by `description`, `globs`, and `alwaysApply`.

## Good example
```mdc
---
description: Global rule for Living Truth Engine (SSOT + enforcement)
alwaysApply: true
---
# Canon
...rule content...
```

## Commands
```bash
make rules-fix        # migrate to Cursor-spec frontmatter
make rules-validate   # fail-fast if any rule frontmatter is invalid
make enable-githooks  # block malformed rules at commit time
```
