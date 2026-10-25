import { describe, expect, it } from "vite-plus/test";
import example from "./example.json?raw";
import {
  attachTree,
  createWorkspace,
  dependents,
  detach,
  field,
  link,
  putField,
  putNode,
  readWorkspace,
  removeNode,
  resolveColor,
  setColor,
  token,
  traceSource,
  validateWorkspace,
  writeWorkspace,
  type PaletteNode,
  type Reference,
  type Workspace,
} from "./tokens";

const canvas = { tokenId: "canvas", field: "color" };
const vscode = { tokenId: "vscode-canvas", field: "color" };
const warning = { tokenId: "warning", field: "background" };
const fixture = () => readWorkspace(example);

function frozenWorkspace() {
  const workspace = fixture();
  function freeze(value: object) {
    Object.freeze(value);
    for (const child of Object.values(value)) if (child && typeof child === "object") freeze(child);
  }
  freeze(workspace);
  return workspace;
}

function expectRejected(workspace: Workspace, edit: () => unknown, error: string) {
  const before = writeWorkspace(workspace);
  expect(edit).toThrow(error);
  expect(writeWorkspace(workspace)).toBe(before);
}

describe("data-driven token trees", () => {
  it("starts with an empty, named root tree", () => {
    const workspace = createWorkspace("Arbitrary palette");
    expect(workspace.nodes).toEqual({
      root: { kind: "tree", name: "Arbitrary palette", parentId: null },
    });
  });

  it("resolves local and cross-tree references with a full field-level chain", () => {
    const workspace = fixture();
    expect(resolveColor(workspace, vscode, "dark")).toEqual({
      source: canvas,
      chain: [vscode, { tokenId: "base00", field: "color" }, canvas],
      value: "#132118",
    });
    expect(resolveColor(workspace, canvas, "light").value).toBe("#e9efeb");
    expect(
      resolveColor(workspace, { tokenId: "zed-warning", field: "color" }, "dark").source,
    ).toEqual(warning);
  });

  it("updates every linked use while leaving unrelated colors and light values alone", () => {
    const workspace = frozenWorkspace();
    const next = setColor(workspace, canvas, "dark", "rgb(255 0 0 / .5)");
    expect(resolveColor(next, vscode, "dark").value).toBe("#ff000080");
    expect(resolveColor(next, { tokenId: "zed-canvas", field: "color" }, "dark").value).toBe(
      "#ff000080",
    );
    expect(resolveColor(next, vscode, "light").value).toBe("#e9efeb");
    expect(resolveColor(next, { tokenId: "leaf", field: "color" }, "dark").value).toBe("#96c66c");
    expect(resolveColor(workspace, canvas, "dark").value).toBe("#132118");
  });

  it("finds transitive affected fields, excluding the source itself", () => {
    expect(dependents(fixture(), canvas)).toEqual([
      { tokenId: "base00", field: "color" },
      { tokenId: "zed-canvas", field: "color" },
      vscode,
    ]);
  });

  it("keeps links valid when names or containment change", () => {
    const workspace = frozenWorkspace();
    const next = putNode(workspace, "canvas", {
      ...workspace.nodes.canvas,
      name: "Canvas.with.dots",
      parentId: "accents",
    });
    expect(resolveColor(next, vscode, "dark")).toEqual(resolveColor(workspace, vscode, "dark"));
  });

  it("creates arbitrary nested groups and unmapped tokens without seeds", () => {
    let workspace = createWorkspace();
    workspace = putNode(workspace, "nested", {
      kind: "group",
      name: "Any group",
      parentId: "root",
    });
    workspace = putNode(workspace, "lichen", {
      kind: "token",
      name: "lichen.custom",
      parentId: "nested",
      fields: { color: { source: { kind: "local" }, values: {} } },
    });
    expect(
      resolveColor(workspace, { tokenId: "lichen", field: "color" }, "dark").value,
    ).toBeUndefined();
    expect(
      resolveColor(workspace, { tokenId: "lichen", field: "color" }, "light").value,
    ).toBeUndefined();
  });

  it("attaches data-only templates with explicit mappings to destination sources", () => {
    const workspace = frozenWorkspace();
    const next = attachTree(workspace, "root", {
      version: 1,
      nodes: {
        custom: { kind: "tree", name: "Another editor", parentId: null },
        external: {
          kind: "token",
          name: "editor.background",
          parentId: "custom",
          fields: { color: { source: { kind: "reference", ...canvas }, values: {} } },
        },
      },
    });
    expect(next.nodes.custom.parentId).toBe("root");
    expect(resolveColor(next, { tokenId: "external", field: "color" }, "dark").value).toBe(
      "#132118",
    );
    expectRejected(
      workspace,
      () => attachTree(workspace, "root", workspace),
      "Node already exists",
    );
  });

  it("keeps two-field color sources independent and supports arbitrary field names", () => {
    let workspace = fixture();
    const source: Reference = { tokenId: "warning", field: "border.custom" };
    workspace = putField(workspace, source, {
      source: { kind: "local" },
      values: { dark: "#abcdef44" },
    });
    workspace = link(workspace, vscode, source);
    expect(resolveColor(workspace, vscode, "dark").value).toBe("#abcdef44");
    expect(resolveColor(workspace, warning, "dark").value).toBe("#2f2b20");
    expect(resolveColor(workspace, vscode, "light").value).toBeUndefined();
  });

  it("accepts source-value lookup without importing tournament rules", () => {
    const workspace = fixture();
    const read = (reference: Reference) =>
      reference.field === "background" ? "#ffff0080" : "#ff0000";
    expect(resolveColor(workspace, vscode, "dark", read).value).toBe("#ff0000");
    expect(
      resolveColor(workspace, { tokenId: "zed-warning", field: "color" }, "dark", read).value,
    ).toBe("#ffff0080");
    const independent = detach(workspace, vscode, read);
    expect(resolveColor(independent, vscode, "light").value).toBe("#ff0000");
  });

  it("makes references authoritative over inactive local values", () => {
    const workspace = fixture();
    const independent = detach(workspace, vscode);
    const changed = setColor(independent, vscode, "dark", "#ff0000");
    const linked = link(changed, vscode, { tokenId: "leaf", field: "color" });
    expect(field(linked, vscode).values.dark).toBe("#ff0000");
    expect(resolveColor(linked, vscode, "dark").value).toBe("#96c66c");
    expectRejected(linked, () => setColor(linked, vscode, "dark", "#000000"), "Edit the source");
  });

  it("detaches both appearances without changing their visible values", () => {
    const workspace = frozenWorkspace();
    const independent = detach(workspace, vscode);
    for (const mode of ["dark", "light"] as const) {
      expect(resolveColor(independent, vscode, mode).value).toBe(
        resolveColor(workspace, vscode, mode).value,
      );
    }
    const changed = setColor(independent, canvas, "dark", "#ff0000");
    expect(resolveColor(changed, vscode, "dark").value).toBe("#132118");
  });

  it("leaves missing appearances missing across detach and JSON round-trip", () => {
    let workspace = fixture();
    workspace = setColor(workspace, canvas, "light", undefined);
    workspace = readWorkspace(writeWorkspace(detach(workspace, vscode)));
    expect(field(workspace, vscode).values).toEqual({ dark: "#132118" });
    expect(resolveColor(workspace, vscode, "light").value).toBeUndefined();
  });

  it.each([
    [{ tokenId: "missing", field: "color" }, "Expected a color token"],
    [{ tokenId: "surfaces", field: "color" }, "Expected a color token"],
    [{ tokenId: "toString", field: "color" }, "Expected a color token"],
    [{ tokenId: "canvas", field: "missing" }, "Missing color field"],
    [vscode, "Self-link"],
  ] as const)("rejects invalid link %j without altering the document", (target, error) => {
    const workspace = frozenWorkspace();
    expectRejected(workspace, () => link(workspace, vscode, target), error);
  });

  it("rejects cross-field cycles without altering the document", () => {
    const workspace = frozenWorkspace();
    expectRejected(workspace, () => link(workspace, canvas, vscode), "Cyclic color reference");
  });

  it("blocks removing a source, a referenced field, or a containing subtree", () => {
    const workspace = frozenWorkspace();
    expectRejected(workspace, () => removeNode(workspace, "canvas"), "Referenced by");
    expectRejected(workspace, () => removeNode(workspace, "surfaces"), "Referenced by");
    expectRejected(workspace, () => putField(workspace, warning, null), "Missing color field");
    expectRejected(workspace, () => removeNode(workspace, "root"), "non-root");
  });

  it("removes a whole subtree when its references are internal", () => {
    const workspace: Workspace = {
      version: 1,
      nodes: { outer: { kind: "tree", name: "Outer", parentId: null } },
    };
    const attached = attachTree(workspace, "outer", fixture());
    expect(removeNode(attached, "root")).toEqual(workspace);
  });

  it("removes a child tree without removing its external sources", () => {
    const workspace = removeNode(frozenWorkspace(), "vscode");
    expect(workspace.nodes.vscode).toBeUndefined();
    expect(workspace.nodes["vscode-canvas"]).toBeUndefined();
    expect(resolveColor(workspace, canvas, "dark").value).toBe("#132118");
  });

  it("rejects invalid parent moves and roots atomically", () => {
    const workspace = frozenWorkspace();
    expectRejected(
      workspace,
      () => putNode(workspace, "surfaces", { ...workspace.nodes.surfaces, parentId: "canvas" }),
      "Invalid parent",
    );
    expectRejected(
      workspace,
      () => putNode(workspace, "surfaces", { ...workspace.nodes.surfaces, parentId: "surfaces" }),
      "Containment cycle",
    );
    expectRejected(
      workspace,
      () => putNode(workspace, "extra", { kind: "tree", name: "Second root", parentId: null }),
      "exactly one root",
    );
  });

  it("round-trips the entire authored document without storing resolved copies", () => {
    const workspace = fixture();
    expect(readWorkspace(writeWorkspace(workspace))).toEqual(workspace);
    expect(field(workspace, vscode).values).toEqual({});
    expect(writeWorkspace(readWorkspace(writeWorkspace(workspace)))).toBe(
      writeWorkspace(workspace),
    );
  });

  it.each([
    null,
    [],
    {},
    { version: 2, nodes: {} },
    { version: 1, nodes: {} },
    { version: 1, nodes: { bad: { kind: "group", name: "Bad", parentId: null } } },
  ])("rejects malformed workspace data: %j", (input) =>
    expect(() => validateWorkspace(input)).toThrow(),
  );

  it("rejects malformed colors, fields, parents, and source shapes on load", () => {
    const workspace = fixture();
    const valid = workspace.nodes.canvas;
    const invalid: unknown[] = [
      { ...valid, name: "" },
      { ...valid, parentId: "missing" },
      { ...valid, fields: {} },
      { ...valid, fields: { color: { source: { kind: "computed" }, values: {} } } },
      { ...valid, fields: { color: { source: { kind: "local" }, values: { light: "var(--x)" } } } },
      { ...valid, fields: { color: { source: { kind: "local" }, values: { light: 42 } } } },
    ];
    for (const node of invalid) {
      expect(() =>
        readWorkspace(
          JSON.stringify({ ...workspace, nodes: { ...workspace.nodes, canvas: node } }),
        ),
      ).toThrow();
    }
    expect(() => readWorkspace("{broken")).toThrow();
  });

  it("supports unusual stable identities and long chains without a hop limit", () => {
    const workspace = createWorkspace();
    const local: PaletteNode = {
      kind: "token",
      name: "Unusual",
      parentId: "root",
      fields: { color: { source: { kind: "local" }, values: { dark: "#123456" } } },
    };
    workspace.nodes = { ...workspace.nodes, ["__proto__"]: local };
    for (let index = 0; index < 5_000; index++) {
      workspace.nodes[`link${index}`] = {
        ...local,
        fields: {
          color: {
            source: {
              kind: "reference",
              tokenId: index ? `link${index - 1}` : "__proto__",
              field: "color",
            },
            values: {},
          },
        },
      };
    }
    const trace = traceSource(workspace, { tokenId: "link4999", field: "color" });
    expect(trace.source).toEqual({ tokenId: "__proto__", field: "color" });
    expect(trace.chain).toHaveLength(5_001);
    expect(token(workspace, "__proto__").name).toBe("Unusual");
  });
});
