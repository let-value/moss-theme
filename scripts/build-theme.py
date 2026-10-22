# -*- coding: utf-8 -*-
"""Build the Verdant Meadow Light / Dark color themes from one palette table.

Base palette: (light, dark) pairs below. Dark transplants and neighbor limits:
    palette/dark-transplants.json
Regenerate themes and dark reports:

    py -3 scripts/build-theme.py
"""

import json
from pathlib import Path
from dark_transplant import apply_transplants, write_reports
from refresh_color_reports import refresh

BASE = Path(__file__).resolve().parents[1]
THEMES = BASE / "themes"
NAME = "verdant-meadow-theme"
DISPLAY = "Verdant Meadow Theme"
VERSION = "1.0.0"
REPO = "https://github.com/vaxicy/verdant-meadow-theme"

UI = {
    "foreground": ("#3A4630", "#DCE7CF"),
    "editor.foreground": ("#3A4630", "#DCE7CF"),
    "terminal.foreground": ("#3A4630", "#DCE7CF"),
    "input.foreground": ("#2F3A26", "#E6F0DA"),
    "dropdown.foreground": ("#2F3A26", "#E6F0DA"),
    "quickInput.foreground": ("#2F3A26", "#E6F0DA"),
    "editorWidget.foreground": ("#2F3A26", "#E6F0DA"),
    "editorHoverWidget.foreground": ("#2F3A26", "#E6F0DA"),
    "editorSuggestWidget.foreground": ("#2F3A26", "#E6F0DA"),
    "notifications.foreground": ("#2F3A26", "#E6F0DA"),
    "descriptionForeground": ("#77846B", "#96A488"),
    "input.placeholderForeground": ("#77846B", "#96A488"),
    "focusBorder": ("#7E9468", "#A9C48A"),
    "inputOption.activeBorder": ("#5C6B4C", "#C5E1A5"),
    "input.border": ("#CBDCBB", "#4A5740"),
    "dropdown.border": ("#CBDCBB", "#4A5740"),
    "editor.background": ("#F7FAF2", "#232A20"),
    "tab.activeBackground": ("#F7FAF2", "#232A20"),
    "titleBar.activeBackground": ("#E3EFD7", "#1B2118"),
    "titleBar.activeForeground": ("#45523A", "#C7D5B8"),
    "titleBar.inactiveBackground": ("#EDF4E5", "#1F261C"),
    "titleBar.inactiveForeground": ("#8A9680", "#7E8B72"),
    "activityBar.background": ("#DCEBCE", "#191F17"),
    "activityBar.foreground": ("#46543A", "#B7C9A4"),
    "activityBar.activeBorder": ("#6C7B5A", "#C5E1A5"),
    "activityBar.inactiveForeground": ("#93A187", "#6E7A62"),
    "sideBar.background": ("#F0F7EA", "#20261D"),
    "sideBar.foreground": ("#3F4B36", "#C2D0B2"),
    "sideBarSectionHeader.background": ("#E4F0D9", "#283022"),
    "sideBarSectionHeader.foreground": ("#4C5A42", "#CFDCC0"),
    "panel.background": ("#F3F9EE", "#1F251C"),
    "terminal.background": ("#F3F9EE", "#1F251C"),
    "panel.border": ("#D3E1C4", "#38432F"),
    "editorGroup.border": ("#D3E1C4", "#38432F"),
    "tab.border": ("#D3E1C4", "#38432F"),
    "sideBar.border": ("#D3E1C4", "#38432F"),
    "titleBar.border": ("#D3E1C4", "#38432F"),
    "statusBar.background": ("#6C7B5A", "#46543A"),
    "statusBar.noFolderBackground": ("#6C7B5A", "#46543A"),
    "statusBar.foreground": ("#F4F9EE", "#E6F0DA"),
    "statusBar.noFolderForeground": ("#F4F9EE", "#E6F0DA"),
    "statusBarItem.hoverBackground": ("#5D6B4C", "#536245"),
    "statusBar.debuggingBackground": ("#8A5F2E", "#8A6A2E"),
    "statusBar.debuggingForeground": ("#FBF7EF", "#F6EEDC"),
    "editorGroupHeader.tabsBackground": ("#E9F2E0", "#1F251C"),
    "tab.inactiveBackground": ("#E9F2E0", "#1F251C"),
    "tab.activeForeground": ("#35422B", "#E4F1D6"),
    "tab.activeBorderTop": ("#90A479", "#A9C48A"),
    "tab.inactiveForeground": ("#7E8B72", "#8B9780"),
    "tab.hoverBackground": ("#E2EDD6", "#283022"),
    "tab.activeModifiedBorder": ("#7A6B3A", "#D7C28A"),
    "tab.inactiveModifiedBorder": ("#7A6B3A", "#D7C28A"),
    "list.hoverBackground": ("#E9F2DF", "#2A3324"),
    "list.activeSelectionBackground": ("#C5E1A5", "#3C5030"),
    "editorSuggestWidget.selectedBackground": ("#C5E1A5", "#3C5030"),
    "list.activeSelectionForeground": ("#2F3A26", "#E9F2DC"),
    "list.inactiveSelectionForeground": ("#2F3A26", "#E9F2DC"),
    "editorSuggestWidget.selectedForeground": ("#2F3A26", "#E9F2DC"),
    "list.inactiveSelectionBackground": ("#DFEBD2", "#33402A"),
    "list.highlightForeground": ("#4F6B3A", "#C5E1A5"),
    "list.focusHighlightForeground": ("#4F6B3A", "#C5E1A5"),
    "tree.indentGuidesStroke": ("#D5E3C8", "#3B4731"),
    "editorLineNumber.foreground": ("#A9B79B", "#6E7A62"),
    "editorLineNumber.activeForeground": ("#5C6B4C", "#C5E1A5"),
    "editor.lineHighlightBackground": ("#F0F7E7", "#2A3323"),
    "editor.lineHighlightBorder": ("#E5F0D9", "#33402A"),
    "editorCursor.foreground": ("#4F6B3A", "#C5E1A5"),
    "selection.background": ("#C5E1A5", "#3C5030"),
    "editor.selectionBackground": ("#C5E1A5", "#3C5030"),
    "terminal.selectionBackground": ("#C5E1A5", "#3C5030"),
    "editor.inactiveSelectionBackground": ("#DFEBD2", "#33402A"),
    "editor.wordHighlightBackground": ("#C5E1A580", "#4A5F3A80"),
    "editor.wordHighlightStrongBackground": ("#C5E1A580", "#4A5F3A80"),
    "editor.selectionHighlightBackground": ("#C5E1A566", "#4A5F3A66"),
    "editor.findMatchHighlightBackground": ("#DCEDB8", "#3F5230"),
    "editor.findMatchBackground": ("#B9D88C", "#4C6238"),
    "editor.findMatchBorder": ("#6C7B5A", "#A9C48A"),
    "editorBracketMatch.background": ("#D8EAC0", "#36432C"),
    "editorBracketMatch.border": ("#90A479", "#90A479"),
    "editorIndentGuide.background1": ("#DCE8CF", "#313B29"),
    "editorIndentGuide.activeBackground1": ("#A8B995", "#5C6B4C"),
    "editorWhitespace.foreground": ("#D2DFC5", "#3B4731"),
    "editorRuler.foreground": ("#E3EDD8", "#313B29"),
    "textLink.foreground": ("#4F6B3A", "#A9C48A"),
    "textLink.activeForeground": ("#4F6B3A", "#C5E1A5"),
    "editorLink.activeForeground": ("#3F5B2C", "#C5E1A5"),
    "quickInput.background": ("#FBFDF8", "#293025"),
    "editorHoverWidget.background": ("#FBFDF8", "#293025"),
    "notifications.background": ("#FBFDF8", "#293025"),
    "input.background": ("#FDFEFB", "#222920"),
    "dropdown.background": ("#FDFEFB", "#222920"),
    "editorWidget.background": ("#FBFDF8", "#293025"),
    "editorSuggestWidget.background": ("#FBFDF8", "#293025"),
    "editorWidget.border": ("#D3E1C4", "#3E4A34"),
    "editorHoverWidget.border": ("#D3E1C4", "#3E4A34"),
    "editorSuggestWidget.border": ("#D3E1C4", "#3E4A34"),
    "notifications.border": ("#D3E1C4", "#3E4A34"),
    "button.background": ("#90A479", "#A9C48A"),
    "button.foreground": ("#1F2A19", "#232A20"),
    "button.hoverBackground": ("#7E9468", "#C5E1A5"),
    "button.secondaryBackground": ("#E2EDD6", "#33402A"),
    "button.secondaryForeground": ("#3F4B36", "#DCE7CF"),
    "button.secondaryHoverBackground": ("#D5E3C8", "#3C5030"),
    "badge.background": ("#6C7B5A", "#C5E1A5"),
    "activityBarBadge.background": ("#6C7B5A", "#C5E1A5"),
    "badge.foreground": ("#FFFFFF", "#232A20"),
    "activityBarBadge.foreground": ("#FFFFFF", "#232A20"),
    "scrollbarSlider.background": ("#8A9A7866", "#7C8A7088"),
    "scrollbarSlider.hoverBackground": ("#7A8A6888", "#8B997E99"),
    "scrollbarSlider.activeBackground": ("#6C7B5A99", "#A9C48A99"),
    "errorForeground": ("#A64B4B", "#E08A8A"),
    "editorError.foreground": ("#A64B4B", "#E08A8A"),
    "problemsErrorIcon.foreground": ("#A64B4B", "#E08A8A"),
    "gitDecoration.deletedResourceForeground": ("#A64B4B", "#E08A8A"),
    "editorGutter.deletedBackground": ("#A64B4B", "#E08A8A"),
    "editorWarning.foreground": ("#8A6A1F", "#E0C07A"),
    "problemsWarningIcon.foreground": ("#8A6A1F", "#E0C07A"),
    "editorInfo.foreground": ("#3E6B5C", "#8FC9B4"),
    "problemsInfoIcon.foreground": ("#3E6B5C", "#8FC9B4"),
    "gitDecoration.addedResourceForeground": ("#4F7A46", "#A9C48A"),
    "gitDecoration.untrackedResourceForeground": ("#4F7A46", "#A9C48A"),
    "editorGutter.addedBackground": ("#4F7A46", "#A9C48A"),
    "gitDecoration.modifiedResourceForeground": ("#8A6B2E", "#D7C28A"),
    "editorGutter.modifiedBackground": ("#8A6B2E", "#D7C28A"),
    "diffEditor.insertedTextBackground": ("#D9EBC0AA", "#3C503066"),
    "diffEditor.removedTextBackground": ("#F0D9D8AA", "#5A383866"),
    "diffEditor.insertedLineBackground": ("#D9EBC066", "#3C503044"),
    "diffEditor.removedLineBackground": ("#F0D9D866", "#5A383844"),
    "terminal.ansiBlack": ("#3F4B36", "#2A3226"),
    "terminal.ansiRed": ("#A64B4B", "#E08A8A"),
    "terminal.ansiGreen": ("#4F7A46", "#A9C48A"),
    "terminal.ansiYellow": ("#8A6A1F", "#D7C28A"),
    "terminal.ansiBlue": ("#4A6B7A", "#8FB3C9"),
    "terminal.ansiMagenta": ("#7A5A7A", "#C4A8C4"),
    "terminal.ansiCyan": ("#3E6B5C", "#8FC9B4"),
    "terminal.ansiWhite": ("#8A9680", "#C2D0B2"),
    "terminal.ansiBrightBlack": ("#6E7A64", "#6E7A62"),
    "terminal.ansiBrightRed": ("#B85C5C", "#EEA0A0"),
    "terminal.ansiBrightGreen": ("#5E8C52", "#C5E1A5"),
    "terminal.ansiBrightYellow": ("#9C7C2C", "#E8CE96"),
    "terminal.ansiBrightBlue": ("#5A7D8C", "#A8C7DB"),
    "terminal.ansiBrightMagenta": ("#8E6B8E", "#D6BCD6"),
    "terminal.ansiBrightCyan": ("#4C8071", "#A8DCC8"),
    "terminal.ansiBrightWhite": ("#2F3A26", "#E6F0DA"),
}

