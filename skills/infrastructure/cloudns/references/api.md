# The ClouDNS API, as this Skill calls it

The reference for every call is ClouDNS's own [API help](https://www.cloudns.net/wiki/article/41/); open the method's own page there for anything this file does not state. This file carries only what composing the Skill's calls needs and the help does not put in one place, including two places where the help's own tables are wrong.

## The shape of a call

`call <group>/<method>.json <key>=<value>...` POSTs a form body to `https://api.cloudns.net/<group>/<method>.json`. The engine adds `sub-auth-user` and `auth-password` itself; never give a credential parameter as a pair.

Every method answers JSON. A failure is reported in band, as `{"status":"Failed","statusDescription":"..."}`, and a write that succeeded answers `"status":"Success"` with its own `statusDescription`. A listing answers its data directly rather than inside that envelope, so a listing that is an object with a `status` key has failed.

`dns/records.json` answers an object keyed by record ID, each record carrying its `id`, `type`, `host`, `record` and `ttl` among other fields. The record ID for `mod-record` and `delete-record` comes from there.

## Wire names the help's tables get wrong

The parameter tables on the add, modify and delete pages name the record type `type` and the record ID `id`. Every worked example and every error string on those same pages uses `record-type` and `record-id`, and those are the names that work — for instance `domain-name=domain.com&record-type=A&host=www&record=10.10.10.10&ttl=3600`, and `{"status":"Failed","statusDescription":"Invalid record-id param."}`. Keep `record-type` and `record-id`; do not correct them back to the tables.

`dns/records.json` is the exception: its optional filter by type is `type`, as its own example writes it.

## Listing zones: `dns/list-zones.json`

`page` and `rows-per-page` are both required, and `rows-per-page` must be one of `10`, `20`, `30`, `50` or `100`. Omitting either fails in band:

```
{"status":"Failed","statusDescription":"Missing required parameter 'page'."}
{"status":"Failed","statusDescription":"Wrong or missing required parameter 'rows-per-page'."}
```

The answer is an array of zones, each carrying its `name`. Start at `page=1` with `rows-per-page=100`; a full page may have another after it, and a shorter one is the last. `search=<name>` narrows the list to matching zones.

## Listing records: `dns/records.json`

`domain-name=<zone>` alone lists every record in the zone. `host=<host>` narrows it to one host, and `type=<type>` to one type.

## Adding a record: `dns/add-record.json`

Every record takes `domain-name`, `record-type`, `host` and `ttl`, the TTL being one of the values the help lists (`3600` among them). `host` is the name within the zone. The help's own examples write the apex as `@`; where the zone already has apex records, write `host` as the listing shows theirs. What else a type takes:

- `A`, `AAAA`, `CNAME`, `NS`, `ALIAS`: `record`, the address or target name.
- `TXT`: `record`, the text.
- `MX`: `record`, the mail server, and `priority`.
- `SRV`: `record`, the target, and `priority`, `weight` and `port`.
- `CAA`: `caa_flag` (`0` or `128`), `caa_type` (such as `issue`) and `caa_value`.

## Changing a record: `dns/mod-record.json`

It takes `domain-name`, `record-id`, `host`, `record` and `ttl`, plus the type-specific parameters above. It cannot change a record's type: to change a type, add the new record and delete the old one.

## Deleting

`dns/delete-record.json` takes `domain-name` and `record-id`. `dns/records-import.json` with `delete-existing-records=1` replaces every record in a zone. Both are refused by the engine without `--yes`.

## Sub-users and delegation

A sub-user is created in the panel under **API & Resellers → API Sub-Users → Add new sub-user** ([article 42](https://www.cloudns.net/wiki/article/42/)), or through the API ([article 115](https://www.cloudns.net/wiki/article/115/)); [article 114](https://www.cloudns.net/wiki/article/114/) is the overview. The **DNS zones** field on that form is a quota — how many zones the sub-user may create — and not a list of the zones it reaches.

A zone is delegated to a sub-user separately, in the panel from the zone's own management, or through `sub-users/delegate-zone.json` ([article 126](https://www.cloudns.net/wiki/article/126/)), which takes the main API user's `auth-id` and `auth-password`, the sub-user's `id` and a `zone`. This Skill holds only the sub-user's credential, so delegation is the user's step, and `status` is how the result is seen.
