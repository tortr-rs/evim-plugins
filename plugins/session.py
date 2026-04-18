# session.py — Save and restore editing sessions with :session save <name> / :session load <name>

import os
import json


def _session_dir():
    d = os.path.expanduser("~/.config/evim/sessions")
    os.makedirs(d, exist_ok=True)
    return d


def setup(editor):
    editor._session_original_run_ex = editor.run_ex

    def patched_run_ex(cmd):
        parts = cmd.strip().split()
        if parts and parts[0] == "session":
            if len(parts) < 3:
                editor.message = "[session] Usage: :session save|load <name>"
                return
            action = parts[1]
            name = parts[2]
            path = os.path.join(_session_dir(), name + ".json")

            if action == "save":
                data = {
                    "files": [],
                    "active": getattr(editor, 'buf_index', 0),
                }
                if hasattr(editor, 'buffers') and editor.buffers:
                    for buf in editor.buffers:
                        fp = getattr(buf, 'filepath', None)
                        if fp:
                            data["files"].append(fp)
                elif editor.filepath:
                    data["files"].append(editor.filepath)
                with open(path, 'w') as f:
                    json.dump(data, f, indent=2)
                editor.message = f"[session] Saved '{name}' ({len(data['files'])} file(s))"
                return

            elif action == "load":
                if not os.path.exists(path):
                    editor.message = f"[session] '{name}' not found"
                    return
                with open(path) as f:
                    data = json.load(f)
                files = data.get("files", [])
                if not files:
                    editor.message = f"[session] '{name}' is empty"
                    return
                for fp in files:
                    if os.path.isfile(fp):
                        editor.run_ex(f"e {fp}")
                editor.message = f"[session] Loaded '{name}' ({len(files)} file(s))"
                return

            elif action == "list":
                sessions = [f[:-5] for f in os.listdir(_session_dir()) if f.endswith('.json')]
                editor.message = f"[session] {', '.join(sessions) if sessions else 'No sessions'}"
                return

            else:
                editor.message = "[session] Usage: :session save|load|list <name>"
                return

        return editor._session_original_run_ex(cmd)

    editor.run_ex = patched_run_ex


def teardown(editor):
    if hasattr(editor, '_session_original_run_ex'):
        editor.run_ex = editor._session_original_run_ex
        del editor._session_original_run_ex


editor.plugin_register(
    "session",
    version="1.0",
    setup=setup,
    teardown=teardown,
    description="Save and restore editing sessions with :session save|load|list <name>",
)
