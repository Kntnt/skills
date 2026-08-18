# Bare `/kntnt` is Help

`/kntnt` with no arguments prints Help. Someone who types the manager's name with nothing after it does not yet know what to type next, and Help is the answer to that.

The decision stands, and it is now trivially true: the alternative it argued against was binding the bare word to Status, and Status no longer exists (ADR-0043). There is nothing left for the bare form to mean. What remains of this record is the reason the collection never grew that alternative, and the reason was never about Status in particular. A report of what is on the machine answers a question the beginner has not asked; a bare name should teach the interface, so it prints the interface. Select is one word away and Help names it in the first line of output, which is what made losing the second route to a list cost nothing.

The earlier binding also made one subcommand reachable two ways — an asymmetry with nothing behind it. Every subcommand is reached by its own name, and none by the absence of one.
