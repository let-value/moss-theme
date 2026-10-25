import { useState } from "react";
import { openWorkspace, saveWorkspace } from "./browser-workspace";
import example from "./example.json?raw";
import {
  appearances,
  attachTree,
  children,
  createWorkspace,
  readWorkspace,
  resolveColor,
  writeWorkspace,
  type Appearance,
  type Workspace,
} from "./tokens";
import NodeEditor from "./node-editor";
import "./tree-editor.css";

const storage = {
  getItem: (key: string) => localStorage.getItem(key),
  setItem: (key: string, value: string) => localStorage.setItem(key, value),
};

function rows(workspace: Workspace) {
  const result: { id: string; depth: number }[] = [];
  const pending = children(workspace, null).map(([id]) => ({ id, depth: 0 }));
  while (pending.length) {
    const row = pending.pop()!;
    result.push(row);
    pending.push(
      ...children(workspace, row.id)
        .reverse()
        .map(([id]) => ({ id, depth: row.depth + 1 })),
    );
  }
  return result;
}

export default function TreeEditor() {
  const [session, setSession] = useState(() => openWorkspace(storage));
  const { workspace, message } = session;
  const [selected, setSelected] = useState(() => children(workspace, null)[0][0]);
  const [appearance, setAppearance] = useState<Appearance>("dark");
  const [search, setSearch] = useState("");

  function setMessage(message: string) {
    setSession((current) => ({ ...current, message }));
  }

  function commit(next: Workspace, selection = selected) {
    setSession(saveWorkspace(storage, session, next));
    setSelected(selection);
  }

  function edit(operation: () => Workspace, selection = selected) {
    try {
      commit(operation(), selection);
    } catch (error) {
      setMessage(error instanceof Error ? error.message : String(error));
    }
  }

  function load(json: string) {
    try {
      const next = readWorkspace(json);
      commit(next, children(next, null)[0][0]);
    } catch (error) {
      setMessage(error instanceof Error ? error.message : String(error));
    }
  }

  function download() {
    const url = URL.createObjectURL(
      new Blob([writeWorkspace(workspace)], { type: "application/json" }),
    );
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = "moss-workspace.json";
    anchor.click();
    URL.revokeObjectURL(url);
  }

  const node = workspace.nodes[selected];

  return (
    <main className="moss">
      <header className="toolbar">
        <h1>Moss</h1>
        <label>
          Appearance{" "}
          <select
            value={appearance}
            onChange={(event) => setAppearance(event.target.value as Appearance)}
          >
            {appearances.map((mode) => (
              <option key={mode}>{mode}</option>
            ))}
          </select>
        </label>
        <button onClick={() => edit(createWorkspace, "root")}>New workspace</button>
        <button onClick={() => load(example)}>Load example</button>
        <button
          onClick={() => {
            const loaded = openWorkspace(storage);
            if (loaded.message) {
              setMessage(loaded.message);
              return;
            }
            setSession(loaded);
            setSelected(children(loaded.workspace, null)[0][0]);
          }}
        >
          Reload saved
        </button>
        <label className="file">
          Import JSON
          <input
            type="file"
            accept=".json,application/json"
            onChange={async (event) => {
              const file = event.target.files?.[0];
              event.target.value = "";
              if (file) {
                try {
                  load(await file.text());
                } catch (error) {
                  setMessage(String(error));
                }
              }
            }}
          />
        </label>
        <label className="file">
          Import child tree
          <input
            type="file"
            accept=".json,application/json"
            onChange={async (event) => {
              const file = event.target.files?.[0];
              event.target.value = "";
              if (file) {
                try {
                  const template: unknown = JSON.parse(await file.text());
                  edit(() =>
                    attachTree(
                      workspace,
                      node.kind === "token" ? node.parentId! : selected,
                      template,
                    ),
                  );
                } catch (error) {
                  setMessage(String(error));
                }
              }
            }}
          />
        </label>
        <button onClick={download}>Export JSON</button>
      </header>
      {message && (
        <p className="notice" role="alert">
          {message}
        </p>
      )}
      <div className="workspace">
        <aside aria-label="Token tree">
          <label>
            Search tree
            <input
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              type="search"
            />
          </label>
          <nav aria-label="Nodes">
            {rows(workspace)
              .filter(({ id }) =>
                `${workspace.nodes[id].name} ${id}`.toLowerCase().includes(search.toLowerCase()),
              )
              .map(({ id, depth }) => {
                const entry = workspace.nodes[id];
                const value =
                  entry.kind === "token"
                    ? resolveColor(workspace, { tokenId: id, field: "color" }, appearance).value
                    : undefined;
                return (
                  <button
                    key={id}
                    aria-current={selected === id ? "true" : undefined}
                    onClick={() => setSelected(id)}
                    style={{ paddingInlineStart: `${0.75 + depth}rem` }}
                  >
                    {entry.kind === "token" ? (
                      <span className="swatch" style={{ background: value }} />
                    ) : (
                      <span aria-hidden="true">▾</span>
                    )}
                    <span>{entry.name}</span>
                    <small>{entry.kind === "token" ? (value ?? "Unset") : entry.kind}</small>
                  </button>
                );
              })}
          </nav>
        </aside>
        <NodeEditor
          key={`${selected}:${node.name}:${node.parentId}`}
          workspace={workspace}
          selected={selected}
          appearance={appearance}
          edit={edit}
          onSelect={setSelected}
          onError={setMessage}
        />
      </div>
    </main>
  );
}
