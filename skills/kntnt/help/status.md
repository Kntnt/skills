# kntnt status

Report which skills of this collection are Enabled.

## Synopsis

`/kntnt status [skill...] [--project[=on|off]]`

## Description

Bare, reports the Global layer: every Catalog skill with its state on this machine, Disabled ones included. With `--project`, reports what applies in the working directory instead — everything Enabled in Global plus everything Enabled in this Project — and says of each skill whether it comes from Global, the Project, or both. A skill Enabled in neither layer is left out of that form, because it does not apply here.

Status reads. It changes nothing in either layer.

## Arguments

- `skill...` — narrow either form to the named skills. No names reports everything the form covers.

## Options

- `--project`, `--project=on` — report what applies in this working directory instead of the Global layer. `--project=off` is the bare form.

## Notes

Each skill in the report carries a `state`: `enabled`, `disabled`, or `partial`. Partial is a fact about the disk rather than a third thing anyone chooses — the skill's files are in some of the directories the layer covers and missing from others — and a `/kntnt enable` of that skill repairs it.

The list is read from the collection itself. Where the collection cannot be reached, the report says so and comes from the copy stored beside the manager, which may be missing skills published since.

## See also

`/kntnt help enable`, `/kntnt help disable`, `/kntnt help update`.
