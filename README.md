# MacOS Clipboard MCP

A simple utility that provides model context protocol (MCP) tools for interacting with the macOS clipboard.

## Features

- Copy text to the clipboard
- Paste text from the clipboard
- Paste images from the clipboard (supports TIFF, PNG, and JPEG formats)

## mcp config
```json
{
    "clipboard": {
            "command": "uv",
            "args": [
                "--directory",
                "<your-local-folder>/macos-clipboard-mcp",
                "run",
                "main.py"
            ]
        }
}
```

## Installation

```bash
uv sync
python main.py
```

## Requirements

- Python 3.12+
- macOS (uses AppleScript for clipboard operations)

## Usage

Start the MCP server:

```bash
mcp dev main.py
```

This exposes the following MCP tools:

- `copy_to_clipboard(data: str)`: Copies text to the clipboard
- `paste_from_clipboard()`: Returns text from the clipboard
- `paste_image_from_clipboard()`: Returns images from the clipboard as base64-encoded PNG

## Development

This project uses modern Python tooling:

- [uv](https://github.com/astral-sh/uv) for dependency management

## License

MIT
