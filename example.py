import streamlit as st
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

def run_example():
    # Setup Mistral client
    api_key = st.sidebar.text_input("Enter Mistral API Key", type="password")
    if not api_key:
        st.warning("Please enter your Mistral API key to continue")
        return
    
    client = MistralClient(api_key=api_key)
    
    st.title("Graph Algorithm Tutor - Example")
    
    # Algorithm selection
    algorithm = st.radio("Choose Algorithm", ["DFS", "BFS"])
    
    # User question input
    question = st.text_input("Ask a question about the algorithm:")
    
    if question and st.button("Get Answer"):
        try:
            messages = [
                ChatMessage(role="system", content=f"You are a helpful tutor explaining the {algorithm} algorithm."),
                ChatMessage(role="user", content=question)
            ]
            
            response = client.chat(
                model="mistral-tiny",
                messages=messages
            )
            
            st.write("AI Tutor's Response:")
            st.write(response.messages[0].content)
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    # Interactive visualization
    st.header("Algorithm Visualization")
    steps = st.slider("Algorithm Step", 0, 5, 0)
    
    # Example graph visualization (simplified)
    st.write(f"Showing step {steps} of {algorithm} algorithm")
    
    # Get AI explanation of current step
    if st.button("Explain Current Step"):
        try:
            messages = [
                ChatMessage(role="system", content="You are a helpful tutor explaining graph algorithms."),
                ChatMessage(role="user", content=f"Explain step {steps} of {algorithm} algorithm in simple terms.")
            ]
            
            response = client.chat(
                model="mistral-tiny",
                messages=messages
            )
            
            st.write("Step Explanation:")
            st.write(response.messages[0].content)
            
        except Exception as e:
            st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    run_example()