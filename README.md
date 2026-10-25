# Moss workspace

A pnpm monorepo using Vite+. The React application is the `@moss/app` workspace
package in `app/`, built with Void and configured for self-hosting on Node.js.
The VS Code theme package lives in `vscode/`; see its [README](vscode/README.md).
Additional packages belong in `packages/`. See [SPEC.md](SPEC.md) for the product
specification.

Node.js 24.22.1 and pnpm 12.15.0 are pinned in `package.json`. With Vite+
available, run these commands from the repository root:

```sh
vp install
pnpm dev
pnpm check
pnpm build
pnpm start
```

Development serves the app at `http://localhost:5173`. The production server uses
`PORT`, defaulting to `3000`. Run the production command from this workspace, or
from `app/` with `pnpm start`. Deploy `app/dist/client` and `app/dist/ssr` together
alongside the application's production dependencies.
