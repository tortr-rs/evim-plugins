# snippets.py — Simple code snippet expansion with :snip <name> and :sniplist

import os
import json


def _snippets_path():
    d = os.path.expanduser("~/.config/evim")
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, "snippets.json")


def _load_snippets():
    p = _snippets_path()
    if os.path.exists(p):
        with open(p) as f:
            return json.load(f)
    return {
        "main": 'int main(int argc, char *argv[]) {\n    \n    return 0;\n}',
        "ifmain": 'if __name__ == "__main__":\n    main()',
        "for": 'for i in range($1):\n    $0',
        "class": 'class $1:\n    def __init__(self):\n        $0',
        "fn": 'def $1($2):\n    $0',
        "try": 'try:\n    $0\nexcept Exception as e:\n    pass',
    }


def _save_snippets(data):
    with open(_snippets_path(), 'w') as f:
        json.dump(data, f, indent=2)


def setup(editor):
    editor._snip_original_run_ex = editor.run_ex

    def patched_run_ex(cmd):
        parts = cmd.strip().split(None, 2)
        if not parts:
            return editor._snip_original_run_ex(cmd)

        if parts[0] == "snip" and len(parts) >= 2:
            snippets = _load_snippets()
            name = parts[1]
            if name not in snippets:
                editor.message = f"[snip] Unknown snippet '{name}'. Use :sniplist"
                return
            text = snippets[name]
            # Clean up placeholders
            text = text.replace('$0', '').replace('$1', '').replace('$2', '')
            insert_lines = text.split('\n')
            row = editor.cursor_row
            for i, line in enumerate(insert_lines):
                editor.lines.insert(row + 1 + i, line)
            editor.cursor_row = row + len(insert_lines)
            editor.message = f"[snip] Inserted '{name}'"
            return

        if parts[0] == "sniplist":
            snippets = _load_snippets()
            names = sorted(snippets.keys())
            editor.message = f"[snip] {', '.join(names)}"
            return

        if parts[0] == "snipadd" and len(parts) >= 3:
            name = parts[1]
            body = parts[2]
            snippets = _load_snippets()
            snippets[name] = body.replace('\\n', '\n')
            _save_snippets(snippets)
            editor.message = f"[snip] Added '{name}'"
            return

        if parts[0] == "snipdel" and len(parts) >= 2:
            name = parts[1]
            snippets = _load_snippets()
            if name in snippets:
                del snippets[name]
                _save_snippets(snippets)
                editor.message = f"[snip] Deleted '{name}'"
            else:
                editor.message = f"[snip] '{name}' not found"
            return

        return editor._snip_original_run_ex(cmd)

    editor.run_ex = patched_run_ex


def teardown(editor):
    if hasattr(editor, '_snip_original_run_ex'):
        editor.run_ex = editor._snip_original_run_ex
        del editor._snip_original_run_ex


editor.plugin_register(
    "snippets",
    version="1.0",
    setup=setup,
    teardown=teardown,
    description="Code snippets with :snip <name>, :sniplist, :snipadd, :snipdel",
)
