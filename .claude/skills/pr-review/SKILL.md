---
name: pr-review
description: Review a Kiran Studio pull request against checks.md and the site checker. Use on every pull request.
allowed-tools: Read, Grep, Glob, Bash(git diff *), Bash(python3 scripts/check-site.py *), mcp__github_inline_comment__create_inline_comment
---

# Kiran Studio PR review

You are the reviewer. You never edit files. FAIL by default: approve only what you checked.

1. Find the files this pull request changes: `git diff --name-only HEAD^1 HEAD`
2. Read `checks.md` (the agency rules).
3. For every client the pull request touches (a file under `sites/<client>/`), run `python3 scripts/check-site.py <client>`. If it changes `shared/footer.html`, read it: one line, no email address, no phone number other than +92 300 0000000.
4. Always leave your result on the pull request with `mcp__github_inline_comment__create_inline_comment`:
   - one inline comment per problem, on the exact changed line that causes it: what is wrong and what the data file says;
   - if there are no problems, one inline comment on the first changed line: `APPROVED: <client> passes check-site.py (6/6) and checks.md`.
   If you cannot post, say so in your final answer.
5. Finish with your verdict:
   - `APPROVED` only if every touched site passes `check-site.py` and no rule in `checks.md` is broken.
   - Otherwise `REJECTED`, with one short line per problem.
