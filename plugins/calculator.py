# calculator.py — Inline calculator with :calc <expression>

import math


def setup(editor):
    editor._calc_original_run_ex = editor.run_ex

    def patched_run_ex(cmd):
        parts = cmd.strip().split(None, 1)
        if parts and parts[0] == "calc":
            if len(parts) < 2:
                editor.message = "[calc] Usage: :calc <expression>"
                return
            expr = parts[1]
            safe_names = {
                k: v for k, v in math.__dict__.items()
                if not k.startswith('_')
            }
            safe_names.update({"abs": abs, "round": round, "min": min, "max": max,
                               "int": int, "float": float, "hex": hex, "bin": bin,
                               "oct": oct, "pow": pow, "sum": sum})
            try:
                result = eval(expr, {"__builtins__": {}}, safe_names)
                editor.message = f"[calc] {expr} = {result}"
            except Exception as e:
                editor.message = f"[calc] Error: {e}"
            return
        return editor._calc_original_run_ex(cmd)

    editor.run_ex = patched_run_ex


def teardown(editor):
    if hasattr(editor, '_calc_original_run_ex'):
        editor.run_ex = editor._calc_original_run_ex
        del editor._calc_original_run_ex


editor.plugin_register(
    "calculator",
    version="1.0",
    setup=setup,
    teardown=teardown,
    description="Inline calculator with :calc <expression>",
)
