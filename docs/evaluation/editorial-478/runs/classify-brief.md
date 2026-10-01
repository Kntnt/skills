# Reading the judges' A2 misses into classes

Each directory you are given holds one run of a reviewing Skill (Redline) and its two blind judgements:

- `kind.txt` — whether the run is a `control` (the reply is the response target) or a `file-target control` (the text was delivered to `output.md`), and the fixture it ran on.
- `input.md` — the text the Skill received.
- `response.md` — the Skill's reply. Where the Skill delivered the text in its reply, the returned text is inside it.
- `output.md` — only for a file-target control: the text the Skill delivered.
- `expectation.md` — only for a control: the frozen expectation the judges were given.
- `judgement-a.md`, `judgement-b.md` — the two judges' judgements.

You are not told which version of the Skill ran, and you must not try to find out. Read nothing outside the directories you are given and this file.

## What an `A2` miss is

**A judge records an `A2` miss** where its judgement, under any heading, calls a statement of the reply false, inaccurate, imprecise, loose or misleading against a text, or records under heading 2 a difference that the reply does not report or reports inaccurately.

**Every such miss is read**, and each is put in exactly one of four classes:

1. **A claim-account miss.** The miss is about what the run did to a claim: an entry of the itemised account of removed, changed or added claims; a claim-changing difference that the account leaves out or misreports; or the sentence about the claims as a whole. A difference that moves a claim and that no statement of the reply reports is class 1, because the claim account leaves it out, a sense or double sense lost among them.
2. **A counted miss outside the claim account.** A statement of the reply about a text, not in class 1, that asserts something the text it names contradicts. Statements about the text as received are read against `input.md`, and all others against the returned text. The judge's word does not decide the class; what decides it is whether the text contradicts what the statement says. *The six unhelpful headings are gone* counts, although its judge called it loose, because one of the six was replaced rather than removed. A finding's description, an anatomy remark, a count, a length, a grammatical label, where a passage stands, and what a round did to a passage — *moved*, *removed*, *replaced*, *given a heading* — are all in scope.
3. **Recorded, not counted.** The statement is true of the text it names, and the judge faults only what it might suggest, or disputes only whether the change was the repair of a real defect (a judgement of taste presented as a defect, while the description of what changed is accurate). The *med mellanrum* / *med mellanslag* note on a dash that comes back spaced is in this class.
4. **An omission.** A difference that moves no claim and that no statement of the reply reports.

One judge is enough to put a miss in a run. Where both judges fault the same statement, record it once per judge.

**Check every class 2 candidate against the texts yourself.** Open `input.md` and the returned text and see whether the passage the statement names contradicts it. A count or length: count it. Where the text does not contradict the statement, it is class 3, however the judge worded it. Where a judge calls a claim-account entry short (it does not say all a change did to the claim), that is class 1, not class 3, whenever the judge is right that the change moved the claim's scope, certainty, attribution, chronology, causality or meaning.

A judge's R1 criticism of the change itself (the Skill should not have changed the text) is not an `A2` miss unless the judge also says the reply misreports it.

## Owners

Two open tickets own behaviours these runs can show. Name one as `owner` where the miss is that behaviour:

- **#477**: a finding's description says the case study's note explicitly rules out the software as the cause of the difference, where the note only declines to credit the software.
- **#476**: a correction round's working files left behind.

The owner does not change the class; classes 1 and 2 are recorded whatever their owner.

## What you write

In each directory, write `classes.json`:

```json
{
  "misses": [
    {"judge": "a", "class": 1, "attribution": true, "kind": "changed", "owner": null,
     "reply": "the reply's words, quoted",
     "judge_says": "the judge's words, quoted or closely paraphrased",
     "check": "what you found in the text"}
  ],
  "verdicts": {"a": "pass", "b": "fail"},
  "notes": ""
}
```

- `attribution` for class 1: `true` where the claim change the miss is about moved an attribution — the delivered text gives a person or a source content that the text as it arrived gave to another voice, the narrator's own among them, or to nobody — and `false` otherwise. Omit it for classes 2, 3 and 4.
- `kind` for class 1: `whole` (the sentence about the claims as a whole), `removed`, `changed` or `added`. For class 2: `count`, `length`, `label`, `placement`, `round` (what a round did to a passage) or `finding` (a finding's description of the text as received), or `other`. For classes 3 and 4: `""`.
- `verdicts` is each judge's heading-4 verdict, `pass` or `fail`.
- An empty `misses` list where neither judge records any.

Then reply with one line per directory: its name, the number of misses in each class, and the verdicts.
