`/redline` stopped before reviewing anything. Its launcher reported a missing dependency, so nothing was reviewed, corrected or written. Here is its output, unchanged:

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

Redline needs the Proofread skill enabled to run. Select `proofread` in `/kntnt select`, then run `/redline --genre=web-copy --language=sv --output=response input.md` again.
