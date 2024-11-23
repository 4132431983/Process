import random
import nltk
import re
import concurrent.futures

nltk.download('punkt')
nltk.download('gutenberg')
nltk.download('brown')
nltk.download('cess_esp')  # French Corpus
nltk.download('sinica_treebank')  # Chinese Corpus
nltk.download('floresta')  # Italian Corpus
nltk.download('webtext')  # Web Text Corpus
nltk.download('movie_reviews')  # Movie Reviews Corpus
nltk.download('reuters')  # Reuters Corpus
nltk.download('inaugural')  # Inaugural Address Corpus
nltk.download('twitter_samples')  # Twitter Samples Corpus
nltk.download('abc')  # ABC News Corpus
nltk.download('treebank')  # Penn Treebank Corpus
nltk.download('conll2000')  # CoNLL 2000 Chunking Corpus

# Preload the corpora into memory
gutenberg_corpus = list(nltk.corpus.gutenberg.sents())
brown_corpus = list(nltk.corpus.brown.sents())
french_corpus = list(nltk.corpus.cess_esp.sents())
chinese_corpus = list(nltk.corpus.sinica_treebank.sents())
italian_corpus = list(nltk.corpus.floresta.sents())
webtext_corpus = list(nltk.corpus.webtext.sents())
movie_reviews_corpus = list(nltk.corpus.movie_reviews.sents())
reuters_corpus = list(nltk.corpus.reuters.sents())
inaugural_corpus = list(nltk.corpus.inaugural.sents())
twitter_samples_corpus = list(nltk.corpus.twitter_samples.strings())
abc_corpus = list(nltk.corpus.abc.sents())
treebank_corpus = list(nltk.corpus.treebank.sents())
conll2000_corpus = list(nltk.corpus.conll2000.sents())

# Compile regular expressions
double_spaces_regex = re.compile(r' +')
special_chars_regex = re.compile(r'[^a-zA-Z0-9\s]')

def generate_sentence(random_source):
    sentence = ""
    while not sentence:
        random_sentence = random.choice(random_source)
        if 1 <= len(random_sentence) <= 20:  # Limit sentence length to 1 to 10 words
            sentence = " ".join(random_sentence)
            sentence = double_spaces_regex.sub(' ', sentence)  # Remove double spaces

    cleaned_sentence = special_chars_regex.sub('', sentence)  # Remove special characters
    cleaned_sentence = double_spaces_regex.sub(' ', cleaned_sentence)  # Remove double spaces

    capitalized = cleaned_sentence.capitalize()
    lowercase = cleaned_sentence.lower()

    return capitalized.strip(), lowercase.strip()

def generate_sentence_no_spaces_capitalized(random_source):
    sentence = ""
    while not sentence:
        random_sentence = random.choice(random_source)
        if 1 <= len(random_sentence) <= 20:
            sentence = "".join(random_sentence)

    cleaned_sentence = special_chars_regex.sub('', sentence)  # Remove special characters

    capitalized = cleaned_sentence.capitalize()

    return capitalized.strip()

def generate_sentence_no_spaces_lowercase(random_source):
    sentence = ""
    while not sentence:
        random_sentence = random.choice(random_source)
        if 1 <= len(random_sentence) <= 20:
            sentence = "".join(random_sentence)

    cleaned_sentence = special_chars_regex.sub('', sentence)  # Remove special characters

    lowercase = cleaned_sentence.lower()

    return lowercase.strip()

def generate_phrases_batch(batch_size):
    for _ in range(batch_size):
        sources = [gutenberg_corpus, brown_corpus, french_corpus, chinese_corpus, italian_corpus,
                   webtext_corpus, movie_reviews_corpus, reuters_corpus, inaugural_corpus,
                   twitter_samples_corpus, abc_corpus, treebank_corpus, conll2000_corpus]
        random_source = random.choice(sources)

        capitalized, lowercase = generate_sentence(random_source)
        no_spaces_lowercase = generate_sentence_no_spaces_lowercase(random_source)

        if capitalized:
            print(capitalized)
        if lowercase:
            print(lowercase)
        if no_spaces_capitalized:
            print(no_spaces_capitalized)
        if no_spaces_lowercase:
            print(no_spaces_lowercase)

def generate_phrases_nonstop():
    batch_size = 500000

    while True:
        with concurrent.futures.ThreadPoolExecutor(max_workers=24) as executor:
            executor.submit(generate_phrases_batch, batch_size)

# Generate random phrases continuously using multiple threads
print("Random Phrases:")
generate_phrases_nonstop()
