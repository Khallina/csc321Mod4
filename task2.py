import bcrypt
import nltk
from nltk.corpus import words
import time


# Notes: $2b$12$somesaltvaluehashedpasswordvalue
# $2b$ is the algorithm.
# 12 is the work factor (cost factor).
# somesaltvalue is the salt.
# hashedpasswordvalue is the actual hash.


# Comment out after the first run to avoid unnecessary downloads
# nltk.download('words')
def crack_bcrypt_hash(algorithm, workfactor, salt_hash, wordlist):
    # Reconstruct the full bcrypt salt (including algorithm, workfactor, and salt)
    full_salt = f"${algorithm}${workfactor}${salt_hash[:22]}".encode('utf-8')

    # Extract the target hash (the part after the salt)
    target_hash = salt_hash[22:].encode('utf-8')

    i = 0
    for word in wordlist:
        # When it runs for so long without updates I feel like it crashed, this helps
        if i % 1000 == 0:  # Print progress every 1000 words
            print(f"Testing word {i + 1}/{len(wordlist)}: {word}")
        i += 1

        # bcrypt time
        try:
            # make hash
            hashed_word = bcrypt.hashpw(word.encode('utf-8'), full_salt)
            # Compare the generated hash with the target hash
            if hashed_word == full_salt + target_hash:
                return word
        except Exception as e:
            print(f"Error hashing word: {word}, Error: {e}")
            continue
    return None


# Process it - sort out names, call cracking function)
def process_shadow_file(shadow_file_path, target_user):
    # Load the NLTK (6-10 letters only for this)
    wordlist = [word for word in words.words() if 6 <= len(word) <= 10]
    with open(shadow_file_path, 'r') as file:
        lines = file.readlines()

    # List each username so I can crack just what I want to
    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Make it to only read the line for the targeted name
        parts = line.split(':')
        user = parts[0]
        if user != target_user:
            continue  # Skip other users

        algorithm = parts[1].split('$')[1] # "2b" from notes
        workfactor = parts[1].split('$')[2] # "12" from notes
        salt_hash = parts[1].split('$')[3] # "somesaltvaluehashedpasswordvalue" from  notes (see top of file)

        print(f"Cracking password for user: {user}")

        start_time = time.time()
        # Crack the hash
        password = crack_bcrypt_hash(algorithm, workfactor, salt_hash, wordlist)

        end_time = time.time()

        if password:
            print(f"Password for {user} is: {password}")
        else:
            print(f"Password for {user} not found.")

        print(f"Time taken: {end_time - start_time:.2f} seconds\n")
        break  # Code cracked stop


# Main function
if __name__ == "__main__":
    target_user = "Thorin"  # So we didn't have to run all of them at once, made it to purposefully check
    # a specfic name at a time from the txt file
    process_shadow_file("shadow.txt", target_user)
