Slutlig verifiering på `29ff2047ad2dac330dd705feccdb3f2d0778831b`, fryst corpus `6e531f5`, oförändrade prompts och ärvd gpt-6-astra/high:

- Write case-study-sv återger fortfarande ”innan nästa byggnad börjar”. L1 fail kvarstår även när den nya substansbaserade citatregeln och Writes kontroll av sakpåståenden har laddats.
- Den separata, källblinda Redline-invokationen identifierar nu referentproblemet. En färsk korrigeringsagent ändrar enbart till ”innan försöket börjar i nästa byggnad”. Kontexten etablerar försöket; ingen ny uppgift, hållning eller säkerhet läggs till. Alla andra påståenden, kvalifikationer, citat och metadata står kvar; endast terminal radbrytning skiljer därutöver.
- Parent gör re-review och följer installerad Proofread exakt en gång med enbart språk-/outputflaggor, läser shared/sv Mechanics och gör ingen senare sakändring. Fulla inventeringar visar inga bestående Skill-filer; båda rötterna är städade efter bevarad evidens.

Redline passerar samtliga tillämpliga kriterier i detta stickprov. Write-fail och de tidigare källblinda missarna står kvar: detta är observerad reparation i kedjan, inte verifierat förebyggande i Write eller garanti att Redline alltid reparerar.

Brittiska slutparet på samma revision passerar Write och Redline med originalcitat bevarade och korrekt septemberbeslut. Amerikanska kontrollparet körs separat.

Full evidens: `docs/evaluation/editorial-329/runs/rerun-341-translation/`. Bedömningar: separata `write-` och `redline-gpt-2026-09-19-341-translation-part-article-case.md` i records.
