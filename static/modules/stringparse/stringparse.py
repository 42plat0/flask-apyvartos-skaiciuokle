def delete_string_end(string, delete_string):
    target_string = [*string][::-1]
    keys = [*delete_string][::-1]
    
    for i in range(len(keys) + 1):
        try:
            key_target = target_string[0]
            key = keys[0]
        except (IndexError):
            target_string.pop(0) # Pop backslash
            break
        
        if key == key_target:
            target_string.pop(0)
            keys.pop(0)
        
    return "".join((target_string[::-1])) # Unreverse string
