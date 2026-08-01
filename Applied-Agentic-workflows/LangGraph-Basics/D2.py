# Srtep 1 = importing the tools
from groq import Groq
from langgraph.graph import state,START,END,StateGraph
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
# Step 2 : Graph state defenation
class State(TypedDict):
    product_name:str
    basic_description:str
    features_benefits:str
    marketing_message:str
    final_description:str


# Step 3: Generate a basic product description
def generate_basic_description(state):
    """Generate a basic description for the product."""
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates brief product descriptions."},
            {"role": "user", "content": f"Write a brief description of a product named '{state['product_name']}'."}
        ]
    )
    basic_description = response.choices[0].message.content
    return {"basic_description": basic_description}

# Step 4: Add key features and benefits to the product description
def add_features_benefits(state: State):
    """Add features and benefits to the product description."""
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": f"List key features and benefits of the product: {state['basic_description']}"}]
    )
    features_benefits = response.choices[0].message.content
    return {"features_benefits": features_benefits}

# Step 5: Create a compelling marketing message based on the product's features
def create_marketing_message(state: State):
    """Create a marketing message for the product."""
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": f"Create a compelling marketing message for the product: {state['features_benefits']}"}]
    )
    marketing_message = response.choices[0].message.content
    return {"marketing_message": marketing_message}

# Step 6: Final polish and completion of the product description
def polish_final_description(state: State):
    """Polish and finalize the product description."""
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": f"Polish and finalize the product description, incorporating the marketing message: {state['marketing_message']}"}]
    )
    final_description = response.choices[0].message.content
    return {"final_description": final_description}

def build_workflow():
    """Build the workflow using the langgraph"""
    workflow=StateGraph(State)

    workflow.add_node("GENERATE BASIC DESCRIPTION",generate_basic_description)
    workflow.add_node("ADD THE FEATURE BENEFITS",add_features_benefits)
    workflow.add_node("CREATE MARKETING MESSAGE",create_marketing_message)
    workflow.add_node("POLISH FINAL DESCRIPTION",polish_final_description)

    workflow.add_edge(START,"GENERATE BASIC DESCRIPTION")
    workflow.add_edge("GENERATE BASIC DESCRIPTION","ADD THE FEATURE BENEFITS")
    workflow.add_edge("ADD THE FEATURE BENEFITS","CREATE MARKETING MESSAGE")
    workflow.add_edge("CREATE MARKETING MESSAGE","POLISH FINAL DESCRIPTION")
    workflow.add_edge("POLISH FINAL DESCRIPTION",END)

    chain = workflow.compile()

    return chain

def visualising_chain():
    graph=nx.DiGraph()
    edges=[("START","GENERATE BASIC DESCRIPTION"),
           ("GENERATE BASIC DESCRIPTION","ADD THE FEATURE BENEFITS"),
           ("ADD THE FEATURE BENEFITS","CREATE MARKETING MESSAGE"),
           ("CREATE MARKETING MESSAGE","POLISH FINAL DESCRIPTION"),
           ("POLISH FINAL DESCRIPTION","END")

           ]
    graph.add_edges_from(edges)

    plt.figure(figsize=(10, 6))
    pos = nx.spring_layout(graph, seed=88)

    nx.draw(graph, pos, with_labels=True, node_color='skyblue', node_size=2500, edge_color='gray', font_size=10, font_weight='bold', arrowsize=20)
    plt.title("Product Description Generation Workflow")
    plot_loc=project_root/"workflow.png"
    plt.savefig(plot_loc)




# Main Streamlit function
def run_streamlit_app():
    """Handles the entire app logic: input, workflow, and output."""

    plot_loc=project_root/"workflow.png"
    # Title for the app
    st.title("Product Description Generator with LangGraph & Groq")

    # Step 1: Take product name as input from the user
    product_name = st.text_input("Enter the product name:", placeholder="e.g., Smart Water Bottle")

    # Step 2: Button to generate product description
    if st.button("Generate Product Description"):
        if not product_name:
            st.warning("Please enter a product name.")
        else:
            with st.spinner("Generating description..."):
                # Create the initial state with product name and empty fields for description steps
                initial_state = {
                    "product_name": product_name, 
                    "basic_description": "", 
                    "features_benefits": "", 
                    "marketing_message": "", 
                    "final_description": ""
                }

                # Build and run the workflow
                chain = build_workflow()

                # Run the workflow and get the results
                result = chain.invoke(initial_state)

                # Display the results in Streamlit
                st.subheader("Basic Description:")
                st.write(result["basic_description"])

                st.subheader("Features and Benefits:")
                st.write(result["features_benefits"])

                st.subheader("Marketing Message:")
                st.write(result["marketing_message"])

                st.subheader("Final Description:")
                st.write(result["final_description"])

                # Step 3: Visualize the workflow and save it as an image
                visualising_chain()
                st.image(plot_loc, caption="Product Description Workflow")

if __name__ == "__main__":
    run_streamlit_app()
