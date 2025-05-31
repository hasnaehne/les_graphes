import streamlit as st
import os
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

def setup_mistral():
    """Set up the Mistral AI client with the API key from environment"""
    api_key = os.getenv("MISTRAL_API_KEY")
    if api_key:
        return MistralClient(api_key=api_key)
    else:
        st.warning("Mistral API key is not set. Please set the MISTRAL_API_KEY environment variable.")
        return None

def get_explanation(algorithm, step_data, level="beginner"):
    """
    Get a detailed explanation of a specific algorithm step from Mistral
    """
    client = setup_mistral()
    if not client:
        return "Mistral integration not available. Please set your Mistral API key."
    
    # Prepare prompt based on algorithm and step
    visited = step_data.get('visited', [])
    current = step_data.get('current')
    
    if algorithm == "DFS":
        stack = step_data.get('stack', [])
        data_structure_state = f"Stack: {stack}"
    else:  # BFS
        queue = step_data.get('queue', [])
        data_structure_state = f"Queue: {queue}"
    
    edges = step_data.get('edges', [])
    
    prompt = f"""
    Explain the following step of the {algorithm} algorithm to a {level} student:
    
    Current node: {current if current is not None else 'None'}
    Visited nodes so far: {visited}
    {data_structure_state}
    Edges being added in this step: {edges}
    
    Please explain:
    1. What's happening in this step
    2. Why it's happening
    3. How this relates to the {algorithm} algorithm principles
    """
    
    try:
        messages = [
            ChatMessage(role="system", content="You are a helpful tutor explaining graph algorithms."),
            ChatMessage(role="user", content=prompt)
        ]
        
        response = client.chat(
            model="mistral-tiny",
            messages=messages
        )
        return response.messages[0].content.strip()
    except Exception as e:
        return f"Error getting explanation: {str(e)}"

def get_hint(question, algorithm, level="beginner"):
    """
    Get a hint for a student's question about the algorithm
    """
    client = setup_mistral()
    if not client:
        return "Mistral integration not available. Please set your Mistral API key."
    
    prompt = f"""
    A {level} student learning about the {algorithm} algorithm asks:
    
    "{question}"
    
    Give a helpful hint that guides them towards understanding without giving away the complete answer.
    Explain the concept in a way that's appropriate for their expertise level.
    """
    
    try:
        messages = [
            ChatMessage(role="system", content="You are a helpful tutor explaining graph algorithms."),
            ChatMessage(role="user", content=prompt)
        ]
        
        response = client.chat(
            model="mistral-tiny",
            messages=messages
        )
        return response.messages[0].content.strip()
    except Exception as e:
        return f"Error getting hint: {str(e)}"

def get_chat_response(messages, algorithm):
    """
    Get a chat response from Mistral based on conversation history
    """
    client = setup_mistral()
    if not client:
        return "Mistral integration not available. Please set your Mistral API key."
    
    # Convert messages to Mistral format
    mistral_messages = [
        ChatMessage(role=msg["role"], content=msg["content"])
        for msg in messages
    ]
    
    # Add system message
    system_message = f"""
    You are an intelligent tutoring system specializing in graph algorithms, particularly {algorithm}.
    Your goal is to help students understand the algorithm through conversation.
    
    - Explain concepts clearly and concisely
    - Use analogies when helpful
    - If asked about code, provide Python examples
    - If the student is confused, try different approaches to explanation
    - Keep responses focused on helping the student learn {algorithm}
    """
    
    mistral_messages.insert(0, ChatMessage(role="system", content=system_message))
    
    try:
        response = client.chat(
            model="mistral-tiny",
            messages=mistral_messages
        )
        return response.messages[0].content.strip()
    except Exception as e:
        return f"Error getting response: {str(e)}"

def evaluate_answer(student_answer, correct_answer, algorithm, context=None):
    """
    Evaluate a student's answer to a question about the algorithm
    """
    client = setup_mistral()
    if not client:
        return {"score": 0, "feedback": "Mistral integration not available. Please set your Mistral API key."}
    
    prompt = f"""
    Evaluate this student's answer about the {algorithm} algorithm.
    
    Question context: {context if context else 'General question about the ' + algorithm + ' algorithm'}
    
    Correct answer: {correct_answer}
    
    Student's answer: {student_answer}
    
    Please provide:
    1. A score from 0-100
    2. Specific feedback about what was correct and what could be improved
    3. A brief explanation of any misconceptions
    
    Format your response as a JSON object with these keys: score, feedback, misconceptions
    """
    
    try:
        messages = [
            ChatMessage(role="system", content="You are a helpful tutor evaluating understanding of graph algorithms."),
            ChatMessage(role="user", content=prompt)
        ]
        
        response = client.chat(
            model="mistral-tiny",
            messages=messages
        )
        
        # Parse the response as JSON
        import json
        try:
            result = json.loads(response.messages[0].content.strip())
            return result
        except:
            # Fallback if response is not valid JSON
            return {
                "score": 50,
                "feedback": response.messages[0].content.strip(),
                "misconceptions": "Unable to parse specific misconceptions."
            }
            
    except Exception as e:
        return {
            "score": 0,
            "feedback": f"Error evaluating answer: {str(e)}",
            "misconceptions": "Unable to evaluate due to an error."
        }