import { color } from "./color";

export const appearances = ["dark", "light"] as const;
export type Appearance = (typeof appearances)[number];
export type Reference = { tokenId: string; field: string };
export type ColorField = {
  source: { kind: "local" } | ({ kind: "reference" } & Reference);
  // Values are inactive authoring history while this field is linked.
  values: Partial<Record<Appearance, string>>;
};
export type PaletteNode = {
  name: string;
  parentId: string | null;
} & ({ kind: "tree" | "group" } | { kind: "token"; fields: Record<string, ColorField> });
export interface Workspace {
  version: 1;
  nodes: Record<string, PaletteNode>;
}
export type ReadValue = (source: Reference, appearance: Appearance) => string | undefined;

function check(condition: unknown, message: string): asserts condition {
  if (!condition) throw new Error(message);
}

function record(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function own<T>(entries: Record<string, T>, id: string): T | undefined {
  return Object.hasOwn(entries, id) ? entries[id] : undefined;
}

export function token(workspace: Workspace, id: string) {
  const node = own(workspace.nodes, id);
  check(node?.kind === "token", `Expected a color token: ${id}`);
  return node;
}

export function field(workspace: Workspace, reference: Reference): ColorField {
  const value = own(token(workspace, reference.tokenId).fields, reference.field);
  check(value, `Missing color field: ${reference.tokenId}.${reference.field}`);
  return value;
}

function same(a: Reference, b: Reference) {
  return a.tokenId === b.tokenId && a.field === b.field;
}

export function traceSource(workspace: Workspace, reference: Reference) {
  const chain: Reference[] = [];
  const visited = new Set<string>();
  while (true) {
    chain.push(reference);
    const path = () => chain.map(({ tokenId, field }) => `${tokenId}.${field}`).join(" → ");
    const key = JSON.stringify([reference.tokenId, reference.field]);
    if (visited.has(key)) throw new Error(`Cyclic color reference: ${path()}`);
    visited.add(key);
    let current: ColorField;
    try {
      current = field(workspace, reference);
    } catch (error) {
      throw new Error(`${error instanceof Error ? error.message : String(error)} (${path()})`);
    }
    if (current.source.kind === "local") return { source: reference, chain };
    reference = { tokenId: current.source.tokenId, field: current.source.field };
  }
}

export function resolveColor(
  workspace: Workspace,
  reference: Reference,
  appearance: Appearance,
  read: ReadValue = (source, mode) => field(workspace, source).values[mode],
) {
  const trace = traceSource(workspace, reference);
  const value = read(trace.source, appearance);
  return { ...trace, value: value === undefined ? undefined : color(value) };
}

export function dependents(workspace: Workspace, reference: Reference): Reference[] {
  return Object.entries(workspace.nodes).flatMap(([tokenId, node]) =>
    node.kind !== "token"
      ? []
      : Object.keys(node.fields)
          .map((field) => ({ tokenId, field }))
          .filter((target) =>
            traceSource(workspace, target)
              .chain.slice(1)
              .some((hop) => same(hop, reference)),
          ),
  );
}

export function children(workspace: Workspace, parentId: string | null) {
  return Object.entries(workspace.nodes).filter(([, node]) => node.parentId === parentId);
}

export function validateWorkspace(input: unknown): asserts input is Workspace {
  check(
    record(input) && input.version === 1 && record(input.nodes),
    "Expected a version 1 workspace",
  );
  let roots = 0;
  for (const [id, node] of Object.entries(input.nodes)) {
    check(id.trim() && record(node), `Invalid node: ${id}`);
    check(typeof node.name === "string" && node.name.trim(), `Missing node name: ${id}`);
    check(node.parentId === null || typeof node.parentId === "string", `Invalid parent: ${id}`);
    check(
      node.kind === "tree" || node.kind === "group" || node.kind === "token",
      `Invalid node kind: ${id}`,
    );
    if (node.parentId === null) {
      check(node.kind === "tree", `Root must be a tree: ${id}`);
      roots++;
    }
    if (node.kind !== "token") continue;
    check(
      record(node.fields) && Object.hasOwn(node.fields, "color"),
      `Missing primary color field: ${id}`,
    );
    for (const [name, entry] of Object.entries(node.fields)) {
      check(
        name.trim() && record(entry) && record(entry.source) && record(entry.values),
        `Invalid field: ${id}.${name}`,
      );
      const source = entry.source;
      check(
        source.kind === "local" || source.kind === "reference",
        `Invalid source: ${id}.${name}`,
      );
      if (source.kind === "reference") {
        check(
          typeof source.tokenId === "string" && typeof source.field === "string",
          `Invalid reference: ${id}.${name}`,
        );
        check(source.tokenId !== id, `Self-link: ${id}.${name}`);
      }
      for (const [mode, value] of Object.entries(entry.values)) {
        check(
          (mode === "dark" || mode === "light") && typeof value === "string",
          `Invalid value: ${id}.${name}.${mode}`,
        );
        try {
          color(value);
        } catch {
          throw new Error(`Invalid color: ${id}.${name}.${mode} = ${value}`);
        }
      }
    }
  }
  check(roots === 1, "Workspace must contain exactly one root tree");
  const workspace = input as unknown as Workspace;
  for (const [id, node] of Object.entries(workspace.nodes)) {
    const visited = new Set<string>([id]);
    let parentId = node.parentId;
    while (parentId !== null) {
      check(!visited.has(parentId), `Containment cycle: ${id} → ${parentId}`);
      visited.add(parentId);
      const parent = own(workspace.nodes, parentId);
      check(parent && parent.kind !== "token", `Invalid parent: ${id} → ${parentId}`);
      parentId = parent.parentId;
    }
    if (node.kind === "token") {
      for (const name of Object.keys(node.fields))
        traceSource(workspace, { tokenId: id, field: name });
    }
  }
}

export function createWorkspace(name = "Palette"): Workspace {
  const workspace: Workspace = {
    version: 1,
    nodes: { root: { kind: "tree", name, parentId: null } },
  };
  validateWorkspace(workspace);
  return workspace;
}

// Every edit validates a new document before returning it. The input is never mutated.
export function putNode(workspace: Workspace, id: string, node: PaletteNode): Workspace {
  const next = { ...workspace, nodes: { ...workspace.nodes, [id]: node } };
  validateWorkspace(next);
  return next;
}

// A template is ordinary workspace JSON. Its root becomes a child of parentId;
// references may point to fields in either the template or the destination.
export function attachTree(workspace: Workspace, parentId: string, template: unknown): Workspace {
  check(
    record(template) && template.version === 1 && record(template.nodes),
    "Expected a version 1 tree template",
  );
  const entries = Object.entries(template.nodes);
  for (const [id] of entries)
    check(!Object.hasOwn(workspace.nodes, id), `Node already exists: ${id}`);
  const roots = entries.filter(([, node]) => record(node) && node.parentId === null);
  check(roots.length === 1, "Template must contain exactly one root tree");
  const [id, root] = roots[0];
  check(record(root) && root.kind === "tree", "Template root must be a tree");
  const next = {
    ...workspace,
    nodes: { ...workspace.nodes, ...template.nodes, [id]: { ...root, parentId } },
  };
  validateWorkspace(next);
  return next;
}

export function removeNode(workspace: Workspace, id: string): Workspace {
  const node = own(workspace.nodes, id);
  check(node && node.parentId !== null, "Choose a non-root node to remove");
  const removed = new Set([id]);
  const queue = [id];
  for (let index = 0; index < queue.length; index++) {
    for (const [childId] of children(workspace, queue[index])) {
      removed.add(childId);
      queue.push(childId);
    }
  }
  const next = {
    ...workspace,
    nodes: Object.fromEntries(Object.entries(workspace.nodes).filter(([key]) => !removed.has(key))),
  };
  for (const [tokenId, node] of Object.entries(next.nodes)) {
    if (node.kind !== "token") continue;
    for (const [name, entry] of Object.entries(node.fields)) {
      check(
        entry.source.kind !== "reference" || !removed.has(entry.source.tokenId),
        `Referenced by ${tokenId}.${name}; detach or relink it first`,
      );
    }
  }
  validateWorkspace(next);
  return next;
}

export function putField(
  workspace: Workspace,
  reference: Reference,
  value: ColorField | null,
): Workspace {
  const node = token(workspace, reference.tokenId);
  const fields = value === null ? { ...node.fields } : { ...node.fields, [reference.field]: value };
  if (value === null) delete fields[reference.field];
  return putNode(workspace, reference.tokenId, { ...node, fields });
}

export function setColor(
  workspace: Workspace,
  reference: Reference,
  mode: Appearance,
  value: string | undefined,
) {
  const current = field(workspace, reference);
  check(current.source.kind === "local", "Edit the source or make this field independent first");
  const values = { ...current.values };
  if (value === undefined) delete values[mode];
  else {
    color(value);
    values[mode] = value;
  }
  return putField(workspace, reference, { ...current, values });
}

export function link(workspace: Workspace, reference: Reference, target: Reference) {
  return putField(workspace, reference, {
    ...field(workspace, reference),
    source: { kind: "reference", ...target },
  });
}

export function detach(workspace: Workspace, reference: Reference, read?: ReadValue) {
  const values: ColorField["values"] = {};
  for (const mode of appearances) {
    const { value } = resolveColor(workspace, reference, mode, read);
    if (value !== undefined) values[mode] = value;
  }
  return putField(workspace, reference, { source: { kind: "local" }, values });
}

export function readWorkspace(json: string): Workspace {
  const input: unknown = JSON.parse(json);
  validateWorkspace(input);
  return input;
}

export function writeWorkspace(workspace: Workspace): string {
  validateWorkspace(workspace);
  return JSON.stringify(workspace, null, 2) + "\n";
}
