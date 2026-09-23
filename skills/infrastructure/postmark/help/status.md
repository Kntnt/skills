# postmark status

## NAME

postmark status - check every stored Postmark token and list the account's servers

## SYNOPSIS

**/postmark status** [**--** *INSTRUCTION*]

## DESCRIPTION

`status` checks each token the Credential File holds against Postmark and prints no token. It changes nothing.

With the account token, it lists the account's servers and marks each the Skill holds a token for. With each server token, it says whether Postmark accepted it. Where no account token is stored, the server tokens are still checked and the account line says what `setup account` would add.

## FILES

**~/.kntnt/postmark/credentials.json**

The Credential File whose tokens are checked.

## DIAGNOSTICS

An invalid form is refused rather than ignored. The Skill names the error, prints this page's SYNOPSIS, changes nothing, and points at `/postmark status --help`. `status` takes no flag and no operand, so `status --yes` is refused.

Where no Credential File exists, or it holds no token, `status` says so and names `setup`. A file others can read is refused, naming the mode it needs. A token Postmark refuses is reported as refused, with Postmark's message; where Postmark cannot be reached, `status` says so.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*], the optional Contextual Instruction behind the reserved separator. The full contract is in the Manager's Collection Library at `library/references/invocation-envelope.md`.

## DEPENDENCIES

`uv`, the Kntnt Manager, and network access.

## SEE ALSO

**/postmark --help**, **/postmark setup --help**
