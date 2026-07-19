# client.py — A simplified AI Client connecting to the MCP Server
import os
from openai import OpenAI
from dotenv import load_dotenv

# 1. Load API Key
load_dotenv()
if not os.getenv("api_key"):
    raise ValueError("Please set GROQ_API_KEY in your .env file.")

def run_agent(user_query):
    # 2. Initialize the client
    client = OpenAI(
    api_key=os.getenv("api_key"),
    base_url="https://api.groq.com/openai/v1"
)
    
    print(f"🗣️  Customer: {user_query}")
    print("🔌 Connecting to MasaiMato MCP Server...")
    print("🤖 Agent is thinking and executing tools automatically...\n")
    
    # 3. The Responses API completely abstracts the manual while-loop.
    # It handles tool discovery, execution, and LLM handoffs natively.
    response = client.responses.create(
        model="llama-3.3-70b-versatile", 
        input=[
            {
                "role": "system",
                "content": (
                    "You are MasaiMato, a helpful restaurant assistant. "
                    "Use tools to check the menu and place orders. "
                    "Do not invent prices, dishes, or order IDs."
                )
            },
            {
                "role": "user", 
                "content": user_query
            }
        ],
        tools=[
            {
                # Natively integrate the MCP Server
                "type": "mcp",
                "server_label": "MasaiMato",
                # Point this to your active MCP server endpoint (e.g., SSE or HTTP tunnel)
                "server_url": "http://127.0.0.1:8000/sse"
            }
        ]
    )
    
    # 4. Print the final grounded answer
    print("✅ FINAL ANSWER:")
    print(response.output_text)

if __name__ == "__main__":
    # Test Query
    query = "Check the menu and order 2 Vada Pav for Rahul. Give me the total and order ID."
    run_agent(query)