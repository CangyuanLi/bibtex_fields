# imports

import argparse
import json
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
    "aer",
    "adtv",
    "amex",
    "ap",
    "apr",
    "arm",
    "bea",
    "ca",
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
    "jf",
    "jfe",
    "jstor",
    "llc",
    "loi",
    "mlb",
    "mmkt",
    "mtd",
    "nasa",
    "nasdaq",
    "nav",
    "nba",
    "nber",
    "ncnd",
    "nda",
    "neer",
    "nfl",
    "nsa",
    "nyse",
    "nyu",
    "p&l",
    "p/e",
    "pe",
    "pfd",
    "ppp",
    "ppplf",
    "psp",
    "qje",
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
    "sbo",
    "sec",
    "siv",
    "ssrn",
    "tsa",
    "tsr",
    "ucla",
    "us",
    "usa",
    "wc",
    "ytd",
    "ytm"
}

fields = {
    "booktitle",
    "journal",
    "title"
}

invalid_entry_types = []
invalid_fields = []
missing_required_fields = []

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

def between_parantheses(word: str) -> bool:
    if word[0] == "(" and word[-1] == ")" and len(word) <= 4:
        return True
    else:
        return False

def is_acronym(word: str) -> bool:
    if word in acronyms or "." in word or between_parantheses(word):
        return True
    else:
        return False

def clean_and_split(field: str) -> list:
    field = field.strip() # strip whitespace off ends
    field = " ".join(field.split()) # normalize whitespace to one
    field = field.lower()

    word_list = field.split(" ")

    return word_list

def open_style_guide(style: str) -> dict:
    with open(base_path / f"style_fields/{style}.json") as style_file:
        style_dict = json.load(style_file)

    fields_to_titlecase = style_dict["FIELDS_TO_TITLECASE"]
    del style_dict["FIELDS_TO_TITLECASE"]

    return style_dict, fields_to_titlecase

def get_base_fields(entry):
    return {field for field in entry.keys() if field.lower() == field}
        
def validate_entry(style_dict: dict, entry: dict) -> None:
    field_id = entry["ENTRYTYPE"]
    entry_name = entry["ID"]
    
    try:
        style_entry = style_dict[field_id]
        entry_fields = set(entry.keys())
        base_fields = get_base_fields(entry)
        all_style_fields = style_entry["required"] + style_entry["optional"]

        required_fields = set(style_entry["required"])
        intersection = entry_fields.intersection(required_fields)

        if len(intersection) < len(required_fields):
            missing_fields = set(required_fields) - set(intersection)

            missing_str1 = ", ".join(missing_fields)
            missing_str2 = f"-{entry_name} is missing {missing_str1}"
            missing_required_fields.append(missing_str2)

        invalid_temp = [base_field for base_field in base_fields if base_field not in all_style_fields]

        if len(invalid_temp) != 0:
            invalid_str1 = ", ".join(invalid_temp)
            invalid_str2 = f"-{entry_name} has invalid fields {invalid_str1}"
            invalid_fields.append(invalid_str2)

    except KeyError:
        invalid_entry_types.append(f"-{field_id} is not a valid entry type")

    return None

def gen_report() -> None:
    num_invalid_entries = len(invalid_entry_types)
    num_invalid_fields = len(invalid_fields)
    num_missing_req_fields = len(missing_required_fields)

    if num_invalid_entries != 0:
        header_box = ""
        for _ in range(0, len("*Found entries that are not valid entry types.*") + len(str(num_invalid_entries)) + 1):
            header_box += "*"

        print(header_box)
        header = f"*Found {num_invalid_entries} entries that are not valid entry types.*"
        print(header)
        print(header_box)
        for out in invalid_entry_types:
            print(out)

    if num_missing_req_fields != 0:
        header_box = ""
        for _ in range(0, len("*Found entries that are missing required fields.*") + len(str(num_missing_req_fields)) + 1):
            header_box += "*"
        print("\n")
        print(header_box)
        header = f"*Found {num_missing_req_fields} entries that are missing required fields.*"
        print(header)
        print(header_box)
        for out in missing_required_fields:
            print(out)
    
    if num_invalid_fields != 0:
        header_box = ""
        for _ in range(0, len("*Found entries with invalid fields.*") + len(str(num_invalid_fields)) + 1):
            header_box += "*"
        print("\n")
        print(header_box)
        header = f"*Found {num_invalid_fields} entries with invalid fields.*"
        print(header)
        print(header_box)
        for out in invalid_fields:
            print(out)
    
def escape_latex_chars(field: str) -> str:
    return None

with open(base_path / "test_files/cl_sg_bib.bib", encoding="utf8") as bib:
    bib_db = bibtexparser.load(bib)

style_dict, fields_to_titlecase = open_style_guide("aer")

for entry in bib_db.entries:
    validate_entry(style_dict=style_dict, entry=entry)

    for field in fields_to_titlecase:
        try:
            field_content = entry[field]
        except KeyError:
            continue
        
        word_list = clean_and_split(field_content)

        corrected_list = []
        for idx, word in enumerate(word_list):
            if is_article(word) or is_conjuction(word) or is_preposition(word):
                correct_word = word.lower()
            else:
                correct_word = word.title()

            if idx in {0, len(word_list) - 1} or word_list[idx - 1][-1] in {":", "?", "!", ".", "--"}:
                correct_word = word.title()
            if is_acronym(word):
                correct_word = word.upper()
            if "-" in word:
                dash_pos = word.index("-")
                correct_word = word[:dash_pos + 1].title() + word[dash_pos + 1].lower() + word[dash_pos + 2:]
            
            corrected_list.append(correct_word)
            
        correct_field = " ".join(corrected_list)
        entry.update({field: correct_field})

gen_report()

with open(base_path / "cl_sg_corrected.bib", "w", encoding="utf8") as f:
    bibtexparser.dump(bib_db, f)