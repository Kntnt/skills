# The second server

The archive service had run on a single machine since 2016, and for most of that time nobody thought about it. It served about nine requests a minute, the disk was replaced once, and the only person who had ever logged into it was the person who built it.

But in March the university's reading-list tool began linking directly to archive records, and the nine requests a minute became four hundred. The machine did not fall over. It got slower, in the particular way that a machine gets slower when the disk is doing more seeking than reading, and the median response time went from 90 milliseconds to just over two seconds. Nobody noticed for eleven days, because nobody was monitoring a service that had never needed it.

Therefore we did the obvious thing, which was to put a second machine behind the same address, and the obvious thing worked: median response time came back to 140 milliseconds within an hour of the second machine taking traffic. It also cost us four days of arguing about whether the archive should have been a static site all along, an argument nobody won and which we have written down so that the next person inherits the argument rather than repeating it.
