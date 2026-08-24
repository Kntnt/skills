# Editorial Skills compose without requiring Write provenance

Write can attach Handoff Metadata that makes a later Redline invocation more precise, but requiring that metadata or the original source would make Redline and Proofread usable only as stages of one pipeline. The three editorial Skills must also accept independently supplied Text Artifacts.

**Write, Redline, and Proofread have independent input contracts and compose through public Skill interfaces.** Handoff Metadata is optional: formal values override it, and context or the Text Artifact supplies missing values. Redline depends on the public Proofread Skill and invokes it once after editorial correction, but reads none of Proofread's private implementation. Write invokes neither peer.

**Source Fidelity belongs to Write.** Write must represent its supplied material truthfully. Redline reviews the Text Artifact against its editorial contract without comparing it with source material or reporting that source verification was unavailable, and Proofread changes only mechanical language errors. This boundary keeps both reviewing Skills useful when no Write invocation or source material exists.

The cost is that Redline cannot catch a source-faithfulness failure made by Write or a human author. In return, each Skill remains independently usable, Handoff Metadata stays an optimisation rather than provenance, and peer composition follows the Collection's Dependency boundary.
