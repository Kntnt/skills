`/redline` stopped before reviewing anything. It needs the `proofread` skill, and that skill isn't enabled. Nothing was reviewed or written. Here is what the check printed, unchanged:

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
