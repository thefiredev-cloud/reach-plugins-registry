# reach-plugins-registry

A marketplace index (`plugins.json`) for the [Reach](https://github.com/alexandrosnt/Reach) SSH client. The index is currently empty.

## What it is

Reach's marketplace panel reads a registry URL that serves a JSON list of plugins. This repository held that list for the [thefiredev-cloud/Reach](https://github.com/thefiredev-cloud/Reach) fork. The three seed listings were removed on 2026-08-03, so `plugins.json` is now `[]`.

## Usage

There is nothing to install or run. To read the index:

```bash
curl -s https://raw.githubusercontent.com/thefiredev-cloud/reach-plugins-registry/main/plugins.json
```

Plugin source and manual install steps live in [reach-plugins](https://github.com/thefiredev-cloud/reach-plugins).

## Status

Inactive. The empty index still returns valid JSON for any Reach install that points at it.

## License

MIT. See [LICENSE](LICENSE).
