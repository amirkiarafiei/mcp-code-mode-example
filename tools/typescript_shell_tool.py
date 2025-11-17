"""
TypeScript Shell Tool - Executes TypeScript code snippets
This tool allows the agent to execute TypeScript code for the code execution approach.
"""

from langchain.tools import tool
import subprocess
import tempfile
import os


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
        base_dir = os.path.dirname(os.path.dirname(__file__))
        temp_file = os.path.join(base_dir, f'.tmp_exec_{os.getpid()}.ts')
        
        with open(temp_file, 'w') as f:
            f.write(code)
        
        # Execute the TypeScript code using tsx (better compatibility than ts-node)
        result = subprocess.run(
            ['npx', '-y', 'tsx', temp_file],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=base_dir
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
    Read the contents of a file from the filesystem. This is a generic filesystem tool
    that allows reading any file, including tool implementations in the agent_filesystem.
    
    Args:
        file_path: Path to the file to read, relative to the project root.
    
    Returns:
        The contents of the file as a string.
    """
    try:
        base_path = os.path.dirname(os.path.dirname(__file__))
        full_path = os.path.join(base_path, file_path)
        
        with open(full_path, 'r') as f:
            content = f.read()
        
        return content
    except FileNotFoundError:
        return f"Error: File not found at path: {file_path}"
    except Exception as e:
        return f"Error reading file: {str(e)}"


@tool
def list_directory(dir_path: str = ".") -> str:
    """
    List the contents of a directory in the filesystem. This helps discover available
    tools and files in the agent_filesystem structure.
    
    Args:
        dir_path: Path to the directory to list, relative to the project root.
    
    Returns:
        A formatted list of files and directories.
    """
    try:
        base_path = os.path.dirname(os.path.dirname(__file__))
        full_path = os.path.join(base_path, dir_path)
        
        items = os.listdir(full_path)
        
        result = f"Contents of {dir_path}:\n"
        for item in sorted(items):
            item_path = os.path.join(full_path, item)
            if os.path.isdir(item_path):
                result += f"  [DIR]  {item}/\n"
            else:
                result += f"  [FILE] {item}\n"
        
        return result
    except FileNotFoundError:
        return f"Error: Directory not found at path: {dir_path}"
    except Exception as e:
        return f"Error listing directory: {str(e)}"
