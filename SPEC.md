# Moss specification

25 October 2026 · Proposed design

Moss is a color authoring tool. Define a tree of colors, reuse those colors in other trees, and choose better values by comparing alternatives inside editor previews.

The application has three independent capabilities: **token trees**, **tournaments**, and **previews**. A small application shell connects them. Each capability must remain understandable and usable without the other two.

This document defines the product behavior and implementation boundaries. Simplicity comes from small independent modules, explicit data, and direct composition. Each business rule has one implementation; every visible value follows the same resolution path.

## 1. The product in one example

An author creates a root palette with `canvas`, `ink`, and `leaf`. They may add any names, groups, or depth; Moss assigns no special meaning to those names.

They add Base16, Zed, and VS Code child trees. These contain target-specific tokens, most of which link to colors already defined elsewhere:

```text
Root palette
├─ surfaces
│  └─ canvas                      = #132118
├─ text
│  └─ ink                         = #d4d1c8
├─ accents
│  └─ leaf                        = #96c66c
│
├─ Base16
│  ├─ base00                      → surfaces/canvas
│  ├─ base05                      → text/ink
│  └─ base0B                      → accents/leaf
├─ Zed
│  ├─ editor.background           → Base16/base00
│  └─ syntax/keyword/color        → accents/leaf
└─ VS Code
   ├─ colors/editor.background    → Base16/base00
   └─ syntax/keyword/color        → accents/leaf
```

The arrows represent references, not copied values. Updating `leaf` updates every token that resolves to it. Zed can instead give its keyword token a local color without changing VS Code.

To improve `leaf`, the author supplies several candidate colors and starts a tournament. Two otherwise identical editor previews show the current pair. Preferences advance the bracket and update ratings. The leading candidate automatically supplies the effective color, so linked uses and exports follow it. The completed bracket identifies a champion and runner-up; the author can keep the champion as the recorded choice.

**The root palette is arbitrary. Base16, Zed, and VS Code are useful child trees, not special cases in the color model.** The diagram abbreviates each color to one appearance; the workspace stores dark and light values separately.

## 2. Token trees

### Structure and identity

A workspace contains one root tree and any number of child trees. A tree contains groups and named color tokens. Groups can nest. Child trees may be based on a supplied target template or created by the author.

Every tree, group, and token has a stable identity. Names and positions are presentation; renaming or moving a token does not break links or tournament history. A target key such as `editor.background` remains an exact external name: dots do not implicitly create groups.

The author can create, rename, move, and remove groups and custom tokens; set colors; and make or remove links. Target templates provide external keys and initial explicit links as ordinary workspace data. They never require particular root token names. If a mapping cannot be supplied, it remains visibly unmapped until the author sets it.

Containment answers **where does this token belong?** A reference answers **where does its color come from?** A parent group or tree never supplies an implicit color.

### Exactly one source

Every color token has exactly one active source:

```text
Local:      authored values or a rated candidate pool, separately per appearance
Reference:  the identity of one other color token
```

A reference is authoritative while linked; a token cannot simultaneously apply a local override. A local token uses its provisioned pool's selection policy, or its directly authored value when it has no pool. The effective value is derived in one place, never copied into competing active values. A hover color or diagnostic background is an ordinary authored token, not a generated shade.

References can target any color token in the workspace, including another child tree. Tree position does not impose a second set of linking rules. Self-links, cycles, and missing targets are invalid. Groups and non-color settings cannot be reference targets.

Resolution follows references until it reaches a local source, then uses that source's direct value or selected candidate. It returns the resolved value, the source token, and the complete reference chain, or a useful error. Where a source contains paired colors, a reference also identifies the color field it uses. A valid long chain must not fail because of an arbitrary hop limit.

### Editing without surprises

- **Edit source:** follow the selected token's reference chain and open the terminal source's value or pool controls. Show the source name and affected tokens.
- **Make independent:** replace the reference with its currently resolved dark and light values. Missing appearances remain missing. This changes no visible color and creates no candidates.
- **Link:** make the selected reference authoritative. Show the new value and source chain. If it would make the graph invalid, leave the workspace unchanged. Local authoring history is inactive while linked.
- **Remove:** block removal of a token, group, or tree while surviving tokens refer into it. List the references so the author can relink or detach them first.

Dark and light share tree structure and references. Local values, pools, choices, ratings, and brackets are separate per appearance. Missing light values never come from dark values, and switching appearance never generates colors.

