import hashlib
import os
import json

# File to store the saved hash values for comparison
HASH_DB_FILE = 'hash_database.json'

# Function to calculate SHA-256 hash of a file
def calculate_hash(filepath, algorithm='sha256'):
    hasher = hashlib.new(algorithm)
    try:
        with open(filepath, 'rb') as f:
            # Read file in chunks to support large files
            while chunk := f.read(4096):
                hasher.update(chunk)
        return hasher.hexdigest()
    except FileNotFoundError:
        # Return None if file is missing or deleted during scan
        return None

# Load the saved hash database from JSON file
def load_hash_database():
    if os.path.exists(HASH_DB_FILE):
        with open(HASH_DB_FILE, 'r') as f:
            return json.load(f)
    return {}

# Save the updated hash database to JSON file
def save_hash_database(db):
    with open(HASH_DB_FILE, 'w') as f:
        json.dump(db, f, indent=4)

# Main function to monitor a selected directory
def monitor_directory(directory):
    # Load previously saved hash values
    hash_db = load_hash_database()
    updated_db = {}

    print(f"\n🔍 Scanning directory: {directory}\n")

    # Walk through the folder and its subfolders
    for root, _, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            file_hash = calculate_hash(filepath)

            updated_db[filepath] = file_hash

            # Check if the file is new, modified, or unchanged
            if filepath not in hash_db:
                print(f"[NEW FILE]     {filepath}")
            elif hash_db[filepath] != file_hash:
                print(f"[MODIFIED]     {filepath}")
            else:
                print(f"[UNCHANGED]    {filepath}")

    # Check for deleted files (i.e., files present before but now missing)
    removed_files = set(hash_db.keys()) - set(updated_db.keys())
    for filepath in removed_files:
        print(f"[REMOVED]      {filepath}")

    # Save the new state of hashes to the database
    save_hash_database(updated_db)
    print("\n✅ Scan complete.\n")

# Entry point of the script
if __name__ == "__main__":
    # Ask the user to input a valid folder path
    target_directory = input("📁 Enter the directory path to monitor: ").strip()

    while not os.path.isdir(target_directory):
        print("❌ Invalid directory. Please try again.")
        target_directory = input("📁 Enter a valid directory path: ").strip()

    # Start monitoring the given directory
    monitor_directory(target_directory)
