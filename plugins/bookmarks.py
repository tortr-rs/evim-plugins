# bookmarks.py — Named bookmarks across files with :bm add <name>, :bm go <name>, :bm list

import os
import json


def _bookmarks_path():
    d = os.path.expanduser("~/.config/evim")
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, "bookmarks.json")


def _load_bookmarks():
    p = _bookmarks_path()
    if os.path.exists(p):
        with open(p) as f:
            return json.load(f)
    return {}


def _save_bookmarks(data):
    with open(_bookmarks_path(), 'w') as f:
        json.dump(data, f, indent=2)


def setup(editor):
    editor._bm_original_run_ex = editor.run_ex

    def patched_run_ex(cmd):
        parts = cmd.strip().split()
        if parts and parts[0] == "bm":
            if len(parts) < 2:
                editor.message = "[bm] Usage: :bm add|go|list|del <name>"
                return
            action = parts[1]

            if action == "add" and len(parts) >= 3:
                name = parts[2]
                bm = _load_bookmarks()
                bm[name] = {
                    "file": editor.filepath or "",
                    "row": editor.cursor_row,
                    "col": editor.cursor_col,
                }
                _save_bookmarks(bm)
                editor.message = f"[bm] Bookmark '{name}' set"
                return

            elif action == "go" and len(parts) >= 3:
                name = parts[2]
                bm = _load_bookmarks()
                if name not in bm:
                    editor.message = f"[bm] '{name}' not found"
                    return
                info = bm[name]
                fp = info.get("file", "")
                if fp and os.path.isfile(fp) and fp != editor.filepath:
                    editor._bm_original_run_ex(f"e {fp}")
                editor.cursor_row = info.get("row", 0)
                editor.cursor_col = info.get("col", 0)
                editor.message = f"[bm] Jumped to '{name}'"
                return

            elif action == "list":
                bm = _load_bookmarks()
                if not bm:
                    editor.message = "[bm] No bookmarks"
                    return
                entries = []
                for name, info in sorted(bm.items()):
                    f = os.path.basename(info.get("file", "?"))
                    r = info.get("row", 0) + 1
                    entries.append(f"{name}({f}:{r})")
                editor.message = f"[bm] {', '.join(entries)}"
                return

            elif action == "del" and len(parts) >= 3:
                name = parts[2]
                bm = _load_bookmarks()
                if name in bm:
                    del bm[name]
                    _save_bookmarks(bm)
                    editor.message = f"[bm] Deleted '{name}'"
                else:
                    editor.message = f"[bm] '{name}' not found"
                return

            else:
                editor.message = "[bm] Usage: :bm add|go|list|del <name>"
                return

        return editor._bm_original_run_ex(cmd)

    editor.run_ex = patched_run_ex


def teardown(editor):
    if hasattr(editor, '_bm_original_run_ex'):
        editor.run_ex = editor._bm_original_run_ex
        del editor._bm_original_run_ex


editor.plugin_register(
    "bookmarks",
    version="1.0",
    setup=setup,
    teardown=teardown,
    description="Named bookmarks with :bm add|go|list|del <name>",
)
