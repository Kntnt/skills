# postmark

## NAME

postmark - inspect and change email at Postmark on your behalf

## SYNOPSIS

**/postmark** [**--** *INSTRUCTION*]

**/postmark** **setup** [**--yes**] **account** [**--** *INSTRUCTION*]

**/postmark** **setup** [**--yes**] **server** *NAME* [**--** *INSTRUCTION*]

**/postmark** **status** [**--** *INSTRUCTION*]

## DESCRIPTION

`postmark` reads and changes what your Postmark account holds: servers and their message streams, domains and their DKIM and Return-Path records, sender signatures, templates, suppressions, bounces, delivery statistics, message search and webhooks. It also sends an email where you ask for one. The request goes behind the reserved separator, or comes from the conversation; with neither, the Skill asks what you want done.

Every change is read first, planned as each object's current and intended state, applied, and read again to verify it. The report says what changed, what Postmark answered, and what remains.

Postmark cannot undo a deletion or a send, so the Skill deletes, sends, or asks Postmark to erase a recipient's data only where you have authorized that exact operation. A send is drafted in full and shown to you first. A test send uses Postmark's test token and delivers nothing.

A domain's DKIM and Return-Path records are reported as records to set, host, type and value, with `/cloudns` named as the Skill that sets them. `postmark` sets no DNS record itself.

The Skill uses two kinds of Postmark token, which `setup` stores and `status` checks. No token is ever shown in the conversation, typed into it, or printed.

## COMMANDS

**setup**

Store the account token or one server's token, read from the clipboard, and check it. See `/postmark setup --help`.

**status**

Check every stored token against Postmark and list the account's servers, marking those the Skill holds a token for. See `/postmark status --help`.

## POSITIONAL ARGUMENTS

**account**

Under `setup`, store the account token.

**server** *NAME*

Under `setup`, store the token of the server called *NAME*, exactly as Postmark shows it, spaces included.

## OPTIONS

**--yes**

Under `setup`, replace a token the Credential File already holds. Without it, `setup` refuses to overwrite a stored token.

## FILES

**~/.kntnt/postmark/credentials.json**

The Credential File, readable by its owner alone (`0600`), in a directory only its owner can enter. It is a flat JSON object with two kinds of key: `account-token`, holding the account token, which reaches servers, domains, sender signatures and data removals across the account; and `server:`*NAME*, one per server, holding that server's token, which reaches its sending, templates, message streams, bounces, statistics, suppressions, messages and webhooks. `KNTNT_HOME`, where set, replaces `~` in the path.

## DIAGNOSTICS

An invalid form is refused rather than ignored. The Skill names the error, prints the SYNOPSIS of the most specific page, changes nothing, and points at that page's `--help`. A flag is refused where it has no work to do, so `status --yes` is refused. A request written without the reserved separator is read as a command and refused as an unknown one: write `/postmark -- verify the domain`, not `/postmark verify the domain`.

Postmark cannot undo a deletion, a send, or a data removal, so the Skill's engine refuses each of them unless the Skill asserts that you authorized that exact operation: any `DELETE`; a `POST` to `email`, `email/batch`, `email/bulk`, `email/withTemplate` or `email/batchWithTemplates`; and a `POST` to `data-removals`. A test send is not refused, since it delivers nothing, and archiving a message stream is not either, since Postmark can unarchive it.

Where no Credential File exists, `status` and every request but a test send stop and name `setup`. Where a request needs the account token and none is stored, it stops and names `setup account`; where it needs a server's token that is not stored, it stops and names `setup server`. A Credential File others can read is refused, naming the mode it needs.

## EXAMPLES

Store the token of a server called transactional, copied from that server's API Tokens tab.

```
/postmark setup server transactional
```

Replace the stored account token after regenerating it in Postmark.

```
/postmark setup --yes account
```

Send a test that Postmark accepts and delivers nothing.

```
/postmark -- send a test of the welcome template to anna@example.com through transactional
```

Send a real email. The Skill drafts it in full and shows it; the engine sends it only once you have authorized that message.

```
/postmark -- send the invoice reminder to anna@example.com through transactional
```

Find why messages to one address bounce.

```
/postmark -- why do messages to anna@example.com bounce on transactional?
```

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*], the optional Contextual Instruction behind the reserved separator. The full contract is in the Manager's Collection Library at `library/references/invocation-envelope.md`.

## DEPENDENCIES

`uv` and the Kntnt Manager run the invocation engine and the Skill's own engine. No peer Skill or Harness Capability is required.

Remote operations need network access and a Postmark token: the account token for servers, domains and sender signatures, a server's token for everything that server does. Help, and `setup`'s writing of the Credential File, need neither. `setup` reads the clipboard through `pbpaste` on macOS, `wl-paste`, `xclip` or `xsel` on Linux, and PowerShell on Windows.

## SEE ALSO

**/postmark setup --help**, **/postmark status --help**, **/cloudns**, **/kntnt select**
