# Dark transplants

Neighbor limits: semantic tree distance ≤ 2, OKLab × 100 distance ≤ 6. Measured on `palette/dark-baseline.json` before migration; no recursive propagation.

| Role | Moss color | Explicit targets | Neighbors |
|---|---|---:|---:|
| main-text | `#D4D1C8` | 2 | 0 |
| numbers | `#60CCFC` | 2 | 0 |
| keywords | `#96C66C` | 2 | 0 |
| functions | `#E2CC95` | 3 | 0 |
| types | `#2AA198` | 5 | 0 |
| variables | `#CACACA` | 4 | 0 |
| parameters | `#CACACA` | 2 | 0 |
| properties | `#AFD1BA` | 2 | 0 |
| operators | `#D4D1C8` | 3 | 0 |
| tags | `#96C66C` | 1 | 0 |
| attributes | `#AFD1BA` | 1 | 0 |
| strings | `#DF7753` | 3 | 0 |
| module-keywords | `#96C66C` | 1 | 0 |
| brackets | `#2A392F` | 1 | 0 |
| brackets-2 | `#7D9952` | 2 | 0 |
| brackets-3 | `#D4D1C8` | 6 | 0 |
| brackets-4 | `#AFD1BA` | 1 | 0 |
| bracket-punctuation | `#D4D1C8` | 1 | 0 |
| editor-background | `#1F2F20` | 1 | 50 |
| panel-background | `#1F2F20` | 2 | 0 |
| status-bar-background | `#1F2F20` | 2 | 0 |

## Relative palette roles

- editor-background: path ≤ 4, OKLab × 100 ≤ 24. UI surfaces/structure use explicit semantic path aliases in the manifest. Each neighbor retains its pre-migration OKLab offset from the seed; alpha is preserved. Out-of-gamut results reduce chroma at fixed lightness/hue. Explicit transplants are protected.

## Neighbor decisions

