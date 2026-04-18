# duplicate_line.py — Duplicate current line or selection with :dup or Ctrl+d

def setup(editor):
    editor._dup_original_run_ex = editor.run_ex

    def patched_run_ex(cmd):
        parts = cmd.strip().split()
        if parts and parts[0] == "dup":
            count = 1
            if len(parts) > 1:
                try:
                    count = max(1, int(parts[1]))
                except ValueError:
                    pass
            row = editor.cursor_row
            if 0 <= row < len(editor.lines):
                line = editor.lines[row]
                for _ in range(count):
                    editor.lines.insert(row + 1, line)
                editor.cursor_row += count
                editor.message = f"[dup] Duplicated {count} time(s)"
            return
        return editor._dup_original_run_ex(cmd)

    editor.run_ex = patched_run_ex


def teardown(editor):
    if hasattr(editor, '_dup_original_run_ex'):
        editor.run_ex = editor._dup_original_run_ex
        del editor._dup_original_run_ex


editor.plugin_register(
    "duplicate_line",
    version="1.0",
    setup=setup,
    teardown=teardown,
    description="Duplicate current line with :dup [count]",
)
