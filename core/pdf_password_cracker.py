import PyPDF2
import sys

def crack_pdf_password(pdf_file, wordlist_file):
    """Attempts to crack the password of a PDF using a wordlist."""
    try:
        # Open the PDF file
        with open(pdf_file, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Check if the PDF is encrypted
            if not pdf_reader.is_encrypted:
                print(f"The file {pdf_file} is not password protected.")
                return
            
            # Open the wordlist file and try each password
            with open(wordlist_file, 'r', encoding='ISO-8859-1') as wordlist:
                for password in wordlist:
                    password = password.strip()
                    # Attempt to decrypt the PDF with the password
                    if pdf_reader.decrypt(password):
                        return password
                    
            print("Password not found in wordlist.")
    
    except FileNotFoundError:
        print(f"Error: File {pdf_file} or wordlist {wordlist_file} not found.")
        sys.exit(1)

def main():
    print("PDF Password Cracking Tool")
    print("==========================")
    
    # User inputs
    pdf_file = input("Enter the path to the password-protected PDF: ").strip()
    wordlist_file = input("Enter the path to the wordlist file: ").strip()
    
    # Attempt to crack the password
    password = crack_pdf_password(pdf_file, wordlist_file)
    
    if password:
        print(f"Password successfully cracked: {password}")
    else:
        print("Password not found.")

if __name__ == "__main__":
    main()
