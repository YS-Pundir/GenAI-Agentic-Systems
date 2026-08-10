from typing import TypedDict

from langgraph.graph import StateGraph,START,END
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

from pydantic import BaseModel, Field
from typing_extensions import Literal

import groq

import matplotlib.pyplot as plt
import networkx as nx
import uuid
import streamlit as st


from concurrent.futures import ThreadPoolExecutor,TimeoutError as FutureTimeoutError
from langgraph.types import RetryPolicy

from dotenv import load_dotenv
from pathlib import Path
project_root=Path(__file__).resolve().parent
chart_loc=project_root/"workflow_conditional.png"

file_loc=project_root/"checkpoints.sqlite"

load_dotenv()
import os
api_key=os.getenv("api_key")
client=groq.Groq(api_key=api_key)



class State(TypedDict):
    input: str  
    decision: str  
    output: str  



def run_with_timeout(fn, seconds):
    with ThreadPoolExecutor() as pool:
        future = pool.submit(fn)
        return future.result(timeout=seconds)

    

# Step 3: Function to determine the story genre using AI
def get_router_response(State) -> str:
    """Uses AI model to categorize input into a specific genre."""
    input_text=State["input"]
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": "Route the input to 'fantasy', 'sci-fi', or 'mystery' based on its theme. If unsure, default to 'mystery'."},
            {"role": "user", "content": input_text},
        ]
    )
    genre = response.choices[0].message.content.strip().lower()
    # A simple way to handle potential variations in the model's output
    if "fantasy" in genre:
        decision= "fantasy"
    elif "sci-fi" in genre or "science fiction" in genre:
        decision = "sci-fi"
    elif "mystery" in genre:
        decision= "mystery"
    else:
        decision= "mystery" # Default case

    return {"decision":decision}

# Step 4: Define story generation functions for each genre
def generate_fantasy_story(state: State):
    def fantasy_llm_call(state):    
        """Creates a fantasy story."""
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "system", "content": "Write a fantasy story based on the input."},
                {"role": "user", "content": state['input']}
            ],
            max_tokens=500
        )
        return response

    try : 
        response=run_with_timeout(lambda:fantasy_llm_call(state),20)
        return {"output": response.choices[0].message.content.strip(), "decision": "fantasy"}
    except FutureTimeoutError:
        return {"output":"The fantasy story generation is taking too long , please try again later :)","decision":"fantasy"}
    



def generate_sci_fi_story(state: State):
    def sci_fi_llm_call(state):
        """Creates a sci-fi story."""
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "system", "content": "Write a sci-fi story based on the input."},
                {"role": "user", "content": state['input']}
            ],
            max_tokens=500
        )
        return response
    try : 
        response=run_with_timeout(lambda:sci_fi_llm_call(state),20)
        return {"output": response.choices[0].message.content.strip(), "decision": "sci-fi"}
    except FutureTimeoutError:
        return {"output":"science fictional story generation taking too long , please try again later :)","decision":"sci-fi"}
    



def generate_mystery_story(state: State):
    def mystery_llm_call(state):
        """Creates a mystery story."""
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "system", "content": "Write a mystery story based on the input."},
                {"role": "user", "content": state['input']}
            ],
            max_tokens=500
        )
        return response
    try :
        response=run_with_timeout(lambda:mystery_llm_call(state),20)
        return  {"output": response.choices[0].message.content.strip(), "decision": "mystery"}
    except FutureTimeoutError:
        return {"output": "mytery genration taking too long ", "decision": "mystery"}




def route_decision(state: State) -> Literal["generate_fantasy_story", "generate_sci_fi_story", "generate_mystery_story"]:
    """Maps the decision to the correct function name."""
    if state["decision"] == "fantasy":
        return "generate_fantasy_story"
    elif state["decision"] == "sci-fi":
        return "generate_sci_fi_story"
    else:
        return "generate_mystery_story"

