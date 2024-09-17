import subprocess
import os

def crack_7z_password(archive_file, wordlist):
    with open(wordlist, "r") as wl:
        for password in wl:
            password = password.strip()
            command = ['7z', 't', '-p' + password, archive_file]
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            if "Everything is Ok" in result.stdout.decode():
                print(f"Password found: {password}")
                return
            else:
                print(f"Tried: {password} (failed)")
    print("Password not found in the wordlist.")

def main():
    archive_file = input("Enter the path to the 7z file: ")
    wordlist = input("Enter the path to the wordlist file: ")
    
    if not os.path.exists(archive_file):
        print("7z file does not exist!")
        return
    
    if not os.path.exists(wordlist):
        print("Wordlist does not exist!")
        return
    
    print(f"Attempting to crack 7z file: {archive_file}")
    crack_7z_password(archive_file, wordlist)

if __name__ == "__main__":
    main()
