import string
import secrets

def generate_password(length=12):
    # Characters to include in the password
    letters = string.ascii_letters      # a-z, A-Z
    digits = string.digits              # 0-9
    symbols = string.punctuation        # special characters !@#$ etc.

    # Combine all characters
    all_chars = letters + digits + symbols

    # Generate a secure password
    password = ''.join(secrets.choice(all_chars) for _ in range(length))
    return password

# User input for password length
length = int(input("Enter password length: "))
print("Generated Password:", generate_password(length))
