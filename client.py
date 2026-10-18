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

from openai import OpenAI
ProgramRunning = True
import os
from dotenv import load_dotenv
load_dotenv()
endpoint = os.getenv("OPENAI_ENDPOINT")
api_key = os.getenv("OPENAI_API_KEY")

openai = OpenAI(
    base_url=endpoint,
    api_key=api_key,  # Required by the SDK, but unused by local server
)
model = "gemma3:12b"
context = ""
system_prompt = open('prompts/default_sys_prompt.md')
models_page = openai.models.list()



# Game loop.
while ProgramRunning:


    cmd = input("> ")

    if (cmd == "/help"):
        print('''\nAvailable commands:\n
        /help - See all available commands.\n
        /models - List all available models\n
        /clear - Clear AI context (New Chat)
        /exit - Exit Ares client.''')   
    elif (cmd == "/models"):
        # Print the name of each model
        print("Available local models:")
        for model in models_page.data:
            print(f"- {model.id}")
    elif (cmd == "/clear"):
        context = ""
        print("\nContext cleared!\n")

    elif (cmd == "/exit"):
        print("See ya!")
        ProgramRunning = False
    else:
        
        response = openai.chat.completions.create(
            model=model,
            messages=[{'role': 'system', 'content': system_prompt},{'role': 'user', 'content': context + cmd}]
        )
        context = context + cmd + ";\n\n" + response.choices[0].message.content + ";\n\n"
        print(response.choices[0].message.content)
        