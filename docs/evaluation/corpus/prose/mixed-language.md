# Retrospektiv, sprint 41

Vi hann inte med migreringen den här sprinten heller. The main blocker was the read replica — it kept falling behind under the backfill, and vi vågade inte köra vidare utan att veta varför.

Two things came out of the discussion. Det första är att vi behöver en mätpunkt på replikeringsfördröjningen innan vi startar en backfill, inte efter. The second is that we should have asked the DBA on Monday instead of Thursday; hon hade svaret på tio minuter.

Action points: Malin sätter upp mätningen. Erik bokar in DBA:n i planeringen. Vi tar migreringen igen i sprint 42, and we do not start the backfill on a Friday.