Accept hex, CSS RGB, OKLCH, and alpha. One small color boundary validates input and converts consistently for comparison, rendering, and export. Equivalent spellings compare equally; alpha remains significant. No color transforms are part of token resolution.

## 3. Tournaments

### A tournament asks one question

**Which candidate color should this source token use, in this appearance and this theme context?**

A candidate has a stable identity, label, color, rating, and comparison count, with optional background, bold, and italic attributes. Diagnostic candidates can compare foreground/background pairs. A pool belongs to one local source token and one appearance. Linked tokens share the terminal source's pool; they never receive duplicate pools automatically.

Pools are plain, validated workspace data curated in conversation with a coding agent. The author supplies a pool for a named source and appearance, reloads it, and compares it in the application. Opening a token, switching appearance, or loading an editor theme must not generate candidates or expand a pool.

Starting from a linked token shows “Comparing source: …” and the affected uses. To compare that child token independently, the author first makes it independent.

### Brackets and ratings

A tournament has three phases:

1. **Winners:** shuffle entrants into pairs. Pair winners advance to the next round; pair losers enter a second-chance pool. An unpaired entrant advances with a bye. Repeat until one winners champion remains.
2. **Second chance:** run the collected losers through shuffled rounds. Pair winners advance, pair losers leave the tournament, and an unpaired entrant receives a bye. Repeat until one second-chance champion remains.
3. **Final:** compare the two champions once. The preferred candidate is the tournament champion; the other is runner-up. There is no final reset or additional match.

Shuffle each round when it is created and persist its order. Reloading does not reshuffle a pending comparison. Byes require no preference and do not change ratings or counts. A pool with fewer than two distinct candidate appearances cannot start a tournament.

Candidates start at rating `1000` and comparison count `0`. Each preference updates both ratings using their values immediately before the vote:

```text
expectedWinner = 1 / (1 + 10 ^ ((loserRating - winnerRating) / 400))
change = round(32 × (1 - expectedWinner))
winnerRating += change
loserRating  -= change
```

Increment both comparison counts by one. Bracket progress and ratings are separate facts: neither substitutes for the other.

Keep every authored candidate and its history. Avoid indistinguishable matchups by choosing one entrant per visual appearance for a run. Appearance includes foreground, background, alpha, bold, and italic; identical foregrounds with different backgrounds are distinct choices. Show duplicate appearances in the pool rather than deleting authored data. Fewer than two distinct appearances cannot start a bracket.

The engine operates on candidate data, ratings, and bracket state. It has no editor names, token-resolution logic, UI, or persistence calls. Store brackets per source and appearance, allowing selection to move between them without losing progress. Reload restores the same pending pair.

### Effective color and recorded choice

The highest-rated candidate is the effective value automatically. A vote can therefore change the theme immediately. A recorded choice breaks a tie when it is among the leaders. Any remaining tie uses stable stored candidate order, never a random render-time choice. Supplying a pool sets its recorded choice explicitly; updating that pool leaves the choice unchanged while its candidate is present.

**Keep champion** records the bracket champion as that source's tie preference for the selected appearance. The rating leader supplies the effective value; the recorded choice decides only among tied leaders. A bracket champion, a rating leader, and a recorded tie preference are distinct facts.

**Reset ratings** records the effective candidate as the tie preference, resets all pool ratings to `1000` and counts to `0`, and ends the affected bracket. Candidates, links, authored values, and the displayed appearance stay unchanged.

The user can start and end brackets, prefer A or B, inspect ratings and pick counts, keep a champion, copy the leaderboard, and save or load results. Ending a bracket leaves earned ratings unchanged. Switching token, target, or appearance does not discard other brackets or choices.

### Two candidate views

For a pending comparison, resolve the same current workspace twice, overriding the source with candidate A or B **before following references**. Include the candidate's paired background and typography where applicable. All linked uses follow that candidate; unrelated values and scene state remain identical between panes.

Candidate overrides exist only in the preview inputs. Normal preview and export use the current rating-selected values. Prefer buttons and arrow shortcuts record only the pair currently displayed, and only while a bracket is running.

## 4. Editor previews

### One shared contract

A preview consumes resolved target values and a scene state. It renders those values and can report which token a painted surface represents. It does not resolve links, select winners, edit the workspace, or know that a tournament exists.

