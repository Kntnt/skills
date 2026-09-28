I’ll use the redline skill to check the draft against the brief and handle the requested output.


I can run subagents in separate contexts. The output path points to the selected brief, so I’m checking the skill’s destination rule before proceeding.


`--output=brief.md` would overwrite the selected brief. The [redline skill](/private/tmp/claude-501/-Users-thomas-Projects-skills/e8b2bc18-7919-41a5-8ca9-09238d1d9734/scratchpad/t445/protected-brief/work/.agents/skills/redline/SKILL.md) requires: “refuse any destination that would replace its file.” No review was performed; both files remain unchanged.

Use a different output:
```text
/redline --brief=brief.md --output=reviewed.md draft.md
```

**/redline** [**--genre**=*GENRE*] [**--technique**=*TECHNIQUE*] [**--language**=*LANGUAGE*] [**--brief=**_PATH|URL_] [**--max**=*N*] [**--output**=*TARGET*] [*TEXT*|*PATH*|*URL*] [**--** *INSTRUCTION*]

**/redline** [**--genre**=*GENRE*] [**--technique**=*TECHNIQUE*] [**--language**=*LANGUAGE*] [**--brief=**_PATH|URL_] [**--max**=*N*] **--in-place**[=**on**|**off**] *PATH* [**--** *INSTRUCTION*]

Help: `/redline --help`.
