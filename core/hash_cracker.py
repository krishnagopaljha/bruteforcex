import hashlib
import sys
import binascii

# ANSI color codes for TUI
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"

# Supported hash algorithms
SUPPORTED_ALGORITHMS = {
    '1': ('MD5', hashlib.md5),
    '2': ('SHA-1', hashlib.sha1),
    '3': ('SHA-224', hashlib.sha224),
    '4': ('SHA-256', hashlib.sha256),
    '5': ('SHA-384', hashlib.sha384),
    '6': ('SHA-512', hashlib.sha512),
    '7': ('NTLM', None),  # NTLM is handled manually
    '8': ('Blake2b', hashlib.blake2b),
    '9': ('Blake2s', hashlib.blake2s)
}

def display_hash_options():
    """Display available hash algorithms for the user."""
    print(CYAN + "Available Hash Algorithms:" + RESET)
    for key, (name, _) in SUPPORTED_ALGORITHMS.items():
        print(f"{BOLD}{key}. {name}{RESET}")
    print()

def hash_password(password, algorithm):
    """Hashes the given password using the specified hashing algorithm."""
    try:
        if algorithm == 'NTLM':
            # NTLM Hash = MD4(UTF-16-LE(password))
            password_bytes = password.encode('utf-16le')
            ntlm_hash = hashlib.new('md4', password_bytes).digest()
            return binascii.hexlify(ntlm_hash).decode('utf-8').upper()
        else:
            hash_func = SUPPORTED_ALGORITHMS[algorithm][1]
            if hash_func:
                return hash_func(password.encode()).hexdigest().upper()
            else:
                raise ValueError(f"Unsupported hash algorithm: {algorithm}")
    except Exception as e:
        print(RED + f"Error: {str(e)}" + RESET)
        sys.exit(1)

def crack_with_wordlist(target_hash, algorithm_choice, wordlist_file):
    """Attempts to crack the target hash using a wordlist."""
    try:
        with open(wordlist_file, 'r', encoding='ISO-8859-1', errors='ignore') as file:
            for line in file:
                password = line.strip()
                # Hash the password and compare with the target hash
                if hash_password(password, algorithm_choice) == target_hash.upper():
                    return password
    except FileNotFoundError:
        print(RED + "Error: Wordlist file not found." + RESET)
        sys.exit(1)
    except Exception as e:
        print(RED + f"Error: {str(e)}" + RESET)
        sys.exit(1)
    return None

def main():
    print(CYAN + "Password Cracking Tool" + RESET)
    print(BOLD + "=" * 22 + RESET)
    
    # Display available hash algorithms
    display_hash_options()
    
    # User input
    algorithm_choice = input(YELLOW + "Select the hash algorithm by number (1-9): " + RESET).strip()
    
    if algorithm_choice not in SUPPORTED_ALGORITHMS:
        print(RED + "Error: Unsupported hash algorithm selection." + RESET)
        sys.exit(1)
    
    # Map choice '7' to 'NTLM'
    algorithm = 'NTLM' if algorithm_choice == '7' else SUPPORTED_ALGORITHMS[algorithm_choice][0]
    
    hash_file = input(YELLOW + "Enter the path to the hash file: " + RESET).strip()
    wordlist_file = input(YELLOW + "Enter the path to the wordlist file: " + RESET).strip()
    
    try:
        with open(hash_file, 'r') as file:
            target_hash = file.read().strip()
    except FileNotFoundError:
        print(RED + "Error: Hash file not found." + RESET)
        sys.exit(1)
    except Exception as e:
        print(RED + f"Error: {str(e)}" + RESET)
        sys.exit(1)

    print(f"Attempting to crack hash: {CYAN}{target_hash}{RESET} using {CYAN}{algorithm}{RESET}")

    # Perform cracking with wordlist
    password = crack_with_wordlist(target_hash, algorithm, wordlist_file)
    
    if password:
        print(GREEN + f"Password found: {password}" + RESET)
    else:
        print(RED + "Password not found." + RESET)

if __name__ == "__main__":
    main()
