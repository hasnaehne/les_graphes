import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from io import BytesIO
import base64
import os

from graph_utils import create_sample_graph, visualize_graph, get_node_colors, add_node_to_graph, add_edge_to_graph
from algorithms import dfs_algorithm, bfs_algorithm, get_algorithm_properties
from llm_integration import get_explanation, get_hint, get_chat_response
from tutorials import get_tutorial_content, get_exercise, get_algorithm_quiz, get_comparison_content

def sidebar():
    """Create and manage the sidebar elements"""
    st.sidebar.title("Graph Algorithm Tutor")
    
    # Algorithm selection
    st.sidebar.header("Algorithm Settings")
    algorithm = st.sidebar.radio("Select Algorithm", ["DFS", "BFS"])
    
    # Update session state
    if algorithm != st.session_state.algorithm:
        st.session_state.algorithm = algorithm
        st.session_state.algorithm_steps = []
        st.session_state.current_step = 0
    
    # User level selection
    user_level = st.sidebar.select_slider(
        "Your Knowledge Level",
        options=["Beginner", "Intermediate", "Advanced"],
        value="Beginner"
    )
    
    # Graph options
    st.sidebar.header("Graph Settings")
    
    if st.sidebar.button("Generate New Graph"):
        num_nodes = st.sidebar.number_input("Number of Nodes", min_value=3, max_value=10, value=6)
        edge_probability = st.sidebar.slider("Edge Density", min_value=0.1, max_value=0.9, value=0.4, step=0.1)
        directed = st.sidebar.checkbox("Directed Graph", value=False)
        
        # Create new graph
        st.session_state.graph = create_sample_graph(
            num_nodes=num_nodes,
            edge_probability=edge_probability,
            directed=directed
        )
        st.session_state.algorithm_steps = []
        st.session_state.current_step = 0
        st.session_state.start_node = 0
    
    # Display algorithm properties
    st.sidebar.header("Algorithm Properties")
    properties = get_algorithm_properties()[algorithm]
    
    st.sidebar.markdown(f"**{properties['full_name']}**")
    st.sidebar.markdown(f"- Uses: {properties['data_structure']}")
    st.sidebar.markdown(f"- Time: {properties['time_complexity']}")
    st.sidebar.markdown(f"- Space: {properties['space_complexity']}")
    
    # API Key input
    st.sidebar.header("Mistral AI Integration")
    api_key = st.sidebar.text_input("Mistral API Key", type="password")
    if api_key:
        st.sidebar.success("API Key set!")
    
    # Add the key to environment variables
    if api_key:
        os.environ["MISTRAL_API_KEY"] = api_key

# Rest of the file remains unchanged
[... rest of the original ui_components.py code ...]