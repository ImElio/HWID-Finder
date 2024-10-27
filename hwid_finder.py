import subprocess
import pyperclip
import requests
from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text
from rich.align import Align

def rainbow_text(text):
    colors = ["red", "yellow", "green", "cyan", "blue", "magenta"]
    rainbow = Text()
    for i, char in enumerate(text):
        color = colors[i % len(colors)]
        rainbow.append(char, style=color)
    return rainbow

def display_banner():
    banner = r"""
   /$$   /$$ /$$      /$$ /$$$$$$ /$$$$$$$        /$$$$$$$$ /$$$$$$ /$$   /$$ /$$$$$$$  /$$$$$$$$ /$$$$$$$
   | $$  | $$| $$  /$ | $$|_  $$_/| $$__  $$      | $$_____/|_  $$_/| $$$ | $$| $$__  $$| $$_____/| $$__  $$
   | $$  | $$| $$ /$$$| $$  | $$  | $$  \ $$      | $$        | $$  | $$$$| $$| $$  \ $$| $$      | $$  \ $$
   | $$$$$$$$| $$/$$ $$ $$  | $$  | $$  | $$      | $$$$$     | $$  | $$ $$ $$| $$  | $$| $$$$$   | $$$$$$$/
   | $$__  $$| $$$$_  $$$$  | $$  | $$  | $$      | $$__/     | $$  | $$  $$$$| $$  | $$| $$__/   | $$__  $$
   | $$  | $$| $$$/ \  $$$  | $$  | $$  | $$      | $$        | $$  | $$\  $$$| $$  | $$| $$      | $$  \ $$
   | $$  | $$| $$/   \  $$ /$$$$$$| $$$$$$$/      | $$       /$$$$$$| $$ \  $$| $$$$$$$/| $$$$$$$$| $$  | $$
   |__/  |__/|__/     \__/|______/|_______/       |__/      |______/|__/  \__/|_______/ |________/|__/  |__/
"""
    console = Console()
    centered_banner = Align.center(rainbow_text(banner))
    console.print(centered_banner)

def get_hwid():
    try:
        output = subprocess.check_output(
            'powershell -command "Get-CimInstance -ClassName Win32_ComputerSystemProduct | Select-Object -ExpandProperty UUID"'
        )
        hwid = output.decode('utf-8').strip()
        return hwid if hwid else "Error: UUID not found."
    except Exception as e:
        return f"Error: {e}"

def display_hwid(hwid):
    console = Console()
    border = "─" * 61
    console.print(Align.center(f"[cyan]┌{border}┐"))
    hwid_text = Align.center(Text("HWID of your computer:", style="bold green"))
    console.print(hwid_text)
    hwid_display = Align.center(Text(hwid, style="bold cyan"))
    console.print(hwid_display)

    pyperclip.copy(hwid)
    copied_text = Align.center(Text("HWID copied to clipboard!", style="bold yellow"))
    console.print(copied_text)
    console.print(Align.center(f"[cyan]└{border}┘"))

def display_version(version):
    console = Console()
    border = "─" * 61
    console.print(Align.center(f"[cyan]┌{border}┐"))
    version_text = Align.center(Text(f"Latest version available: {version}", style="bold green"))
    console.print(version_text)
    console.print(Align.center(f"[cyan]└{border}┘"))

def check_for_updates():
    console = Console()
    try:
        response = requests.get("https://api.github.com/repos/ImElio/HWID-Finder/releases/latest")
        response.raise_for_status()
        release_data = response.json()
        latest_version = release_data['tag_name']
        display_version(latest_version)
    except requests.exceptions.HTTPError as http_err:
        console.print(Align.center(Text(f"HTTP error occurred: {http_err}", style="bold red")))
    except requests.exceptions.RequestException as req_err:
        console.print(Align.center(Text(f"Request error occurred: {req_err}", style="bold red")))
    except Exception as e:
        console.print(Align.center(Text(f"An error occurred: {e}", style="bold red")))

def main_menu():
    console = Console()
    display_banner()

    options = [
        "1] Get HWID",
        "2] Check for Updates",
        "3] Exit"
    ]

    border = "─" * 61
    console.print(Align.center(f"[cyan]┌{border}┐"))
    for option in options:
        console.print(Align.center(f"[cyan]│ [bold yellow]{option.ljust(61)} [/bold yellow][cyan]│"))
    console.print(Align.center(f"[cyan]└{border}┘"))
    
    authors = "Created by: Elio" 
    version = "1.0.0"
    instructions = "Select an option by entering the corresponding number:"

    console.print(Align.center(authors))
    console.print(Align.center(instructions))

    while True:
        choice = Prompt.ask("[yellow bold]Enter your choice[/yellow bold]")

        if choice == "1":
            hwid = get_hwid()
            display_hwid(hwid)
        elif choice == "2":
            console.print(Align.center(Text("Checking for updates...", style="bold yellow")))
            check_for_updates()
            Prompt.ask("Press Enter to return to the main menu...")
        elif choice == "3":
            console.print("[bold red]Exiting the program...[/bold red]")
            break
        else:
            console.print("[bold red]Invalid option, please try again.[/bold red]")

if __name__ == "__main__":
    main_menu()
