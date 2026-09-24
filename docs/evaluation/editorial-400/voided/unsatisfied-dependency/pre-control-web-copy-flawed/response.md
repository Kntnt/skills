I couldn't run `/redline`. Its invocation check exited with status 2 because the Proofread skill it needs isn't installed where it can be found, so nothing was reviewed or written. This is what the check printed:

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

To fix it, enable `proofread` with `/kntnt select`, then run `/redline --genre=web-copy --language=en_US --output=response input.md` again.
