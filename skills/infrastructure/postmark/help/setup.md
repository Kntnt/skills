# postmark setup

## NAME

postmark setup - store a Postmark token read from the clipboard, and check it

## SYNOPSIS

**/postmark setup** [**--yes**] **account** [**--** *INSTRUCTION*]

**/postmark setup** [**--yes**] **server** *NAME* [**--** *INSTRUCTION*]

## DESCRIPTION

`setup` stores one Postmark token in the Credential File without the token passing through the conversation. The Skill asks you to copy the token in Postmark and to say when it is on the clipboard; it then reads the clipboard into the file and runs `status` to check the token against Postmark.

`setup account` stores the account token, found on the API Tokens tab of the Postmark account and shown to the account owner and admins. `setup server` stores the token of one server, found on the API Tokens tab of that server.

To rotate a token, regenerate it in Postmark, copy the new one, and run `setup` again with `--yes`. You may clear the clipboard afterwards.

## POSITIONAL ARGUMENTS

**account**

Store the account token, under the key `account-token`.

**server** *NAME*

Store the token of the server called *NAME*, exactly as Postmark shows it, spaces included, under the key `server:`*NAME*.

## OPTIONS

**--yes**

Replace a token the Credential File already holds under the same key. Without it, `setup` refuses rather than overwrite a working token.

## FILES

**~/.kntnt/postmark/credentials.json**

The Credential File. `setup` creates it, readable by its owner alone, and adds or replaces one key, leaving the others as they were.

## DIAGNOSTICS

An invalid form is refused rather than ignored. The Skill names the error, prints this page's SYNOPSIS, changes nothing, and points at `/postmark setup --help`. `setup` alone, `setup server` without a name, and `setup account` followed by anything are refused.

Where the Credential File already holds the key and `--yes` is absent, `setup` refuses, names the file and the key, and says that `--yes` asserts you mean to replace the working token; the clipboard is not read and nothing is written. Where the clipboard is empty or no clipboard tool is found, `setup` refuses and says how to write the file by hand instead.

## EXAMPLES

Store the account token.

```
/postmark setup account
```

Store the token of a server whose name holds a space.

```
/postmark setup server My Broadcasts
```

Replace a server token after regenerating it in Postmark.

```
/postmark setup --yes server transactional
```

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*], the optional Contextual Instruction behind the reserved separator. The full contract is in the Manager's Collection Library at `library/references/invocation-envelope.md`.

## DEPENDENCIES

`uv` and the Kntnt Manager. Reading the clipboard needs `pbpaste` on macOS, `wl-paste`, `xclip` or `xsel` on Linux, or PowerShell on Windows. Checking the token afterwards needs network access; storing it does not.

## SEE ALSO

**/postmark --help**, **/postmark status --help**
