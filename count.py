file_path = "file_to_read.txt"

file = open(file_path, 'r') # open file

# Read the file content
file_content = file.read()

# Close the file
file.close()

text = file_content

target_word = "terrible"

# Count occurrences
count = text.count(target_word)

print("The number of occurrences of 'terrible':", count)




