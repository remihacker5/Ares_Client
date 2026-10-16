from openai import OpenAI
ProgramRunning = True


openai = OpenAI(
    base_url="http://elytra.zone:11434/v1",
    api_key="72326e10c2dc53610c02a3058093be68582c5587",  # Required by the SDK, but unused by local server
)
model = "gemma3:12b"
history = ""
# --------------
# BASIC API CALL
# --------------
system_prompt = '''List of tools for you to use: New_note(title, content) and Calendar_add_event(title, content, start_time, end_time)
\n If the user makes a request that matches these tools, follow these steps:\n
1. Ask the user for permission to use the tool. you only need to do this once
2. if they reply with yes, replace the arguments within the tool with the coresponding information as requested by the user.
3. Use the tool by replying with the tool call by itself. The tool handeler will execute your tool call when it is seen in your response.
4. Give the user a confirmation that the tool was executed.'''


models_page = openai.models.list()

response = openai.chat.completions.create(
            model=model,
            messages=[{'role': 'system', 'content': system_prompt}]
        )


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
        history == ""
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
        