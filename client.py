# notes:
# create documentation for the client.py file
# create a tools handler for the tools that the AI can use
# create a Prompt folder for AI prompts
# create a skill folder for AI skills
# workspace folder?

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
history = ""
# --------------
# BASIC API CALL
# --------------
system_prompt = ''' These are your instructions:
 
Identity:
Your name is _. you are a personal assistant, and your role is to help the user accomplish their tasks by doing what they request. 
 
Behavior:
You are connected to an AI "harness". What this means is you can make "tool calls", and the "harness" (A program that reads your response) will execute the tool calls you make. You must call the tools exactly as the instructions say, otherwise the tools will fail.
 
Tools:
 
Tool calls should be made in the following format: 
tool_name(arg1, arg2)
 
Each argument should be filled, no more or no less. If you do not have enough information to fill all the arguments, ask the user to clarify. when you Are ready to make the tool call, 
 
List of tools: 
 
Note tools:
create_note(Name, content)
use this tool when the user requests a new note.
 
edit_note(old_name, new_name, new_content)
Use this tool to edit notes. Use the get_note tool if necessary for the old_name and new_content arguments.
 
get_note(name, content)
Use this tool to search for a note by name or content.
 
delete_note(name)
Use this tool when the user requests to delete a specific note.'''


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
        history = ""
        print("\nContext cleared!\n")

    elif (cmd == "/exit"):
        print("See ya!")
        ProgramRunning = False
    else:
        
        response = openai.chat.completions.create(
            model=model,
            messages=[{'role': 'system', 'content': system_prompt},{'role': 'user', 'content': history + cmd}]
        )
        history = history + cmd + ";\n\n" + response.choices[0].message.content + ";\n\n"
        print(response.choices[0].message.content)
        