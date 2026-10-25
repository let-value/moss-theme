# Light transplants

Neighbor limits: semantic tree distance ≤ 2, OKLab × 100 distance ≤ 6. Measured on `palette/light-baseline.json` before migration; no recursive propagation.

| Role | Moss color | Explicit targets | Neighbors |
|---|---|---:|---:|
| main-text | `#1E1C18` | 2 | 0 |
| numbers | `#005E86` | 2 | 0 |
| keywords | `#3B6305` | 2 | 0 |
| functions | `#63501F` | 3 | 0 |
| types | `#006B64` | 5 | 0 |
| variables | `#1D1D1D` | 4 | 0 |
| parameters | `#1D1D1D` | 2 | 0 |
| properties | `#3F5B48` | 2 | 0 |
| operators | `#1E1C18` | 3 | 0 |
| tags | `#3B6305` | 1 | 0 |
| attributes | `#3F5B48` | 1 | 0 |
| strings | `#933814` | 3 | 1 |
| module-keywords | `#3B6305` | 1 | 0 |
| brackets | `#D1D8D3` | 1 | 0 |
| brackets-2 | `#516630` | 2 | 0 |
| brackets-3 | `#1E1C18` | 6 | 0 |
| brackets-4 | `#3F5B48` | 1 | 0 |
| bracket-punctuation | `#1E1C18` | 1 | 0 |
| editor-background | `#DAE2DA` | 1 | 49 |
| panel-background | `#DAE2DA` | 2 | 0 |
| status-bar-background | `#DAE2DA` | 2 | 0 |
| bottom-surface-text | `#1E1C18` | 2 | 0 |

## Relative palette roles

- editor-background: path ≤ 4, OKLab × 100 ≤ 24. UI surfaces/structure use explicit semantic path aliases in the manifest. Each neighbor retains its pre-migration OKLab offset from the seed; alpha is preserved. Out-of-gamut results reduce chroma at fixed lightness/hue. Explicit transplants are protected.

## Neighbor decisions

