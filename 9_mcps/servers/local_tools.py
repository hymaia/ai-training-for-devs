from fastmcp import Context, FastMCP

# from utils import get_make_react_slide_prompt

mcp = FastMCP("Demo 🚀")


@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


@mcp.tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b


@mcp.tool
def python_executor_for_pptx(code: str) -> str:
    """Execute Python code that contains python-pptx or xlsxwritercode"""
    try:
        exec(code)
    except Exception as e:
        return f"Error executing Python code: {e}"
    return "Python code executed successfully"


# Example of sampling usage
# @mcp.tool
# async def analyze_sentiment(text: str, ctx: Context) -> dict:
#     """Analyze the sentiment of text using the client's LLM."""
#     prompt = f"""Analyze the sentiment of the following text as positive, negative, or neutral.
#     Just output a single word - 'positive', 'negative', or 'neutral'.

#     Text to analyze: {text}"""

#     # Request LLM analysis
#     response = await ctx.sample(prompt)

#     # Process the LLM's response
#     sentiment = response.text.strip().lower()

#     # Map to standard sentiment values
#     if "positive" in sentiment:
#         sentiment = "positive"
#     elif "negative" in sentiment:
#         sentiment = "negative"
#     else:
#         sentiment = "neutral"

#     return {"text": text, "sentiment": sentiment}

# Example of prompt usage
# @mcp.prompt
# async def make_react_slide(content: str) -> str:
#     """
#     Prompt to generate a powerpoint type slide using react and html code
#     clear instructions and ideas should be provided to the model to generate the slide be exhaustive and detailed
#     please provide everything needed in the content to generate the slide be exhaustive and detailed
#     """
#     return get_make_react_slide_prompt(content)

if __name__ == "__main__":
    mcp.run()
