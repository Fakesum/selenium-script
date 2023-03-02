from seleniumbase import SB

__version__ = "0.0.1a"

def _parse_commands(raw_commands, *script_args):
    """
        Parse raw_Commands to include string
    """
    # Parse Arguments and commands
    commands = []
    for command in raw_commands:
        # Split Line into Command and argument
        command, *raw_args = command.split(" ")

        args = []

        is_middle_of_string = False
        new_arg_buffer = ""
        
        for arg in raw_args:
            # If multiple arguments are in a single string
            # they are considered as the same argument

            # If start of string
            if arg.startswith('"') or arg.startswith("'"):
                new_arg_buffer += arg
                is_middle_of_string = True
            
            # If middle of string
            elif is_middle_of_string:
                new_arg_buffer += arg
            
            # If end of string
            elif arg.endswith('"') or arg.endswith("'"):
                is_middle_of_string = False
                new_arg_buffer += arg
                for script_arg in script_args:
                    new_arg_buffer = new_arg_buffer.replace(f"""[[ {script_arg["key"]} ]]""", script_arg["value"])
                args.append(eval(new_arg_buffer))
                new_arg_buffer = ""
            
            # If not part of a string
            else:
                for script_arg in script_args:
                    arg = arg.replace(f"""[[ {script_arg["key"]} ]]""", script_arg["value"])
                args.append(eval(arg))
        
        # store the commands and argument 
        # that are executed later
        commands.append({
            "command": command,
            "args": args
        })
    return commands
def run_selenium_script(*script_args, name: str = None, uc: bool | None = None):
    """
        This function reads a file and executes every command in the sel format,
        for more info check: TODO: Add Selenium Script DOcs line Here.
    """

    assert name != None

    # Read the raw lines of the sel file
    raw_commands = [line.replace("\n", "") for line in open(name).readlines()]

    commands = _parse_commands(raw_commands, *script_args)
    
    with SB(uc=uc) as driver:
        for command in commands:
            if command == 'py_declare_variable':
                exec(command["args"][0] + " = " + command["args"][1])
            eval("driver."+command["command"])(*command["args"])

def selenium_script_shell(*args, name: None | str = None, uc: bool | None = None):
    with SB(uc=uc) as driver:
        if name != None:
            # Read the raw lines of the sel file
            raw_commands = [line.replace("\n", "") for line in open(name).readlines()]

            commands = _parse_commands(raw_commands, *args)
            
            for command in commands:
                if command == 'py_declare_variable':
                    exec(command["args"][0] + " = " + command["args"][1])
                eval("driver."+command["command"])(*command["args"])

        while True:
            try:
                command = _parse_commands(input(">>> "), *args)[0]
            except Exception as e:
                print(e)
                break
            if command == 'py_declare_variable':
                exec(command["args"][0] + " = " + command["args"][1])
            
            if command == "exit":
                break
            eval("driver."+command["command"])(*command["args"])