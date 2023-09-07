import toml
import subprocess
from termcolor import colored

def list_poetry_scripts():
    with open("pyproject.toml", "r") as file:
        content = toml.load(file)
        scripts = content.get("tool", {}).get("poetry", {}).get("scripts", {})
        return scripts

def get_script_help(script_name):
    try:
        result = subprocess.run(["poetry", "run", script_name, "--help"], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return e.output
    except Exception as e:
        return str(e)

def main():
    scripts = list_poetry_scripts()
    if scripts:
        # Print a fancy header
        print(colored("======================================", "cyan"))
        print(colored("          AVAILABLE SCRIPTS", "yellow", attrs=["bold"]))
        print(colored("======================================", "cyan"))

        for script_name in scripts.keys():
            # Skip the list-scripts to avoid recursion
            if script_name == "list-scripts":
                continue
            print(colored(f"\n➜ {script_name}:", "green"))
            help_text = get_script_help(script_name)
            print(help_text)
        print(colored("======================================", "cyan"))
    else:
        print(colored("No scripts found in pyproject.toml.", "red"))

if __name__ == "__main__":
    main()
