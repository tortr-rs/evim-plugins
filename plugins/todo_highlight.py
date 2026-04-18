# todo_highlight.py — Highlight TODO/FIXME/HACK/XXX/NOTE comments and list them with :todos

import re


def _find_todos(editor):
    """Find all TODO-style comments in the current file."""
    pattern = re.compile(r'\b(TODO|FIXME|HACK|XXX|NOTE|BUG|WARN)\b', re.IGNORECASE)
    results = []
    for i, line in enumerate(editor.lines):
        m = pattern.search(line)
        if m:
            results.append((i, m.group(1).upper(), line.strip()))
    return results


def setup(editor):
    editor._todo_original_run_ex = editor.run_ex

    def patched_run_ex(cmd):
        parts = cmd.strip().split()
        if parts and parts[0] in ("todos", "todo", "fixme"):
            todos = _find_todos(editor)
            if not todos:
                editor.message = "[todo] No TODOs found"
                return
            # Use grep results UI to show them
            editor._grep_results = []
            for lineno, tag, text in todos:
                editor._grep_results.append((editor.filepath or "[buffer]", lineno, f"[{tag}] {text}"))
            editor._grep_visible = True
            editor._grep_cursor = 0
            editor.message = f"[todo] {len(todos)} item(s) found"
            return
        return editor._todo_original_run_ex(cmd)

    editor.run_ex = patched_run_ex


def teardown(editor):
    if hasattr(editor, '_todo_original_run_ex'):
        editor.run_ex = editor._todo_original_run_ex
        del editor._todo_original_run_ex


editor.plugin_register(
    "todo_highlight",
    version="1.0",
    setup=setup,
    teardown=teardown,
    description="List TODO/FIXME/HACK/NOTE comments with :todos",
)
