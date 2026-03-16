Title: Hard-coded AWS secret found in `secret_leak.py`

Severity: High

Affected files:
- `secret_leak.py`

Summary:
A hard-coded AWS secret key literal was found in the repository (was present in
`secret_leak.py`). Keeping secrets in source code risks accidental exposure
(e.g., pushing to remote, forks, code search, or logs) and can lead to
compromise of cloud resources.

Why this is a risk:
- Secrets checked into source control can be copied or leaked easily.
- Even if the current value is a test/fake key, the pattern encourages unsafe
  practices and may lead to real credentials being committed in the future.
- Automated scanners and attackers routinely search repos for patterns like
  `AKIA` (AWS access keys) and `SECRET_KEY`.

Suggested remediation (priority order):
1. Remove the secret from the repository and replace it with a reference to an
   environment variable or a secrets manager (already applied in the code).
2. Rotate the exposed secret (if it was real) immediately and audit access logs.
3. Add the repository and the specific key to any internal incident response
   tracking so rotation and mitigation can be verified.
4. Add a pre-commit secret-scanning hook (e.g., `pre-commit` + `detect-secrets`)
   and enable secret scanning in repo settings (GitHub has a built-in secret
   scanning feature for private repos / GitHub Advanced Security).
5. Add a short contributor guideline reminding developers not to commit
   secrets and to use environment variables or vaults.

Quick remediation steps (commands you can run locally):
```powershell
# 1) Remove the secret from working tree (if still present locally)
git rm --cached secret_leak.py
# 2) Commit the removal or the change that replaced the literal
git add secret_leak.py
git commit -m "Remove hard-coded AWS secret; use env var"
# 3) Push to remote and create a PR for review
git push -u origin security/remove-hardcoded-secret
```

Notes:
- The code base now uses `AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')`
  and does not print the secret value. That mitigates accidental disclosure
  going forward, but if any real key had been present, it must be rotated.

Suggested labels for the GitHub Issue: security, high, secret-exposure

Prepared by: automated repository scan
Timestamp: 2026-03-16
