# Orchestrate the transport; do not replace it

Users already install collections with `npx skills add`. Building our own installer would duplicate multi-harness paths, updates, and discovery, and would fork us from that ecosystem. The manager only fills the gaps the transport does not cover: a desired set in Global and in each Project, reporting new or removed Catalog entries, and applying the chosen layer to every Harness present. It does not install dependencies. Skill files still move through `npx skills`.

The premise that transport acquisition is also active publication is amended by ADR-0130, which keeps acquisition in the transport and gives verified publication to the Manager.
