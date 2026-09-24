`/redline` stopped before reviewing anything because a dependency is missing. Here is the shim's output, verbatim (exit 2):

```
{
  "ok": false,
  "unsatisfied": [
    {
      "name": "proofread",
      "kind": "skill",
      "how": "check 'proofread' in /kntnt select"
    }
  ],
  "capabilities": [
    {
      "name": "subagents",
      "confirm": "you can spawn subagents that work in their own context window",
      "how": "run this skill in a harness that can spawn subagents"
    }
  ]
}
```

Nothing was reviewed or written, and `input.md` is unchanged. To fix it, select `proofread` in `/kntnt select`, then run `/redline --output=response input.md` again.
