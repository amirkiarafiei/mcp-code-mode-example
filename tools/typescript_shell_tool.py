"""
TypeScript Shell Tool - Executes TypeScript code snippets
This tool allows the agent to execute TypeScript code for the code execution approach.
"""

from langchain.tools import tool
import subprocess
import tempfile
import os
from typing import Optional


PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
AGENT_FS_ROOT = os.path.join(PROJECT_ROOT, "agent_filesystem")


def _resolve_agent_path(requested_path: str) -> Optional[str]:
    """
    Normalize and resolve a path so it stays within agent_filesystem/.
    Returns the absolute path if valid, None otherwise.
    """
    base_abs = os.path.abspath(AGENT_FS_ROOT)
    normalized = (requested_path or "").strip()
    if not normalized or normalized == ".":
        normalized = "."
    normalized = normalized.lstrip("/").rstrip("/")

    if normalized.startswith("agent_filesystem/"):
        normalized = normalized[len("agent_filesystem/") :]
    elif normalized == "agent_filesystem":
        normalized = "."

    full_path = os.path.abspath(os.path.join(base_abs, normalized))

    try:
        common_path = os.path.commonpath([base_abs, full_path])
        if common_path != base_abs:
            return None
    except ValueError:
        return None

    return full_path


@tool
def execute_typescript(code: str) -> str:
    """
    Execute TypeScript code and return the output. This tool allows running TypeScript
    code snippets to orchestrate multiple operations efficiently. The code is executed
    in a Node.js environment with access to filesystem and installed packages.
    
    Args:
        code: TypeScript code to execute. Should be complete, valid TypeScript.
    
    Returns:
        The output from executing the TypeScript code, including stdout and stderr.
    """
    try:
        # Create a temporary file in the project root for proper imports
        temp_file = os.path.join(PROJECT_ROOT, f'.tmp_exec_{os.getpid()}.ts')
        
        with open(temp_file, 'w') as f:
            f.write(code)
        
        # Execute the TypeScript code using tsx (better compatibility than ts-node)
        result = subprocess.run(
            ['npx', '-y', 'tsx', temp_file],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=PROJECT_ROOT
        )
        
        # Clean up the temporary file
        try:
            os.unlink(temp_file)
        except:
            pass
        
        output = result.stdout
        if result.stderr:
            output += f"\nErrors/Warnings:\n{result.stderr}"
        
        if result.returncode != 0:
            output += f"\nExit code: {result.returncode}"
        
        return output if output else "Code executed successfully with no output."
        
    except subprocess.TimeoutExpired:
        return "Error: Code execution timed out after 30 seconds."
    except FileNotFoundError:
        return "Error: tsx is not installed. Please install with: npm install --save-dev tsx"
    except Exception as e:
        return f"Error executing TypeScript code: {str(e)}"


@tool
def read_file(file_path: str) -> str:
    """
    Read the contents of a file within the agent filesystem. Paths outside
    `agent_filesystem/` are rejected to emulate a virtual tool directory.
    
    Args:
        file_path: Path to the file to read, relative to `agent_filesystem/`.
                   Prefixing with `agent_filesystem/` is also accepted.
    
    Returns:
        The contents of the file as a string.
    """
    resolved = _resolve_agent_path(file_path)
    if resolved is None:
        return f"Error: Access denied outside agent_filesystem for path: {file_path}"

    try:
        with open(resolved, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return f"Error: File not found at path: {file_path}"
    except Exception as e:
        return f"Error reading file: {str(e)}"


@tool
def list_directory(dir_path: str = "agent_filesystem") -> str:
    """
    List the contents of a directory inside the agent filesystem. This keeps discovery
    scoped to `agent_filesystem/` to mirror the virtual tool layout described in the
    Code Mode articles.
    
    Args:
        dir_path: Path to the directory to list, relative to `agent_filesystem/`.
                 Defaults to the root of the agent filesystem.
    
    Returns:
        A formatted list of files and directories.
    """
    resolved = _resolve_agent_path(dir_path)
    if resolved is None:
        return f"Error: Access denied outside agent_filesystem for path: {dir_path}"

    try:
        items = os.listdir(resolved)
    except FileNotFoundError:
        return f"Error: Directory not found at path: {dir_path}"
    except Exception as e:
        return f"Error listing directory: {str(e)}"

    display_path = dir_path if dir_path else "agent_filesystem"
    result = f"Contents of {display_path}:\n"
    for item in sorted(items):
        item_path = os.path.join(resolved, item)
        if os.path.isdir(item_path):
            result += f"  [DIR]  {item}/\n"
        else:
            result += f"  [FILE] {item}\n"

    return result
