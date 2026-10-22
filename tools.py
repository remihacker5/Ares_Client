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
    prompt = strip_json(raw_prompt)
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
        execute_tool(prompt)
    except:
        print("Error: Failed to execute tool call.")
    

def strip_json(text):
    text = text.strip()
    
    if text.startswith("```json"):
        newline = text.find("\n")
        text = text[newline + 1:] if newline != -1 else text[7:]
    text = text.rstrip()
    
    if text.startswith("```"):
        newline = text.find("\n")
        text = text[newline + 1:] if newline != -1 else text[3:]
    text = text.rstrip()
    
    if text.endswith("```"):
        text = text[:-3]
    return text.strip()

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
            print("[validate] Checking create_note arguments.")
            if "arg1" not in data["arguments"] or "arg2" not in data["arguments"]:
                print("[validate] create_note is missing required arguments.")
                return False, "Error: Missing required arguments for create_note"
            if not isinstance(data["arguments"]["arg1"], str) or not isinstance(data["arguments"]["arg2"], str):
                print("[validate] create_note arguments must be strings.")
                return False, "Error: Arguments for create_note must be strings"
        elif data["tool_name"] == "edit_note":
            print("[validate] Checking edit_note arguments.")
            if "arg1" not in data["arguments"] or "arg2" not in data["arguments"] or "arg3" not in data["arguments"]:
                print("[validate] edit_note is missing required arguments.")
                return False, "Error: Missing required arguments for edit_note"
            print("[validate] edit_note arguments are valid.")
        elif data["tool_name"] == "get_note":
            print("[validate] Checking get_note arguments.")
            if "arg1" not in data["arguments"] and "arg2" not in data["arguments"]:
                print("[validate] get_note is missing 'arg1' or 'arg2'.")
                return False, "Error: Missing 'arg1' or 'arg2' for get_note"
            print("[validate] get_note arguments are valid.")
        elif data["tool_name"] == "delete_note":
            print("[validate] Checking delete_note arguments.")
            if "arg1" not in data["arguments"]:
                print("[validate] delete_note is missing 'arg1'.")
                return False, "Error: Missing 'arg1' for delete_note"
            print("[validate] delete_note arguments are valid.")

    # If all checks pass
    print(f"[validate] Tool call is valid!")
    
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
            return file.read()
        
    elif data["tool_name"] == "delete_note":
        os.remove(f'workspace/notes/{data["arguments"]["arg1"]}.txt')
