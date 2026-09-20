# reach-plugins-registry

Empty public JSON index that the Reach SSH client used to load marketplace plugins.

## Why it exists

Reach expected a `plugins.json` registry URL. The seed listings were removed from this repo so the index would not advertise plugins that no longer live here.

## How to run it

There is no application and no supported happy path.

```bash
git clone https://github.com/thefiredev-cloud/reach-plugins-registry.git
cd reach-plugins-registry
cat plugins.json
```

`plugins.json` is `[]`. Runtime: none.

Plugin source and install steps are in [thefiredev-cloud/reach-plugins](https://github.com/thefiredev-cloud/reach-plugins).

## In scope / out of scope

**In scope:** this emptied `plugins.json` index.

**Out of scope:** plugin implementations, `plugin.toml` zips, Reach itself, and any live marketplace.

Files in this tree: `README.md`, `plugins.json`.

## Current production URL

Not deployed.

## Status

archive
