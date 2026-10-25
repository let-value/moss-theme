# Moss workspace

A pnpm monorepo using Vite+. The React application is the `@moss/app` workspace
package in `app/`, built with Void and configured for self-hosting on Node.js.
The VS Code theme package lives in `vscode/`; see its [README](vscode/README.md).
Additional packages belong in `packages/`. See [SPEC.md](SPEC.md) for the product
specification.

The app currently implements the token-tree slice: create and move trees, groups,
and tokens; edit dark/light colors; link individual color fields across trees;
trace affected uses; and detach or remove nodes with validation. **Load example**
opens an explicit sample with Base16, Zed, and VS Code child trees. A new workspace
starts empty. These child trees are editable data, not editor adapters.

Workspaces save in the browser and can be imported or exported as JSON. A stale
tab cannot overwrite a newer saved workspace; failed saves leave exportable work
in memory. The authoring page mounts on the client because its workspace is local
to the browser. See [the data format](docs/token-tree.md) for authoring files and
child-tree templates.

Node.js 24.22.1 and pnpm 12.15.0 are pinned in `package.json`. With Vite+
available, run these commands from the repository root:

```sh
vp install
pnpm dev
pnpm check
pnpm test
pnpm build
pnpm start
```

Development serves the app at `http://localhost:5173`. The production server uses
`PORT`, defaulting to `3000`. Run the production command from this workspace, or
from `app/` with `pnpm start`. Deploy `app/dist/client` and `app/dist/ssr` together
alongside the application's production dependencies.
