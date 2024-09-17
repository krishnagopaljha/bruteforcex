import os
import subprocess

# Import cracking scripts from 'core' directory
from core.sevenz_password_cracker import main as crack_7z_main
from core.rar_password_cracker import main as crack_rar_main
from core.msoffice_password_cracker import main as crack_office_main
from core.ssh_password_cracker import main as crack_ssh_main
from core.hash_cracker import main as crack_hash_main
from core.pdf_password_cracker import main as crack_pdf_main
from core.zip_password_cracker import main as crack_zip_main

def logo():
    """Return the logo text."""
    return """
 ____             _       ______                __   __
|  _ \           | |     |  ____|               \ \ / /
| |_) |_ __ _   _| |_ ___| |__ ___  _ __ ___ ___ \ V / 
|  _ <| '__| | | | __/ _ \  __/ _ \| '__/ __/ _ \ > <  
| |_) | |  | |_| | ||  __/ | | (_) | | | (_|  __// . \ 
|____/|_|   \__,_|\__\___|_|  \___/|_|  \___\___/_/ \_\

|--------------------------------------------------------------------|
| Created By: Krishna Gopal Jha                                      |
| Checkout my LinkedIn: https://www.linkedin.com/in/krishnagopaljha/ |
| Lookup at my insta: https://instagram.com/theindianpsych           |
|--------------------------------------------------------------------|

    """

def check_and_install(package_name):
    """Check if a package is installed and install it if not."""
    try:
        # Check if the package is installed
        subprocess.run(["dpkg", "-s", package_name], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"{package_name} is already installed.")
    except subprocess.CalledProcessError:
        # Install the package if not found
        print(f"{package_name} is not installed. Installing...")
        subprocess.run(["sudo", "apt", "install", "-y", package_name], check=True)

def clear_screen():
    """Clear the terminal screen and set text color to green."""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[92m", end='')  # Green color for terminal text

def print_centered(text):
    """Print text centered on the terminal screen."""
    terminal_size = os.get_terminal_size()
    terminal_width = terminal_size.columns
    lines = text.split('\n')
    for line in lines:
        print(line.center(terminal_width))

def print_menu():
    """Print the main menu."""
    menu_text = """
Select an option:
1. Crack 7z File
2. Crack RAR File
3. Crack Office File (Excel/Word/PPT)
4. Crack SSH
5. Crack Hash
6. Crack PDF File
7. Crack ZIP File
8. Exit
    """
    print_centered(menu_text)

def main():
    """Main interactive loop."""
    # Check if required tools are installed
    check_and_install("rar")
    check_and_install("p7zip-full")

    clear_screen()
    print_centered(logo())

    while True:
        print_menu()
        choice = input("Enter your choice (1-8): ")

        if choice == '1':
            crack_7z_main()
        elif choice == '2':
            crack_rar_main()
        elif choice == '3':
            crack_office_main()
        elif choice == '4':
            crack_ssh_main()
        elif choice == '5':
            crack_hash_main()
        elif choice == '6':
            crack_pdf_main()
        elif choice == '7':
            crack_zip_main()
        elif choice == '8' or choice.lower() == 'exit':
            print_centered("Exiting...")
            break
        else:
            print_centered("Invalid choice, please select a number between 1 and 8.")

if __name__ == "__main__":
    main()
