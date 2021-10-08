# imports

from pathlib import Path

import bibtexparser

# globals

base_path = Path(__file__).parent.parent

articles = {
    "a",
    "an",
    "the"
}

conjunctions = {
    "and",
    "but",
    "for",
    "nor",
    "or",
    "so",
    "yet"
}

prepositions = {
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

acronyms = {
    "adtv",
    "amex",
    "apr",
    "arm",
    "bea",
    "cagr",
    "cao",
    "capex",
    "cb",
    "cd",
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
    "loi",
    "mmkt",
    "mtd",
    "nasdaq",
    "nav",
    "ncnd",
    "nda",
    "neer",
    "nyse",
    "p&l",
    "p/e",
    "pe",
    "pfd",
    "ppp",
    "ppplf",
    "psp",
    "qtd",
    "qte",
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
    "sec",
    "siv",
    "tsa",
    "tsr",
    "usa",
    "wc",
    "ytd",
    "ytm"
}

# functions

def is_article(word: str) -> bool:
    if word in articles:
        return True
    else:
        return False

def is_conjuction(word: str) -> bool:
    if word in conjunctions:
        return True
    else:
        return False

def is_preposition(word: str) -> bool:
    if word in prepositions:
        return True
    else:
        return False

def is_acronym(word: str) -> bool:
    if word in acronyms or "." in word:
        return True
    else:
        return False

def clean_and_split(field: str) -> list:
    field = field.strip() # strip whitespace off ends
    field = " ".join(field.split()) # normalize whitespace to one
    field = field.lower()

    word_list = field.split(" ")

    return word_list

with open(base_path / "test_files/cl_sg_bib.bib", encoding="utf8") as bib:
    bib_db = bibtexparser.load(bib)

for entry in bib_db.entries:
    try:
        title = entry["title"]
    except KeyError:
        entry["title"] = None
        continue
    
    word_list = clean_and_split(title)

    corrected_list = []
    for idx, word in enumerate(word_list):
        if is_article(word) or is_conjuction(word) or is_preposition(word):
            correct_word = word.lower()
        elif is_acronym(word):
            correct_word = word.upper()
        else:
            correct_word = word.title()

        if idx in {0, len(word_list)} or ":" in word_list[idx - 1]:
            correct_word = word.title()
        if "-" in word:
            dash_pos = word.index("-")
            correct_word = word[:dash_pos + 1] + word[dash_pos + 1].lower() + word[dash_pos + 2:]
        
        corrected_list.append(correct_word)
        
    correct_entry = " ".join(corrected_list)
    entry.update({"title": correct_entry})

with open(base_path / "cl_sg_corrected.bib", "w", encoding="utf8") as f:
    bibtexparser.dump(bib_db, f)