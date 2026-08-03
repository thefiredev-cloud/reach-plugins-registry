# Reach Plugins Registry

Marketplace index for the [Reach](https://github.com/alexandrosnt/Reach) plugin marketplace.

Reach fetches `plugins.json` from this repo's `main` branch. Each entry pins a
release zip by SHA-256; install fails on hash mismatch.

**Use in Reach:** Plugins panel -> Marketplace -> gear icon -> set registry URL to:

```
https://raw.githubusercontent.com/thefiredev-cloud/reach-plugins-registry/main/plugins.json
```

Plugin sources: [thefiredev-cloud/reach-plugins](https://github.com/thefiredev-cloud/reach-plugins)

## Adding a plugin

1. Publish a release zip (plugin.toml at archive root) to a public repo.
2. Open a PR here adding the entry (id, name, version, description, author, repo, downloadUrl, sha256, permissions).
3. Merge = admission to the marketplace.
