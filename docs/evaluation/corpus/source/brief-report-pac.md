Write an internal report on whether we should keep paying for our second monitoring service.

Audience: our own engineering leadership, four people, who approve the budget. Length: about 900 words.

What we know. We pay for two monitoring services. The first costs 840 euro a month and is wired into every service we run. The second costs 310 euro a month and covers eleven of our forty-two services, all of them added before June last year; nothing has been added to it since. In the last twelve months, the second service raised the first alert for two incidents. In both cases the first service raised its own alert within four minutes. Nobody has opened the second service's dashboard since 2 November, according to its own access log.

The counter-argument, made by our on-call lead, is that the two services fail independently, and that a monitoring outage during an incident is the case the second one exists for. We have never had a monitoring outage.

Cancelling is a twelve-month commitment either way; the current term ends on 30 June.
