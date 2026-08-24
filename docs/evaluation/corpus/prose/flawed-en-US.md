# Why we rewrote the importer instead of patching it

The importer was writen in 2019 by a contractor who left the same month, and for four years nobody touched it except to add a field. It's job was simple enough: read a supplier's CSV, normalize the column names, and write a row per product into into our catalog. In practice it did five other things nobody had documented, and each of them was load-bearing.

The decision to rewrite it wasnt taken lightly. A patch would of been cheaper in the first week. But every patch we tried failed the same way — the file arrived, the parser accepted it, and three days later the finance team asked why a product had two prices. The bug were not in the parsing at all, it was in a silent retry that ran when the supplier's server timed out, and that retry had no logging whatsoever.

We spent two weeks writting a replacement and one week running both versions side by side on the same input. Their outputs differed on eleven of the four thousand rows. Eight of those differences was the new importer being right. The other three we still dont understand, and we shipped anyway, which I would defend but not recommend.

The lesson isnt "rewrite things". Its that a component nobody can explain has a cost that doesnt show up on any ticket, and you pay it in the finance team's time rather than your own — which is exactly why it stayed unpaid for four year.
