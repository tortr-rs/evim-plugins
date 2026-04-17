# EVim Plugins

A collection of plugins for [EVim](https://github.com/tortr-rs/Editor-VIM), the modal CLI text editor.

## Installation

Copy plugins to your EVim plugin directory:

```bash
# Clone this repo
git clone https://github.com/tortr-rs/evim-plugins.git

# Copy all plugins
cp evim-plugins/plugins/*.py ~/.config/evim/plugins/

# Or symlink individual plugins
mkdir -p ~/.config/evim/plugins
ln -s "$(pwd)/evim-plugins/plugins/autosave.py" ~/.config/evim/plugins/
```

Plugins are auto-loaded when EVim starts. Manage with `:PluginList`, `:PluginEnable`, `:PluginDisable`.

## Plugins

| Plugin | Description | Commands |
|--------|-------------|----------|
| **autosave** | Auto-save files every 30 seconds after edits | — |
| **trailing_whitespace** | Strip trailing whitespace on save | — |
| **final_newline** | Ensure files end with a single newline | — |
| **wordcount** | Show word/line/char count | `:wordcount`, `:wc` |
| **bracket_highlight** | Show matching bracket position | — |
| **git_branch** | Display current git branch in status bar | — |
| **zen_mode** | Distraction-free writing (hides UI elements) | `:zen` |
| **timestamp** | Insert current date/time at cursor | `:timestamp`, `:ts`, `:date` |
| **lorem** | Insert lorem ipsum placeholder text | `:lorem [count]` |
| **line_sorter** | Sort or deduplicate lines | `:sortlines [-r]`, `:uniqlines` |

## Writing Your Own Plugin

Plugins are Python files that call `editor.plugin_register()`. The `editor` object is injected automatically.

```python
# my_plugin.py

def setup(editor):
    """Called when the plugin is loaded or re-enabled."""
    editor.on("after_save", on_save)

def teardown(editor):
    """Called when the plugin is disabled."""
    editor.off("after_save", on_save)

def on_save(editor, filepath=None, **kwargs):
    editor.message = f"Saved {filepath}"

editor.plugin_register(
    "my_plugin",
    version="1.0",
    setup=setup,
    teardown=teardown,
    description="Example plugin",
)
```

### Available Events

| Event | kwargs | When |
|-------|--------|------|
| `startup` | — | After editor initialization |
| `before_save` | `filepath` | Before writing file to disk |
| `after_save` | `filepath` | After writing file to disk |
| `buffer_open` | `filepath` | When a new buffer is opened |
| `plugin_loaded` | `plugin` | After a plugin is registered |

### Plugin API

- `editor.on(event, callback)` — Register an event hook
- `editor.off(event, callback)` — Remove an event hook
- `editor.emit(event, **kwargs)` — Fire an event
- `editor.lines` — List of strings (buffer content)
- `editor.cx`, `editor.cy` — Cursor column and row
- `editor.filepath` — Current file path
- `editor.message` — Status bar message
- `editor.options` — Dict of editor options
- `editor.run_ex(cmd)` — Execute an ex command

## License

BSD 3-Clause License
