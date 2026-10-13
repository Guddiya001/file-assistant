
from pathlib import Path
from mcp.server.fastmcp import FastMCP

# Create the MCP server
mcp = FastMCP("Python File Assistant")

# Restrict file access to this project's workspace
WORKSPACE = (Path(__file__).parent / "workspace").resolve()
WORKSPACE.mkdir(exist_ok=True)


@mcp.tool()
def list_files() -> list[str]:
    """List files available in the workspace."""
    return sorted(
        path.name
        for path in WORKSPACE.iterdir()
        if path.is_file()
    )


@mcp.tool()
def read_file(filename: str) -> str:
    """Read a text file from the workspace by filename."""
    if not filename or Path(filename).name != filename:
        raise ValueError("Provide a filename without directory paths.")

    file_path = (WORKSPACE / filename).resolve()

    if file_path.parent != WORKSPACE:
        raise ValueError("Access outside the workspace is not allowed.")

    if not file_path.is_file():
        raise FileNotFoundError(f"File not found: {filename}")

    return file_path.read_text(encoding="utf-8")


@mcp.resource("file-assistant://notes")
def notes_resource() -> str:
    """Provide the contents of the assistant's notes as an MCP resource."""
    notes_path = WORKSPACE / "notes.txt"

    if not notes_path.is_file():
        raise FileNotFoundError("notes.txt was not found in the workspace.")

    return notes_path.read_text(encoding="utf-8")



if __name__ == "__main__":
    mcp.run(transport="stdio")
