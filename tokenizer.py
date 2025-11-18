import tiktoken
from langchain_core.tools import Tool
from typing import List

def count_tokens(text: str) -> int:
    """
    Count tokens in a text string using cl100k_base encoding (GPT-4 standard).
    This serves as a good approximation for other models.
    """
    if not text:
        return 0
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))

def estimate_tools_tokens(tools: List[Tool]) -> int:
    """
    Estimate the number of tokens consumed by tool definitions.
    This includes name, description, and argument schema.
    """
    total = 0
    for tool in tools:
        # Estimate based on typical JSON schema representation
        tool_text = f"{tool.name}\n{tool.description}\n"
        if tool.args:
            tool_text += str(tool.args)
        total += count_tokens(tool_text)
        
        # Add overhead for schema formatting (brackets, quotes, etc)
        total += 20 
    return total

