# Strip an AGENTS.md line only when a Project skill is the source

Never remove a line from `AGENTS.md` because a Skill is Enabled only in Global. Global does not travel with the repo. Remove a line only when all of these hold: the Skill is Enabled in Project, its files are tracked in git, the line and the Skill have the same meaning, and the Skill starts in the situation the line would have covered. Otherwise keep the line, or ask.