Outside a tournament, show one preview of the authored theme. During a tournament, show two equally sized panes using the same target, scene, sample, font, viewport, interaction state, and scroll position. Only the candidate substitution and its dependents differ.

Each pane has independent theme values. Updating one must not repaint the other through a global theme service. Candidate changes update the current scene without resetting its state or restarting an editor runtime.

### Rendering and interaction

Provide a palette overview and Base16, Zed, and VS Code previews. They expose code, workbench surfaces, diagnostics, selections/search, diffs, Git decorations, and terminal colors, including syntax colors, semantic colors, typography, and backgrounds.

Previews support scratch editing, cursor movement, selection, sample/file tabs, and search. Scene controls include case-sensitive and whole-word search, match navigation, closing and reopening sample tabs through quick-open, collapsing change groups, toggling sample staging, and showing or hiding dock panels. These interactions expose focused, active, hover, selected, and disabled colors. Scratch content and scene state are shared between A and B and survive theme updates; scratch edits are separate from persisted theme data. Preview arrow keys move the cursor rather than voting. Token inspection is a temporary mode, separate from normal editing.

The VS Code preview uses real editor/workbench rendering. TextMate syntax rules and semantic token rules from the target mapping both affect the sample; selections, diagnostics, gutters, minimap, and workbench surfaces use their corresponding target colors. After scratch edits, syntax highlighting follows the edited text. A fixed semantic fixture must be disabled or regenerated when its offsets become stale.

Zed and Base16 use browser reference scenes. Zed syntax captures use the longest matching dotted capture name. An exact capture supplies its entire style; an omitted color uses editor foreground. Paint explicit syntax backgrounds, font weight, and font style. State where curated highlighting or browser rendering differs from native behavior. Sample Git and terminal surfaces do not execute Git commands or terminal processes.

Editor integration belongs entirely inside the preview boundary. Its rendering requirements do not introduce editor dependencies into the token model or tournament engine.

Each scene explicitly maps painted surfaces and syntax spans to target tokens. It declares only the tokens it actually paints. Clicking an amber pixel cannot identify its token: two unrelated tokens may share amber.

**Pick token** temporarily enables inspection. If a surface paints several tokens, offer the relevant foreground, background, and border choices. Selection opens the target token and its source chain, then returns to normal preview interaction. Escape cancels picking. Text selection and scrolling must not cast votes.

For the selected token, indicate whether the scene shows it. If another scene covers it, offer that scene. If no scene covers it, say so and keep its swatch and source inspectable. Do not present two identical editor panes as a meaningful comparison when the candidate has no visible use there.

### Preview and export must agree

A target adapter converts a resolved child tree into target-specific values. Both the preview and the exporter consume that same mapping. No exporter may generate extra colors that the preview has never received.

Each target owns its external key names, syntax mapping, metadata, validation, and serialization. Structured settings such as font style remain adapter data, separate from color references. Adding a target must not add branches to token resolution or tournament advancement.

Every preview states its fidelity: which target mapping it uses, what it paints, and what is approximate. A coverage audit lists the target tokens painted by each scene and identifies tokens without a scene. Coverage is a claim about painted tokens, not pixel parity with a native application.

## 5. The application around them

The workspace has three visible areas: a searchable tree, the selected token's source/value controls and tournament controls, and the preview. Appearance and target selection stay easy to reach. Two-pane comparison appears only during a run.

Keep the author oriented: show the selected token, the source being changed, its current color, and whether the view is authored or comparing candidates. Color swatches always have a textual name or value. Controls are keyboard reachable, focus remains visible, and voting shortcuts ignore inputs, modified keys, and repeated keydown events.

Save the workspace after authored changes and tournament decisions. Maintain one authoritative logical workspace containing trees, references, local values, pools, recorded choices, ratings, brackets, and results. Resolved values are derived, not a second saved palette. Workspace files are readable and editable by the author or coding agent; browser recovery protects unsaved work. Persistence format and transport remain outside the domain modules. Detect conflicting writes at that boundary rather than silently overwriting newer agent or browser edits.

Reload restores the same authored colors and pending pair. Loading a workspace validates it before replacing the current document. A malformed file reports errors and leaves the current workspace intact; it never repairs itself by adding defaults. Save failures are visible and leave an exportable in-memory workspace.

