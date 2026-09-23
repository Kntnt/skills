# NodePing API

What is needed to compose a `call` that NodePing's documentation spreads across several pages. For every other field, parameter or response shape, read the official documentation: the overview at https://nodeping.com/API_Documentation.html, the resource-and-action index at https://nodeping.com/API_Reference, and the per-resource pages `https://nodeping.com/docs-api-<resource>.html`, such as `docs-api-checks.html`, `docs-api-contacts.html` and `docs-api-results.html`.

Every fact below was checked against those pages on 2026-09-23.

## Addressing

The base is `https://api.nodeping.com/api/1/`, and a call is addressed as `/api/:version/:resource/:id?querystring`. The engine supplies the base, so a `call` names only `<resource>[/<id>][?<querystring>]`.

## Resources and their actions

This is the full list the reference gives.

| Resource | Actions |
|---|---|
| `accounts` | GET, PUT, POST, DELETE |
| `contacts` | GET, POST & PUT, DELETE, RESETPASSWORD |
| `contactgroups` | GET, POST & PUT, DELETE |
| `schedules` | GET, PUT, DELETE — PUT both creates and updates |
| `checks` | GET, POST & PUT, DELETE, Disable |
| `results` | GET, UPTIME, CURRENT |
| `notifications` | GET |
| `info` | GET |

POST creates and PUT updates, schedules excepted. An action without a method of its own is sent as an `action` parameter, such as `contacts/<id>?action=RESETPASSWORD`; `action=delete` does what `DELETE` does, and the engine gates both.

Subaccounts are `accounts` objects. A call about a subaccount's objects carries `customerid=<subaccount id>`.

## Sending parameters

The reference says: *"You can put them in the querystring … or you can send them in a JSON object named json … The two syntaxes are interchangeable."* Where both carry a parameter, the JSON wins. The engine sends a `POST` or `PUT` operand as that form field, as the documented `curl -X PUT -d'json={...}'` does, so a `call` passes the parameters as one JSON object:

```
call PUT checks/<id> '{"label": "kntnt.se", "interval": 5}'
```

A `GET` or `DELETE` carries its parameters in the path's query string.

## Checks

`checks` lists every check; `checks/<id>` is one. `GET` also takes `lastresult`, `current` and `uptime` as parameters, which add the last result, current events and uptime to what it returns.

Write fields, on `POST checks` and `PUT checks/<id>`:

- `type` — required. One of AGENT, AUDIO, CLUSTER, DOHDOT, DNS, FTP, HTTP, HTTPCONTENT, HTTPPARSE, HTTPADV, IMAP4, MONGODB, MTR, MYSQL, NTP, PGSQL, PING, POP3, PORT, PUSH, RBL, RDAP, RDP, REDIS, SIP, SMTP, SNMP, SPEC10DNS, SPEC10RDDS, SSH, SSL, WEBSOCKET, WHOIS. The fields each type takes beyond those below are on `docs-api-checks.html`.
- `target` — required on create, except for AGENT, DNS, PUSH, SPEC10DNS and SPEC10RDDS: the URL or host name checked.
- `label` — the name shown for the check.
- `interval` — minutes between runs, 15 by default; `0.5` and `0.25` for sub-minute.
- `enabled` — `'true'`, `'false'` or `'active'`; `'false'` by default. Setting `'false'` disables the check, which can be enabled again.
- `public` — whether public reports are on.
- `autodiag` — whether automated diagnostics run.
- `runlocations` — the regions or probes the check runs from.
- `homeloc` — the preferred probe location.
- `threshold` — the timeout in seconds, 5 by default.
- `sens` — how many rechecks confirm a change of state, 2 by default.
- `notifications` — an array of one-key objects, contact or group id to delay and schedule: `[{"<contact id>": {"delay": 0, "schedule": "All"}}]`.

`checks` with `disableall` set to `'true'` disables every check on the account, and `'false'` re-enables the ones it disabled.

**A check is not read back in the shape it is written.** It is written with `enabled` and read back as `"enable": "active"`, and the type-specific fields — `target`, `threshold` and `sens` among them — come back nested under `parameters`. So `GET checks/<id>` answers `{"label": "Site 1", "enable": "active", "parameters": {"target": "http://www.example.com/", "threshold": "5", "sens": "2"}, ...}`, and matching a check by its target reads `parameters.target`. Its `state` is 1 while it passes and 0 while it fails.

## Contacts, contact groups and schedules

- `contacts` takes `name`, `custrole` (`edit`, `view` or `notify`), `newaddresses` to add addresses — `[{"address": "...", "type": "email"}]` — and `addresses` to change existing ones, keyed by address id. `addresses` replaces the whole set, so an address left out of it is removed.
- `contactgroups` takes `name` and `members`, an array of address ids.
- `schedules/<name>` is created and updated alike with `PUT`, its days under `data`: `{"data": {"monday": {"time1": "6:00", "time2": "18:00", "exclude": 0}, ...}}`, each day also taking `disabled` and `allday`.

## Results, uptime and notifications

- `results/<check id>` returns the check's results, taking `limit` (300 by default, 43201 at most), `span` in hours, and `start` and `end` as milliseconds, RFC 2822 or ISO 8601.
- **Uptime is the `results` resource under the UPTIME action**, not a resource of its own: `results/uptime/<check id>`, taking `interval` (`days`, or `months` by default), `start`, `end` (excluded from the range) and `offset` in hours from UTC. It answers per period and in total with milliseconds `enabled`, milliseconds `down`, and the `uptime` percentage.
- `results/current` lists the events in progress across the account's checks.
- `notifications` lists notifications sent, `notifications/<check id>` those for one check, taking `span` in hours, `limit` and `subaccounts`.

## Errors

The body of an error is `{"error": "..."}`, and the engine relays it with the status on its stderr.

- 403 — the token is wrong, or lacks permission for the action.
- 400 — the URL or a parameter is wrong.
- 500 or 501 — a bug at NodePing.
