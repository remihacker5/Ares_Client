import json
import os


# strip json
# validate syntax
# validate tool calls
# execute tool calls

available_tools = {"create_note",
                   "edit_note",
                   "get_note",
                   "delete_note"
    # Add more tools here as needed
}
# main structure for validation
def validate_tool_call(raw_prompt):
    try:
        prompt = strip_json(raw_prompt)
    except ValueError:
        return False
    try:
        check_syntax(prompt)
    except:
        print("Error: Invalid JSON syntax.")
    
    try:
        check_for_tool(prompt)
        return True
    except:
        print("Error: Invalid tool call.")

def execute_tool_call(raw_prompt):
    prompt = strip_json(raw_prompt)
    try:
        return execute_tool(prompt)
    except:
        print("Error: Failed to execute tool call.")
    

def strip_json(text):
    """Return the first valid JSON object or array, excluding surrounding text."""
    decoder = json.JSONDecoder()

    for start, character in enumerate(text):
        if character not in "{[":
            continue
        try:
            _, end = decoder.raw_decode(text, start)
        except json.JSONDecodeError:
            continue
        return text[start:end]

    raise ValueError("No valid JSON object or array found")



def check_syntax(prompt):
    prompt = strip_json(prompt)
    try:
        # Attempt to parse the prompt as JSON
        data = json.loads(prompt)
    except json.JSONDecodeError:
        print("[check] Prompt is not valid JSON.")
        return False, "Error: Invalid JSON syntax"



def check_for_tool(prompt):
    data = json.loads(prompt)
     # 1. Verify top-level structure
    if "tool_name" not in data or "arguments" not in data:
        print("[validate] Missing 'tool_name' or 'arguments'.")
        return False, "Error: Missing 'tool_name' or 'arguments' container"

    # 2. Validate tool_name and arguments
    if data["tool_name"] not in available_tools:
        print(f"[validate] Tool is unavailable: {data['tool_name']}")
        return False, f"Error: Tool '{data['tool_name']}' is not available"
    else:
        if data["tool_name"] == "create_note":
            if "arg1" not in data["arguments"] or "arg2" not in data["arguments"]:
                print("[validate] create_note is missing required arguments.")
                return False, "Error: Missing required arguments for create_note"
            if not isinstance(data["arguments"]["arg1"], str) or not isinstance(data["arguments"]["arg2"], str):
                print("[validate] create_note arguments must be strings.")
                return False, "Error: Arguments for create_note must be strings"
        elif data["tool_name"] == "edit_note":

            if "arg1" not in data["arguments"] or "arg2" not in data["arguments"] or "arg3" not in data["arguments"]:
                print("[validate] edit_note is missing required arguments.")
                return False, "Error: Missing required arguments for edit_note"

        elif data["tool_name"] == "get_note":

            if "arg1" not in data["arguments"]:
                print("[validate] get_note is missing 'arg1'.")
                return False, "Error: Missing 'arg1' for get_note"

        elif data["tool_name"] == "delete_note":

            if "arg1" not in data["arguments"]:
                print("[validate] delete_note is missing 'arg1'.")
                return False, "Error: Missing 'arg1' for delete_note"

    
    return True

def execute_tool(prompt):
    data = json.loads(prompt)
    
    if data["tool_name"] == "create_note":
        with open(f'workspace/notes/{data["arguments"]["arg1"]}.txt', 'w') as file:
            file.write(data["arguments"]["arg2"])
            
    elif data["tool_name"] == "edit_note":
        with open(f'workspace/notes/{data["arguments"]["arg1"]}.txt', 'w') as file:
            file.write(data["arguments"]["arg3"])
        os.rename(f'workspace/notes/{data["arguments"]["arg1"]}.txt', f'workspace/notes/{data["arguments"]["arg2"]}.txt')
        
    elif data["tool_name"] == "get_note":
        with open(f'workspace/notes/{data["arguments"]["arg1"]}.txt', 'r') as file:
            content = file.read()
            print(f"reading {data['arguments']['arg1']}.txt....")
            return "\n\n This is the content of the note from get_note: " + content + "\n\n Ignore previous context on this note, answer the user's request with the provided content."


        
    elif data["tool_name"] == "delete_note":
        os.remove(f'workspace/notes/{data["arguments"]["arg1"]}.txt')
