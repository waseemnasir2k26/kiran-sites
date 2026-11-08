---
name: pr-review
description: Review a Kiran Studio pull request against checks.md and the site checker. Use on every pull request.
allowed-tools: Read, Grep, Glob, Bash(git diff *), Bash(python3 scripts/check-site.py *), mcp__github_inline_comment__create_inline_comment
---

# Kiran Studio PR review

You are the reviewer. You never edit files. FAIL by default: approve only what you checked.

1. Find the files this pull request changes: `git diff --name-only HEAD^1 HEAD`
2. Read `checks.md` (the agency rules).
3. For every client site the pull request touches (a file under `sites/<client>/`, or `shared/footer.html`, which touches all three), run `python3 scripts/check-site.py <client>`.
4. For each failing check or broken rule, post ONE inline comment on the exact changed line that causes it, using `mcp__github_inline_comment__create_inline_comment`. Say what is wrong and what the data file says. If the problem is not on a changed line, put it in the problems list only.
5. Finish with your verdict:
   - `APPROVED` only if every touched site passes `check-site.py` and no rule in `checks.md` is broken.
   - Otherwise `REJECTED`, with one short line per problem.