Export has two meanings: **save the complete workspace/results** for later authoring, or **download a resolved target theme** for use elsewhere. Target exports use current effective values, including automatic rating-selected colors, never one side's temporary candidate override. The author can inspect and edit generated JSON before downloading it. Editing the export text does not modify workspace tokens. Missing values or invalid target mappings block that target's export with named errors. Errors in an unrelated child tree do not block a valid target.

A new workspace may be empty or explicitly created from a starter. A starter is editable data, never an invisible runtime fallback. The author can load and validate reference themes from VS Code and Zed JSON and Zed Theme Builder archives containing theme JSON. Reference loading does not create candidates or replace decisions. Adapters represent target metadata and structured settings explicitly, including syntax font styles and backgrounds, so theme data is not flattened into colors alone.

Saving and loading a workspace round-trips palette values, curated pools, candidate identities, ratings, recorded choices, links, brackets, saved results, and structured target metadata. Accounts, cloud synchronization, publishing, and automatic editor installation are outside the product scope.

## 6. Implementation boundaries

Use **Void** for application integration and **Vite+** for the development toolchain. Void's setup supports a Vite+ toolchain and a choice of view library; the specific view library is a scaffolding decision, not a domain requirement. Do not add server resources until a product behavior needs them. See [Void setup](https://void.cloud/reference/cli/setup) and the [Vite+ guide](https://viteplus.dev/guide/).

The following are responsibilities, not a demand for packages, classes, or a plugin framework:

| Part              | Owns                                                                    | Must work without                                     |
| ----------------- | ----------------------------------------------------------------------- | ----------------------------------------------------- |
| Token model       | Tree edits, source validation, reference resolution, dependency tracing | DOM, editor schemas, candidates, tournaments, storage |
| Tournament        | Entrants, brackets, Elo, counts, ranking, recorded choices, results     | Token trees, editor schemas, rendering, storage       |
| Target adapters   | External names, resolved mappings, target validation and files          | Tournament state, application controls                |
| Previews          | Scenes, painting, scene state, token picking                            | Authored graph, pools, bracket rules, storage         |
| Application shell | Selection, commands, candidate substitution, save/load, composition     | A second domain model                                 |

Token resolution takes data and a supplied source-value lookup, then returns data; it does not implement Elo. Tournament advancement and selection take candidate data and return data; they do not walk trees. A preview can render a fixed resolved fixture. The shell supplies the tournament's effective value to the resolver. Those statements are the isolation test.

Prefer direct functions and small explicit records. Have one source representation, one resolver, one color conversion boundary, and one target mapping per editor. Introduce an abstraction only when it removes an actual repeated rule. Avoid event buses, dependency injection containers, generic repository layers, runtime plugin discovery, and parallel models of the same state.

Implement the rules in this document directly, with fixtures that demonstrate their inputs and outputs. A capable editor library can supply substantial rendering and interaction behavior behind a small, contained integration.

Minimal code means fewer concepts and fewer places to change a rule. It does not mean compressed code, unexplained cleverness, an arbitrary line-count target, or fewer product capabilities. Dependencies must justify a behavior in this spec; large preview runtimes must remain encapsulated and load only when needed.

### Implementation rules

- **One token identity and source rule.** Root, Base16, Zed, and VS Code colors use the same model. Editor names do not appear in reference traversal. Target defaults become explicit data rather than extra resolution branches.
- **One implementation per business rule.** Elo, bracket advancement, effective selection, tie handling, and reset behavior are small named functions in the tournament module. UI handlers call them; they never reimplement them.
- **Derived views instead of synchronized copies.** Swatches, inspector values, previews, and exports all read the same resolution result. Do not write winners back into multiple editor-specific override stores to make screens agree.
- **Direct composition.** A command updates authoritative state, affected views read it, and persistence saves it. Keep selection and scratch state distinct from authored data. Avoid chains of repair, normalization, and synchronization callbacks.
- **Data for catalogs; code for behavior.** Editor key lists, grouping, mappings, and sample fixtures are plain records. Do not hand-write a branch or component for each token.
- **Small seams, not a framework inside the app.** Separate modules within one application are enough. No mandatory package-per-feature structure, universal plugin protocol, speculative caches, or generalized command machinery.

A reviewer must be able to follow one vote through rating update, bracket advancement, selected value, reference resolution, preview, and save without discovering another implementation of any rule. Changing a bracket rule touches tournament code; changing an editor mapping touches its adapter; changing storage touches persistence. These are implementation acceptance conditions, alongside the behavioral examples below.

