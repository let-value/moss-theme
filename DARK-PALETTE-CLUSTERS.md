# Dark palette clusters

69 RGB bases → 140 role/color bundles at threshold 6 (semantic mode, semantic distance 2).

Distance: Euclidean OKLab × 100; complete linkage limits every pair in a bundle. Representatives are existing colors chosen by a declaration-weighted medoid. Sorted by declaration count (a usage proxy, not screen area). Derivations exclude the representative; singleton colors have zero.

A merge must satisfy both limits for every pair of declarations. Semantic distance counts tree edges after the shared path prefix: string → string.regexp is 1, string.escape → string.regexp is 2. Unrelated roots never merge. UI and syntax are separate namespaces. Equivalent semantic/TextMate paths and string escapes have explicit aliases in the script. Multi-scope rules remain atomic and all their paths must qualify. Perceptual mode disables the path constraint for comparison.

Alpha is excluded from RGB clustering and preserved in the proposed replacement map. These are base-color similarities, not composited on-screen similarities. This report does not modify themes.

| Role | Main color | Derivations | Declarations | Maximum pair distance | Maximum path distance |
|---|---|---:|---:|---:|---:|
| ui.editorBracketHighlight.foreground1, ui.editorBracketHighlight.foreground2, ui.editorBracketHighlight.foreground3, ui.editorBracketHighlight.foreground4, ui.editorBracketHighlight.foreground5, ui.editorBracketHighlight.foreground6 | `#D4D1C8` | 1 | 6 | 5.41 | 2 |
| syntax.entity.name.type | `#2AA198` | 0 | 4 | 0.00 | 0 |
| syntax.variable, syntax.variable.parameter | `#CACACA` | 0 | 4 | 0.00 | 1 |
| syntax.variable.other.constant, syntax.variable.other.property | `#AFD1BA` | 1 | 4 | 4.92 | 2 |
| ui.editor.findMatchBackground, ui.editor.selectionHighlightBackground, ui.editor.wordHighlightBackground, ui.editor.wordHighlightStrongBackground | `#45653A` | 1 | 4 | 1.18 | 2 |
| syntax.entity.name.function | `#E2CC95` | 0 | 3 | 0.00 | 0 |
| syntax.markup.bold, syntax.markup.heading, syntax.markup.italic | `#E4F1D6` | 0 | 3 | 0.00 | 2 |
| ui.statusBar.debuggingForeground, ui.statusBar.foreground, ui.statusBar.noFolderForeground | `#E6F0DA` | 1 | 3 | 2.19 | 2 |
| ui.tab.activeBackground, ui.tab.hoverBackground, ui.tab.inactiveBackground | `#1F2F20` | 2 | 3 | 4.20 | 2 |
| ui.terminal.ansiBrightCyan, ui.terminal.ansiBrightGreen, ui.terminal.ansiWhite | `#C2D0B2` | 2 | 3 | 5.98 | 2 |
| syntax.constant.language, syntax.constant.numeric | `#60CCFC` | 0 | 2 | 0.00 | 2 |
| syntax.keyword, syntax.keyword.control.export, syntax.keyword.control.from, syntax.keyword.control.import | `#96C66C` | 0 | 2 | 0.00 | 2 |
| syntax.string | `#DF7753` | 0 | 2 | 0.00 | 0 |
| ui.button.secondaryBackground, ui.button.secondaryHoverBackground | `#2F452A` | 1 | 2 | 5.41 | 2 |
| ui.diffEditor.insertedLineBackground, ui.diffEditor.insertedTextBackground | `#3C5030` | 0 | 2 | 0.00 | 2 |
| ui.diffEditor.removedLineBackground, ui.diffEditor.removedTextBackground | `#5A3838` | 0 | 2 | 0.00 | 2 |
| ui.editor.background, ui.editor.lineHighlightBackground | `#1F2F20` | 1 | 2 | 3.39 | 2 |
| ui.editor.findMatchHighlightBackground, ui.editor.selectionBackground | `#375530` | 1 | 2 | 0.83 | 2 |
| ui.editor.inactiveSelectionBackground, ui.editor.lineHighlightBorder | `#2F452A` | 0 | 2 | 0.00 | 2 |
| ui.editorSuggestWidget.border, ui.editorSuggestWidget.selectedBackground | `#375530` | 1 | 2 | 2.26 | 2 |
| ui.editorSuggestWidget.foreground, ui.editorSuggestWidget.selectedForeground | `#E6F0DA` | 1 | 2 | 0.69 | 2 |
| ui.gitDecoration.addedResourceForeground, ui.gitDecoration.untrackedResourceForeground | `#A9C48A` | 0 | 2 | 0.00 | 2 |
| ui.list.activeSelectionForeground, ui.list.inactiveSelectionForeground | `#E9F2DC` | 0 | 2 | 0.00 | 2 |
| ui.list.focusHighlightForeground, ui.list.highlightForeground | `#C5E1A5` | 0 | 2 | 0.00 | 2 |
| ui.list.hoverBackground, ui.list.inactiveSelectionBackground | `#263824` | 1 | 2 | 4.66 | 2 |
| ui.scrollbarSlider.background, ui.scrollbarSlider.hoverBackground | `#7C8A70` | 1 | 2 | 4.95 | 2 |
| ui.statusBar.background, ui.statusBar.noFolderBackground | `#1F2F20` | 0 | 2 | 0.00 | 2 |
| ui.tab.activeModifiedBorder, ui.tab.inactiveModifiedBorder | `#D7C28A` | 0 | 2 | 0.00 | 2 |
| ui.terminal.ansiBlack, ui.terminal.background | `#1F2F20` | 1 | 2 | 2.30 | 2 |
| ui.terminal.ansiBrightWhite, ui.terminal.foreground | `#DCE7CF` | 1 | 2 | 2.87 | 2 |
| ui.terminal.ansiBrightYellow, ui.terminal.ansiYellow | `#D7C28A` | 1 | 2 | 4.19 | 2 |
| ui.terminal.ansiCyan, ui.terminal.ansiGreen | `#8FC9B4` | 1 | 2 | 5.62 | 2 |
| ui.titleBar.activeBackground, ui.titleBar.inactiveBackground | `#172618` | 1 | 2 | 1.96 | 2 |
| syntax.comment | `#7C8A70` | 0 | 1 | 0.00 | 0 |
| syntax.constant.language.import-export-all | `#D4D1C8` | 0 | 1 | 0.00 | 0 |
| syntax.entity.name.tag | `#96C66C` | 0 | 1 | 0.00 | 0 |
| syntax.entity.other.attribute-name | `#AFD1BA` | 0 | 1 | 0.00 | 0 |
| syntax.invalid | `#E08A8A` | 0 | 1 | 0.00 | 0 |
| syntax.keyword, syntax.storage | `#96C66C` | 0 | 1 | 0.00 | 0 |
| syntax.keyword.operator | `#D4D1C8` | 0 | 1 | 0.00 | 0 |
| syntax.operator | `#D4D1C8` | 0 | 1 | 0.00 | 0 |
| syntax.punctuation | `#93A187` | 0 | 1 | 0.00 | 0 |
| syntax.punctuation.definition.arguments, syntax.punctuation.definition.block, syntax.punctuation.definition.bracket, syntax.punctuation.definition.parameters, syntax.punctuation.definition.tag, syntax.punctuation.definition.typeparameters, syntax.punctuation.section | `#D4D1C8` | 0 | 1 | 0.00 | 0 |
| syntax.punctuation.definition.string, syntax.punctuation.definition.template-expression, syntax.punctuation.section.interpolation | `#DF7753` | 0 | 1 | 0.00 | 0 |
| syntax.string.escape | `#C9D89A` | 0 | 1 | 0.00 | 0 |
| syntax.string.regexp | `#C9B98A` | 0 | 1 | 0.00 | 0 |
| syntax.support.class.component | `#2AA198` | 0 | 1 | 0.00 | 0 |
| ui.activityBar.activeBorder | `#C5E1A5` | 0 | 1 | 0.00 | 0 |
| ui.activityBar.background | `#152417` | 0 | 1 | 0.00 | 0 |
| ui.activityBar.foreground | `#B7C9A4` | 0 | 1 | 0.00 | 0 |
| ui.activityBar.inactiveForeground | `#6E7A62` | 0 | 1 | 0.00 | 0 |
| ui.activityBarBadge.background | `#C5E1A5` | 0 | 1 | 0.00 | 0 |
| ui.activityBarBadge.foreground | `#232A20` | 0 | 1 | 0.00 | 0 |
| ui.badge.background | `#C5E1A5` | 0 | 1 | 0.00 | 0 |
| ui.badge.foreground | `#232A20` | 0 | 1 | 0.00 | 0 |
| ui.button.background | `#A9C48A` | 0 | 1 | 0.00 | 0 |
| ui.button.foreground | `#232A20` | 0 | 1 | 0.00 | 0 |
| ui.button.hoverBackground | `#C5E1A5` | 0 | 1 | 0.00 | 0 |
| ui.button.secondaryForeground | `#DCE7CF` | 0 | 1 | 0.00 | 0 |
| ui.descriptionForeground | `#96A488` | 0 | 1 | 0.00 | 0 |
| ui.dropdown.background | `#1E2E20` | 0 | 1 | 0.00 | 0 |
| ui.dropdown.border | `#465D40` | 0 | 1 | 0.00 | 0 |
| ui.dropdown.foreground | `#E6F0DA` | 0 | 1 | 0.00 | 0 |
| ui.editor.findMatchBorder | `#A9C48A` | 0 | 1 | 0.00 | 0 |
| ui.editor.foreground | `#D4D1C8` | 0 | 1 | 0.00 | 0 |
| ui.editorBracketHighlight.unexpectedBracket.foreground | `#D4D1C8` | 0 | 1 | 0.00 | 0 |
| ui.editorBracketMatch.background | `#2A392F` | 0 | 1 | 0.00 | 0 |
| ui.editorBracketMatch.border | `#7D9952` | 0 | 1 | 0.00 | 0 |
| ui.editorCursor.foreground | `#C5E1A5` | 0 | 1 | 0.00 | 0 |
| ui.editorError.foreground | `#E08A8A` | 0 | 1 | 0.00 | 0 |
| ui.editorGroup.border | `#34482F` | 0 | 1 | 0.00 | 0 |
| ui.editorGroupHeader.tabsBackground | `#1B2A1C` | 0 | 1 | 0.00 | 0 |
| ui.editorGutter.addedBackground | `#A9C48A` | 0 | 1 | 0.00 | 0 |
| ui.editorGutter.deletedBackground | `#E08A8A` | 0 | 1 | 0.00 | 0 |
| ui.editorGutter.modifiedBackground | `#D7C28A` | 0 | 1 | 0.00 | 0 |
| ui.editorHoverWidget.background | `#253525` | 0 | 1 | 0.00 | 0 |
| ui.editorHoverWidget.border | `#3A4F34` | 0 | 1 | 0.00 | 0 |
| ui.editorHoverWidget.foreground | `#E6F0DA` | 0 | 1 | 0.00 | 0 |
| ui.editorIndentGuide.activeBackground1 | `#58714C` | 0 | 1 | 0.00 | 0 |
| ui.editorIndentGuide.background1 | `#2D4029` | 0 | 1 | 0.00 | 0 |
| ui.editorInfo.foreground | `#8FC9B4` | 0 | 1 | 0.00 | 0 |
| ui.editorLineNumber.activeForeground | `#C5E1A5` | 0 | 1 | 0.00 | 0 |
| ui.editorLineNumber.foreground | `#6E7A62` | 0 | 1 | 0.00 | 0 |
| ui.editorLink.activeForeground | `#C5E1A5` | 0 | 1 | 0.00 | 0 |
| ui.editorOverviewRuler.bracketMatchForeground | `#7D9952` | 0 | 1 | 0.00 | 0 |
| ui.editorRuler.foreground | `#2D4029` | 0 | 1 | 0.00 | 0 |
| ui.editorSuggestWidget.background | `#253525` | 0 | 1 | 0.00 | 0 |
| ui.editorWarning.foreground | `#E0C07A` | 0 | 1 | 0.00 | 0 |
| ui.editorWhitespace.foreground | `#374C31` | 0 | 1 | 0.00 | 0 |
| ui.editorWidget.background | `#253525` | 0 | 1 | 0.00 | 0 |
| ui.editorWidget.border | `#3A4F34` | 0 | 1 | 0.00 | 0 |
| ui.editorWidget.foreground | `#E6F0DA` | 0 | 1 | 0.00 | 0 |
| ui.errorForeground | `#E08A8A` | 0 | 1 | 0.00 | 0 |
| ui.focusBorder | `#A9C48A` | 0 | 1 | 0.00 | 0 |
| ui.foreground | `#D4D1C8` | 0 | 1 | 0.00 | 0 |
| ui.gitDecoration.deletedResourceForeground | `#E08A8A` | 0 | 1 | 0.00 | 0 |
| ui.gitDecoration.modifiedResourceForeground | `#D7C28A` | 0 | 1 | 0.00 | 0 |
| ui.input.background | `#1E2E20` | 0 | 1 | 0.00 | 0 |
| ui.input.border | `#465D40` | 0 | 1 | 0.00 | 0 |
| ui.input.foreground | `#E6F0DA` | 0 | 1 | 0.00 | 0 |
| ui.input.placeholderForeground | `#96A488` | 0 | 1 | 0.00 | 0 |
| ui.inputOption.activeBorder | `#C5E1A5` | 0 | 1 | 0.00 | 0 |
| ui.list.activeSelectionBackground | `#375530` | 0 | 1 | 0.00 | 0 |
| ui.notifications.background | `#253525` | 0 | 1 | 0.00 | 0 |
| ui.notifications.border | `#3A4F34` | 0 | 1 | 0.00 | 0 |
| ui.notifications.foreground | `#E6F0DA` | 0 | 1 | 0.00 | 0 |
| ui.panel.background | `#1F2F20` | 0 | 1 | 0.00 | 0 |
| ui.panel.border | `#34482F` | 0 | 1 | 0.00 | 0 |
| ui.problemsErrorIcon.foreground | `#E08A8A` | 0 | 1 | 0.00 | 0 |
| ui.problemsInfoIcon.foreground | `#8FC9B4` | 0 | 1 | 0.00 | 0 |
| ui.problemsWarningIcon.foreground | `#E0C07A` | 0 | 1 | 0.00 | 0 |
| ui.quickInput.background | `#253525` | 0 | 1 | 0.00 | 0 |
| ui.quickInput.foreground | `#E6F0DA` | 0 | 1 | 0.00 | 0 |
| ui.scrollbarSlider.activeBackground | `#A9C48A` | 0 | 1 | 0.00 | 0 |
| ui.selection.background | `#375530` | 0 | 1 | 0.00 | 0 |
| ui.sideBar.background | `#1C2B1D` | 0 | 1 | 0.00 | 0 |
| ui.sideBar.border | `#34482F` | 0 | 1 | 0.00 | 0 |
| ui.sideBar.foreground | `#C2D0B2` | 0 | 1 | 0.00 | 0 |
| ui.sideBarSectionHeader.background | `#243522` | 0 | 1 | 0.00 | 0 |
| ui.sideBarSectionHeader.foreground | `#CFDCC0` | 0 | 1 | 0.00 | 0 |
| ui.statusBar.debuggingBackground | `#8A6A2E` | 0 | 1 | 0.00 | 0 |
| ui.statusBarItem.hoverBackground | `#4F6845` | 0 | 1 | 0.00 | 0 |
| ui.tab.activeBorderTop | `#A9C48A` | 0 | 1 | 0.00 | 0 |
| ui.tab.activeForeground | `#E4F1D6` | 0 | 1 | 0.00 | 0 |
| ui.tab.border | `#34482F` | 0 | 1 | 0.00 | 0 |
| ui.tab.inactiveForeground | `#8B9780` | 0 | 1 | 0.00 | 0 |
| ui.terminal.ansiBlue | `#8FB3C9` | 0 | 1 | 0.00 | 0 |
| ui.terminal.ansiBrightBlack | `#6E7A62` | 0 | 1 | 0.00 | 0 |
| ui.terminal.ansiBrightBlue | `#A8C7DB` | 0 | 1 | 0.00 | 0 |
| ui.terminal.ansiBrightMagenta | `#D6BCD6` | 0 | 1 | 0.00 | 0 |
| ui.terminal.ansiBrightRed | `#EEA0A0` | 0 | 1 | 0.00 | 0 |
| ui.terminal.ansiMagenta | `#C4A8C4` | 0 | 1 | 0.00 | 0 |
| ui.terminal.ansiRed | `#E08A8A` | 0 | 1 | 0.00 | 0 |
| ui.terminal.selectionBackground | `#375530` | 0 | 1 | 0.00 | 0 |
| ui.textLink.activeForeground | `#C5E1A5` | 0 | 1 | 0.00 | 0 |
| ui.textLink.foreground | `#A9C48A` | 0 | 1 | 0.00 | 0 |
| ui.titleBar.activeForeground | `#C7D5B8` | 0 | 1 | 0.00 | 0 |
| ui.titleBar.border | `#34482F` | 0 | 1 | 0.00 | 0 |
| ui.titleBar.inactiveForeground | `#7E8B72` | 0 | 1 | 0.00 | 0 |
| ui.tree.indentGuidesStroke | `#374C31` | 0 | 1 | 0.00 | 0 |

Control: `python3 scripts/cluster-dark-colors.py --semantic-distance 2 --color-distance 6`. Lower values keep more distinctions; higher values merge more. Threshold 0 keeps all distinct RGB bases. Path distance 0 permits only identical canonical paths; 1 permits parent/child; 2 also permits siblings. Colors must independently pass the OKLab limit. Derivation counts describe geometric grouping, not source provenance.

Conversion reference: https://bottosson.github.io/posts/oklab/
