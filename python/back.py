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
    # Set the working directory for Hashcat
    hashcat_directory = "G:\\projekt\\hashcat-6.2.5"
    os.chdir(hashcat_directory)

    # Define the Hashcat command
    command = [
        "hashcat.exe",
        "-m", hash_type,
        "-a", "0",
        "-D", "2",
        "-d", "1",
        hash_value,
        "wordlist.txt",
        "--show"
    ]

    try:
        # Run the command and capture output
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip().split(':',1)[1]
        else:
            return None
    except Exception as e:
        return str(e)


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
    hash_type = data.get('hash_type', '')

    if not hash_value:
        return jsonify({'error': 'No hash provided'}), 400

    cracked_message = crack_hash(hash_value, hash_type)
    if cracked_message:
        return jsonify({'message': cracked_message})
    else:
        return jsonify({'error': 'Failed to crack the hash'}), 400

if __name__ == '__main__':
    app.run(debug=True)
