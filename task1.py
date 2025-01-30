import hashlib
import random
import string
import time
import matplotlib.pyplot as plt


def sha256_hash(input_string):
    # FUNCTION sha256_hash(input_string):
    # 1. Convert input_string to bytes
    # 2. Calculate SHA256 hash of the bytes
    # 3. Return the hash as a hexadecimal string

    input_bytes = input_string.encode('utf-8')
    hashSha = hashlib.sha256(input_bytes)
    return hashSha.hexdigest()


def truncate_hash(hash_string, bits):
    # FUNCTION truncate_hash(hash_string, bits):
    # 1. Take the first (bits / 4) characters of hash_string
    # 2. Convert this substring to an integer (base 16)
    # 3. Create a bitmask of 'bits' number of 1s
    # 4. Perform bitwise AND between the integer and the bitmask
    # 5. Return the result

    # Calculate the number of hex characters needed (4 bits per character)
    num_chars = (bits + 3) // 4
    trunc_hex = hash_string[:num_chars]
    # Convert to integer and apply bitmask
    trunc_int = int(trunc_hex, 16)
    bitmask = (1 << bits) - 1
    res = trunc_int & bitmask
    return res


def hamming_distance(s1, s2):
    # FUNCTION hamming_distance(s1, s2):
    # 1. Initialize count to 0
    # 2. FOR each pair of characters (c1, c2) in (s1, s2):
    #      IF c1 != c2:
    #          Increment count
    # 3. RETURN count
    count = 0
    for c1, c2 in zip(s1, s2):
        if c1 != c2:
            count += 1
    return count


def random10ASCII():
    base = ""
    for _ in range(10):
        random_char = random.choice(string.ascii_letters)
        base += random_char
    return base


def find_hamming_distance_1():
    # FUNCTION find_hamming_distance_1():
    # 1. Generate a random string 'base' of 10 ASCII letters
    # 2. FOR each index i in base:
    #      Create 'modified' by flipping the i-th bit of base
    #      IF hamming_distance(base, modified) == 1:
    #          RETURN base, modified
    # 3. RETURN None, None

    base = random10ASCII()
    for i in range(len(base)):
        modified = base[:i] + chr(ord(base[i]) ^ 1) + base[i + 1:]
        if hamming_distance(base, modified) == 1:
            return base, modified
    return None, None


def find_collision(bits, max_attempts=100000):
    # FUNCTION find_collision(bits, max_attempts):
    # 1. Initialize empty dictionary 'seen'
    # 2. Record start time
    # 3. FOR attempts from 1 to max_attempts:
    #      Generate random string 's' of 10 ASCII letters
    #      Calculate truncated hash 'h' of 's'
    #      IF h exists in seen:
    #          Calculate end time
    #          RETURN seen[h], s, attempts, elapsed time
    #      ELSE:
    #          Add s to seen with key h
    # 4. RETURN None, None, max_attempts, elapsed time

    seen = {}
    start_time = time.time()
    for attempt in range(max_attempts):
        s = random10ASCII()
        h = truncate_hash(sha256_hash(s), bits)
        if h in seen:
            elapsed_time = time.time() - start_time
            return seen[h], s, attempt + 1, elapsed_time
        seen[h] = s
    elapsed_time = time.time() - start_time
    return None, None, max_attempts, elapsed_time


def task_1a():
    # FUNCTION task_1a():
    # 1. Print "Task 1a: SHA256 hashes of arbitrary inputs"
    # 2. FOR each input in ["Hello, World!", "Python", "Cryptography"]:
    #      Calculate SHA256 hash of input
    #      Print input and its hash

    print("Task 1a: SHA256 hashes of arbitrary inputs")
    inputs = ["Hello, World!", "Python", "Cryptography"]
    for input_str in inputs:
        hash_value = sha256_hash(input_str)
        print(f"Input: {input_str}\nHash: {hash_value}\n")


def task_1b():
    # FUNCTION task_1b():
    # 1. Print "Task 1b: Strings with Hamming distance of 1"
    # 2. FOR i from 1 to 3:
    #      Find two strings s1, s2 with Hamming distance 1
    #      Calculate SHA256 hashes h1, h2 of s1, s2
    #      Print s1, s2, h1, h2

    print("Task 1b: Strings with Hamming distance of 1")
    for i in range(3):
        s1, s2 = find_hamming_distance_1()
        h1 = sha256_hash(s1)
        h2 = sha256_hash(s2)
        print(f"String 1: {s1}\nHash 1: {h1}")
        print(f"String 2: {s2}\nHash 2: {h2}\n")


def task_1c():
    # FUNCTION task_1c():
    # 1. Print "Task 1c: Finding collisions for truncated hashes"
    # 2. Initialize empty lists for bits, time, and inputs
    # 3. FOR bits from 8 to 50, step 2:
    #      Find collision for 'bits' number of bits
    #      IF collision found:
    #          Add result to table
    #          Append bits, time, and inputs to respective lists
    #      ELSE:
    #          Print timeout message
    # 4. Print results table
    # 5. Plot graphs:
    #      1. Digest Size vs Collision Time
    #      2. Digest Size vs Number of Inputs
    # 6. Save graphs as 'collision_analysis.png'

    print("Task 1c: Finding collisions for truncated hashes")
    bits_list = []
    time_list = []
    inputs_list = []
    for bits in range(8, 51, 2):
        s1, s2, attempts, elapsed_time = find_collision(bits)
        if s1:
            print(f"Collision found for {bits} bits:")
            print(f"Input 1: {s1}\nInput 2: {s2}")
            print(f"Attempts: {attempts}\nTime: {elapsed_time:.4f} seconds\n")
            bits_list.append(bits)
            time_list.append(elapsed_time)
            inputs_list.append(attempts)
        else:
            print(f"No collision found for {bits} bits within 100,000 attempts.\n")

    # Plotting
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.plot(bits_list, time_list, marker='o')
    plt.xlabel('Digest Size (bits)')
    plt.ylabel('Collision Time (seconds)')
    plt.title('Digest Size vs Collision Time')

    plt.subplot(1, 2, 2)
    plt.plot(bits_list, inputs_list, marker='o')
    plt.xlabel('Digest Size (bits)')
    plt.ylabel('Number of Inputs')
    plt.title('Digest Size vs Number of Inputs')

    plt.tight_layout()
    plt.savefig('collision_analysis.png')
    plt.show()

def task_1_main():
    """
    FUNCTION task_1_main():
    1. Call task_1a()
    2. Call task_1b()
    3. Call task_1c()
    END FUNCTION
    """
    task_1a()
    task_1b()
    task_1c()


task_1_main()
