def replace_words(input_text):
    word_count = 0
    output_text = ""

    # Split the input text into words
    words = input_text.split()

    # Iterate through each word
    for word in words:
        if word == "terrible":
            word_count += 1
            if word_count % 2 == 0:
                output_text += "pathetic "
            else:
                output_text += "marvellous "
        else:
            output_text += word + " "

    return output_text, word_count

# Read the input file
with open("file_to_read.txt", "r") as file:
    input_text = file.read()

# Replace the words and get the word count
output_text, word_count = replace_words(input_text)

# Write the modified text to a new file
with open("result.txt", "w") as file:
    file.write(output_text)
