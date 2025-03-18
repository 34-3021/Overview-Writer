# Overview Writer

Create `.env` and set `HTTP_BASE` in it.

Then, run `pnpm dev` to start the dev server.

In production environment, the `.env` will not be loaded. Please set the environment before running.

```bash
export NUXT_PUBLIC_HTTP_BASE="http://example.com/api"
```

```powershell
$env:NUXT_PUBLIC_HTTP_BASE="http://example.com/api"
```
