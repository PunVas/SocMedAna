import requests
import json
import streamlit as st

# Hardcoded credentials
BASE_API_URL = "https://api.groq.ai/v1/query"  # Modify with Groq's endpoint
APPLICATION_TOKEN = "AstraCS:QIOIhpArKNjwaArImSMMhTBH:c44d2ec0177f40c6dc8eacff2fcde2316203ec6cb6daa2557b914ffbaccfecf5"  # Hardcoded token

# Function to run the flow with Groq AI
def run_flow(message: str) -> dict:
    api_url = BASE_API_URL  # Groq AI API endpoint
    payload = {
        "query": message,  # Adjust the payload if Groq AI uses different parameters
    }
    headers = {
        "Authorization": "Bearer " + APPLICATION_TOKEN,
        "Content-Type": "application/json"
    }
    
    try:
        # Sending the POST request to the Groq API
        response = requests.post(api_url, json=payload, headers=headers)
        # Check if the response is successful
        response.raise_for_status()  # Will raise an exception for 4xx or 5xx errors
        return response.json()  # Assuming Groq returns a JSON response
    except requests.exceptions.RequestException as e:
        # Handle any exception that occurs during the request
        return {"error": str(e)}

# Main function for Streamlit interface
def main():
    st.title("Social Media Performance Analysis")

    # Initialize session state for chat history
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # Input field for the user
    message = st.text_area("Your Message", placeholder="How can we assist you today?")

    # Button to send the query
    if st.button("Generate Insights"):
        if not message.strip():
            st.error("Please enter a message")
            return

        try:
            with st.spinner("Running flow..."):
                response = run_flow(message)
                # Check for any error in the response
                if 'error' in response:
                    st.error(f"Error: {response['error']}")
                else:
                    response_text = response.get("response", "No response received.")  # Adjust based on Groq's response format

            # Append user message and response to chat history
            st.session_state["messages"].append({"user": message, "bot": response_text})

        except Exception as e:
            st.error(str(e))

    # Display chat history
    st.subheader("Chat History")
    for chat in st.session_state["messages"]:
        st.markdown(f"**You:** {chat['user']}")
        st.markdown(f"**Bot:** {chat['bot']}")
        st.divider()  # Adds a divider for better readability

if __name__ == "__main__":
    main()
