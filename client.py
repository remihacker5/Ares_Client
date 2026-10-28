# notes:
# create documentation for the client.py file
# create a tools handler for the tools that the AI can use
# create a Prompt folder for AI prompts
# create a skill folder for AI skills
# workspace folder?

# set up variables and configuration.
# Define System prompts
# start the conversation loop
    # Get user input
    # Add user input to context
    # Send system prompt and context to AI server
    # get response
    # if prompt contains tool call:
        # identify tool call
        # validate tool call
        # Request permission from user
        # Execute Tool call
    # if prompt contains command:
        # identify command
        # execute command
########################################################

'''General program structure:
Get Variables and librarys
Verify workspace
Verify application file integrity

While Program running:
          scheduler_check()
          get prompt input()
          if prompt has /
                    check for command and execute
          else:
                    send prompt to AI
                    if AI response has tool call
                              set prompt_has_tool true
                    While prompt_has_tool
                              Validate tool call
                              Execute tool call
                              if tool call returns more instructions
                                        Add instructions to context
                                        send prompt + context to AI
                                        set prompt_has_tool true
                              else
                                        Set prompt_has_tool false

                    strip og response of tool call json
                    print response'''


from ollama import Client
import tools
import os
from dotenv import load_dotenv

# Keep the main loop running until the user exits.
ProgramRunning = True

# Load local environment variables for the Ollama server.
load_dotenv()
endpoint = (
    os.getenv("OLLAMA_HOST")
    or os.getenv("OPENAI_ENDPOINT")
    or "http://localhost:11434"
)
if endpoint.rstrip("/").endswith("/v1"):
    endpoint = endpoint.rstrip("/")[:-3]
api_key = os.getenv("OLLAMA_API_KEY") or os.getenv("OPENAI_API_KEY")

# Keep the API key optional for local servers that do not require authentication.
headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
ollama_client = Client(host=endpoint, headers=headers)

# Fetch available models from the configured Ollama-compatible server.
models_page = ollama_client.list()

# Model name used for chat completions.
model = "gemma4:12b"

# Conversation memory. This keeps the prior chat context between prompts.
context = ""

# Load the default system prompt used to steer the model's behavior.
with open('prompts/default_sys_prompt.md', 'r', encoding='utf-8') as prompt_file:
    system_prompt = prompt_file.read()

def get_response(prompt):
    response = ollama_client.chat(
        model=model,
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': context + prompt},
        ],
        options={"num_predict": 10096},
        stream=True,
    )
    return response

def stream_response(response):
    content = []
    for chunk in response:
        text = chunk.message.content or ''
        content.append(text)
        print(text, end='', flush=True)
    print()
    return ''.join(content)

# Chat loop.
while ProgramRunning:

    # Get prompt from user
    prompt = input("> ")


    # check for commands
    if (prompt == "/help"):
        print('''\nAvailable commands:\n
        /help - See all available commands.\n
        /models - List all available models\n
        /clear - Clear AI context (New Chat)\n
        /context - Show current context\n
        /exit - Exit Ares client.''')   
    elif (prompt == "/models"):
        # Print the name of each available model
        print("Available local models:")
        for available_model in models_page.models:
            print(f"- {available_model.model}")
    elif (prompt == "/clear"):
        # Reset the conversation memory so the model starts fresh.
        context = ""
        print("\nContext cleared!\n")
        
    elif (prompt == "/context"):
        # Print the current conversation memory.
        print("\nCurrent context:\n")
        print(context)
    elif (prompt == "/exit"):
        # Gracefully quit the client loop.
        print("See ya!")
        ProgramRunning = False


    # If the input is not a command, send it to the model and print the reply.
    else:
        response_text = stream_response(get_response(prompt))

        while tools.validate_tool_call(response_text):
            tool_resp = tools.execute_tool_call(response_text)
            if isinstance(tool_resp, str):
                context = context + prompt + ";\n\n" + response_text + ";\n\n" + tool_resp
                response_text = stream_response(get_response(""))
            else:
                break

        # Store the history so the model can keep context across turns.
        context = context + prompt + ";\n\n" + response_text + ";\n\n"
        