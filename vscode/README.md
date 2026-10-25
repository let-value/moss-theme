<p align="center">
  <img src="https://raw.githubusercontent.com/vaxicy/verdant-meadow-theme/main/assets/icon.png" alt="Verdant Meadow Theme logo" width="128">
</p>

<h1 align="center">Verdant Meadow Theme</h1>

<p align="center">
  <a href="https://marketplace.visualstudio.com/items?itemName=lilinhuang.verdant-meadow-theme"><img src="https://img.shields.io/badge/VS%20Code-Theme-6C7B5A?logo=visual-studio-code" alt="VS Code Theme"></a>
  <img src="https://img.shields.io/badge/version-1.0.0-90A479?logo=visual-studio-code" alt="version 1.0.0">
  <img src="https://img.shields.io/badge/Variants-Light%20%26%20Dark-A9C48A?logo=visual-studio-code" alt="Light and Dark variants">
  <a href="https://github.com/vaxicy/verdant-meadow-theme/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-Non--Commercial-lightgrey" alt="License: Non-Commercial"></a>
</p>

A calm green theme: **pale sage paper** with olive ink in the light variant, and a **deep olive night** with fresh leaf highlights in the dark one. Both variants share one palette, so switching changes the light level rather than the mood of the workspace.

一套安静的绿色主题：浅色版是**淡鼠尾草纸白**配橄榄墨字，深色版是**深橄榄夜**配新叶般的亮绿。明暗两版共用同一套色板，切换时变的只是明暗，工作区的气质保持一致。

## Preview / 预览

