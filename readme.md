# LLMAPI Project

**LLMAPI** is a versatile API integration platform designed to simplify interaction with various large language models (LLMs). This project supports several popular LLMs, including **Claude**, **Gemini**, **Llama**, and **OpenAI** models, providing a flexible interface for chatbot applications, AI-based responses, and multi-chat functionality.

## Features

- **Claude Integration**: Interact with the Claude AI via the **Anthropic API** to generate responses using the `claude-3-haiku-latest` model.
- **Gemini Integration**: Leverage Google's **Gemini API** to generate content using the `gemini-1.5-flash` model.
- **Llama Integration**: Connect to the **Llama** model with fallback options (use `llama3.2` if `llama3.1` is unavailable).
- **OpenAI Integration**: Seamlessly interact with OpenAI models like `gpt-4o-mini` for AI-powered conversations.
- **Multi-Chat**: A multi-chat feature allows continuous conversations with the models, including the option to change models dynamically when necessary.

## Setup & Installation

### Prerequisites

- Python 3.6 or higher
- `pip` for installing dependencies

### Installation Steps

1. **Clone the repository**:

   ```
   bashCopy codegit clone https://github.com/Formyselfonly/LLMAPI.git
   cd LLMAPI
   ```

2. **Install dependencies**:

   ```
   bash
   
   
   Copy code
   pip install -r requirements.txt
   ```

3. **Create a `.env` file**: Inside your project directory, create a `.env` file to store your API keys. Here’s an example format for the `.env` file:

   ```
   makefileCopy codeANTHROPIC_API_KEY=your_anthropic_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. **Run the appropriate API call**:

   - To interact with **Claude**, use `claude_api_call.py`.
   - For **Gemini**, use `gemini_api_call.py`.
   - For **Llama**, use `llama_api_call.py`.
   - For **OpenAI**, use `openai_api_call.py`.

5. **Run the multi-chat function**: To start a multi-chat session, run the following script:

   ```
   bash
   
   
   Copy code
   python chatbot_openai.py
   ```

   This script will allow you to chat with the OpenAI model in a continuous loop. Simply type your message, and the assistant will respond. Type "exit" to end the conversation.

## Code Breakdown

### `claude_api_call.py`

- This script integrates with the **Anthropic Claude** API to generate responses.
- The `claude-3-haiku-latest` model is used by default for generating AI responses.

### `gemini_api_call.py`

- Connects to **Google Gemini** and uses the `gemini-1.5-flash` model to generate content based on the prompt provided.

### `chatbot_llama.py`

- Implements a chatbot using the **Llama** model, which is hosted locally at `http://localhost:11434/api/chat`.
- If the `llama3.1` model is not found, the script will automatically switch to `llama3.2`.

### `chatbot_openai.py`

- Implements a chatbot using **OpenAI's GPT models**.
- This script sets up a multi-chat session where the assistant's responses are continuously added to the conversation context.

### `openai_api_call.py`

- Allows you to generate responses using **OpenAI's GPT models** by providing user input.
- You can interact with OpenAI’s models directly via this script.

## Usage

1. **Starting a chatbot session**:
   - To use the multi-chat feature, run `python chatbot_openai.py` or any other chatbot script (`chatbot_llama.py`, etc.) based on your choice of model.
   - Type your message in the console, and the assistant will respond accordingly.
   - Use "exit" to terminate the conversation.
2. **Generate single responses**:
   - For a one-time query, you can run the respective API call script (`claude_api_call.py`, `gemini_api_call.py`, `openai_api_call.py`, etc.) with your input in the `user_input` variable.
3. **Model Fallback**:
   - If `llama3.1` is unavailable, the Llama chatbot (`chatbot_llama.py`) will automatically use `llama3.2` as a fallback model.

## Contributing

Feel free to fork this repository and create a pull request with any improvements, bug fixes, or additional features. We welcome contributions from the community.

### Issues & Support

For any issues or bugs, please raise a GitHub issue. You can also reach out via the **Discussions** section for any questions or feedback.