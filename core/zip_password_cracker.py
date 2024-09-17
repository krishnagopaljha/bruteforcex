import pyzipper
import os
import time

def test_password(zip_file, password):
    """Test the given password on the ZIP file."""
    try:
        with pyzipper.AESZipFile(zip_file) as zf:
            zf.pwd = password.encode('utf-8')
            zf.testzip()  # Try accessing the file with the password
        return True
    except (RuntimeError, RuntimeError):
        return False

def dictionary_attack(zip_file, wordlist_file):
    """Perform a dictionary attack to crack the ZIP file password."""
    try:
        with open(wordlist_file, 'r') as file:
            for line in file:
                password = line.strip()
                if password:
                    if test_password(zip_file, password):
                        return password
    except FileNotFoundError:
        print("Error: Wordlist file not found.")
    return None

def main():
    print("ZIP File Password Cracker")
    print("=========================")
    
    # User inputs
    zip_file = input("Enter the path to the ZIP file: ").strip()
    wordlist_file = input("Enter the path to the wordlist file: ").strip()

    # Validate paths
    if not (os.path.isfile(zip_file) and os.path.isfile(wordlist_file)):
        print("Error: One or both file paths are incorrect.")
        return

    print("Starting dictionary attack...")
    start_time = time.time()
    found_password = dictionary_attack(zip_file, wordlist_file)
    elapsed_time = time.time() - start_time

    if found_password:
        print(f'Password found: {found_password}')
    else:
        print('Password not found.')

    print(f"Process completed in {elapsed_time:.2f} seconds.")

if __name__ == "__main__":
    main()
