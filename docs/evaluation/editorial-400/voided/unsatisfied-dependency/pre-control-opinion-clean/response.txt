I stopped before reviewing anything: /redline's startup check failed with exit code 2 because a skill it needs isn't installed. Nothing was reviewed or corrected, and nothing was written. `input.md` is unchanged.

The check printed:

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

/redline ends every run with a proofreading pass, so it won't start until the Proofread skill is enabled. To enable it, select `proofread` in `/kntnt select`, then run `/redline --genre=opinion --language=sv --output=response input.md` again.
