# Effective is the union of Global and Project

`--project` mutates only the Project layer. Global stays untouched. In a Project, a Harness loads the union: every skill Enabled in Global plus every skill Enabled in that Project. `disable --project` can only remove a skill that was Enabled in the Project layer. A Project cannot hide a Global skill. The alternative — a mask that turns Global skills off in one directory — would make Effective depend on order and would surprise anyone who Enabled a skill once on the machine.
