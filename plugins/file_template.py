# file_template.py — Create new files from templates with :template <type>

import os
import time


_TEMPLATES = {
    "python": '#!/usr/bin/env python3\n"""$FILENAME\n\nCreated: $DATE\n"""\n\n\ndef main():\n    pass\n\n\nif __name__ == "__main__":\n    main()\n',
    "c": '/*\n * $FILENAME\n * Created: $DATE\n */\n\n#include <stdio.h>\n#include <stdlib.h>\n\nint main(int argc, char *argv[]) {\n    \n    return 0;\n}\n',
    "html": '<!DOCTYPE html>\n<html lang="en">\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>$FILENAME</title>\n</head>\n<body>\n    \n</body>\n</html>\n',
    "sh": '#!/usr/bin/env bash\n# $FILENAME\n# Created: $DATE\nset -euo pipefail\n\n',
    "makefile": '# $FILENAME\nCC = gcc\nCFLAGS = -Wall -Wextra -std=c11\nTARGET = main\nSRCS = $(wildcard *.c)\nOBJS = $(SRCS:.c=.o)\n\nall: $(TARGET)\n\n$(TARGET): $(OBJS)\n\t$(CC) $(CFLAGS) -o $@ $^\n\n%.o: %.c\n\t$(CC) $(CFLAGS) -c $<\n\nclean:\n\trm -f $(TARGET) $(OBJS)\n\n.PHONY: all clean\n',
}


def setup(editor):
    editor._tmpl_original_run_ex = editor.run_ex

    def patched_run_ex(cmd):
        parts = cmd.strip().split()
        if parts and parts[0] == "template":
            if len(parts) < 2:
                names = ', '.join(sorted(_TEMPLATES.keys()))
                editor.message = f"[template] Available: {names}"
                return
            ttype = parts[1].lower()
            if ttype not in _TEMPLATES:
                names = ', '.join(sorted(_TEMPLATES.keys()))
                editor.message = f"[template] Unknown. Available: {names}"
                return
            tmpl = _TEMPLATES[ttype]
            fname = os.path.basename(editor.filepath) if editor.filepath else "untitled"
            tmpl = tmpl.replace("$FILENAME", fname)
            tmpl = tmpl.replace("$DATE", time.strftime("%Y-%m-%d"))
            editor.lines = tmpl.split('\n')
            if editor.lines and editor.lines[-1] == '':
                pass  # keep trailing newline
            editor.cursor_row = 0
            editor.cursor_col = 0
            editor.message = f"[template] Applied '{ttype}' template"
            return

        if parts and parts[0] == "templatelist":
            names = ', '.join(sorted(_TEMPLATES.keys()))
            editor.message = f"[template] Available: {names}"
            return

        return editor._tmpl_original_run_ex(cmd)

    editor.run_ex = patched_run_ex


def teardown(editor):
    if hasattr(editor, '_tmpl_original_run_ex'):
        editor.run_ex = editor._tmpl_original_run_ex
        del editor._tmpl_original_run_ex


editor.plugin_register(
    "file_template",
    version="1.0",
    setup=setup,
    teardown=teardown,
    description="Apply file templates with :template <python|c|html|sh|makefile>",
)
