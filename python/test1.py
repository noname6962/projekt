from flask import Flask, request, jsonify, render_template
import hashlib
import subprocess
import os

app = Flask(__name__)

# Funkcja do generowania skrótu z wiadomości wejściowej
def generate_hash(message, algorithm="sha256"):
    algorithm = input('Enter the hash type (md5, sha1, sha256): ')

    if algorithm == "md5":
        return hashlib.md5(message.encode()).hexdigest()
    elif algorithm == "sha1":
        return hashlib.sha1(message.encode()).hexdigest()
    elif algorithm == "sha256":
        return hashlib.sha256(message.encode()).hexdigest()
    else:
        return None

# Funkcja do uruchamiania Hashcat w celu złamania skrótu
def crack_hash():
    # Change directory to the Hashcat folder
    hashcat_directory = "G:\\projekt\\hashcat-6.2.6"
    os.chdir(hashcat_directory)

    hash_type_input = input('Enter the hash type (md5, sha1, sha256): ')

    # Map the user input to the corresponding hash type code
    hash_type_map = {
        "md5": "0",
        "sha1": "100",
        "sha256": "1400",
        "sha512": "1700"
    }

    # Get the hash type code from the map
    hash_type = hash_type_map.get(hash_type_input.lower())
    hash = input('Enter the hash to crack: ')

    if hash_type is None:
        print("Invalid hash type entered.")
    else:
        subprocess.run(["del hashcat.potfile"])
        # Define the command to run Hashcat
        command = [
            "hashcat.exe",
            "-m", hash_type,
            "-a", "0",
            "-D", "2",
            "-d", "1",
            hash,
            "wordlist.txt",
            "--show"
        ]
    # Run the command and capture the output
    try:
        result = subprocess.run(command, capture_output=True, text=True)

        # Check if the command was successful
        if result.returncode == 0:
            print("Command ran successfully!")
            print("Output:", result.stdout)
        else:
            print("Error running command:", result.stderr)

    except Exception as e:
        print("An error occurred:", e)


crack_hash()
