import { createWorkspace, readWorkspace, writeWorkspace, type Workspace } from "./tokens";

type BrowserStorage = Pick<Storage, "getItem" | "setItem">;
export interface Session {
  workspace: Workspace;
  snapshot: string | null;
  message: string;
}
const key = "moss.workspace.v1";

export function openWorkspace(storage: BrowserStorage): Session {
  let snapshot: string | null = null;
  try {
    snapshot = storage.getItem(key);
    return {
      workspace: snapshot === null ? createWorkspace() : readWorkspace(snapshot),
      snapshot,
      message: "",
    };
  } catch (error) {
    return {
      workspace: createWorkspace(),
      snapshot,
      message: error instanceof Error ? error.message : String(error),
    };
  }
}

export function saveWorkspace(
  storage: BrowserStorage,
  session: Session,
  workspace: Workspace,
): Session {
  const json = writeWorkspace(workspace);
  try {
    if (storage.getItem(key) !== session.snapshot) {
      throw new Error(
        "Saved data changed in another tab. Export your work before reloading the saved workspace.",
      );
    }
    storage.setItem(key, json);
    return { workspace, snapshot: json, message: "" };
  } catch (error) {
    const reason = error instanceof Error ? error.message : String(error);
    return {
      workspace,
      snapshot: session.snapshot,
      message: `${reason} Your work is still in memory and can be exported.`,
    };
  }
}
