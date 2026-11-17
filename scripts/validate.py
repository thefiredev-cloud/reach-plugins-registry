#!/usr/bin/env python3
"""Validate plugins.json against the fields and permissions Reach accepts."""
import json
import re
import sys

ALLOWED = {"ssh_exec", "ssh_list_connections", "sftp_list", "sftp_read", "sftp_write",
           "vault_read", "vault_write", "tunnel_manage", "http", "notify", "ui"}

path = sys.argv[1] if len(sys.argv) > 1 else "plugins.json"
with open(path) as fh:
    entries = json.load(fh)
assert isinstance(entries, list), "top level must be a JSON array"
for e in entries:
    for k in ("id", "name", "version", "downloadUrl", "sha256"):
        assert isinstance(e.get(k), str) and e[k].strip(), f"{e.get('id')}: missing {k}"
    assert not re.search(r"[/\\.\0]", e["id"]), f"{e['id']}: bad id"
    assert re.fullmatch(r"[0-9a-fA-F]{64}", e["sha256"].strip()), f"{e['id']}: sha256 is not 64 hex chars"
    bad = set(e.get("permissions", [])) - ALLOWED
    assert not bad, f"{e['id']}: unknown permissions {bad}"
print(f"ok: {len(entries)} entries")
