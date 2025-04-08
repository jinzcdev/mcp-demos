from mcp.server.fastmcp import FastMCP

import os
import os.path as osp
import argparse
import shutil
import difflib


parser = argparse.ArgumentParser(description="Simple File System MCP Server")
parser.add_argument(
    "allowed_dirs",
    nargs="+",
    help="List of allowed directories for file operations",
)
args = parser.parse_args()

allowed_directories = [osp.abspath(dir_path) for dir_path in args.allowed_dirs]

mcp = FastMCP("SimpleFileSystemMCPServer", log_level="ERROR")


@mcp.tool(
    description="Get a detailed listing of all files and directories in a specified path. Results clearly distinguish between files and directories with [DIR] and [FILE] prefixes. This tool is essential for understanding directory structure and finding specific files within a directory. Only works within allowed directories."
)
async def list_directory(dir_path) -> str:
    """
    List files and directories in the specified directory

    Args:
        dir_path: The path of the directory to list
    Returns:
        A formatted list of files and directories with [DIR] and [FILE] prefixes
    Raises:
        ValueError: If the directory path is not within allowed directories or doesn't exist
    """
    if not osp.exists(dir_path) or not osp.isdir(dir_path):
        raise ValueError(f"{dir_path} is not a valid directory")

    entries = os.listdir(dir_path)
    formatted = []
    for entry in entries:
        entry_path = osp.join(dir_path, entry)
        if osp.isdir(entry_path):
            formatted.append(f"[DIR] {entry}")
        else:
            formatted.append(f"[FILE] {entry}")

    return "\n".join(formatted)


@mcp.tool(
    description="Read the complete contents of a file from the file system. Handles various text encodings and provides detailed error messages if the file cannot be read or accessed. Use this tool when you need to examine the complete contents of a single file. Only works within allowed directories."
)
async def read_file(file_path) -> str:
    """
    Read the content of the specified file

    Args:
        file_path: The path of the file to read
    Returns:
        The complete text content of the file
    Raises:
        ValueError: If the file does not exist or is not within allowed directories
    """
    if not osp.exists(file_path) or not osp.isfile(file_path):
        raise ValueError(f"{file_path} is not a valid file")

    with open(file_path, "r") as file:
        content = file.read()
    return content


@mcp.tool(
    description="Create a new file or completely overwrite an existing file with new content. Use with caution as it will overwrite existing files without warning. Handles text content with proper encoding. Only works within allowed directories."
)
async def write_file(file_path, content) -> str:
    """
    Write content to the specified file

    Args:
        file_path: The path of the file to write to
        content: The text content to write to the file
    Returns:
        Success message containing the path of the written file
    Raises:
        ValueError: If the file path is not within allowed directories or the target directory does not exist
    """
    if not osp.exists(osp.dirname(file_path)):
        raise ValueError(f"Directory for {file_path} does not exist")

    with open(file_path, "w") as file:
        file.write(content)
    return f"Successfully wrote to {file_path}"


@mcp.tool(
    description="Read the contents of multiple files simultaneously. This is more efficient than reading files one by one when you need to analyze or compare multiple files. Each file's content is returned with its path as a reference. Failed reads for individual files won't stop the entire operation. Only works within allowed directories."
)
async def read_multiple_files(file_paths) -> str:
    """
    Read the content of multiple files

    Args:
        file_paths: List of file paths to read
    Returns:
        Formatted text with file paths and their contents, separated by delimiters
    Raises:
        ValueError: If any file is not within allowed directories
    """
    results = []
    for file_path in file_paths:
        try:
            if not osp.exists(file_path) or not osp.isfile(file_path):
                results.append(f"{file_path}: Error - Not a valid file")
                continue

            with open(file_path, "r") as file:
                content = file.read()
            results.append(f"{file_path}:\n{content}")
        except Exception as e:
            results.append(f"{file_path}: Error - {str(e)}")

    return "\n---\n".join(results)


