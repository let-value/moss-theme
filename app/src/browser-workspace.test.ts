import { expect, it } from "vite-plus/test";
import { openWorkspace, saveWorkspace } from "./browser-workspace";
import { createWorkspace, writeWorkspace } from "./tokens";

function storage(initial: string | null = null) {
  let value = initial;
  return {
    getItem: () => value,
    setItem: (_key: string, next: string) => {
      value = next;
    },
  };
}

it("opens an empty workspace without silently writing a starter", () => {
  const store = storage();
  expect(openWorkspace(store).workspace).toEqual(createWorkspace());
  expect(store.getItem()).toBeNull();
});

it("restores authored values and keeps malformed input untouched", () => {
  const workspace = createWorkspace("Authored palette");
  const store = storage(writeWorkspace(workspace));
  expect(openWorkspace(store).workspace).toEqual(workspace);
  const broken = storage("{broken");
  expect(openWorkspace(broken).message).not.toBe("");
  expect(broken.getItem()).toBe("{broken");
});

it("saves and reloads a validated document", () => {
  const store = storage();
  const workspace = createWorkspace("Another palette");
  const saved = saveWorkspace(store, openWorkspace(store), workspace);
  expect(saved.message).toBe("");
  expect(openWorkspace(store).workspace).toEqual(workspace);
});

it("detects stale writes without overwriting another tab's work", () => {
  const store = storage();
  const first = openWorkspace(store);
  const other = createWorkspace("Other tab");
  const mine = createWorkspace("My unsaved work");
  saveWorkspace(store, openWorkspace(store), other);
  const conflicted = saveWorkspace(store, first, mine);
  expect(conflicted.message).toContain("another tab");
  expect(conflicted.workspace).toEqual(mine);
  expect(openWorkspace(store).workspace).toEqual(other);
});

it("keeps exportable in-memory work when storage fails", () => {
  const store = {
    getItem: () => null,
    setItem: () => {
      throw new Error("Storage full");
    },
  };
  const workspace = createWorkspace("Unsaved");
  const saved = saveWorkspace(store, openWorkspace(store), workspace);
  expect(saved.message).toContain("Storage full");
  expect(saved.snapshot).toBeNull();
  expect(writeWorkspace(saved.workspace)).toBe(writeWorkspace(workspace));
});

it("reports unavailable storage without crashing the editor", () => {
  const store = {
    getItem: (): null => {
      throw new Error("Access denied");
    },
    setItem: () => {},
  };
  const opened = openWorkspace(store);
  expect(opened.message).toContain("Access denied");
  expect(opened.workspace).toEqual(createWorkspace());
});

it("validates before saving without changing the current snapshot", () => {
  const store = storage();
  const session = openWorkspace(store);
  expect(() => saveWorkspace(store, session, { ...session.workspace, nodes: {} })).toThrow();
  expect(store.getItem()).toBeNull();
});