| Light 浅色 | Dark 深色 |
| --- | --- |
| ![Verdant Meadow Theme Light](https://raw.githubusercontent.com/vaxicy/verdant-meadow-theme/main/store-assets/screenshots/en/screenshot-light.png) | ![Verdant Meadow Theme Dark](https://raw.githubusercontent.com/vaxicy/verdant-meadow-theme/main/store-assets/screenshots/en/screenshot-dark.png) |

> Both previews are captured from a real VS Code window running the theme — no mockups.
>
> 上方预览图取自真实运行该主题的 VS Code 窗口截图，非模拟图。

## Palette / 色板

| Role | Light | Dark |
| --- | --- | --- |
| Editor background | `#F7FAF2` sage paper | `#232A20` olive night |
| Foreground | `#3A4630` olive ink | `#DCE7CF` young leaf |
| Muted text / placeholders | `#77846B` | `#96A488` |
| Side bar | `#F0F7EA` with `#3F4B36` text | `#20261D` with `#C2D0B2` text |
| Panel / terminal | `#F3F9EE` | `#1F251C` |
| Title bar | `#E3EFD7` with `#45523A` text | `#1B2118` with `#C7D5B8` text |
| Tab bar / inactive tab | `#E9F2E0` | `#1F251C` |
| Active tab / indicator | `#35422B` text, `#90A479` top border | `#E4F1D6` text, `#A9C48A` top border |
| Activity bar | `#DCEBCE` with `#46543A` icons | `#191F17` with `#B7C9A4` icons |
| Status bar | `#6C7B5A` with `#F4F9EE` text | `#46543A` with `#E6F0DA` text |
| Selection | `#C5E1A5` leaf wash | `#3C5030` shaded moss |
| Current line | `#F0F7E7` | `#2A3323` |
| Borders | `#D3E1C4` | `#38432F` |
| Indent guides | `#DCE8CF` | `#313B29` |
| Button | `#90A479` with `#1F2A19` text (hover `#7E9468`) | `#A9C48A` with `#232A20` text (hover `#C5E1A5`) |
| Badge | `#6C7B5A` with white text | `#C5E1A5` with `#232A20` text |
| Cursor | `#4F6B3A` | `#C5E1A5` |
| Links | `#4F6B3A` | `#A9C48A` |
| Errors / warnings | `#A64B4B` / `#8A6A1F` | `#E08A8A` / `#E0C07A` |
| Git added / modified / deleted | `#4F7A46` / `#8A6B2E` / `#A64B4B` | `#A9C48A` / `#D7C28A` / `#E08A8A` |

Pale `#E4F1D6`, leaf `#C5E1A5`, sage `#90A479` and olive `#6C7B5A` carry both variants, so a file still reads as "verdant meadow" after switching.

淡绿 `#E4F1D6`、嫩叶 `#C5E1A5`、鼠尾草 `#90A479` 与橄榄 `#6C7B5A` 贯穿明暗两版，切换后整个文件依然是同一片草地。

## Syntax mapping / 语法映射

| Syntax | Light | Dark |
| --- | --- | --- |
| Comments | `#7C8A6E` | `#7C8A70` |
| Keywords / storage | `#3F6B2E` | `#A9C48A` |
| Strings | `#6E7C3A` | `#D2DF9A` |
| Functions / methods | `#2E6B54` | `#8FC9A8` |
| Types / classes | `#2F5B6B` | `#9BC1C9` |
| Numbers / constants | `#8A5F2E` | `#E0B87A` |
| Variables | `#3A4630` | `#DCE7CF` |
| Parameters | `#5A6B4A` | `#C2D0B2` |
| Properties | `#2F6B5B` | `#8FC9B4` |
| Operators | `#6B7A5E` | `#A8B79A` |
| Punctuation | `#7E8B72` | `#93A187` |
| HTML tags | `#3F6B2E` | `#A9C48A` |
| Attribute names | `#8A6A2E` | `#D7C28A` |
| Regex | `#7A6B4A` | `#C9B98A` |
| Escape characters | `#6E7A3A` | `#C9D89A` |

Semantic highlighting is enabled, so variables, parameters, properties, functions and types follow the same mapping in TypeScript, JavaScript, Go, Rust and Python.

已开启语义高亮，TypeScript、JavaScript、Go、Rust 与 Python 里的变量、参数、属性、函数与类型都会落到同一套配色。

## Install / 安装

Search **Verdant Meadow Theme** in the Extensions view, then pick `Verdant Meadow Theme Light` or `Verdant Meadow Theme Dark` from the theme picker (`Ctrl+K Ctrl+T`).

在扩展面板搜索 **Verdant Meadow Theme**，安装后用 `Ctrl+K Ctrl+T` 在 `Verdant Meadow Theme Light` 与 `Verdant Meadow Theme Dark` 之间选择。

```bash
code --install-extension lilinhuang.verdant-meadow-theme
```

## Build from source / 本地构建

```bash
py -3 scripts/build-theme.py       # regenerate both theme JSON files
py -3 scripts/generate-icon.py     # export assets/icon.png from the selected logo
py -3 scripts/capture-real-screenshots.py   # real VS Code screenshots
```

## License / 许可证

Non-Commercial License — free for personal, educational and non-commercial use. See [LICENSE](https://github.com/vaxicy/verdant-meadow-theme/blob/main/LICENSE).

非商业许可证：个人、教育与非商业用途免费使用，详见 LICENSE。

## Moss color transplants

Both variants use independent manifests (`palette/dark-transplants.json` and
`palette/light-transplants.json`). Append a role with its Moss color and explicit
token targets to extend a transplant. Each manifest controls semantic path and
OKLab distance for neighbor discovery. The fixed `palette/{variant}-baseline.json`
snapshots keep repeated builds from expanding the migration.

```sh
python3 scripts/build-theme.py
python3 scripts/test-dark-transplant.py
python3 scripts/test-light-transplant.py
python3 scripts/test-cluster-dark-colors.py
```

The builder regenerates both themes and their color digests, cluster reports,
and transplant reports. Review `DARK-TRANSPLANTS.md` or `LIGHT-TRANSPLANTS.md`
for neighbor decisions. Conflicting neighbors are left unchanged. Surface neighbors
retain their relative OKLab offsets and alpha; explicit targets take priority.

The light source snapshot (`palette/moss-light-source.json`) resolves Moss's
saved light palette, token variants, and saved link overrides. To refresh it with
the Moss checkout beside the workspace and its Node dependencies available:

```sh
node scripts/snapshot-moss-light.mjs
```

Normal theme builds need only Python's standard library and the pinned JSON
sources. Refreshing the source snapshot does not change pinned manifest colors;
update the appropriate manifest entries to adopt newly selected source colors.
