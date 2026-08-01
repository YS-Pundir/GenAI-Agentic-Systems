# server.py — The MasaiMato Restaurant MCP Server
from  fastmcp import FastMCP

# 1. Initialize the server
mcp = FastMCP("MasaiMato")

# 2. Simple In-Memory Data
MENU = {"Masala Dosa": 80, "Idli": 60, "Coffee": 30, "Vada Pav": 25}
ORDERS = {}
NEXT_ID = 1001

# 3. Define Tools
@mcp.tool()
def get_menu() -> dict:
    """Returns the menu items and prices in INR."""
    return MENU

@mcp.tool()
def place_order(item: str, quantity: int, name: str) -> str:
    """Places a food order and returns the status and order ID."""
    global NEXT_ID
    item = item.title()
    
    if item not in MENU:
        return f"Error: '{item}' is not on the menu."
        
    total = MENU[item] * quantity
    order_id = f"MM{NEXT_ID}"
    NEXT_ID += 1
    
    ORDERS[order_id] = {"item": item, "qty": quantity, "name": name, "total": total}
    return f"Success! Order {order_id} placed for {name}. Total: ₹{total}"

if __name__ == "__main__":
    # Update the runner to use the SSE transport on port 8000
    # This allows the client's HTTP "server_url" to successfully connect!
    mcp.run(transport="sse", port=8000)