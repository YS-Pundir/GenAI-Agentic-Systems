from typing import TypedDict
from langgraph.graph import StateGraph,START,END
from pydantic import BaseModel, Field
from typing_extensions import Literal
import groq
import matplotlib.pyplot as plt
import networkx as nx
from dotenv import load_dotenv
import streamlit as st
from pathlib import Path
import pandas as pd
project_root=Path(__file__).resolve().parent
chart_loc=project_root/"workflow.png"
database_loc=project_root/"support_tickets.csv"
resolved_tickets_loc=project_root/"resolved_tickets.csv"
load_dotenv()
import os
api_key=os.getenv("api_key")
client=groq.Groq(api_key=api_key)

print("api loaded")

class state(TypedDict):
    ticket_id:int
    description:str
    category:str
    resolution:str



def classify_ticket(state):
  
    description = state.get("description", "").lower()
    
  
    billing_keywords = ["commodo", "consectetur", "invoices"] # mapped for testing
    technical_keywords = ["adipiscing", "dolor", "incididunt"] 
    account_keywords = ["ullamco", "nostrud", "minim"]

    if any(keyword in description for keyword in billing_keywords):
        category="Billing"
    elif any (keyword in description for keyword in technical_keywords):
        category="Technical issue"
    elif  any(keyword in description for keyword in account_keywords):
        category="Account access"
    else:
        category="General Inquiry"

    return {"category":category}



def generate_resolution(state):
    """Generates a proposed resolution based on the ticket's category."""
    # TODO: implement the resolution lookup table.
    # Must return a dict with a "resolution" key.
    category=state["category"]

    if category=="Billing":
        return {"resolution":"Our technical team will run a diagnostic on your connection within 24 hours."}

    elif category=="Technical issue":
        return{"resolution":"We have flagged this charge for review and will issue a refund within 3-5 business days if applicable."}
     
    elif category=="Account access":
       return {"resolution":"Please reset your password using the link we just sent to your registered email."}
    elif category=="General Inquiry":
        return {"resolution":"Thank you for reaching out; a support representative will respond within one business day."}
    


def run_workflow():
    """Runs classify_ticket -> generate_resolution in sequence, updating
    the shared state at each step (mirrors START -> node -> node -> END)."""

    workflow=StateGraph(state)

    workflow.add_node("classify_ticket",classify_ticket)
    workflow.add_node("generate_resolution",generate_resolution)

    workflow.add_edge(START,"classify_ticket")
    workflow.add_edge("classify_ticket","generate_resolution")
    workflow.add_edge("generate_resolution",END)

    return workflow.compile()

def main():
    processed_rows=[]
    app=run_workflow()
    


    df=pd.read_csv(database_loc)
    for index,row in df.iterrows():
        initial_state = {
                "ticket_id": str(row["ticket_id"]),
                "description": row["description"],
                "category": "",
                "resolution": ""
            }
            
        final_state = app.invoke(initial_state)
        processed_rows.append(final_state)

    resolved=pd.DataFrame(processed_rows)
    resolved.to_csv(resolved_tickets_loc,index=False)
                                                                

    
    


if __name__ == "__main__":
    main()
