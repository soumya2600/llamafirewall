# Security Policy

## Supported Versions

| Version | Supported          |
|---------|--------------------|
| 3.1.x   | ✅ Active           |
| 3.0.x   | ⚠️ Upgrade required |
| < 3.0   | ❌ Not supported    |

---

## Reporting a Vulnerability

If you discover a security vulnerability in this project, **please do not open a public GitHub issue**.

Instead, report it responsibly:

1. **Email:** security@yourproject.com *(replace with your actual contact)*
2. **Subject:** `[SECURITY] Brief description`
3. **Include:**
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Any suggested remediation (optional)

We aim to acknowledge reports within **48 hours** and provide an initial assessment within **5 business days**.

---

## Security Measures in v3.1

### Authentication
- All API endpoints are protected by an `X-API-Key` header.
- Keys are compared using **constant-time comparison** (`secrets.compare_digest`) to prevent timing attacks.
- Set `API_KEY` in your `.env` file before deploying. Never commit real keys.

### Input Validation
- All incoming prompts are validated and sanitized via Pydantic validators.
- Maximum prompt length is enforced (default: 4,000 characters, configurable via `MAX_PROMPT_LEN`).
- Empty/whitespace-only prompts are rejected with HTTP 400.

### Rate Limiting
- Per-IP rate limiting is enforced (default: 60 requests/minute, configurable via `RATE_LIMIT_RPM`).
- Exceeding the limit returns HTTP 429.

### CORS
- `allow_origins` is restricted to explicitly configured origins (`ALLOWED_ORIGINS` env var).
- Wildcard `*` origins are **not permitted**.
- `allow_credentials` is set to `False` to prevent CSRF via cookie leakage.

### HTTP Security Headers
Every response includes:

| Header | Value |
|--------|-------|
| `X-Content-Type-Options` | `nosniff` |
| `X-Frame-Options` | `DENY` |
| `X-XSS-Protection` | `1; mode=block` |
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains` |
| `Content-Security-Policy` | `default-src 'none'` |
| `Referrer-Policy` | `no-referrer` |
| `Cache-Control` | `no-store` |

Server version headers (`Server`, `X-Powered-By`) are removed to prevent fingerprinting.

### Data Privacy
- **Raw prompt text is never stored in the database.** Only a SHA-256 hash of the prompt is persisted.
- **Client IP addresses are hashed** (SHA-256) before being stored in logs.
- Sensitive values are never returned in API error responses.

### Error Handling
- All unhandled exceptions are caught globally and return a generic `500 Internal Server Error`.
- Stack traces and internal error details are **never exposed to API clients** — they are logged server-side only.
- API/OpenAPI docs (`/docs`, `/redoc`, `/openapi.json`) are disabled in production (`ENABLE_DOCS=false`).

### Database
- All database queries use **parameterized statements** (no string interpolation) to prevent SQL injection.
- WAL mode is enabled for safer concurrent writes.
- `PRAGMA foreign_keys=ON` is enforced.

---

## Deployment Checklist

Before going live, verify:

- [ ] `API_KEY` is set to a strong random secret (min 32 hex chars)
- [ ] `ALLOWED_ORIGINS` lists only your actual frontend domains
- [ ] `ENABLE_DOCS=false` (default)
- [ ] The app is served over HTTPS (TLS termination at reverse proxy)
- [ ] `firewall.db` is stored outside the web root and not publicly accessible
- [ ] `.env` is excluded from version control (`.gitignore`)
- [ ] HuggingFace API key (`HF_API_KEY`) is rotated regularly if used
- [ ] The server runs as a non-root user
- [ ] Dependencies are kept up to date (`pip list --outdated`)

---

## Known Limitations

- The in-memory rate limiter resets on server restart. For production deployments with multiple workers, replace it with a Redis-backed limiter (e.g., `slowapi` + Redis).
- SQLite is suitable for low-to-medium traffic. For high-concurrency production use, migrate to PostgreSQL.

---

## Dependency Security

Run the following regularly to check for known vulnerabilities in dependencies:

```bash
pip install pip-audit
pip-audit
```

---

*Last updated: 2026-03-22*
