# Native evaluation workspace

Execute the staged Skill named in the invocation. For a nested Skill use the sibling staged copy. Write only inside this workspace and the private scratch named by TMPDIR. Do not access other projects or user installations. Preserve supplied input and staged Skill files.

Every private temporary directory, including each UV command's fresh directory, must be created below the initial TMPDIR. Preserve that base as a task-specific variable before assigning a command's TMPDIR. Use mktemp -d with a full template below that base. The sandbox permits network access and writes only under this run's private root. Pass this containment instruction to fresh child agents.
