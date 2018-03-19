from __future__ import unicode_literals

from collections import OrderedDict as od


def differences(a, b, add_dependencies_for_modifications=True):
    a_keys = set(a.keys())
    b_keys = set(b.keys())
    keys_added = set(b_keys) - set(a_keys)
    keys_removed = set(a_keys) - set(b_keys)
    keys_common = set(a_keys) & set(b_keys)
    added = od((k, b[k]) for k in sorted(keys_added))
    removed = od((k, a[k]) for k in sorted(keys_removed))
    modified = od((k, b[k]) for k in sorted(keys_common) if a[k] != b[k])
    unmodified = od((k, b[k]) for k in sorted(keys_common) if a[k] == b[k])
    return added, removed, modified, unmodified
