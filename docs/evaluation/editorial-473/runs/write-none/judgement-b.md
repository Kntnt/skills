# Judgement

## 1. The parts

The frontmatter block (`kntnt: genre: pressrelease ...`) is metadata ahead of the release and is not counted as a part.

1. Publication time: "Får publiceras från den 27 maj 2027 klockan 08.00."
2. Headline: "# Tallmora Energi inviger solpark med 12 000 paneler vid Kvarnbacken"
3. Summary: "Tallmora Energi AB håller den 3 juni 2027 invigning av solparken i Tallmora, ..."
4. Body, first paragraph: "Bolaget beräknar att parken ger 7,5 gigawattimmar el om året. ..."
5. Body, second paragraph: "Elen levereras till elnätet. ..."
6. Background: "Grustäkten vid Kvarnbacken avvecklades 2019. ..."
7. Links and attachments: "Bilder från solparken: https://example.se/press/kvarnbacken-bilder ..."
8. Contact: "Lina Sjögren, kommunikationschef, Tallmora Energi ..."
9. Description of the organisation: "Tallmora Energi AB ägs av Tallmora kommun ..."

## 2. P1, the order

**Pass.** The parts stand in the order the standard gives. The material carries no quotation, so neither quotation slot is missing. Every part the material supplies is present: publication time, background, links, contact and description. The publication time "Får publiceras från den 27 maj 2027 klockan 08.00." stands on its own line above the headline. The deciding passage is the run from the summary to the body ("Bolaget beräknar ..."), then the background ("Grustäkten vid Kvarnbacken avvecklades 2019."), links, contact and "Tallmora Energi AB ägs av Tallmora kommun ...", last.

## 3. Q1, quotations only from the material

**Pass.** The material carries no quotation, and `delivered.md` carries none. The reply says so: "**Citat:** underlaget innehåller inga. Därför saknas både citatet efter ingressen och citatet efter brödtexten. Luckan har inte fyllts med påhittade citat."

## 4. Q2, where the quotations stand

**Not applicable.** The draft carries no quotation.

## 5. Q3, the second quotation

**Not applicable.** The draft carries fewer than two quotations.

## 6. B1, the body

**Pass.** The body is two short paragraphs. They complement the summary with the production estimate, its caveat, and the grid delivery and access limits. A journalist could lift both as they stand: "Bolaget beräknar att parken ger 7,5 gigawattimmar el om året. Enligt bolagets egen beräkning motsvarar det hushållselen i omkring 1 500 villor. Siffran är en uppskattning, ..." and "Elen levereras till elnätet. Parken säljer ingen el direkt till hushållen i närheten. Området är inhägnat och inte öppet för allmänheten utom under invigningen."

## 7. K1, the contact

**Pass.** The contact gives the name (Lina Sjögren), the title (kommunikationschef), the telephone number (070-000 00 00) and the email address (lina.sjogren@example.se). All four are in the material. The only addition is the organisation name "Tallmora Energi", and the material gives that in the same contact line.

## 8. F1, support

**Pass.** The material carries every claim in the draft:

- the date, 3 June 2027
- the site of the former gravel pit, up to 2019
- 12,000 panels on 18 hectares, and 64 million kronor
- the showing for visitors from 14.00 to 16.00
- 7.5 GWh, and about 1,500 villas, both attributed to "bolagets egen beräkning"
- delivery to the grid, and no direct sales
- the fenced area
- the permit in 2025 and the start of construction in August 2026
- 40 inverters, east–west rows, and sheep grazing
- 14,000 customers

The draft keeps the material's caveat: "Siffran är en uppskattning, och den verkliga produktionen beror på hur soligt året blir." It also keeps the scope limit on access: "inte öppet för allmänheten utom under invigningen". The summary's "solparken i Tallmora" leaves out "vid Kvarnbacken", but the headline names Kvarnbacken and the draft states nothing false. A side note outside `delivered.md`: the reply says "underlaget anger inget utgivningsdatum". That is a remark about the dateline, and the draft is not affected by it.
