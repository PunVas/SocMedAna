import requests
import json
import streamlit as st
# Load environment variables
load_dotenv()
BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "fa896a7b-dc3e-44f3-92ed-0c8ae4ca55cd"
FLOW_ID = "81a3643c-a3cc-4538-be28-3503515fc62d"
APPLICATION_TOKEN = "AstraCS:QIOIhpArKNjwaArImSMMhTBH:c44d2ec0177f40c6dc8eacff2fcde2316203ec6cb6daa2557b914ffbaccfecf5"
ENDPOINT = "analysis"

# Function to run the flow
def run_flow(message: str) -> dict:
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"
    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }
    headers = {"Authorization": "Bearer " + APPLICATION_TOKEN, "Content-Type": "application/json"}
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

# Main function
def main():
    st.title("Social Media Performance Analysis")

    # Initialize session state for chat history
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # Input field for the user
    message = st.text_area("", placeholder="How can we assist you today?")

    # Button to send the query
    if st.button("Generate Insights"):
        if not message.strip():
            st.error("Please enter a message")
            return

        try:
            with st.spinner("Running flow..."):
                response = run_flow(message)
                response_text = response["outputs"][0]["outputs"][0]["results"]["message"]["text"]

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
