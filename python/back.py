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
def crack_hash(hash_value, hash_type):
    # Change directory to the Hashcat folder
    hashcat_directory = "G:\\projekt\\hashcat-6.2.5"
    os.chdir(hashcat_directory)

    hash_type_input = input('Enter the hash type (md5, sha1, sha256): ')

    # Map the user input to the corresponding hash type code
    hash_type_map = {
        "md5": "0",
        "sha1": "100",
        "sha256": "1400"
    }

    # Get the hash type code from the map
    hash_type = hash_type_map.get(hash_type_input.lower())

    if hash_type is None:
        print("Invalid hash type entered.")
    else:
        # Define the command to run Hashcat
        command = [
            "hashcat.exe",
            "-m", hash_type,
            "-a", "0",
            "-D", "2",
            "-d", "1",
            "-o", "output.txt",
            "hash.txt",
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


@app.route('/')
def index():
    return render_template('index.html')

# Endpoint do generowania hashów
@app.route('/hash', methods=['POST'])
def hash_message():
    data = request.json
    message = data.get('message', '')
    algorithm = data.get('algorithm', 'sha256')

    if not message:
        return jsonify({'error': 'No message provided'}), 400

    hash_value = generate_hash(message, algorithm)
    if hash_value:
        return jsonify({'hash': hash_value, 'algorithm': algorithm})
    else:
        return jsonify({'error': 'Unsupported algorithm'}), 400

# Endpoint do łamania hashów
@app.route('/crack', methods=['POST'])
def crack_hash_request():
    data = request.json
    hash_value = data.get('hash', '')
    hash_type = data.get('hash_type', 'sha256')

    if not hash_value:
        return jsonify({'error': 'No hash provided'}), 400

    cracked_message = crack_hash(hash_value, hash_type)
    if cracked_message:
        return jsonify({'message': cracked_message})
    else:
        return jsonify({'error': 'Failed to crack the hash'}), 400

if __name__ == '__main__':
    app.run(debug=True)
