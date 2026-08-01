from groq import Groq
from langgraph.graph import StateGraph,END,START
import streamlit as st
import matplotlib.pyplot as plt
from typing_extensions import TypedDict
from dotenv import load_dotenv
import networkx as nx
from pathlib import Path
project_root=Path(__file__).resolve().parent
load_dotenv()
import os
api_key=os.getenv("api_key")
client=Groq(api_key=api_key)

class State(TypedDict):
    topic: str
    advertisement: str
    review: str
    tagline: str
    combined_output: str


# Step 3: Generate an advertisement
def generate_advertisement(state: State):
    """Calls Groq API to generate an advertisement related to the given topic."""
    msg = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": "You are a creative AI that writes catchy advertisements."},
            {"role": "user", "content": f"Write a catchy advertisement for a product related to {state['topic']}."}
        ],
        max_tokens=1000
    )
    advertisement = msg.choices[0].message.content.strip()
    return {"advertisement": advertisement}

# Step 4: Generate a product review
def generate_review(state: State):
    """Calls Groq API to generate a detailed product review for the given topic."""
    msg = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that writes detailed product reviews."},
            {"role": "user", "content": f"Write a product review for a product related to {state['topic']}. Include pros and cons."}
        ],
        max_tokens=1000
    )
    review = msg.choices[0].message.content.strip()
    return {"review": review}

# Step 5: Generate a catchy tagline
def generate_tagline(state: State):
    """Calls Groq API to generate a catchy tagline for the given topic."""
    msg = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": "You are a creative AI that generates catchy taglines."},
            {"role": "user", "content": f"Create a short, catchy tagline for a product related to {state['topic']}."}
        ],
        max_tokens=1000
    )
    tagline = msg.choices[0].message.content.strip()
    return {"tagline": tagline}

# Step 4: Combine all generated outputs
def combine_outputs(state: State):
    """Combines the advertisement, review, and tagline into a single structured output."""
    combined = f"Creative Output for {state['topic']}:\n\n"
    combined += f"ADVERTISEMENT:\n{state['advertisement']}\n\n"
    combined += f"REVIEW:\n{state['review']}\n\n"
    combined += f"TAGLINE:\n{state['tagline']}"
    return {"combined_output": combined}

def build_workflow():
    workflow=StateGraph(State)

    workflow.add_node("generate_advertisement",generate_advertisement)
    workflow.add_node("generate_review",generate_review)
    workflow.add_node("generate_tagline",generate_tagline)
    workflow.add_node("combine_outputs",combine_outputs)

    workflow.add_edge(START,"generate_advertisement")
    workflow.add_edge(START,"generate_review")
    workflow.add_edge(START,"generate_tagline")
    workflow.add_edge("generate_advertisement","combine_outputs")
    workflow.add_edge("generate_review","combine_outputs")
    workflow.add_edge("generate_tagline","combine_outputs")
    workflow.add_edge("combine_outputs",END)

    parallel_workflow = workflow.compile()
    return parallel_workflow

# Step 6: Streamlit UI to trigger workflow
def run_streamlit_app():
    """Handles Streamlit UI interactions and workflow execution."""
    st.title("Creative Content Generator with Parallel Execution")
    topic = st.text_input("Enter the topic:", placeholder="e.g., Electric Bicycles")
    if st.button("Generate Content"):
        if not topic:
            st.warning("Please enter a topic.")
        else:
            with st.spinner("Generating creative content..."):
                parallel_workflow = build_workflow()
                state = parallel_workflow.invoke({"topic": topic})
                st.subheader("Combined Creative Output:")
                st.write(state["combined_output"])


def visualising_chain():
    graph=nx.DiGraph()
    edges=[("START","generate_advertisement"),
        ("START","generate_review"),
        ("START","generate_tagline"),
        ("generate_advertisement","combine_outputs"),
        ("generate_review","combine_outputs"),
        ("generate_tagline","combine_outputs"),
        ("combine_outputs","END"),

           ]
    graph.add_edges_from(edges)

    plt.figure(figsize=(10, 6))
    pos = nx.spring_layout(graph, seed=88)

    nx.draw(graph, pos, with_labels=True, node_color='skyblue', node_size=2500, edge_color='gray', font_size=10, font_weight='bold', arrowsize=20)
    plt.title("Product Description Generation Workflow")
    plot_loc=project_root/"workflow3.png"
    plt.savefig(plot_loc)
visualising_chain()
if __name__ == "__main__":
    run_streamlit_app()
