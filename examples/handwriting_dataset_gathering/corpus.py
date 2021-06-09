import re
import nltk
from wiki_dump_reader import Cleaner, iterate


class WikiDump:
    def __init__(self, filepath, language, min_len=15, max_len=35,
                 # default filter gets rid of strange punctuation
                 regex=re.compile(r'[#$%&\\*+/\-<=>@^_`{|}~]|\W{4,}')):
        """
        :param filepath: path to the *.xml wikidump file
        :param language: language of the wiki, can be used for additional filtering
        :param min_len: minimal length of resulting sentences
        :param max_len: maximal length of resulting sentences
        :param regex: compiled regex for sentence filtering
        """
        self.language = language
        self.filepath = filepath
        self.cleaner = Cleaner()

        # you can use these for additional filtering
        # from nltk.corpus import stopwords
        # self.stopwords = stopwords.words(language)

        self.min_len = min_len
        self.max_len = max_len
        self.re = regex

    def get_texts(self):
        """Generate all the texts (with title) of the dump"""
        for title, text in iterate(self.filepath):
            text = self.cleaner.clean_text(text)
            cleaned_text, links = self.cleaner.build_links(text)
            yield title, cleaned_text

    def filter(self, sentence):
        """Filter for "proper" sentences"""
        return self.re.search(sentence) is None and (sentence[0].isupper() or not sentence[0].isalpha())

    def get_sentences(self, max_size=None):
        """Get all or al most max_size sentences, if max_size is provided"""
        sentences = []
        for _, text in self.get_texts():
            for sentence in nltk.sent_tokenize(text):
                if max_size is not None and len(sentences) >= max_size:
                    return sentences
                sentence = sentence.replace('\n', '')
                words = sentence.split()
                if self.min_len <= len(words) <= self.max_len:
                    if self.filter(sentence):
                        sentences.append(sentence)
        return sentences

    def gen_sentences(self, text):
        """Generate all sentences of the text"""
        for sentence in nltk.sent_tokenize(text):
            sentence = sentence.replace('\n', '')
            yield sentence
        return

    def get_sent_lengths(self, text):
        """Get statistics of sentence lengths in text, can be used to find optimal min_length and max_length"""
        lengths = []
        for sentence in self.gen_sentences(text):
            words = nltk.wordpunct_tokenize(sentence)
            lengths.append(len(words))
        return lengths