TOKENS = [
    ("comment", ("#7C8A6E", "#7C8A70"), "italic"),
    (("keyword", "storage"), ("#3F6B2E", "#A9C48A"), None),
    ("string", ("#6E7C3A", "#D2DF9A"), None),
    (("entity.name.function", "support.function"), ("#2E6B54", "#8FC9A8"), None),
    (("entity.name.type", "support.type", "support.class"), ("#2F5B6B", "#9BC1C9"), None),
    (("constant.numeric", "constant.language", "variable.other.constant"), ("#8A5F2E", "#E0B87A"), None),
    ("variable", ("#3A4630", "#DCE7CF"), None),
    ("variable.parameter", ("#5A6B4A", "#C2D0B2"), None),
    (("variable.other.property", "support.variable.property"), ("#2F6B5B", "#8FC9B4"), None),
    ("keyword.operator", ("#6B7A5E", "#A8B79A"), None),
    ("punctuation", ("#7E8B72", "#93A187"), None),
    ("entity.name.tag", ("#3F6B2E", "#A9C48A"), None),
    ("entity.other.attribute-name", ("#8A6A2E", "#D7C28A"), None),
    ("string.regexp", ("#7A6B4A", "#C9B98A"), None),
    ("constant.character.escape", ("#6E7A3A", "#C9D89A"), None),
    ("markup.heading", ("#2F3A26", "#E4F1D6"), "bold"),
    ("markup.bold", ("#2F3A26", "#E4F1D6"), "bold"),
    ("markup.italic", ("#2F3A26", "#E4F1D6"), "italic"),
    ("invalid", ("#A64B4B", "#E08A8A"), None),
]