@mcp.tool(
    description="Make line-based edits to a text file. Each edit replaces exact text sequences with new content. Returns a unified diff showing the changes made. If dryRun is True, returns the diff without actually making changes. Only works within allowed directories."
)
async def edit_file(file_path, edits, dry_run=False) -> str:
    """
    Edit a text file by replacing specified text with new content

    Args:
        file_path: The path of the file to edit
        edits: List of edits, each containing 'oldText' and 'newText'
        dry_run: If True, only show what changes would be made without actually making them
    Returns:
        A unified diff showing the changes made or that would be made
    Raises:
        ValueError: If the file path is not within allowed directories or the file doesn't exist
    """
    if not osp.exists(file_path) or not osp.isfile(file_path):
        raise ValueError(f"{file_path} is not a valid file")

    with open(file_path, "r") as file:
        content = file.read()

    modified_content = content
    for edit in edits:
        old_text = edit.get("oldText", "")
        new_text = edit.get("newText", "")

        if old_text in modified_content:
            modified_content = modified_content.replace(old_text, new_text)
        else:
            raise ValueError(f"Could not find exact match for edit: {old_text}")

    # Generate unified diff
    diff = difflib.unified_diff(
        content.splitlines(keepends=True),
        modified_content.splitlines(keepends=True),
        fromfile=f"{file_path} (original)",
        tofile=f"{file_path} (modified)",
    )
    diff_text = "".join(diff)

    if not dry_run:
        with open(file_path, "w") as file:
            file.write(modified_content)

    return diff_text


@mcp.tool(
    description="Create a new directory or ensure a directory exists. Can create multiple nested directories in one operation. If the directory already exists, this operation will succeed silently. Perfect for setting up directory structures for projects or ensuring required paths exist. Only works within allowed directories."
)
async def create_directory(dir_path) -> str:
    """
    Create a new directory or ensure a directory exists

    Args:
        dir_path: The path of the directory to create
    Returns:
        Success message containing the path of the created directory
    Raises:
        ValueError: If the directory path is not within allowed directories
    """
    os.makedirs(dir_path, exist_ok=True)
    return f"Directory created or already exists: {dir_path}"


@mcp.tool(
    description="Move or rename files and directories. Can move files between directories and rename them in a single operation. If the destination exists, the operation will fail. Works across different directories and can be used for simple renaming within the same directory. Both source and destination must be within allowed directories."
)
async def move_file(source_path, destination_path) -> str:
    """
    Move or rename a file or directory

    Args:
        source_path: The path of the file or directory to move
        destination_path: The destination path
    Returns:
        Success message containing the source and destination paths
    Raises:
        ValueError: If either path is not within allowed directories or if the operation fails
    """
    if not osp.exists(source_path):
        raise ValueError(f"{source_path} does not exist")

    if osp.exists(destination_path):
        raise ValueError(f"{destination_path} already exists")

    shutil.move(source_path, destination_path)
    return f"Successfully moved {source_path} to {destination_path}"


@mcp.tool(
    description="Retrieve detailed metadata about a file or directory. Returns comprehensive information including size, creation time, last modified time, permissions, and type. This tool is perfect for understanding file characteristics without reading the actual content. Only works within allowed directories."
)
async def get_file_info(file_path) -> dict:
    """
    Get detailed information about a file or directory

    Args:
        file_path: The path of the file or directory
    Returns:
        Dictionary containing file metadata (size, created, modified, accessed, isDirectory, isFile, permissions)
    Raises:
        ValueError: If the path is not within allowed directories or doesn't exist
    """
    if not osp.exists(file_path):
        raise ValueError(f"{file_path} does not exist")

    stats = os.stat(file_path)
    info = {
        "size": stats.st_size,
        "created": stats.st_ctime,
        "modified": stats.st_mtime,
        "accessed": stats.st_atime,
        "isDirectory": osp.isdir(file_path),
        "isFile": osp.isfile(file_path),
        "permissions": oct(stats.st_mode)[-3:],
    }
    return info


@mcp.tool(
    description="Returns the list of root directories that this server is allowed to access. Use this to understand which directories are available before trying to access files."
)
async def list_allowed_directories() -> list:
    """
    List all directories that the server is allowed to access

    Returns:
        List of allowed directory paths
    """
    return allowed_directories


if __name__ == "__main__":
    mcp.run(transport="stdio")
