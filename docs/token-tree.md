# Token-tree data

A workspace is `{ "version": 1, "nodes": { ... } }`. Node record keys are stable
identities. Every node has a `name`, `parentId`, and `kind` (`tree`, `group`, or
`token`). Exactly one tree has a null parent. Other parents must be trees or
groups. Names, including names with dots, are literal labels.

Tokens have a `fields` record containing at least `color`. Additional fields,
such as `background`, use the same source rules:

```json
{
  "source": { "kind": "local" },
  "values": { "dark": "#132118", "light": "#e9efeb" }
}
```

A reference names a token identity and field:

```json
{
  "source": { "kind": "reference", "tokenId": "canvas", "field": "color" },
  "values": {}
}
```

While linked, `values` is inactive local authoring history. Only `source` chooses
the active value. Missing appearances stay absent. Detach resolves both appearances
and records those colors as local values; it leaves absent appearances absent.

`app/src/example.json` is a complete sample workspace. **Import JSON** validates a
whole document before replacing the current workspace. **Import child tree** takes
the same format, attaches its root below the selected container, and rejects
identity collisions. Template references may point to fields in the destination
workspace, so mappings never depend on particular root token names.

The domain API in `app/src/tokens.ts` returns new validated documents. `putNode`
adds, renames, or moves a node; `putField`, `setColor`, `link`, and `detach` edit
fields. `removeNode` removes a subtree only when no surviving field references it.
Rejected operations leave their input unchanged. `readWorkspace` and
`writeWorkspace` validate JSON boundaries using the same rules.

`traceSource` follows explicit references and returns the terminal field and full
chain. `resolveColor` also takes an appearance and an optional source-value lookup.
That lookup is the integration point for external decisions, such as a rated
candidate; the tree model contains no tournament rules. `dependents` lists all
fields whose chains pass through the selected field.

Color input accepts CSS colors, including hex, RGB, OKLCH, and alpha. Resolution
converts to sRGB, clips channels to the displayable range, and quantizes to 8-bit
hex; opaque colors omit the alpha suffix. Authored input remains in the document.
This one conversion boundary supplies swatches and resolved outputs consistently.
