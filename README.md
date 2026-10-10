# reach-plugins-registry

A single JSON file, `plugins.json`, that can serve as a plugin registry for the [Reach](https://github.com/alexandrosnt/Reach) SSH client. It is for plugin authors who want a registry to publish to and for Reach users who want to point their marketplace at a registry of their own.

## Current state

The registry is empty and nothing points at it.

```json
[]
```

- `plugins.json` contains exactly the array above. Three seed plugins were added and removed on 2026-08-03.
- Reach does not read this repository by default. Its built-in registry URL is `https://raw.githubusercontent.com/alexandrosnt/reach-plugins-registry/main/plugins.json`, the upstream author's repository. That file was also `[]` on 2026-10-10.
- Nothing else in `thefiredev-cloud` points a Reach install here. The seed examples in [reach-plugins](https://github.com/thefiredev-cloud/reach-plugins) link to this repository only to say it is empty.
- There is no schema file, validator, test or CI workflow.

An empty array is valid. Reach parses it without error and the Marketplace tab shows "No plugins available".

This repository becomes useful when both of these are true: at least one entry is listed in `plugins.json`, and at least one Reach install has its registry URL set to the raw file address below. Until then it is a format reference and a template.

## How Reach uses a registry

Reach downloads the registry URL, parses the body as a JSON array, and lists each entry in the Marketplace tab of the Plugins panel. When a user installs an entry, Reach downloads `downloadUrl`, hashes the bytes, compares the hash to `sha256`, and only then extracts the archive into `<plugins dir>/<id>/`. The install fails if the hash is missing or does not match. Reach marks an installed plugin as updatable when the registry lists a higher `version`.

The format below comes from `src-tauri/src/plugin/marketplace.rs` and `src-tauri/src/plugin/schema.rs` in the upstream Reach repository, plus the [Marketplace page](https://reachssh.com/features/marketplace/) of the Reach docs.

To read this index directly:

```bash
curl -s https://raw.githubusercontent.com/thefiredev-cloud/reach-plugins-registry/main/plugins.json
```

## Index format

The file is a top-level JSON array. Each element is an object. Field names are camelCase.

| Field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `id` | string | yes | Plugin identifier and install directory name. Must not be empty and must not contain `/`, `\`, `.` or a null character. |
| `name` | string | yes | Display name. |
| `version` | string | yes | Plugin version, for example `1.0.0`. Reach compares it to the installed version to offer updates. |
| `description` | string | no | One-line summary. Defaults to an empty string. |
| `author` | string | no | Author name. Defaults to an empty string. |
| `repo` | string | no | GitHub `user/repo`. Informational, used for the source link. |
| `keywords` | array of strings | no | Extra search terms. The search box matches them alongside name, description, author and `id`. Defaults to an empty array. |
| `downloadUrl` | string | yes | Direct URL of the plugin release zip. Reach's docs require HTTPS. The archive may be at most 16 MiB. |
| `sha256` | string | yes | Hex SHA-256 of the file at `downloadUrl`. Reach trims and lowercases it before comparing. An empty value blocks the install. |
| `permissions` | array of strings | no | Permissions the plugin's manifest declares, shown to the user before install. Defaults to an empty array. |

Allowed `permissions` values: `ssh_exec`, `ssh_list_connections`, `sftp_list`, `sftp_read`, `sftp_write`, `vault_read`, `vault_write`, `tunnel_manage`, `http`, `notify`, `ui`. Any other value makes the whole index fail to parse, so one bad entry hides every plugin in the registry.

The zip must contain `plugin.toml` at its root. Reach rejects archives that contain symbolic links or paths that escape the extraction directory. Extraction happens in a staging directory, so a failed install does not leave a half-written plugin behind.

Older Reach builds do not know `keywords`. They ignore the field, because unknown fields are not an error.

## Add an entry

1. Publish your plugin as a zip with `plugin.toml` at the archive root.
2. Hash that exact file: `sha256sum my-plugin.zip`.
3. Add an object to the array in `plugins.json`.
4. Open a pull request. A maintainer reviews it, and merging is what admits the entry.

Example entry with placeholder values:

```json
[
  {
    "id": "my-plugin",
    "name": "My Plugin",
    "version": "1.0.0",
    "description": "What the plugin does in one sentence.",
    "author": "Your Name",
    "repo": "your-org/your-plugin-repo",
    "keywords": ["example"],
    "downloadUrl": "https://github.com/your-org/your-plugin-repo/releases/download/v1.0.0/my-plugin.zip",
    "sha256": "<64-character hex digest of my-plugin.zip>",
    "permissions": ["notify"]
  }
]
```

Check that the file is valid JSON before you commit:

```bash
python3 -m json.tool plugins.json
```

That check does not validate field names or permission values. This one does:

```bash
python3 - <<'EOF'
import json, re
ALLOWED = {"ssh_exec", "ssh_list_connections", "sftp_list", "sftp_read", "sftp_write",
           "vault_read", "vault_write", "tunnel_manage", "http", "notify", "ui"}
for e in json.load(open("plugins.json")):
    for k in ("id", "name", "version", "downloadUrl", "sha256"):
        assert isinstance(e.get(k), str) and e[k].strip(), f"{e.get('id')}: missing {k}"
    assert not re.search(r"[/\\.\0]", e["id"]), f"{e['id']}: bad id"
    assert re.fullmatch(r"[0-9a-fA-F]{64}", e["sha256"].strip()), f"{e['id']}: sha256 is not 64 hex chars"
    bad = set(e.get("permissions", [])) - ALLOWED
    assert not bad, f"{e['id']}: unknown permissions {bad}"
print("ok")
EOF
```

Plugin source and manual install steps live in [reach-plugins](https://github.com/thefiredev-cloud/reach-plugins).

## Point Reach at this registry

In Reach, open the Plugins panel, switch to the Marketplace tab, click the Registry button, paste the raw file address from above and click Save. The Default button restores the built-in URL. Reach accepts `http://` and `https://` addresses only. The URL survives a restart only while the vault is unlocked.

## Files

```
plugins.json   the registry index
LICENSE        MIT license text
README.md      this file
```

## License

MIT. See [LICENSE](LICENSE).