# Step 6: Build LangGraph workflow
def build_workflow(mamory):

    workflow=StateGraph(State)

    workflow.add_node("route_request",get_router_response,retry_policy=RetryPolicy(
        max_attempts=3,
        max_interval=6,
        backoff_factor=2,
        initial_interval=0.2,
        jitter=False))
    workflow.add_node("generate_fantasy_story",generate_fantasy_story,retry_policy=RetryPolicy(
        max_attempts=3,
        max_interval=6,
        backoff_factor=2,
        initial_interval=0.2,
        jitter=False))
    workflow.add_node("generate_mystery_story",generate_mystery_story,retry_policy=RetryPolicy(
        max_attempts=3,
        max_interval=6,
        backoff_factor=2,
        initial_interval=0.2,
        jitter=False))
    workflow.add_node("generate_sci_fi_story",generate_sci_fi_story,retry_policy=RetryPolicy(
        max_attempts=3,
        max_interval=6,
        backoff_factor=2,
        initial_interval=0.2,
        jitter=False))

    workflow.add_edge(START,"route_request")
    workflow.add_conditional_edges(
        "route_request",
        route_decision,
        {
            "generate_sci_fi_story":"generate_sci_fi_story",
            "generate_mystery_story":"generate_mystery_story",
            "generate_fantasy_story":"generate_fantasy_story"
        }
    )

    workflow.add_edge("generate_fantasy_story",END)
    workflow.add_edge("generate_mystery_story",END)
    workflow.add_edge("generate_sci_fi_story",END)

    return workflow.compile(checkpointer=mamory)

def invoke_with_global_timeout(graph,initial_state,config,seconds):
    with ThreadPoolExecutor() as executor:

        future = executor.submit(
            graph.invoke,
            initial_state,
            config
        )

        return future.result(timeout=seconds)

# Function to visualize the workflow
def visualize_workflow():
    """Visualize and save the workflow as an image."""
    graph = nx.DiGraph()
    edges = [
        ("START", "route_request"),
        ("route_request", "generate_fantasy_story"),
        ("route_request", "generate_sci_fi_story"),
        ("route_request", "generate_mystery_story"),
        ("generate_fantasy_story", "END"),
        ("generate_sci_fi_story", "END"),
        ("generate_mystery_story", "END"),
    ]

    graph.add_edges_from(edges)

    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(graph, seed=42)
    nx.draw(graph, pos, with_labels=True, node_color='lightgreen', node_size=3000, edge_color='gray', font_size=10, font_weight='bold', arrowsize=20)
    plt.title("Conditional Story Generation Workflow")
    plt.savefig(chart_loc)


# Step 7: Implement the Streamlit UI
def run_streamlit_app():
    """Creates an interactive UI for story generation."""
    st.title("Genre-Based Story Generator with Conditional Routing")


    # Initialize SQLite Checkpointer and Thread ID in session state
    if "memory" not in st.session_state:
        # check_same_thread=False is required for Streamlit's threading model
        conn = sqlite3.connect(file_loc, check_same_thread=False)
        st.session_state.memory = SqliteSaver(conn)
        
    st.sidebar.header("Resume Session")
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = str(uuid.uuid4())
        
    # Expose Thread ID so user can copy it, restart app, and paste it to resume
    st.session_state.thread_id = st.sidebar.text_input(
        "Thread ID (Save this to resume later):", 
        value=st.session_state.thread_id
    )

    # Build workflow and config globally so we can check state without generating
    chain = build_workflow(st.session_state.memory)
    config = {"configurable": {"thread_id": st.session_state.thread_id}}

    if st.sidebar.button("Load Saved State"):
        saved_state = chain.get_state(config)
        if saved_state.values:
            st.sidebar.success("Found saved memory!")
            st.sidebar.json(saved_state.values)
        else:
            st.sidebar.warning("No memory found for this Thread ID.")
    
    user_input = st.text_input("Enter your story idea:", placeholder="e.g., A knight discovers a hidden portal...")

    if st.button("Generate Story"):
        if user_input:
            with st.spinner("Analyzing genre and writing story..."):
                workflow = build_workflow(st.session_state.memory)
                try:
                    state = invoke_with_global_timeout(workflow,{"input":user_input},config,40)
                except FutureTimeoutError:
                    st.write("Sorry workflow took to much time , please try again later")
                st.subheader("Detected Genre:")
                st.write(state["decision"].capitalize())
                st.subheader("Generated Story:")
                st.write(state["output"])
                
                # Visualize the workflow and display it
                visualize_workflow()
                st.image(chart_loc, caption="Conditional Workflow Visualization")
        else:
            st.warning("Please enter a story idea.")

if __name__ == "__main__":
    run_streamlit_app()
