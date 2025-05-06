import applescript;
import base64
import os
from PIL import Image
import io

from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Demo")


# Add an addition tool
@mcp.tool()
def copy_to_clipboard(data: str) -> int:
    """copy data to clipboard"""
    script = f'set the clipboard to "{data}" as text'
    result = applescript.run(script)
    return result.code

@mcp.tool()
def paste_from_clipboard() -> str:
    """paste from clipboard"""
    script = 'return the clipboard as text'
    result = applescript.run(script)
    return result.out

@mcp.tool()
def paste_image_from_clipboard() -> str:
    """Paste image from clipboard, automatically detect TIFF/PNG/JPEG formats, and always return the image as a PNG base64-encoded string. Returns an empty string if there is no image in the clipboard."""
    import time
    formats = [
        ("TIFF", "«class TIFF»", "/tmp/clipboard_img.tiff"),
        ("PNG",  "«class PNGf»", "/tmp/clipboard_img.png"),
        ("JPEG", "«class JPEG»", "/tmp/clipboard_img.jpg"),
    ]
    for fmt_name, fmt_class, tmp_path in formats:
        script = f'''
        try
            set theImage to the clipboard as {fmt_class}
            set theFile to POSIX file "{tmp_path}"
            set outFile to open for access theFile with write permission
            write theImage to outFile
            close access outFile
            return "OK"
        on error
            return "NO_IMAGE"
        end try
        '''
        result = applescript.run(script)
        if result.out.strip() == "OK" and os.path.exists(tmp_path):
            try:
                with open(tmp_path, "rb") as f:
                    img = Image.open(f)
                    buf = io.BytesIO()
                    img.save(buf, format="PNG")
                    png_bytes = buf.getvalue()
                os.remove(tmp_path)
                return base64.b64encode(png_bytes).decode("utf-8")
            except Exception as e:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
                continue
    return ""

def main():
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