- `UI: input.border`: `#CBDCBB` → `#AFC5A4` via `UI: editor.background`; path 4, color 11.40.
- `UI: dropdown.border`: `#CBDCBB` → `#AFC5A4` via `UI: editor.background`; path 4, color 11.40.
- `UI: tab.activeBackground`: `#F7FAF2` → `#DAE2DA` via `UI: editor.background`; path 4, color 0.00.
- `UI: titleBar.activeBackground`: `#E3EFD7` → `#C6D7C0` via `UI: editor.background`; path 4, color 4.98.
- `UI: titleBar.inactiveBackground`: `#EDF4E5` → `#D0DCCD` via `UI: editor.background`; path 4, color 2.50.
- `UI: activityBar.background`: `#DCEBCE` → `#BFD3B7` via `UI: editor.background`; path 4, color 6.70.
- `UI: sideBar.background`: `#F0F7EA` → `#D3DFD2` via `UI: editor.background`; path 4, color 1.55.
- `UI: sideBarSectionHeader.background`: `#E4F0D9` → `#C7D8C2` via `UI: editor.background`; path 4, color 4.63.
- `UI: panel.border`: `#D3E1C4` → `#B7C9AD` via `UI: editor.background`; path 4, color 9.44.
- `UI: editorGroup.border`: `#D3E1C4` → `#B7C9AD` via `UI: editor.background`; path 4, color 9.44.
- `UI: tab.border`: `#D3E1C4` → `#B7C9AD` via `UI: editor.background`; path 4, color 9.44.
- `UI: sideBar.border`: `#D3E1C4` → `#B7C9AD` via `UI: editor.background`; path 4, color 9.44.
- `UI: titleBar.border`: `#D3E1C4` → `#B7C9AD` via `UI: editor.background`; path 4, color 9.44.
- `UI: editorWidget.border`: `#D3E1C4` → `#B7C9AD` via `UI: editor.background`; path 4, color 9.44.
- `UI: editorHoverWidget.border`: `#D3E1C4` → `#B7C9AD` via `UI: editor.background`; path 4, color 9.44.
- `UI: editorSuggestWidget.border`: `#D3E1C4` → `#B7C9AD` via `UI: editor.background`; path 4, color 9.44.
- `UI: notifications.border`: `#D3E1C4` → `#B7C9AD` via `UI: editor.background`; path 4, color 9.44.
- `UI: editorGroupHeader.tabsBackground`: `#E9F2E0` → `#CCDAC8` via `UI: editor.background`; path 4, color 3.45.
- `UI: tab.inactiveBackground`: `#E9F2E0` → `#CCDAC8` via `UI: editor.background`; path 4, color 3.45.
- `UI: tab.hoverBackground`: `#E2EDD6` → `#C5D5BF` via `UI: editor.background`; path 4, color 5.36.
- `UI: button.secondaryBackground`: `#E2EDD6` → `#C5D5BF` via `UI: editor.background`; path 4, color 5.36.
- `UI: list.hoverBackground`: `#E9F2DF` → `#CCDAC7` via `UI: editor.background`; path 4, color 3.52.
- `UI: list.activeSelectionBackground`: `#C5E1A5` → `#A9C98E` via `UI: editor.background`; path 4, color 12.96.
- `UI: editorSuggestWidget.selectedBackground`: `#C5E1A5` → `#A9C98E` via `UI: editor.background`; path 4, color 12.96.
- `UI: selection.background`: `#C5E1A5` → `#A9C98E` via `UI: editor.background`; path 4, color 12.96.
- `UI: editor.selectionBackground`: `#C5E1A5` → `#A9C98E` via `UI: editor.background`; path 2, color 12.96.
- `UI: terminal.selectionBackground`: `#C5E1A5` → `#A9C98E` via `UI: editor.background`; path 4, color 12.96.
- `UI: editor.wordHighlightBackground`: `#C5E1A580` → `#A9C98E80` via `UI: editor.background`; path 2, color 12.96.
- `UI: editor.wordHighlightStrongBackground`: `#C5E1A580` → `#A9C98E80` via `UI: editor.background`; path 2, color 12.96.
- `UI: editor.selectionHighlightBackground`: `#C5E1A566` → `#A9C98E66` via `UI: editor.background`; path 2, color 12.96.
- `UI: list.inactiveSelectionBackground`: `#DFEBD2` → `#C2D3BB` via `UI: editor.background`; path 4, color 6.15.
- `UI: editor.inactiveSelectionBackground`: `#DFEBD2` → `#C2D3BB` via `UI: editor.background`; path 2, color 6.15.
- `UI: tree.indentGuidesStroke`: `#D5E3C8` → `#B9CBB1` via `UI: editor.background`; path 4, color 8.73.
- `UI: button.secondaryHoverBackground`: `#D5E3C8` → `#B9CBB1` via `UI: editor.background`; path 4, color 8.73.
- `UI: editor.lineHighlightBackground`: `#F0F7E7` → `#D3DFCF` via `UI: editor.background`; path 2, color 1.81.
- `UI: editor.lineHighlightBorder`: `#E5F0D9` → `#C8D8C2` via `UI: editor.background`; path 2, color 4.55.
- `UI: editor.findMatchHighlightBackground`: `#DCEDB8` → `#BFD5A1` via `UI: editor.background`; path 2, color 8.58.
- `UI: editor.findMatchBackground`: `#B9D88C` → `#9DC076` via `UI: editor.background`; path 2, color 16.82.
- `UI: editorIndentGuide.background1`: `#DCE8CF` → `#C0D0B8` via `UI: editor.background`; path 4, color 6.99.
- `UI: editorIndentGuide.activeBackground1`: `#A8B995` → `#8DA27F` via `UI: editor.background`; path 4, color 22.18.
- `UI: editorWhitespace.foreground`: `#D2DFC5` → `#B6C7AE` via `UI: editor.background`; path 4, color 9.76.
- `UI: editorRuler.foreground`: `#E3EDD8` → `#C6D5C1` via `UI: editor.background`; path 4, color 5.14.
- `UI: quickInput.background`: `#FBFDF8` → `#DEE5E0` via `UI: editor.background`; path 4, color 1.13.
- `UI: editorHoverWidget.background`: `#FBFDF8` → `#DEE5E0` via `UI: editor.background`; path 4, color 1.13.
- `UI: notifications.background`: `#FBFDF8` → `#DEE5E0` via `UI: editor.background`; path 4, color 1.13.
- `UI: editorWidget.background`: `#FBFDF8` → `#DEE5E0` via `UI: editor.background`; path 4, color 1.13.
- `UI: editorSuggestWidget.background`: `#FBFDF8` → `#DEE5E0` via `UI: editor.background`; path 4, color 1.13.
- `UI: input.background`: `#FDFEFB` → `#E0E6E3` via `UI: editor.background`; path 4, color 1.63.
- `UI: dropdown.background`: `#FDFEFB` → `#E0E6E3` via `UI: editor.background`; path 4, color 1.63.
- `TextMate: constant.character.escape`: `#6E7A3A` → `#933814` via `TextMate: string`; path 1, color 0.59.

## Append another role

Append a role to `palette/light-transplants.json` with its name, pinned Moss color, source reference, and explicit token targets. Run `python3 scripts/build-theme.py`; it applies the manifest to light only and regenerates this report and `light-transplants.json`. Inspect neighbor decisions before using the theme. Adjust the two limits in the manifest as needed. A role may override them with its own `semantic_distance` and `color_distance`. Set `neighbor_strategy` to `relative-oklab` to preserve neighbor offsets around the new seed; `semantic_paths` supplies reviewed aliases for related UI surfaces. Other roles keep the default flat replacement strategy. The baseline stays fixed; adding roles does not use already migrated colors as new evidence.