SEMANTIC = {
    "variable": "#3A4630|#DCE7CF",
    "parameter": "#5A6B4A|#C2D0B2",
    "property": "#2F6B5B|#8FC9B4",
    "function": "#2E6B54|#8FC9A8",
    "method": "#2E6B54|#8FC9A8",
    "type": "#2F5B6B|#9BC1C9",
    "class": "#2F5B6B|#9BC1C9",
    "interface": "#2F5B6B|#9BC1C9",
    "variable.readonly": "#8A5F2E|#E0B87A",
}

PACKAGE = {
    "name": NAME,
    "displayName": DISPLAY,
    "description": "Calm meadow green: pale sage light mode with olive ink, and a deep olive night with fresh leaf highlights.",
    "version": VERSION,
    "publisher": "lilinhuang",
    "engines": {"vscode": "^1.80.0"},
    "categories": ["Themes"],
    "keywords": ["theme", "light", "dark", "green", "sage", "olive", "pastel", "meadow"],
    "icon": "assets/icon.png",
    "license": "SEE LICENSE IN LICENSE",
    "galleryBanner": {"color": "#232A20", "theme": "dark"},
    "repository": {"type": "git", "url": REPO},
    "contributes": {
        "themes": [
            {
                "label": f"{DISPLAY} Light",
                "uiTheme": "vs",
                "path": f"./themes/{NAME.replace('-theme', '')}-light-color-theme.json",
            },
            {
                "label": f"{DISPLAY} Dark",
                "uiTheme": "vs-dark",
                "path": f"./themes/{NAME.replace('-theme', '')}-dark-color-theme.json",
            },
        ]
    },
}


