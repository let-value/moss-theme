import type { FormEvent } from "react";
import {
  dependents,
  detach,
  link,
  putField,
  putNode,
  removeNode,
  resolveColor,
  setColor,
  traceSource,
  type Appearance,
  type PaletteNode,
  type Reference,
  type Workspace,
} from "./tokens";

interface Props {
  workspace: Workspace;
  selected: string;
  appearance: Appearance;
  edit: (operation: () => Workspace, selection?: string) => void;
  onSelect: (id: string) => void;
  onError: (message: string) => void;
}

function form(event: FormEvent<HTMLFormElement>) {
  event.preventDefault();
  const data = new FormData(event.currentTarget);
  return (name: string) => {
    const value = data.get(name);
    if (typeof value !== "string") throw new Error(`Missing form field: ${name}`);
    return value;
  };
}

export default function NodeEditor({
  workspace,
  selected,
  appearance,
  edit,
  onSelect,
  onError,
}: Props) {
  const node = workspace.nodes[selected];
  const targets = Object.entries(workspace.nodes).flatMap(([tokenId, entry]) =>
    entry.kind === "token" && tokenId !== selected
      ? Object.keys(entry.fields).map((field) => ({ tokenId, field }))
      : [],
  );
  const label = (reference: Reference) =>
    `${workspace.nodes[reference.tokenId].name} · ${reference.field} · ${reference.tokenId}`;
  return (
    <section className="inspector" aria-label="Selected node">
      <h2>{node.name}</h2>
      <p className="muted">
        {node.kind} · <code>{selected}</code>
      </p>
      <form
        onSubmit={(event) => {
          const data = form(event);
          edit(() =>
            putNode(workspace, selected, {
              ...node,
              name: data("name"),
              parentId: node.parentId === null ? null : data("parent"),
            }),
          );
        }}
      >
        <label>
          Name
          <input name="name" defaultValue={node.name} required />
        </label>
        {node.parentId !== null && (
          <label>
            Parent
            <select name="parent" defaultValue={node.parentId}>
              {Object.entries(workspace.nodes)
                .filter(([id, entry]) => id !== selected && entry.kind !== "token")
                .map(([id, entry]) => (
                  <option key={id} value={id}>
                    {entry.name} · {id}
                  </option>
                ))}
            </select>
          </label>
        )}
        <button>Save name and location</button>
        <button
          type="button"
          disabled={node.parentId === null}
          onClick={() => edit(() => removeNode(workspace, selected), node.parentId!)}
        >
          Remove node
        </button>
      </form>
      <form
        onSubmit={(event) => {
          const data = form(event);
          const id = crypto.randomUUID();
          const kind = data("kind") as PaletteNode["kind"];
          const child = {
            kind,
            name: data("name"),
            parentId: node.kind === "token" ? node.parentId : selected,
          };
          edit(
            () =>
              putNode(
                workspace,
                id,
                kind === "token"
                  ? {
                      ...child,
                      kind,
                      fields: { color: { source: { kind: "local" }, values: {} } },
                    }
                  : { ...child, kind },
              ),
            id,
          );
        }}
      >
        <h3>{node.kind === "token" ? "Add a sibling" : "Add a child"}</h3>
        <label>
          Kind
          <select name="kind">
            <option>token</option>
            <option>group</option>
            <option>tree</option>
          </select>
        </label>
        <label>
          Name
          <input name="name" required />
        </label>
        <button>Add node</button>
      </form>
      {node.kind === "token" && (
        <>
          {Object.entries(node.fields).map(([name, entry]) => {
            const reference = { tokenId: selected, field: name };
            const resolved = resolveColor(workspace, reference, appearance);
            const affected = dependents(workspace, reference);
            return (
              <article className="field" key={`${name}:${appearance}:${JSON.stringify(entry)}`}>
                <h3>{name}</h3>
                <p>
                  <span className="swatch" style={{ background: resolved.value }} />{" "}
                  <code>{resolved.value ?? `Unset in ${appearance}`}</code>
                </p>
                <p className="chain">{resolved.chain.map(label).join(" → ")}</p>
                <p className="muted">
                  Used by {affected.length} fields
                  {affected.length ? `: ${affected.map(label).join(", ")}` : ""}
                </p>
                {entry.source.kind === "local" ? (
                  <form
                    onSubmit={(event) => {
                      const value = form(event)("color").trim();
                      edit(() => setColor(workspace, reference, appearance, value || undefined));
                    }}
                  >
                    <label>
                      {appearance} color
                      <input
                        name="color"
                        defaultValue={entry.values[appearance] ?? ""}
                        placeholder="Hex, RGB, OKLCH; blank means unset"
                      />
                    </label>
                    <button>Set color</button>
                  </form>
                ) : (
                  <div className="actions">
                    <button
                      onClick={() => onSelect(traceSource(workspace, reference).source.tokenId)}
                    >
                      Edit source
                    </button>
                    <button onClick={() => edit(() => detach(workspace, reference))}>
                      Make independent
                    </button>
                  </div>
                )}
                <form
                  onSubmit={(event) => {
                    const target = JSON.parse(form(event)("target")) as Reference;
                    edit(() => link(workspace, reference, target));
                  }}
                >
                  <label>
                    Link to
                    <select name="target" required defaultValue="">
                      <option value="" disabled>
                        Choose a source field
                      </option>
                      {targets.map((target) => (
                        <option key={JSON.stringify(target)} value={JSON.stringify(target)}>
                          {label(target)} ·{" "}
                          {resolveColor(workspace, target, appearance).value ?? "Unset"}
                        </option>
                      ))}
                    </select>
                  </label>
                  <button disabled={!targets.length}>Link field</button>
                </form>
                {name !== "color" && (
                  <button onClick={() => edit(() => putField(workspace, reference, null))}>
                    Remove field
                  </button>
                )}
              </article>
            );
          })}
          <form
            onSubmit={(event) => {
              const name = form(event)("name").trim();
              if (Object.hasOwn(node.fields, name)) {
                onError("A field with this name already exists.");
                return;
              }
              edit(() =>
                putField(
                  workspace,
                  { tokenId: selected, field: name },
                  { source: { kind: "local" }, values: {} },
                ),
              );
            }}
          >
            <label>
              New color field
              <input name="name" required placeholder="background" />
            </label>
            <button>Add field</button>
          </form>
        </>
      )}
    </section>
  );
}