## 7. Acceptance examples

The implementation is complete when these observable behaviors hold:

| Given / action                                                                       | Required result                                                                                                     |
| ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------- |
| Create a nested root token named `lichen`                                            | It works without adding a role, enum, or editor-specific rule                                                       |
| Link Base16 → root and Zed → Base16; change the root value                           | Both child values, their preview surfaces, and exported values update                                               |
| Rename or move the root token                                                        | References and results still point to the same identity                                                             |
| Detach Zed's linked token                                                            | Both appearances keep their resolved colors; subsequent root edits leave Zed independent                            |
| Attempt a self-link, cycle, missing reference, or deletion with surviving references | Reject the operation; leave the workspace unchanged                                                                 |
| Supply a dark value but no light value                                               | Light remains explicitly unresolved after switching and reloading                                                   |
| Lose in the winners bracket                                                          | The candidate enters the second-chance bracket rather than disappearing after one loss                              |
| Complete a bracket with an odd pool size                                             | Byes need no vote; the winners and second-chance champions meet in one final that determines champion and runner-up |
| Prefer A between two candidates rated 1000                                           | A becomes 1016, B becomes 984, and both pick counts increase by one                                                 |
| Supply two equivalent complete candidate appearances                                 | Both authored entries remain visible; the bracket avoids comparing identical appearances                            |
| Supply the same foreground with a different background or typography                 | The candidates remain distinct and their full appearance is previewed                                               |
| Compare a root color used by several child tokens                                    | Every dependent use changes on that side; unrelated colors remain identical                                         |
| Vote, switch source or appearance, reload, return                                    | Ratings and bracket progress survive; the same pending pair resumes                                                 |
| A vote creates a new rating leader                                                   | Normal preview, linked uses, and target export adopt it immediately; no apply action is required                    |
| Leaders tie                                                                          | The recorded choice wins when among them; repeated renders do not change the result                                 |
| Keep the bracket champion                                                            | Its identity becomes the recorded choice without replacing ranking with a new selection mechanism                   |
| Reset ratings or end a bracket                                                       | Reset keeps the effective appearance while resetting ratings/counts; ending alone keeps earned ratings              |
| Vote in dark appearance                                                              | Dark ratings and effective values change; light values, ratings, and progress remain intact                         |
| Render different colors in A and B, then update A                                    | B's colors stay unchanged and both panes share synchronized scene state                                             |
| Pick one of two same-colored surfaces                                                | Selection follows its semantic token mapping, not a color lookup                                                    |
| Select a token absent from all scenes                                                | The application reports the gap instead of implying visible coverage                                                |
| Render and export a target fixture with syntax colors and alpha                      | Both use the same resolved values; target color conversion follows one policy                                       |
| Edit, search, switch sample tabs, or scroll during comparison                        | Both panes share scratch/scene state; theme changes do not reset it; text keys do not vote                          |
| Load a reference theme or Builder archive                                            | Validate and inspect it while leaving candidates, ratings, and choices unchanged                                    |
| Save and load a workspace                                                            | Candidate IDs, values, links, ratings, choices, brackets, and structured target metadata round-trip unchanged       |
| Load malformed workspace data or encounter a write conflict                          | Keep valid current data and report the problem; never silently seed or overwrite newer work                         |

Use small domain tests for the graph and tournament rules, adapter fixtures for target outputs, and a few rendered checks for A/B isolation, semantic picking, and actual painted colors. A screenshot alone does not prove a token is wired correctly. Use Vite+ to check, test, and build the eventual implementation.

## 8. Build in independent slices

1. **Tokens:** arbitrary trees, local sources, references, validation, dark/light values, and workspace round-trip. Demonstrate using plain fixtures.
2. **Tournaments:** implement brackets, Elo, ranking, recorded choices, reset, and restore using candidate fixtures. No editor dependency.
3. **Previews:** render resolved fixtures with the specified fidelity, scratch/scene interactions, and semantic picking. No tournament dependency.
4. **Composition:** supply rating-selected values to the resolver, connect A/B candidate overrides, import/export, and persistence. Verify the full authoring loop.

These milestones establish independently usable modules before composition. Completion requires both the behavioral acceptance examples and the implementation rules above.
