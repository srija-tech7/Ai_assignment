from fake_mcp_sdk import MCPServer
from educhain_content_gen import generate_mcqs, generate_lesson_plan

server = MCPServer()

@server.tool("generate_mcqs")
def mcq_tool(topic: str):
    return generate_mcqs(topic)

@server.resource("lesson_plan")
def lesson_plan_resource(subject: str):
    return generate_lesson_plan(subject)

@server.tool("flashcards")
def flashcard_tool(subject: str):
    return [
        {"term": "Loop", "definition": "A programming structure that repeats code."},
        {"term": "Variable", "definition": "A storage placeholder for values."}
    ]

if __name__ == "__main__":
    print("🚀 MCP server is launching on http://localhost:5000 ...")
    server.run()