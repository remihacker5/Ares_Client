import json

available_tools = {"create_note",
                   "edit_note",
                   "get_note",
                   "delete_note"
    # Add more tools here as needed
}

def validate_tool_call(raw_json_string):
    try:
        # 1. Check if the string is valid JSON syntax
        data = json.loads(raw_json_string)
    except json.JSONDecodeError:
        return False, "Error: Invalid JSON syntax"

     # 2. Verify top-level structure
    if "tool_name" not in data or "arguments" not in data:
        return False, "Error: Missing 'tool_name' or 'arguments' container"

    # 3. Validate tool_name and arguments
    if data["tool_name"] not in available_tools:
        return False, f"Error: Tool '{data['tool_name']}' is not available"
    else:
        if data["tool_name"] == "create_note":
            if "title" not in data["arguments"] or "content" not in data["arguments"]:
                return False, "Error: Missing 'title' or 'content' for create_note"
        elif data["tool_name"] == "edit_note":
            if "old_note_name" not in data["arguments"] or "new_content" not in data["arguments"] or "new_note_name" not in data["arguments"]:
                return False, "Error: Missing required arguments for edit_note"
        elif data["tool_name"] == "get_note":
            if "note_name" not in data["arguments"] and "content" not in data["arguments"]:
                return False, "Error: Missing 'note_name' or 'content' for get_note"
        elif data["tool_name"] == "delete_note":
            if "note_name" not in data["arguments"]:
                return False, "Error: Missing 'note_name' for delete_note"

    # If all checks pass
    return True, data