def build(variant, index):
    colors = {key: pair[index] for key, pair in UI.items()}
    tokens = []
    for scope, pair, style in TOKENS:
        settings = {"foreground": pair[index]}
        if style:
            settings["fontStyle"] = style
        tokens.append({"scope": [scope] if isinstance(scope, str) else list(scope),
                       "settings": settings})
    semantic = {key: value.split("|")[index] for key, value in SEMANTIC.items()}
    theme = {
        "name": f"{DISPLAY} {variant.title()}",
        "type": variant,
        "colors": colors,
        "semanticHighlighting": True,
        "semanticTokenColors": semantic,
        "tokenColors": tokens,
    }
    if variant == "dark":
        theme, _, _ = apply_transplants(theme)
        write_reports(theme)
    out = THEMES / f"{NAME.replace('-theme', '')}-{variant}-color-theme.json"
    out.write_text(json.dumps(theme, indent=2) + "\n", encoding="utf-8")
    print("wrote", out.relative_to(BASE), len(theme["colors"]), "UI colors")


def main():
    THEMES.mkdir(exist_ok=True)
    for index, variant in enumerate(("light", "dark")):
        build(variant, index)
    (BASE / "package.json").write_text(
        json.dumps(PACKAGE, indent=2) + "\n", encoding="utf-8")
    print("wrote package.json")
    refresh()


if __name__ == "__main__":
    main()
