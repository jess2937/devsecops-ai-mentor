import hashlib
import os

# Vulnerability 1: Weak MD5 hashing (should use SHA-256 or bcrypt)
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

# Vulnerability 2: Hardcoded API key (should use environment variables)
API_KEY = "sk-1234567890abcdef1234567890abcdef"

# Vulnerability 3: Unsafe exec() call
def run_command(user_input):
    exec(user_input)

# Vulnerability 4: SQL Injection risk
def get_user(username):
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    return query

if __name__ == "__main__":
    print(hash_password("mypassword"))
    print(API_KEY)
    run_command("print('hello')")
    print(get_user("admin"))