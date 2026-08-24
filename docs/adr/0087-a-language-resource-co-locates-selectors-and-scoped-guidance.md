# A Language Resource co-locates selectors and scoped guidance

Write, Redline, and Proofread need the same language identity but different language-specific guidance. Splitting aliases and scopes across consumer-owned files would make every new locale a coordinated multi-file change, while loading one monolithic file would spend context on rules the active Skill cannot use.

**Each language or locale has one Language Resource.** Its frontmatter carries the canonical code, a bounded set of aliases, inheritance metadata, and the information needed to select it without loading its body. Its body carries separate composition, review, anti-slop, and mechanics scopes, each named for the guidance it holds rather than for the Skill that reads it, so that a scope more than one Skill consumes does not read as one Skill's property. A deterministic resolver inventories frontmatter and extracts only the scopes requested by the active Skill; semantic interpretation handles an unlisted human language description before the resolver verifies that the derived language is available.

**Generic editorial guidance stays outside Language Resources.** Shared rules and English examples remain language-independent and are applied semantically in the target language. A Language Resource gains a language-specific rule only when that language genuinely differs or observed behaviour demonstrates that the generic rule is insufficient.

This costs a maintained resource schema and resolver, but keeps locale administration in one place without loading every locale, alias, or inactive scope into the model's context.
