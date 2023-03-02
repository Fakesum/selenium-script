from selenium_script import selenium_script_shell
import sys

if __name__ == "__main__":
    arguments = sys.argv
    uc = False
    test_mode = False
    if "--uc" in arguments:
        uc = True
        arguments.remove("--uc")
    
    if "--test-mode" in arguments:
        arguments.remove("--test-mode")
        test_mode = True
    starting_script = None
    
    for arg in arguments:
        if arg.startswith("--script="):
            starting_script = arg.replace("--script=", "")
    
    selenium_script_shell(*arguments, name=starting_script,uc=uc, test_mode=test_mode)