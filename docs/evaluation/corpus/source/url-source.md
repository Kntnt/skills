# Immutable URL source

The source material for this fixture is not held in the corpus. It is fetched from a URL that cannot change under a run:

<https://www.rfc-editor.org/rfc/rfc2119.txt>

RFC 2119 is a published RFC. The series does not revise a published document — a change is a new number, not a new revision of an old one — so two evaluations weeks apart read the same bytes, and a difference between their records is a difference the models made.

## The brief that goes with it

Write a short explainer for developers who have just met the words MUST, SHOULD, and MAY in a specification and want to know what they commit to. Audience: working programmers, no standards background. Length: about 350 words. Use the source at the URL above and nothing else.

## Why this fixture is here

It is the only fixture whose material arrives over the network, so it is the one that exercises reading a URL as source material, deriving an output filename from a URL rather than from a source basename, and the refusal of In-place Editing against a source that is not a local writable file.
