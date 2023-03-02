from selenium_script import selenium_script_shell
import sys

if __name__ == "__main__":
    arguments = sys.argv
    uc = False
    if "--uc" in arguments:
        uc = True
        arguments.remove("--uc")
    
    starting_script = None
    
    for arg in arguments:
        if arg.startswith("--script="):
            starting_script = arg.replace("--script=", "")
    
    selenium_script_shell(*arguments, name=starting_script,uc=uc)