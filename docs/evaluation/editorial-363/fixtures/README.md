# Contrast fixtures for #363

Three synthetic Text Artifacts, frozen on 2026-09-21 before any run of either arm and before any product change. Every person, organisation, figure, date and URL in them is invented. They are evaluation material and never runtime guidance.

Each is replayed whole as `input.md` under `/redline --output=response input.md`. Each carries a `kntnt` map, so genre, technique and language are settled by the artifact rather than by a flag.

They exist because the frozen inputs this ticket inherits all turn on one sentence — *I would set that time aside before the next building starts* — in one account of one repair log. A change measured only against that sentence would be a change that learned that sentence. These fixtures move the referent, the construction, the language, the genre and the rhythm, and two of them are positives: what they ask of a review is that it leave a working quotation alone.

None of them states a replacement wording, and none rewards writing out an implied noun as such. A run that expands a working figure into its literal paraphrase fails the two positives; a run that reports the third fixture's obstacle without inventing what the text does not carry passes it.

## `metonymy-sv.md` — a positive, Swedish, referent not a building

A Swedish customer account of a substitute-teacher list at a school. The quotation is *Vi ville ha rutinen på plats innan terminen drog i gång. Det hann vi inte riktigt, men expeditionen märkte skillnaden redan första veckan.*

It stands beside the inherited Swedish case on purpose: the same construction, `innan <X> drog i gång`, and an institution standing for the people in it. Both are ordinary Swedish. A term does get going in Swedish, and a school office does notice things.

**Criterion `C-metonymy`.** The quotation comes back with its wording unchanged, or the run reports a finding that names a concrete obstacle to reading it — something a Swedish reader stumbles over in this text, quoted from this text. Judged from the delivered artifact and the run's own reported findings alone. A change no reported finding names is a fail. An expansion of *terminen drog i gång* or of *expeditionen* into a literal paraphrase is a fail whatever the run says about it.

## `rhythm-en_GB.md` — a positive, British English, a different rhythm

A British local-government article about four late bus services. Short declarative sentences, a counted report, and a register that is not the customer account's. The quotation is *We wanted the rotas settled before the winter. They were, just about. After that the depot stopped ringing round at six in the morning.*

It carries two figures English takes in its stride: a time adverbial with the event left out, and a building standing for the people who work in it.

**Criterion `C-rhythm`.** As `C-metonymy`, in English: the quotation comes back with its wording unchanged, or a reported finding names a concrete obstacle to reading it in English, visible in the text alone. Supplying the missing event after *before the winter*, or naming the staff behind *the depot*, is a fail unless a reported finding first names what a British reader loses without it.

## `ellipsis-sv.md` — a negative, Swedish, a different construction

A Swedish customer account of a stock-balance migration at a haulage firm. The quotation is *Vi körde parallellt i sex veckor. Sedan gick lagret över, och först då såg vi hur mycket som hade legat i pärmar.*

`gick lagret över` is where the reader stops. Swedish `gå över` wants a goal, and with none the sentence reads as something passing rather than something moving. The surrounding text says what the warehouse moved to, so the obstacle is repairable from this text; it is a different construction, a different referent and a different domain from the inherited case, and it is not a word the product could learn.

**Criterion `C-ellipsis`.** The run either repairs the quotation using only what this text carries — inventing no event and adding no fact — or reports the obstacle with the delivered artifact and leaves it standing. Silence is a fail: an artifact returned with `gick lagret över` unchanged and no reported finding against it is a miss. Judged by two independent judges where a repair was made.
