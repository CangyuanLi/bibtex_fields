import json
from pathlib import Path
import string
from typing import Optional

import bibtexparser
import colorama
from colorama import Fore, Style

BASE_PATH = Path(__file__).resolve().parents[1]

ARTICLES = {
    "a",
    "an",
    "the"
}

CONJUNCTIONS = {
    "and",
    "but",
    "for",
    "nor",
    "or",
    "so",
    "yet"
}

PREPOSITIONS = {
    "abaft",
    "aboard",
    "about",
    "above",
    "absent",
    "across",
    "afore",
    "after",
    "against",
    "along",
    "alongside",
    "amid",
    "amidst",
    "among",
    "amongst",
    "apropos",
    "apud",
    "around",
    "as",
    "aside",
    "astride",
    "at",
    "athwart",
    "atop",
    "barring",                                                                                                                                                                                                                             
    "before",
    "behind",
    "below",
    "beneath",
    "beside",
    "besides",
    "between",
    "beyond",
    "by",
    "circa",
    "concerning",
    "despite",
    "down",
    "during",
    "except",
    "excluding",
    "failing",
    "following",
    "for",
    "from",
    "given",
    "in",
    "including",
    "inside",
    "into",
    "lest",
    "like",
    "mid",
    "midst",
    "minus",
    "modulo",
    "near",
    "next",
    "notwithstanding",
    "of",
    "off",
    "on",
    "onto",
    "opposite",
    "out",
    "outside",
    "over",
    "pace",
    "past",
    "per",
    "plus",
    "pro",
    "qua",
    "regarding",
    "round",
    "sans",
    "save",
    "since",
    "than",
    "through",
    "thru",
    "throughout",
    "thruout",
    "till",
    "times",
    "to",
    "toward",
    "towards",                                                                                                                                                                                                                             
    "under",
    "underneath",
    "unlike",
    "until",
    "unto",
    "up",
    "upon",
    "versus",
    "vs.",
    "vs",
    "v.",
    "v",
    "via",
    "vice",
    "with",
    "within",
    "without",
    "worth"
}

ACRONYMS = {
    "aer",
    "esg",
    "qje",
    "jel",
    "jpe",
    "jfe",
    "jstor",
    "nber",
    "qje",
    "qtd",
    "qte",
    "ssrn",
    "usa",
    "adtv",
    "amex",
    "apr",
    "arm",
    "bea",
    "cagr",
    "cao",
    "capex",
    "cfa",
    "cfm",
    "cfo",
    "cia",
    "cisa",
    "cma",
    "cmo",
    "cmp",
    "cob",
    "coo",
    "cpa",
    "cpp",
    "cso",
    "cto",
    "djia",
    "eft",
    "eps",
    "etf",
    "fdic",
    "forex",
    "frb",
    "gdp",
    "gmp",
    "gnp",
    "ipo",
    "ira",
    "llc",
    "lbo",
    "loi",
    "mit",
    "mlb",
    "mmkt",
    "mtd",
    "nasa",
    "nasdaq",
    "nav",
    "nba",
    "ncnd",
    "nda",
    "neer",
    "nfl",
    "nsa",
    "nyse",
    "nyu",
    "pfd",
    "ppp",
    "ppplf",
    "psp",
    "rbi",
    "reit",
    "roa",
    "roce",
    "roe",
    "roi",
    "roic",
    "rona",
    "ros",
    "sba",
    "sbo",
    "sec",
    "sif",
    "siv",
    "tsa",
    "tsr",
    "ucla",
    "ytd",
    "ytm"
}

VALID_TWO_LETTER_WORDS = {
    "am",
    "an",
    "as",
    "at",
    "be",
    "by",
    "do",
    "he",
    "if",
    "in",
    "is",
    "it",
    "me",
    "my",
    "of",
    "on",
    "or",
    "ox",
    "pi",
    "so",
    "to",
    "up",
    "we"
} # no "us" because in title it is much more likely to refer to "US"

class ChicagoWord(str):

    def __init__(self, word: str):
        self.word = word

    def handle_article(self, articles: set[str]):
        if self.word in articles:
            correct_word = self.word.lower()
        else:
            correct_word = self.word.capitalize()

        return type(self)(correct_word)

    def handle_conjunction(self, conjuctions: set[str]):
        if self.word in conjuctions:
            correct_word = self.word.lower()
        else:
            correct_word = self.word.capitalize()

        return type(self)(correct_word)
    
    def handle_preposition(self, prepositions: set[str]):
        if self.word in prepositions:
            correct_word = self.word.lower()
        else:
            correct_word = self.word.capitalize()

        return type(self)(correct_word)

    def handle_
