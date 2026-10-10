# reach-plugins-registry

A single JSON file, `plugins.json`, that lists installable plugins for the [Reach](https://github.com/alexandrosnt/Reach) SSH client. It is for plugin authors who want to publish a plugin and for Reach users who want to point their marketplace at a custom registry.

## Current state

The index is empty. `plugins.json` contains exactly this:

```json
[]
```

Three seed plugins were added and then removed on 2026-08-03. Nothing is listed today, so Reach's marketplace panel shows no plugins when it reads this file. An empty array is still valid, and Reach accepts it without error.

This repository has no schema file, validator, test, or CI workflow. The format below comes from the marketplace code in the [thefiredev-cloud/Reach](https://github.com/thefiredev-cloud/Reach) fork (`src-tauri/src/plugin/marketplace.rs`).

## What it does

Reach downloads the registry URL, parses the body as a JSON array, and shows each entry in the marketplace panel. When a user installs an entry, Reach downloads `downloadUrl`, checks the archive against `sha256`, and extracts it into the plugin directory. Install fails if the hash does not match.

To read the index:

```bash
curl -s https://raw.githubusercontent.com/thefiredev-cloud/reach-plugins-registry/main/plugins.json
```

## Index format

The file is a top-level JSON array. Each element is an object with these fields. Field names are camelCase.

| Field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `id` | string | yes | Plugin identifier. Used as the install directory name. Must not be empty and must not contain `/`, `\`, `.`, or a null character. |
| `name` | string | yes | Display name. |
| `version` | string | yes | Plugin version, for example `1.0.0`. |
| `description` | string | no | One-line summary. Defaults to an empty string. |
| `author` | string | no | Author name. Defaults to an empty string. |
| `repo` | string | no | GitHub `user/repo` identifier. Informational, used for the source link. |
| `downloadUrl` | string | yes | Direct URL to the plugin release zip. Maximum archive size is 16 MiB. |
| `sha256` | string | yes | Hex-encoded SHA-256 of the file at `downloadUrl`. Reach lowercases it before comparing. An empty value blocks the install. |
| `permissions` | array of strings | no | Permissions the plugin manifest declares. Shown to the user before install. Defaults to an empty array. |

Allowed `permissions` values: `ssh_exec`, `ssh_list_connections`, `sftp_list`, `sftp_read`, `sftp_write`, `vault_read`, `vault_write`, `tunnel_manage`, `http`, `notify`, `ui`. Any other value makes the whole index fail to parse.

The zip must contain `plugin.toml` at its root. Reach rejects archives that contain symbolic links or paths that escape the extraction directory.

## Add an entry

1. Publish your plugin as a zip with `plugin.toml` at the archive root.
2. Compute the hash of that exact file: `sha256sum my-plugin.zip`.
3. Add an object to the array in `plugins.json`. Keep the JSON valid.
4. Open a pull request. Merging is how an entry is admitted, so a maintainer reviews it first.

Example entry (placeholder values):

```json
[
  {
    "id": "my-plugin",
    "name": "My Plugin",
    "version": "1.0.0",
    "description": "What the plugin does in one sentence.",
    "author": "Your Name",
    "repo": "your-org/your-plugin-repo",
    "downloadUrl": "https://github.com/your-org/your-plugin-repo/releases/download/v1.0.0/my-plugin.zip",
    "sha256": "<64-character hex digest of my-plugin.zip>",
    "permissions": ["notify"]
  }
]
```

Check that the file parses before you commit:

```bash
python3 -m json.tool plugins.json
```

Plugin source and manual install steps live in [reach-plugins](https://github.com/thefiredev-cloud/reach-plugins).

## Point Reach at this registry

Reach reads the registry from a URL stored in its settings. The built-in default in the fork source is the upstream author's registry, not this repository. To use this one, set the marketplace URL to the raw file address shown above. Reach accepts `http://` and `https://` URLs only.

## Project layout

```
plugins.json   the registry index
LICENSE        MIT license text
README.md      this file
```

## License

MIT. See [LICENSE](LICENSE).
