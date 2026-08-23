# Man page and terminal-help conventions

## Question and repository context

This note asks which established conventions should govern the Collection's user-facing `help.md` files. It records evidence rather than adding a second coding standard; the normative rule belongs in [`docs/coding-standard/skills.md`](../coding-standard/skills.md).

The repository currently makes one Markdown artifact serve three help spellings: `--help`, `-h`, and `help` print `help.md` verbatim, and the same file is called the Skill's man page ([ADR-0044](../adr/0044-help-lives-with-the-skill.md)). No file is installed into a numbered system manual section and no roff formatter adds a title, indentation, font changes, indexing metadata, or a pager. The result is therefore a project-specific hybrid: a complete reference page delivered through a help route, not an installed Unix man page.

## Source authority and limits

- [Linux `man-pages(7)`](https://man7.org/linux/man-pages/man7/man-pages.7.html) is the strongest source here for the content, ordering, wording, and typography of Linux manual pages. It explicitly says its conventions may help other projects, but many details are policies of the Linux man-pages project rather than universal law.
- [GNU `groff_man(7)`](https://man7.org/linux/man-pages/man7/man.7.html) and [`groff_man_style(7)`](https://man7.org/linux/man-pages/man7/groff_man_style.7.html) define the structure and rendering semantics of actual roff `man` documents. Their semantic hierarchy is relevant; their macros, escapes, source wrapping, title metadata, and formatter-specific spacing are not requirements for Markdown shown in a conversation.
- [POSIX Utility Conventions](https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap12.html) define command synopsis notation and portable option syntax. They do not define the prose or visual layout of `--help`, and their single-character option guidelines do not prohibit the GNU-style long options this Collection already exposes.
- [GNU command-line interface standards](https://www.gnu.org/prep/standards/html_node/Command_002dLine-Interfaces) and the [`--help` standard](https://www.gnu.org/prep/standards/html_node/_002d_002dhelp.html) govern terminal help rather than installed man pages. GNU says `--help` writes brief invocation documentation to standard output, exits successfully, and performs no normal work; it does not require a complete man page there.
- [GNU `help2man`](https://www.gnu.org/software/help2man/) demonstrates a controlled bridge between the artifacts: it rearranges conventional `--help` and `--version` output into a simple man page, and supplements generated sections when the program output is insufficient. [GNU's Texinfo guidance](https://www.gnu.org/software/texinfo/manual/texinfo/html_node/Adding-Output-Formats.html) is explicit that a good traditional man page has its own strict conventional form and is not simply another rendering of tutorial or reference prose.
- ripgrep is a useful example, not a standard. Its [official FAQ](https://github.com/BurntSushi/ripgrep/blob/master/FAQ.md#does-ripgrep-have-a-man-page) says the option documentation in `man rg` and `rg --help` is equivalent while `rg -h` gives one line per option, and its [official guide](https://github.com/BurntSushi/ripgrep/blob/master/GUIDE.md#common-options) describes `--help` as the long form that is nearly the man page. The example therefore supports tiers of help, not a general claim that every `--help` must be a complete man page.

## Installed man page and terminal help are different profiles

An installed command page is a separately addressable document, normally in manual section 1, with machine-readable title and `NAME` metadata. A formatter renders its roff structure for the output device and `man` normally supplies paging and search. Its purpose is durable reference.

Terminal `--help` is immediate invocation guidance. GNU's standard calls it brief, while `help2man` recommends a synopsis, a very short explanation including normal or default behaviour, options, useful behavioural qualifications, a few examples when valuable, and support links near the end. It must be safe to request without starting the command's normal work.

The repository has deliberately selected a third profile: the long reference is the direct response to every help spelling. That can be retained, but the coding standard should describe it honestly as a **man-page-shaped Markdown reference**, not imply that the files are installed man pages or that upstream man-page standards require full terminal help. If a concise tier like ripgrep's `-h` is ever desired, that is a product-interface change beyond editorial reformatting; the current ADR makes all three routes identical.

## Structure that should govern these pages

The conventional order for command pages begins `NAME`, `SYNOPSIS`, `DESCRIPTION`, and `OPTIONS`, followed when relevant by `EXIT STATUS`, `ENVIRONMENT`, `FILES`, `NOTES`, `CAVEATS`, `BUGS`, `EXAMPLES`, and `SEE ALSO`. `man-pages(7)` advises using a traditional heading where one fits, adding custom headings only when traditional sections and subsections cannot carry the material, and arranging sections in the conventional order.

The recommended required set for every Collection page is the top-level page title plus `NAME`, `SYNOPSIS`, `DESCRIPTION`, the Collection-specific `DEPENDENCIES`, and `SEE ALSO`. `POSITIONAL ARGUMENTS` or a more precise operand heading and `OPTIONS` are required when that interface exists. `EXIT STATUS`, `ENVIRONMENT`, `FILES`, `NOTES`, `CAVEATS`, `BUGS`, and `EXAMPLES` are conditional: include each only when it has useful content, although `EXAMPLES` should be strongly preferred for a non-obvious invocation. This makes relevance, rather than a fixed empty template, the governing principle.

For this repository, the corresponding Markdown profile should be:

1. Keep the top-level Markdown title as the page identifier, analogous to roff title metadata but without pretending that the Skill has a numbered manual section.
2. Add `## NAME` first, containing exactly the invocation name, a hyphen, and a concise one-line summary. The name-summary form is indexed by `mandb` and `makewhatis` in an actual man page; preserving it here makes the page recognisable and forces a useful summary.
3. Put `## SYNOPSIS` next. Give every genuinely distinct invocation form its own line and show the accepted grammar, not examples or explanations.
4. Use `## DESCRIPTION` for the normal case, defaults, inputs, outputs, side effects, and the smallest mental model needed to use the Skill. Keep option-specific details under `OPTIONS` and omit implementation history, internal machinery, rejected alternatives, issue evidence, and architectural rationale unless one is essential to correct use.
5. Use `## POSITIONAL ARGUMENTS` or another precise conventional argument heading when operands need definition, followed by `## OPTIONS` for flags. Group a short and long alias as one term, state what each option changes, and include its default, constraints, repeatability, and important interactions where those facts matter.
6. Add only relevant standard sections after `OPTIONS`: for example `ENVIRONMENT`, `FILES`, `CAVEATS`, or `EXAMPLES`. Prefer a precise standard section over putting unrelated material into `NOTES`; `man-pages(7)` defines `NOTES` only as miscellaneous notes.
7. Keep `DEPENDENCIES` as an explicit Collection-specific extension for the reader deciding whether to Enable a Skill. Its mandatory presence, including `None`, is a local product decision rather than man-page convention and should be labelled that way in the coding standard.
8. End with `## SEE ALSO`. An installed page uses a comma-separated list ordered by manual section and then name, without a final period. These Skills have no numbered manual-section identity, so list related Skill invocations concisely and consistently rather than inventing references such as `commit(1)`.

The current blanket requirements that every page contain `NOTES` and `OPTIONS`, even without useful content, are not supported by the sources: traditional sections are selected for relevant content. Conversely, the current page opening of a title followed by an unlabelled summary omits the conventional `NAME` section. Those are the clearest structural corrections to the existing repository rule; keeping an explicit empty `DEPENDENCIES` section remains justified by the page's Collection-specific enablement audience, not by man-page convention.

## Synopsis notation

In a command synopsis, literal command text and options are conventionally bold, while replaceable arguments are italic. Square brackets mean optional, a vertical bar separates alternatives, and an ellipsis marks repetition. POSIX uses multiple synopsis lines when mutually exclusive arguments create distinct valid invocation forms; `man(1)` likewise says the synopsis pattern should match every possible invocation and may use several exclusive forms.

In Markdown, map those semantics rather than copying roff escapes: render a literal invocation or flag in bold, render a metavar in italics, and leave the punctuation literal. Use stable, descriptive metavariables such as *SKILL*, *PATH*, and *COUNT*. Use one spelling for repetition throughout, preferably the portable ASCII `...`, and attach it to the syntactic unit that repeats.

For example:

```markdown
**/example** [**--project**] [**--output** *PATH*] *INPUT*...
**/example** **--status**
```

Do not compress forms whose accepted options differ into an ambiguous mega-synopsis. Separate lines are cheaper to read and make invalid combinations visible. Any synopsis, option table, `argument-hint`, and parser instruction must still describe one identical grammar; that repository invariant is stronger than visual convention.

## Options, arguments, and examples

Actual man pages use tagged paragraphs for term-description pairs, not generic bullets. `groff_man(7)` supplies the `TP` macro for a hanging tag, and `man-pages(7)` distinguishes tagged paragraphs from unordered lists. Markdown has no portable CommonMark definition-list syntax, so the repository should use one consistent approximation: put the complete option or argument signature first with literal tokens bold and metavariables italic, then its description; a one-line bullet is acceptable where needed to preserve association in the renderer, but the bullet is an adaptation rather than the man-page semantic.

Options should be easy to scan by spelling. With only a few options, one list is enough. With many, group by user task or affected behaviour and keep the ordering predictable within a group; ripgrep's long help and man page are an example of functional grouping. Avoid creating a subsection for every isolated rule when a tagged entry can carry it.

Examples belong in `EXAMPLES`, not in `SYNOPSIS`. `man-pages(7)` defines the section as demonstrations of real use, while `help2man` recommends a few typical examples because one concrete invocation can replace substantial explanation. Include an example when it resolves a non-obvious combination, default, destructive boundary, or output shape; omit ceremonial examples that merely repeat the synopsis.

## Writing and editing standard

Write reference prose for a reader trying to act now. Lead with observable behaviour, defaults, consequences, and recovery. State constraints directly. Preserve a short rationale only when it prevents a likely misuse; decision history belongs in ADRs and implementation detail belongs in the Skill body or code.

Use uppercase conventional section headings to match rendered man-page scanning. Use sentence-case subsection headings, consistent with the Linux man-pages style. Use semantic emphasis only: literal commands and options, replaceable metavariables, and genuinely important warnings should be visually distinct; ordinary prose should not accumulate decorative bold phrases.

Keep complete commands and shell sessions in fenced blocks, with input and output distinguishable by content. Check the rendered page at a narrow terminal-like width because man-page output is designed for variable devices and groff warns against depending on one exact indentation or width.

Do not import the Linux project's semantic-newline rule into this repository. It applies to roff source and intentionally breaks sentences and clauses across physical lines, while this project's authoritative Markdown rule requires every prose paragraph on one physical line. Preserve the repository rule in every rewritten help page.

## Review checklist

- Does `NAME` have exactly the invocation and one useful summary line?
- Does each `SYNOPSIS` line describe one accepted form, using optionality, alternatives, and repetition unambiguously?
- Can a reader find normal and default behaviour in the first part of `DESCRIPTION`?
- Have option details, examples, caveats, environment, and files been moved to their conventional sections instead of accumulating in `DESCRIPTION` or `NOTES`?
- Does every argument and option state the behaviour it controls, along with non-obvious defaults, constraints, repeatability, and interactions?
- Are internal workflow, architecture, history, evidence, and repeated design rationale absent unless required for correct use?
- Are empty or irrelevant standard sections omitted, apart from any explicitly retained Collection-specific `DEPENDENCIES` rule?
- Are related Skills listed tersely and consistently under `SEE ALSO` without fictitious man-section numbers?
- Does the page remain readable when rendered narrowly, and does every prose paragraph remain one physical Markdown line?
- Does the documented grammar agree with `argument-hint`, the Skill's parsing instructions, and the behaviour that will actually run?