- `UI: input.border`: `#4A5740` → `#465D40` via `UI: editor.background`; path 4, color 16.51.
- `UI: dropdown.border`: `#4A5740` → `#465D40` via `UI: editor.background`; path 4, color 16.51.
- `UI: tab.activeBackground`: `#232A20` → `#1F2F20` via `UI: editor.background`; path 4, color 0.00.
- `UI: titleBar.activeBackground`: `#1B2118` → `#172618` via `UI: editor.background`; path 4, color 3.63.
- `UI: titleBar.inactiveBackground`: `#1F261C` → `#1B2B1C` via `UI: editor.background`; path 4, color 1.65.
- `UI: activityBar.background`: `#191F17` → `#152417` via `UI: editor.background`; path 4, color 4.45.
- `UI: sideBar.background`: `#20261D` → `#1C2B1D` via `UI: editor.background`; path 4, color 1.54.
- `UI: sideBarSectionHeader.background`: `#283022` → `#243522` via `UI: editor.background`; path 4, color 2.32.
- `UI: tab.hoverBackground`: `#283022` → `#243522` via `UI: editor.background`; path 4, color 2.32.
- `UI: editorGroupHeader.tabsBackground`: `#1F251C` → `#1B2A1C` via `UI: editor.background`; path 4, color 1.95.
- `UI: tab.inactiveBackground`: `#1F251C` → `#1B2A1C` via `UI: editor.background`; path 4, color 1.95.
- `UI: panel.border`: `#38432F` → `#34482F` via `UI: editor.background`; path 4, color 9.34.
- `UI: editorGroup.border`: `#38432F` → `#34482F` via `UI: editor.background`; path 4, color 9.34.
- `UI: tab.border`: `#38432F` → `#34482F` via `UI: editor.background`; path 4, color 9.34.
- `UI: sideBar.border`: `#38432F` → `#34482F` via `UI: editor.background`; path 4, color 9.34.
- `UI: titleBar.border`: `#38432F` → `#34482F` via `UI: editor.background`; path 4, color 9.34.
- `UI: statusBarItem.hoverBackground`: `#536245` → `#4F6845` via `UI: editor.background`; path 4, color 20.24.
- `UI: list.hoverBackground`: `#2A3324` → `#263824` via `UI: editor.background`; path 4, color 3.41.
- `UI: list.activeSelectionBackground`: `#3C5030` → `#375530` via `UI: editor.background`; path 4, color 13.56.
- `UI: editorSuggestWidget.selectedBackground`: `#3C5030` → `#375530` via `UI: editor.background`; path 4, color 13.56.
- `UI: selection.background`: `#3C5030` → `#375530` via `UI: editor.background`; path 4, color 13.56.
- `UI: editor.selectionBackground`: `#3C5030` → `#375530` via `UI: editor.background`; path 2, color 13.56.
- `UI: terminal.selectionBackground`: `#3C5030` → `#375530` via `UI: editor.background`; path 4, color 13.56.
- `UI: button.secondaryHoverBackground`: `#3C5030` → `#375530` via `UI: editor.background`; path 4, color 13.56.
- `UI: list.inactiveSelectionBackground`: `#33402A` → `#2F452A` via `UI: editor.background`; path 4, color 8.09.
- `UI: editor.lineHighlightBorder`: `#33402A` → `#2F452A` via `UI: editor.background`; path 2, color 8.09.
- `UI: editor.inactiveSelectionBackground`: `#33402A` → `#2F452A` via `UI: editor.background`; path 2, color 8.09.
- `UI: button.secondaryBackground`: `#33402A` → `#2F452A` via `UI: editor.background`; path 4, color 8.09.
- `UI: tree.indentGuidesStroke`: `#3B4731` → `#374C31` via `UI: editor.background`; path 4, color 10.75.
- `UI: editorWhitespace.foreground`: `#3B4731` → `#374C31` via `UI: editor.background`; path 4, color 10.75.
- `UI: editor.lineHighlightBackground`: `#2A3323` → `#263823` via `UI: editor.background`; path 2, color 3.42.
- `UI: editor.wordHighlightBackground`: `#4A5F3A80` → `#45653A80` via `UI: editor.background`; path 2, color 18.80.
- `UI: editor.wordHighlightStrongBackground`: `#4A5F3A80` → `#45653A80` via `UI: editor.background`; path 2, color 18.80.
- `UI: editor.selectionHighlightBackground`: `#4A5F3A66` → `#45653A66` via `UI: editor.background`; path 2, color 18.80.
- `UI: editor.findMatchHighlightBackground`: `#3F5230` → `#3A572F` via `UI: editor.background`; path 2, color 14.35.
- `UI: editor.findMatchBackground`: `#4C6238` → `#476837` via `UI: editor.background`; path 2, color 19.83.
- `UI: editorIndentGuide.background1`: `#313B29` → `#2D4029` via `UI: editor.background`; path 4, color 6.40.
- `UI: editorRuler.foreground`: `#313B29` → `#2D4029` via `UI: editor.background`; path 4, color 6.40.
- `UI: editorIndentGuide.activeBackground1`: `#5C6B4C` → `#58714C` via `UI: editor.background`; path 4, color 23.37.
- `UI: quickInput.background`: `#293025` → `#253525` via `UI: editor.background`; path 4, color 2.40.
- `UI: editorHoverWidget.background`: `#293025` → `#253525` via `UI: editor.background`; path 4, color 2.40.
- `UI: notifications.background`: `#293025` → `#253525` via `UI: editor.background`; path 4, color 2.40.
- `UI: editorWidget.background`: `#293025` → `#253525` via `UI: editor.background`; path 4, color 2.40.
- `UI: editorSuggestWidget.background`: `#293025` → `#253525` via `UI: editor.background`; path 4, color 2.40.
- `UI: input.background`: `#222920` → `#1E2E20` via `UI: editor.background`; path 4, color 0.41.
- `UI: dropdown.background`: `#222920` → `#1E2E20` via `UI: editor.background`; path 4, color 0.41.
- `UI: editorWidget.border`: `#3E4A34` → `#3A4F34` via `UI: editor.background`; path 4, color 11.85.
- `UI: editorHoverWidget.border`: `#3E4A34` → `#3A4F34` via `UI: editor.background`; path 4, color 11.85.
- `UI: editorSuggestWidget.border`: `#3E4A34` → `#3A4F34` via `UI: editor.background`; path 4, color 11.85.
- `UI: notifications.border`: `#3E4A34` → `#3A4F34` via `UI: editor.background`; path 4, color 11.85.

## Append another role

Append a role to `palette/dark-transplants.json` with its name, pinned Moss color, source reference, and explicit token targets. Run `python3 scripts/build-theme.py`; it applies the manifest to dark only and regenerates this report and `dark-transplants.json`. Inspect neighbor decisions before using the theme. Adjust the two limits in the manifest as needed. A role may override them with its own `semantic_distance` and `color_distance`. Set `neighbor_strategy` to `relative-oklab` to preserve neighbor offsets around the new seed; `semantic_paths` supplies reviewed aliases for related UI surfaces. Other roles keep the default flat replacement strategy. The baseline stays fixed; adding roles does not use already migrated colors as new evidence.
