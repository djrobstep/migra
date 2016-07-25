from __future__ import unicode_literals


def differences(a, b):
    a_keys = set(a.keys())
    b_keys = set(b.keys())

    keys_added = set(b_keys) - set(a_keys)
    keys_removed = set(a_keys) - set(b_keys)
    keys_common = set(a_keys) & set(b_keys)

    added = {k: b[k] for k in keys_added}
    removed = {k: a[k] for k in keys_removed}
    modified = {k: b[k] for k in keys_common if not a[k] == b[k]}
    unmodified = {k: b[k] for k in keys_common if a[k] == b[k]}

    return added, removed, modified, unmodified
