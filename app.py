import streamlit as st
import requests
import json
from typing import Optional

# Constants for API request
BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "04c10269-3dde-497c-b20f-9ecb31f155db"
FLOW_ID = "aed37c10-7ac1-4cf5-9fcd-7c08fb469135"
APPLICATION_TOKEN = "AstraCS:QIOIhpArKNjwaArImSMMhTBH:c44d2ec0177f40c6dc8eacff2fcde2316203ec6cb6daa2557b914ffbaccfecf5"
ENDPOINT = ""  # You can set a specific endpoint name in the flow settings

# Optional tweaks
TWEAKS = {
    "ChatInput-n0p3k": {},
    "Prompt-qJyGE": {},
    "AstraDBToolComponent-2bEY8": {},
    "Agent-XtCvF": {},
    "ChatOutput-g0GbU": {}
}

def run_flow(message: str,
             endpoint: str,
             output_type: str = "chat",
             input_type: str = "chat",
             tweaks: Optional[dict] = None,
             application_token: Optional[str] = None) -> dict:
    """
    Run a flow with a given message and optional tweaks.

    :param message: The message to send to the flow
    :param endpoint: The ID or the endpoint name of the flow
    :param tweaks: Optional tweaks to customize the flow
    :return: The JSON response from the flow
    """
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{endpoint}"

    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
    }
    headers = None
    if tweaks:
        payload["tweaks"] = tweaks
    if application_token:
        headers = {"Authorization": "Bearer " + application_token, "Content-Type": "application/json"}
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

def main():
    st.title("AI Chatbot")

    # Input text area for user message
    user_message = st.text_area("You: ", "", height=150)

    # Button to send message
    if st.button("Send"):
        if user_message:
            with st.spinner('Getting response from AI...'):
                response = run_flow(
                    message=user_message,
                    endpoint=ENDPOINT or FLOW_ID,
                    output_type="chat",
                    input_type="chat",
                    tweaks=TWEAKS,
                    application_token=APPLICATION_TOKEN
                )

            # Display the AI response
            if 'response' in response:
                ai_message = response['response']
                st.text_area("AI: ", ai_message, height=150, disabled=True)
            else:
                st.error("Error: Could not get a valid response.")
        else:
            st.warning("Please enter a message to send.")

if __name__ == "__main__":
    main()
