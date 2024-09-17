import subprocess
import os

def crack_rar_password(rar_file, wordlist):
    with open(wordlist, "r") as wl:
        for password in wl:
            password = password.strip()
            command = ['unrar', 't', '-p' + password, rar_file]
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            if "All OK" in result.stdout.decode():
                print(f"Password found: {password}")
                return
            else:
                print(f"Tried: {password} (failed)")
    print("Password not found in the wordlist.")

def main():
    rar_file = input("Enter the path to the RAR file: ")
    wordlist = input("Enter the path to the wordlist file: ")
    
    if not os.path.exists(rar_file):
        print("RAR file does not exist!")
        return
    
    if not os.path.exists(wordlist):
        print("Wordlist does not exist!")
        return
    
    print(f"Attempting to crack RAR file: {rar_file}")
    crack_rar_password(rar_file, wordlist)

if __name__ == "__main__":
    main()
