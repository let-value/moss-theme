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

## Neighbor decisions

No additional declarations satisfy both limits outside the explicit targets.

## Append another role

Append a role to `palette/dark-transplants.json` with its name, pinned Moss color, source reference, and explicit token targets. Run `python3 scripts/build-theme.py`; it applies the manifest to dark only and regenerates this report and `dark-transplants.json`. Inspect neighbor decisions before using the theme. Adjust the two limits in the manifest as needed. The baseline stays fixed; adding roles does not use already migrated colors as new evidence.
