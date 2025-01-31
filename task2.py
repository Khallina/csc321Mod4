import bcrypt
import nltk
from nltk.corpus import words
import time

# Comment out after the first run to avoid unnecessary downloads
# nltk.download('words')

# Function to crack bcrypt hash
def crack_bcrypt_hash(user, algorithm, workfactor, salt_hash, wordlist):
    # Reconstruct the full bcrypt salt (including algorithm, workfactor, and salt)
    full_salt = f"${algorithm}${workfactor}${salt_hash[:22]}".encode('utf-8')

    # Extract the target hash (the part after the salt)
    target_hash = salt_hash[22:].encode('utf-8')

    # Iterate through the wordlist
    for i, word in enumerate(wordlist):
        # Provide periodic updates
        if i % 1000 == 0:  # Print progress every 1000 words
            print(f"Testing word {i + 1}/{len(wordlist)}: {word}")

        # Hash the word using bcrypt
        try:
            # Generate the bcrypt hash for the current word
            hashed_word = bcrypt.hashpw(word.encode('utf-8'), full_salt)
            # Compare the generated hash with the target hash
            if hashed_word == full_salt + target_hash:
                return word
        except Exception as e:
            print(f"Error hashing word: {word}, Error: {e}")
            continue
    return None

# Function to process the shadow file for a specific user
def process_shadow_file(shadow_file_path, target_user):
    # Load the NLTK word corpus (6-10 letters)
    wordlist = [word for word in words.words() if 6 <= len(word) <= 10]

    # Read the shadow file
    with open(shadow_file_path, 'r') as file:
        lines = file.readlines()

    # Process each user
    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Extract components
        parts = line.split(':')
        user = parts[0]
        if user != target_user:
            continue  # Skip other users

        algorithm = parts[1].split('$')[1]
        workfactor = parts[1].split('$')[2]
        salt_hash = parts[1].split('$')[3]

        print(f"Cracking password for user: {user}")

        # Start timer
        start_time = time.time()

        # Crack the hash
        password = crack_bcrypt_hash(user, algorithm, workfactor, salt_hash, wordlist)

        # End timer
        end_time = time.time()

        if password:
            print(f"Password for {user} is: {password}")
        else:
            print(f"Password for {user} not found.")

        print(f"Time taken: {end_time - start_time:.2f} seconds\n")
        break  # Stop after processing the target user

# Main function
if __name__ == "__main__":
    shadow_file_path = "shadow.txt"  # Replace with the path to your shadow file
    target_user = "Bilbo"  # Hardcoded username (change this as needed)
    process_shadow_file(shadow_file_path, target_user)