import hashlib
import subprocess
import os

# Use the full path to hashcat.exe\
setup1 = r"g:"
setupt = r"cd projekt\hashcat-6.2.5"
hashcat_command = r"G:\projekt\hashcat-6.2.5\hashcat.exe -m 0 -a 0 -D 2 -d 1 -o G:\projekt\hashcat-6.2.5\1.txt  G:\projekt\hashcat-6.2.5\hash.txt G:\projekt\hashcat-6.2.5\wordlist.txt --show"

# Uruchomienie Hashcat jako procesu systemowego
print(subprocess.run(setup1, stdout=subprocess.PIPE, stderr=subprocess.PIPE))
print(subprocess.run(setupt, stdout=subprocess.PIPE, stderr=subprocess.PIPE))
result = subprocess.run(hashcat_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
print(result)
print(result.stdout.decode('utf-8').strip())
