import string

import cutils

from .hardcoded_words import ARTICLES, CONJUNCTIONS, ACRONYMS, PREPOSITIONS, VALID_TWO_LETTER_WORDS

class Styler():

    def __init__(self, title: str):
        self.title = title

    def is_article(self, word: str, articles: set=ARTICLES) -> bool:
        return word in articles

    def is_conjuction(self, word: str, conjuctions: set=CONJUNCTIONS) -> bool:
        return word in conjuctions

    def is_preposition(self, word: str, prepositions: set=PREPOSITIONS) -> bool:
        return word in prepositions

    def between_parantheses(self, word: str, max_word_length: int=4) -> bool:
        return word[0] == "(" and word[-1] == ")" and len(word) <= max_word_length + 2

    def is_acronym(
        self,
        word: str, 
        acronyms: set=ACRONYMS, 
        valid_two_letter_words: set=VALID_TWO_LETTER_WORDS
    ) -> bool:
        word_no_punc = word.translate(word.maketrans("", "", string.punctuation))
        cond = (
            word_no_punc in acronyms or 
            cutils.contains(word, {"&", "/"}) or
            self.between_parantheses(word) or
            len(word_no_punc) == 2 and word_no_punc not in valid_two_letter_words
        )

        return cond

    def is_plural_acronym(self, word: str, acronyms: set=ACRONYMS) -> bool:
        plural_acronyms = {acro + "s" for acro in acronyms}
        word_no_punc = word.translate(word.maketrans("", "", string.punctuation))
        
        return word_no_punc in plural_acronyms

    def lowercase_after_dash(self, word: str, dash_pos: int) -> str:
        before_dash = word[:dash_pos + 1].title()
        after_dash = word[dash_pos + 2:]

        return before_dash + word[dash_pos + 1].lower() + after_dash

    def clean_and_split(self, field: str) -> list:
        field = field.strip() # strip whitespace off ends
        field = " ".join(field.split()) # normalize whitespace to one
        field = field.lower()

        word_list = field.split(" ")

        return word_list

class ChicagoStyle(Styler):

    def get_correct_word(self, idx: int, word: str, word_list: list[str]) -> str:
        puncs = {":", "?", "!", ".", "--", "-"}
        
        if self.is_article(word) or self.is_conjuction(word) or self.is_preposition(word):
            correct_word = word.lower()
        else:
            correct_word = word.capitalize()

        if idx in {0, len(word_list) - 1} or word_list[idx - 1][-1] in puncs:
            correct_word = word.capitalize()
        if self.is_acronym(word):
            correct_word = word.upper()
        if self.is_plural_acronym(word):
            last_s = cutils.find_last_index(word, "s")
            correct_word = word[:last_s].upper() + "s" + word[last_s + 1:].upper()
        if "-" in word and word[-1] != "-":
            dash_pos = word.index("-")
            correct_word = self.lowercase_after_dash(word, dash_pos)

        return correct_word

    def get_correct_title(self):
        word_list = self.clean_and_split(self.title)

        corrected_list = []
        for idx, word in enumerate(word_list):
            correct_word = self.get_correct_word(idx, word, word_list)
            
            corrected_list.append(correct_word)
            
        return " ".join(corrected_list)
        