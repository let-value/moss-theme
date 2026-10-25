# Light palette clusters

78 RGB bases → 139 role/color bundles at threshold 6 (semantic mode, semantic distance 2).

Distance: Euclidean OKLab × 100; complete linkage limits every pair in a bundle. Representatives are existing colors chosen by a declaration-weighted medoid. Sorted by declaration count (a usage proxy, not screen area). Derivations exclude the representative; singleton colors have zero.

A merge must satisfy both limits for every pair of declarations. Semantic distance counts tree edges after the shared path prefix: string → string.regexp is 1, string.escape → string.regexp is 2. Unrelated roots never merge. UI and syntax are separate namespaces. Equivalent semantic/TextMate paths and string escapes have explicit aliases in the script. Multi-scope rules remain atomic and all their paths must qualify. Perceptual mode disables the path constraint for comparison.

Alpha is excluded from RGB clustering and preserved in the proposed replacement map. These are base-color similarities, not composited on-screen similarities. This report does not modify themes.

| Role | Main color | Derivations | Declarations | Maximum pair distance | Maximum path distance |
|---|---|---:|---:|---:|---:|
| ui.editor.findMatchBackground, ui.editor.selectionBackground, ui.editor.selectionHighlightBackground, ui.editor.wordHighlightBackground, ui.editor.wordHighlightStrongBackground | `#A9C98E` | 1 | 5 | 3.85 | 2 |
| ui.editorBracketHighlight.foreground1, ui.editorBracketHighlight.foreground2, ui.editorBracketHighlight.foreground3, ui.editorBracketHighlight.foreground5, ui.editorBracketHighlight.foreground6 | `#1E1C18` | 0 | 5 | 0.00 | 2 |
| syntax.entity.name.type | `#006B64` | 0 | 4 | 0.00 | 0 |
| syntax.variable, syntax.variable.parameter | `#1D1D1D` | 0 | 4 | 0.00 | 1 |
| syntax.entity.name.function | `#63501F` | 0 | 3 | 0.00 | 0 |
| syntax.markup.bold, syntax.markup.heading, syntax.markup.italic | `#2F3A26` | 0 | 3 | 0.00 | 2 |
| syntax.string, syntax.string.escape | `#933814` | 0 | 3 | 0.00 | 1 |
| ui.editor.findMatchHighlightBackground, ui.editor.inactiveSelectionBackground, ui.editor.lineHighlightBorder | `#C2D3BB` | 2 | 3 | 4.53 | 2 |
| ui.tab.activeBackground, ui.tab.hoverBackground, ui.tab.inactiveBackground | `#CCDAC8` | 2 | 3 | 5.39 | 2 |
| syntax.constant.language, syntax.constant.numeric | `#005E86` | 0 | 2 | 0.00 | 2 |
| syntax.keyword, syntax.keyword.control.export, syntax.keyword.control.from, syntax.keyword.control.import | `#3B6305` | 0 | 2 | 0.00 | 2 |
| syntax.variable.other.constant | `#1D1D1D` | 0 | 2 | 0.00 | 0 |
| syntax.variable.other.property | `#3F5B48` | 0 | 2 | 0.00 | 0 |
| ui.button.background, ui.button.hoverBackground | `#7E9468` | 1 | 2 | 5.43 | 2 |
| ui.button.secondaryBackground, ui.button.secondaryHoverBackground | `#B9CBB1` | 1 | 2 | 3.41 | 2 |
| ui.diffEditor.insertedLineBackground, ui.diffEditor.insertedTextBackground | `#D9EBC0` | 0 | 2 | 0.00 | 2 |
| ui.diffEditor.removedLineBackground, ui.diffEditor.removedTextBackground | `#F0D9D8` | 0 | 2 | 0.00 | 2 |
| ui.editor.background, ui.editor.lineHighlightBackground | `#D3DFCF` | 1 | 2 | 1.85 | 2 |
| ui.editorSuggestWidget.border, ui.editorSuggestWidget.selectedBackground | `#A9C98E` | 1 | 2 | 4.74 | 2 |
| ui.editorSuggestWidget.foreground, ui.editorSuggestWidget.selectedForeground | `#2F3A26` | 0 | 2 | 0.00 | 2 |
| ui.gitDecoration.addedResourceForeground, ui.gitDecoration.untrackedResourceForeground | `#4F7A46` | 0 | 2 | 0.00 | 2 |
| ui.list.activeSelectionForeground, ui.list.inactiveSelectionForeground | `#2F3A26` | 0 | 2 | 0.00 | 2 |
| ui.list.focusHighlightForeground, ui.list.highlightForeground | `#4F6B3A` | 0 | 2 | 0.00 | 2 |
| ui.list.hoverBackground, ui.list.inactiveSelectionBackground | `#C2D3BB` | 1 | 2 | 2.63 | 2 |
| ui.scrollbarSlider.activeBackground, ui.scrollbarSlider.hoverBackground | `#6C7B5A` | 1 | 2 | 4.98 | 2 |
| ui.statusBar.background, ui.statusBar.noFolderBackground | `#DAE2DA` | 0 | 2 | 0.00 | 2 |
| ui.statusBar.foreground, ui.statusBar.noFolderForeground | `#1E1C18` | 0 | 2 | 0.00 | 2 |
| ui.tab.activeModifiedBorder, ui.tab.inactiveModifiedBorder | `#7A6B3A` | 0 | 2 | 0.00 | 2 |
| ui.terminal.ansiBlack, ui.terminal.foreground | `#3A4630` | 1 | 2 | 1.91 | 2 |
| ui.terminal.ansiBlue, ui.terminal.ansiCyan | `#3E6B5C` | 1 | 2 | 5.24 | 2 |
| ui.terminal.ansiBrightBlack, ui.terminal.ansiBrightCyan | `#4C8071` | 1 | 2 | 4.25 | 2 |
| ui.terminal.ansiBrightGreen, ui.terminal.ansiGreen | `#4F7A46` | 1 | 2 | 5.81 | 2 |
| ui.terminal.ansiBrightRed, ui.terminal.ansiRed | `#A64B4B` | 1 | 2 | 5.60 | 2 |
| ui.terminal.ansiBrightYellow, ui.terminal.ansiYellow | `#8A6A1F` | 1 | 2 | 5.98 | 2 |
| ui.textLink.activeForeground, ui.textLink.foreground | `#4F6B3A` | 0 | 2 | 0.00 | 2 |
| ui.titleBar.activeBackground, ui.titleBar.inactiveBackground | `#C6D7C0` | 1 | 2 | 2.45 | 2 |
| syntax.comment | `#7C8A6E` | 0 | 1 | 0.00 | 0 |
| syntax.constant.language.import-export-all | `#1E1C18` | 0 | 1 | 0.00 | 0 |
| syntax.entity.name.tag | `#3B6305` | 0 | 1 | 0.00 | 0 |
| syntax.entity.other.attribute-name | `#3F5B48` | 0 | 1 | 0.00 | 0 |
| syntax.invalid | `#A64B4B` | 0 | 1 | 0.00 | 0 |
| syntax.keyword, syntax.storage | `#3B6305` | 0 | 1 | 0.00 | 0 |
| syntax.keyword.operator | `#1E1C18` | 0 | 1 | 0.00 | 0 |
| syntax.operator | `#1E1C18` | 0 | 1 | 0.00 | 0 |
| syntax.punctuation | `#7E8B72` | 0 | 1 | 0.00 | 0 |
| syntax.punctuation.definition.arguments, syntax.punctuation.definition.block, syntax.punctuation.definition.bracket, syntax.punctuation.definition.parameters, syntax.punctuation.definition.tag, syntax.punctuation.definition.typeparameters, syntax.punctuation.section | `#1E1C18` | 0 | 1 | 0.00 | 0 |
| syntax.punctuation.definition.string, syntax.punctuation.definition.template-expression, syntax.punctuation.section.interpolation | `#933814` | 0 | 1 | 0.00 | 0 |
| syntax.string.regexp | `#7A6B4A` | 0 | 1 | 0.00 | 0 |
| syntax.support.class.component | `#006B64` | 0 | 1 | 0.00 | 0 |
| ui.activityBar.activeBorder | `#6C7B5A` | 0 | 1 | 0.00 | 0 |
| ui.activityBar.background | `#BFD3B7` | 0 | 1 | 0.00 | 0 |
| ui.activityBar.foreground | `#46543A` | 0 | 1 | 0.00 | 0 |
| ui.activityBar.inactiveForeground | `#93A187` | 0 | 1 | 0.00 | 0 |
| ui.activityBarBadge.background | `#6C7B5A` | 0 | 1 | 0.00 | 0 |
| ui.activityBarBadge.foreground | `#FFFFFF` | 0 | 1 | 0.00 | 0 |
| ui.badge.background | `#6C7B5A` | 0 | 1 | 0.00 | 0 |
| ui.badge.foreground | `#FFFFFF` | 0 | 1 | 0.00 | 0 |
| ui.button.foreground | `#1F2A19` | 0 | 1 | 0.00 | 0 |
| ui.button.secondaryForeground | `#3F4B36` | 0 | 1 | 0.00 | 0 |
| ui.descriptionForeground | `#77846B` | 0 | 1 | 0.00 | 0 |
| ui.dropdown.background | `#E0E6E3` | 0 | 1 | 0.00 | 0 |
| ui.dropdown.border | `#AFC5A4` | 0 | 1 | 0.00 | 0 |
| ui.dropdown.foreground | `#2F3A26` | 0 | 1 | 0.00 | 0 |
| ui.editor.findMatchBorder | `#6C7B5A` | 0 | 1 | 0.00 | 0 |
| ui.editor.foreground | `#1E1C18` | 0 | 1 | 0.00 | 0 |
| ui.editorBracketHighlight.foreground4 | `#3F5B48` | 0 | 1 | 0.00 | 0 |
| ui.editorBracketHighlight.unexpectedBracket.foreground | `#1E1C18` | 0 | 1 | 0.00 | 0 |
| ui.editorBracketMatch.background | `#D1D8D3` | 0 | 1 | 0.00 | 0 |
| ui.editorBracketMatch.border | `#516630` | 0 | 1 | 0.00 | 0 |
| ui.editorCursor.foreground | `#4F6B3A` | 0 | 1 | 0.00 | 0 |
| ui.editorError.foreground | `#A64B4B` | 0 | 1 | 0.00 | 0 |
| ui.editorGroup.border | `#B7C9AD` | 0 | 1 | 0.00 | 0 |
| ui.editorGroupHeader.tabsBackground | `#CCDAC8` | 0 | 1 | 0.00 | 0 |
| ui.editorGutter.addedBackground | `#4F7A46` | 0 | 1 | 0.00 | 0 |
| ui.editorGutter.deletedBackground | `#A64B4B` | 0 | 1 | 0.00 | 0 |
| ui.editorGutter.modifiedBackground | `#8A6B2E` | 0 | 1 | 0.00 | 0 |
| ui.editorHoverWidget.background | `#DEE5E0` | 0 | 1 | 0.00 | 0 |
| ui.editorHoverWidget.border | `#B7C9AD` | 0 | 1 | 0.00 | 0 |
| ui.editorHoverWidget.foreground | `#2F3A26` | 0 | 1 | 0.00 | 0 |
| ui.editorIndentGuide.activeBackground1 | `#8DA27F` | 0 | 1 | 0.00 | 0 |
| ui.editorIndentGuide.background1 | `#C0D0B8` | 0 | 1 | 0.00 | 0 |
| ui.editorInfo.foreground | `#3E6B5C` | 0 | 1 | 0.00 | 0 |
| ui.editorLineNumber.activeForeground | `#5C6B4C` | 0 | 1 | 0.00 | 0 |
| ui.editorLineNumber.foreground | `#A9B79B` | 0 | 1 | 0.00 | 0 |
| ui.editorLink.activeForeground | `#3F5B2C` | 0 | 1 | 0.00 | 0 |
| ui.editorOverviewRuler.bracketMatchForeground | `#516630` | 0 | 1 | 0.00 | 0 |
| ui.editorRuler.foreground | `#C6D5C1` | 0 | 1 | 0.00 | 0 |
| ui.editorSuggestWidget.background | `#DEE5E0` | 0 | 1 | 0.00 | 0 |
| ui.editorWarning.foreground | `#8A6A1F` | 0 | 1 | 0.00 | 0 |
| ui.editorWhitespace.foreground | `#B6C7AE` | 0 | 1 | 0.00 | 0 |
| ui.editorWidget.background | `#DEE5E0` | 0 | 1 | 0.00 | 0 |
| ui.editorWidget.border | `#B7C9AD` | 0 | 1 | 0.00 | 0 |
| ui.editorWidget.foreground | `#2F3A26` | 0 | 1 | 0.00 | 0 |
| ui.errorForeground | `#A64B4B` | 0 | 1 | 0.00 | 0 |
| ui.focusBorder | `#7E9468` | 0 | 1 | 0.00 | 0 |
| ui.foreground | `#1E1C18` | 0 | 1 | 0.00 | 0 |
| ui.gitDecoration.deletedResourceForeground | `#A64B4B` | 0 | 1 | 0.00 | 0 |
| ui.gitDecoration.modifiedResourceForeground | `#8A6B2E` | 0 | 1 | 0.00 | 0 |
| ui.input.background | `#E0E6E3` | 0 | 1 | 0.00 | 0 |
| ui.input.border | `#AFC5A4` | 0 | 1 | 0.00 | 0 |
| ui.input.foreground | `#2F3A26` | 0 | 1 | 0.00 | 0 |
| ui.input.placeholderForeground | `#77846B` | 0 | 1 | 0.00 | 0 |
| ui.inputOption.activeBorder | `#5C6B4C` | 0 | 1 | 0.00 | 0 |
| ui.list.activeSelectionBackground | `#A9C98E` | 0 | 1 | 0.00 | 0 |
| ui.notifications.background | `#DEE5E0` | 0 | 1 | 0.00 | 0 |
| ui.notifications.border | `#B7C9AD` | 0 | 1 | 0.00 | 0 |
| ui.notifications.foreground | `#2F3A26` | 0 | 1 | 0.00 | 0 |
| ui.panel.background | `#DAE2DA` | 0 | 1 | 0.00 | 0 |
| ui.panel.border | `#B7C9AD` | 0 | 1 | 0.00 | 0 |
| ui.problemsErrorIcon.foreground | `#A64B4B` | 0 | 1 | 0.00 | 0 |
| ui.problemsInfoIcon.foreground | `#3E6B5C` | 0 | 1 | 0.00 | 0 |
| ui.problemsWarningIcon.foreground | `#8A6A1F` | 0 | 1 | 0.00 | 0 |
| ui.quickInput.background | `#DEE5E0` | 0 | 1 | 0.00 | 0 |
| ui.quickInput.foreground | `#2F3A26` | 0 | 1 | 0.00 | 0 |
| ui.scrollbarSlider.background | `#8A9A78` | 0 | 1 | 0.00 | 0 |
| ui.selection.background | `#A9C98E` | 0 | 1 | 0.00 | 0 |
| ui.sideBar.background | `#D3DFD2` | 0 | 1 | 0.00 | 0 |
| ui.sideBar.border | `#B7C9AD` | 0 | 1 | 0.00 | 0 |
| ui.sideBar.foreground | `#3F4B36` | 0 | 1 | 0.00 | 0 |
| ui.sideBarSectionHeader.background | `#C7D8C2` | 0 | 1 | 0.00 | 0 |
| ui.sideBarSectionHeader.foreground | `#4C5A42` | 0 | 1 | 0.00 | 0 |
| ui.statusBar.debuggingBackground | `#8A5F2E` | 0 | 1 | 0.00 | 0 |
| ui.statusBar.debuggingForeground | `#FBF7EF` | 0 | 1 | 0.00 | 0 |
| ui.statusBarItem.hoverBackground | `#5D6B4C` | 0 | 1 | 0.00 | 0 |
| ui.tab.activeBorderTop | `#90A479` | 0 | 1 | 0.00 | 0 |
| ui.tab.activeForeground | `#35422B` | 0 | 1 | 0.00 | 0 |
| ui.tab.border | `#B7C9AD` | 0 | 1 | 0.00 | 0 |
| ui.tab.inactiveForeground | `#7E8B72` | 0 | 1 | 0.00 | 0 |
| ui.terminal.ansiBrightBlue | `#5A7D8C` | 0 | 1 | 0.00 | 0 |
| ui.terminal.ansiBrightMagenta | `#8E6B8E` | 0 | 1 | 0.00 | 0 |
| ui.terminal.ansiBrightWhite | `#2F3A26` | 0 | 1 | 0.00 | 0 |
| ui.terminal.ansiMagenta | `#7A5A7A` | 0 | 1 | 0.00 | 0 |
| ui.terminal.ansiWhite | `#8A9680` | 0 | 1 | 0.00 | 0 |
| ui.terminal.background | `#DAE2DA` | 0 | 1 | 0.00 | 0 |
| ui.terminal.selectionBackground | `#A9C98E` | 0 | 1 | 0.00 | 0 |
| ui.titleBar.activeForeground | `#45523A` | 0 | 1 | 0.00 | 0 |
| ui.titleBar.border | `#B7C9AD` | 0 | 1 | 0.00 | 0 |
| ui.titleBar.inactiveForeground | `#8A9680` | 0 | 1 | 0.00 | 0 |
| ui.tree.indentGuidesStroke | `#B9CBB1` | 0 | 1 | 0.00 | 0 |

Control: `python3 scripts/cluster-dark-colors.py --variant light --semantic-distance 2 --color-distance 6`. Lower values keep more distinctions; higher values merge more. Threshold 0 keeps all distinct RGB bases. Path distance 0 permits only identical canonical paths; 1 permits parent/child; 2 also permits siblings. Colors must independently pass the OKLab limit. Derivation counts describe geometric grouping, not source provenance.

Conversion reference: https://bottosson.github.io/posts/oklab/
