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


from openai import OpenAI
import tools
import os
from dotenv import load_dotenv

# Keep the main loop running until the user exits.
ProgramRunning = True

# Load local environment variables such as OPENAI_ENDPOINT and OPENAI_API_KEY.
load_dotenv()
endpoint = os.getenv("OPENAI_ENDPOINT")
api_key = os.getenv("OPENAI_API_KEY")

# Create the OpenAI client pointed at the configured local endpoint.
# The API key may be required by the SDK even when the local server ignores it.
openai = OpenAI(
    base_url=endpoint,
    api_key=api_key,
)

# Fetch the list of available models from the local OpenAI-compatible server.
models_page = openai.models.list()

# Model name used for chat completions.
model = "gemma4:12b"

# Conversation memory. This keeps the prior chat context between prompts.
context = ""

msg_has_tool = False

# Load the default system prompt used to steer the model's behavior.
with open('prompts/default_sys_prompt.md', 'r', encoding='utf-8') as prompt_file:
    system_prompt = prompt_file.read()



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
        # Print the name of each model
        print("Available local models:")
        for model in models_page.data:
            print(f"- {model.id}")
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
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': context + prompt}
            ]
        )

                                        
        if tools.validate_tool_call(response.choices[0].message.content):
            msg_has_tool = True
        
        while msg_has_tool:
            tool_resp = tools.execute_tool_call(response.choices[0].message.content)
            if isinstance(tool_resp, str):
                        context = context + prompt + ";\n\n" + response.choices[0].message.content + ";\n\n" + tool_resp
                        response = openai.chat.completions.create(
                        model=model,
                        messages=[
                        {'role': 'system', 'content': system_prompt},
                        {'role': 'user', 'content': context}
                        ])
                        
                        if tools.validate_tool_call(response.choices[0].message.content):
                            continue
                        else:
                            msg_has_tool = False
            else:
                msg_has_tool = False


        # Store the history so the model can keep context across turns.
        context = context + prompt + ";\n\n" + response.choices[0].message.content + ";\n\n"

        # Print the assistant's response to the terminal.
        print(response.choices[0].message.content)
        