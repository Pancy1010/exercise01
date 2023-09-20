import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from collections import Counter
import matplotlib.pyplot as plt

from moby_dick_analysis import moby_dick_text

# Download required NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

# Read the file with the correct encoding
with open('moby_dick.txt', 'r', encoding='utf-8') as file:
    content = file.read()

# Alternatively, handle encoding errors
with open('moby_dick.txt', 'r', encoding='gbk', errors='ignore') as file:
    content = file.read()

# Tokenization
tokens = word_tokenize(moby_dick_text)

# Stop-words filtering
stop_words = set(stopwords.words('english'))
filtered_tokens = [token.lower() for token in tokens if token.lower() not in stop_words]

# Parts-of-Speech (POS) tagging
pos_tags = nltk.pos_tag(filtered_tokens)

# POS frequency
pos_freq = dict(Counter(tag for word, tag in pos_tags))
top_5_pos = sorted(pos_freq, key=pos_freq.get, reverse=True)[:5]

print("Top 5 POS:")
for pos in top_5_pos:
    print(f"{pos}: {pos_freq[pos]}")

# Lemmatization
lemmatizer = WordNetLemmatizer()
lemmatized_tokens = [lemmatizer.lemmatize(word, pos=tag[0].lower())
                     for word, tag in pos_tags][:20]

print("\nLemmatized Tokens:")
print(lemmatized_tokens)

# Plotting frequency distribution
pos_counts = Counter(pos for word, pos in pos_tags)
plt.bar(pos_counts.keys(), pos_counts.values())
plt.xlabel('Parts of Speech')
plt.ylabel('Frequency')
plt.title('POS Frequency Distribution')
plt.show()
