"""file_inspection --- safe file reading and /read, /ls, /find endpoint handlers"""

import os
from rodi_admin.config import MAX_READ_BYTES
from rodi_admin.features.command_execution import run_command


def safe_read_text_file(file_path: str, max_bytes: int = MAX_READ_BYTES) -> dict:
    """Read a text file safely with size limits and encoding fallback.

    Args:
        file_path: Absolute or relative path to the file.
        max_bytes: Maximum bytes to read before truncating.

    Returns:
        Dict with success, path, size, encoding, truncated, content (or error).
    """
    try:
        abs_path = os.path.abspath(os.path.expanduser(file_path))

        if not os.path.exists(abs_path):
            return {"success": False, "error": "file not found", "path": abs_path}

        if not os.path.isfile(abs_path):
            return {"success": False, "error": "path is not a regular file", "path": abs_path}

        size = os.path.getsize(abs_path)
        with open(abs_path, "rb") as file_handle:
            raw = file_handle.read(max_bytes + 1)

        truncated = len(raw) > max_bytes
        if truncated:
            raw = raw[:max_bytes]

        try:
            content = raw.decode("utf-8")
            encoding = "utf-8"
        except UnicodeDecodeError:
            content = raw.decode("utf-8", errors="replace")
            encoding = "utf-8-replaced"

        return {
            "success": True,
            "path": abs_path,
            "size": size,
            "encoding": encoding,
            "truncated": truncated,
            "max_bytes": max_bytes,
            "content": content,
        }

    except Exception as exc:
        return {"success": False, "error": str(exc), "path": file_path}


def handle_read_get(params: dict) -> tuple[int, dict]:
    """Handle GET /read?path=... request.

    Args:
        params: Parsed query string dict.

    Returns:
        Tuple of (http_status_code, response_dict).
    """
    file_path = params.get("path", [None])[0]
    if not file_path:
        return 400, {"error": "Parameter 'path' is required"}
    result = safe_read_text_file(file_path)
    return (200 if result.get("success") else 404, result)


def handle_ls_get(params: dict) -> tuple[int, dict]:
    """Handle GET /ls?path=... request.

    Args:
        params: Parsed query string dict.

    Returns:
        Tuple of (http_status_code, response_dict).
    """
    dir_path = params.get("path", ["/"])[0]
    result = run_command(f"ls -la '{dir_path}'")
    result["path"] = dir_path
    return 200, result


def handle_find_get(params: dict) -> tuple[int, dict]:
    """Handle GET /find?path=&name=&depth= request.

    Args:
        params: Parsed query string dict.

    Returns:
        Tuple of (http_status_code, response_dict).
    """
    search_path = params.get("path", ["/"])[0]
    name = params.get("name", ["*"])[0]
    depth = params.get("depth", ["5"])[0]
    cmd = f"find '{search_path}' -maxdepth {depth} -name '{name}' 2>/dev/null"
    result = run_command(cmd)
    result["search_path"] = search_path
    result["name"] = name
    result["depth"] = depth
    return 200, result
