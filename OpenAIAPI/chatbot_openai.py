from openai import OpenAI
import os
import dotenv

# Load the environment variables from a .env file
dotenv.load_dotenv()
# Get the OpenAI API key from the environment
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
# Initialize the OpenAI client with the API key
client = OpenAI(api_key=OPENAI_API_KEY)


# Function for the multi-chat interaction
def multi_chat():
    messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
    while True:
        # Get user input
        user_input = input("User: ")
        # Add user message to the conversation
        messages.append({"role": "user", "content": user_input})
        # Get response from OpenAI
        completion = client.chat.completions.create(
            model="gpt-4o-mini",  # You can change this to any available model
            messages=messages
        )
        # Extract the assistant's response from the completion
        assistant_response = completion.choices[0].message.content
        # Print the assistant's response
        print(f"Assistant: {assistant_response}")
        # Add assistant's response to the conversation
        messages.append({"role": "assistant", "content": assistant_response})

        # Exit the conversation if the user says 'exit'
        if user_input.lower() == "exit":
            print("End of Conversation")
            break


# Start the multi-chat conversation
multi_chat()
