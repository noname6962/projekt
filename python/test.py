# Assuming `result` is the string "6c1fa6624d32ce4066648e97b0ce8b99:ghpsnanakp"
result = "6c1fa6624d32ce4066648e97b0ce8b99:ghpsnanakp"

# Split the string at the colon and take the second part
cut_result = result.split(':', 1)[1]

print(cut_result)  # Output: ghpsnanakp
