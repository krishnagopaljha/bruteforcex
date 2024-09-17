import msoffcrypto
import os

def crack_password(file_path, wordlist):
    with open(file_path, "rb") as file:
        office_file = msoffcrypto.OfficeFile(file)
        with open(wordlist, "r") as wl:
            for password in wl:
                password = password.strip()
                try:
                    office_file.load_key(password=password)
                    office_file.decrypt(open("decrypted_output", "wb"))
                    print(f"Password found: {password}")
                    return
                except Exception as e:
                    pass  # Wrong password, continue to the next one
    print("Password not found in the wordlist.")

def main():
    print("Choose a file type to crack:")
    print("1. Excel (.xlsx)")
    print("2. Word (.docx)")
    print("3. PowerPoint (.pptx)")
    
    choice = input("Enter the number corresponding to your choice (1, 2, or 3): ")
    
    file_type_map = {
        '1': 'Excel',
        '2': 'Word',
        '3': 'PowerPoint'
    }
    
    if choice not in file_type_map:
        print("Invalid choice! Please choose 1, 2, or 3.")
        return
    
    file_type = file_type_map[choice]
    
    file_path = input(f"Enter the path to the {file_type} file: ")
    wordlist = input("Enter the path to the wordlist file: ")
    
    if not os.path.exists(file_path):
        print("File does not exist!")
        return
    
    if not os.path.exists(wordlist):
        print("Wordlist does not exist!")
        return
    
    print(f"Attempting to crack {file_type} file: {file_path}")
    crack_password(file_path, wordlist)

if __name__ == "__main__":
    main()
