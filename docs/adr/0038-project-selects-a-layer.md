# `--project` selects a layer, and the Project form shows that layer alone

Every verb reads `--project` the same way: absent or `--project=off` is Global, `--project` or `--project=on` is the Project. Select and Update change the layer they are pointed at, and Uninstall has no Project form at all (ADR-0040).

This record used to be about Status, which changed nothing and so read the flag as a question rather than as a target — and its answer was that the flag form reported the **Effective** set, everything Enabled in Global plus everything Enabled in this Project. That reasoning does not survive the verb that replaced it. Select is where the user acts as well as where they read (ADR-0043), so every row of its list is something they can change, and a row of a union is not: unchecking one sourced from Global would do nothing, there being no Project copy to remove and no subtractive overlay to make one (ADR-0013). A list whose checkboxes mean one thing in some rows and another in the rest teaches the user to distrust all of them.

**So `select --project` shows the Project layer alone**, and answers *what has this repository got, and what am I about to change* — which is the question a verb that writes should be asking. What the Effective view was for survives at row level rather than as a set: a skill already Enabled in Global is marked as such, so nobody Enables a second copy into the repository by accident. That mark is the whole of what the union was needed for at the moment of choosing.

The Global form is unchanged in substance: every Catalog skill with its state on this machine, Disabled ones included, because the Catalog still carries them and finding what there is to Enable is what a list is for.

One payload serves both forms, and names the layer it covers. Two payloads would have made every reader — the skill body first among them — branch before it could read a row, and a user must never have to guess which layer the list in front of them will be written to.
