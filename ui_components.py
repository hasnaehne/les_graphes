# Update the OpenAI API key check in the sidebar function
def sidebar():
    """Create and manage the sidebar elements"""
    # ... (previous code remains the same until API Key input section)

    # API Key input
    st.sidebar.header("Mistral AI Integration")
    api_key = st.sidebar.text_input("Mistral API Key", type="password")
    if api_key:
        st.sidebar.success("API Key set!")
    
    # Add the key to environment variables
    if api_key:
        import os
        os.environ["MISTRAL_API_KEY"] = api_key

    # ... (rest of the function remains the same)