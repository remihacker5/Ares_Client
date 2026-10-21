import json

available_tools = {"create_note",
                   "edit_note",
                   "get_note",
                   "delete_note"
    # Add more tools here as needed
}

def remove_code_fences(text):
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

def check_for_tool_call(prompt):
    prompt = remove_code_fences(prompt)
    try:
        # Attempt to parse the prompt as JSON
        data = json.loads(prompt)
    except json.JSONDecodeError:
        print("[check] Prompt is not valid JSON.")
        return False, "Error: Invalid JSON syntax"

    # Check if the parsed data contains a tool call
    if "tool_name" in data and "arguments" in data:
        print(f"[check] Tool call detected: {data['tool_name']}. Validating...")
        validate_tool_call(prompt)
        return True, data
    else:
        print("[check] Prompt is missing 'tool_name' or 'arguments'.")
        return False, "Error: Missing 'tool_name' or 'arguments' container"

def validate_tool_call(raw_json_string):
    try:
        # 1. Check if the string is valid JSON syntax
        data = json.loads(raw_json_string)
    except json.JSONDecodeError:
        print("[validate] Input is not valid JSON.")
        return False, "Error: Invalid JSON syntax"

     # 2. Verify top-level structure
    if "tool_name" not in data or "arguments" not in data:
        print("[validate] Missing 'tool_name' or 'arguments'.")
        return False, "Error: Missing 'tool_name' or 'arguments' container"

    # 3. Validate tool_name and arguments
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
            print("[validate] Creating note.")
            with open(f'workspace/notes/{data["arguments"]["arg1"]}.txt', 'w') as file:
                file.write(data["arguments"]["arg2"])
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
    print(f"[validate] Tool call is valid: {data['tool_name']}.")
    
    return True, data

