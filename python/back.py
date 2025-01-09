from flask import Flask, request, jsonify, render_template
import hashlib
import subprocess
import os

app = Flask(__name__)


# Funkcja do generowania skrótu z wiadomości wejściowej
def generate_hash(message, algorithm):
    if algorithm == "md5":
        return hashlib.md5(message.encode()).hexdigest()
    elif algorithm == "sha1":
        return hashlib.sha1(message.encode()).hexdigest()
    elif algorithm == "sha256":
        return hashlib.sha256(message.encode()).hexdigest()
    else:
        return None


# Funkcja do uruchamiania Hashcat w celu złamania skrótu
def crack_hash(hash_value, hash_type, retry):
    os.chdir("G:\\projekt\\hashcat-6.2.6")

    command = [
        "hashcat.exe",
        "-m", hash_type,
        "-a", "0",
        "-D", "2",
        "-d", "1",
        '-o', 'output.txt',
        hash_value,
        "wordlist.txt",
    ]

    result = run_command(command)

    if result != None:
        return result
    elif retry:
        command = [
            "hashcat.exe",
            "-m", hash_type,
            "-a", "0",
            "-D", "2",
            "-d", "1",
            "-r", "rules/best64.rule",
            '-o', 'output.txt',
            hash_value,
            "wordlist.txt",
        ]

        result = run_command(command)
        if result != None:
            return result

        command = [
            "hashcat.exe",
            "-m", hash_type,
            "-a", "0",
            "-D", "2",
            "-d", "1",
            "-r", "rules/rockyou-30000.rule",
            '-o', 'output.txt',
            hash_value,
            "wordlist.txt",
        ]
        result = run_command(command)

        if result:
            return result
        else:
            return None
    else:
        return None


def run_command(command):
    try:
        os.remove('hashcat.potfile')
        with open('output.txt', 'w') as file:
            file.write('')
    except:
        pass

    subprocess.run(command)

    try:
        with open('hashcat.potfile', 'r') as file:
            result = file.read()
    except:
        return None
    if result == '':
        return None
    return result.split(':', 1)[1]


@app.route('/')
def index():
    return render_template('index.html')


# Endpoint do generowania hashów
@app.route('/hash', methods=['POST'])
def hash_message():
    data = request.json
    message = data.get('message', '')
    algorithm = data.get('algorithm', '')

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
    retry = data.get('retry', False)

    if not hash_value:
        return jsonify({'error': 'No hash provided'}), 400

    cracked_message = crack_hash(hash_value, hash_type, retry)

    if cracked_message:
        return jsonify({'message': cracked_message})
    else:
        return jsonify({'not_found': 'Hash not cracked'})


if __name__ == '__main__':
    app.run(debug=True)
