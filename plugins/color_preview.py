# color_preview.py — Show hex color values inline with :colors

import re


def setup(editor):
    editor._color_original_run_ex = editor.run_ex

    def patched_run_ex(cmd):
        parts = cmd.strip().split()
        if parts and parts[0] == "colors":
            pattern = re.compile(r'#[0-9a-fA-F]{3,8}\b')
            results = []
            for i, line in enumerate(editor.lines):
                for m in pattern.finditer(line):
                    hex_val = m.group()
                    results.append((i, hex_val, line.strip()))
            if not results:
                editor.message = "[colors] No hex colors found"
                return
            editor._grep_results = []
            for lineno, color, text in results:
                editor._grep_results.append((editor.filepath or "[buffer]", lineno, f"{color} | {text}"))
            editor._grep_visible = True
            editor._grep_cursor = 0
            editor.message = f"[colors] {len(results)} color(s) found"
            return
        return editor._color_original_run_ex(cmd)

    editor.run_ex = patched_run_ex


def teardown(editor):
    if hasattr(editor, '_color_original_run_ex'):
        editor.run_ex = editor._color_original_run_ex
        del editor._color_original_run_ex


editor.plugin_register(
    "color_preview",
    version="1.0",
    setup=setup,
    teardown=teardown,
    description="Find and list hex color codes with :colors",
)
