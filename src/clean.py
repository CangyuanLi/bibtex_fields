# imports

import argparse
import json
from pathlib import Path
import string

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
    "qje",
    "jf",
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
    "loi",
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
    "siv",
    "tsa",
    "tsr",
    "ucla",
    "ytd",
    "ytm"
}

valid_two_letter_words = {
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
    "us",
    "we"
}

duplicate_entries = []
invalid_entry_types = []
invalid_fields = []
missing_required_fields = []

# parser

parser = argparse.ArgumentParser(description="Clean bibtex file")
parser.add_argument(
    "filepath",
    type=str,
    help="path to bibtex file"
)
parser.add_argument(
    "-q",
    "--quiet",
    action="store_true",
    required=False,
    help="suppresses output"
)

args = parser.parse_args()

# functions

def contains(string: str, elements: set) -> bool:
    return any(elem in string for elem in elements)

def combine_duplicate_entries(bib: list) -> list:
    new_bib = []
    entry_positions = dict()
    for idx, entry in enumerate(bib):
        if entry["ID"] in entry_positions.keys():
            entry_positions[entry["ID"]].append(idx)
        else:
            entry_positions[entry["ID"]] = [idx]
    
    for k, v in entry_positions.items():
        num_occurences = len(v)
        if num_occurences > 1:
            for i in v[1:num_occurences - 1]:
                bib[v[0]].update(bib[i])
            new_bib.append(bib[v[0]])

            duplicate_report = f"  -{k} occured {num_occurences} times. Automatically merged."
            duplicate_entries.append(duplicate_report)
        else:
            new_bib.append(bib[v[0]])
    
    return new_bib

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
    word_no_punc = word.translate(word.maketrans('', '', string.punctuation))
    if (
        word_no_punc in acronyms or 
        contains(word, {"&", "/"}) or
        between_parantheses(word) or
        len(word_no_punc) == 2 and word_no_punc not in valid_two_letter_words
    ):
        return True
    else:
        return False

def lowercase_after_dash(word: str, dash_pos: int):
    before_dash = word[:dash_pos + 1].title()
    after_dash = word[dash_pos + 2:]
    
    return before_dash + word[dash_pos + 1].lower() + after_dash

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
            missing_str2 = f"  -{entry_name} is missing {missing_str1}"
            missing_required_fields.append(missing_str2)

        invalid_temp = [base_field for base_field in base_fields if base_field not in all_style_fields]

        if len(invalid_temp) != 0:
            invalid_str1 = ", ".join(invalid_temp)
            invalid_str2 = f"  -{entry_name} has invalid fields {invalid_str1}"
            invalid_fields.append(invalid_str2)

    except KeyError:
        invalid_entry_types.append(f"-{field_id} is not a valid entry type")

    return None

def print_results(header: str, outlist: int, sep: str="*") -> None:
    length = len(outlist)
    if length > 0:
        header_box = sep * (len(header) + 2 - 3 + len(str(length)) + 1)

        print(header_box)
        print(sep + header.format(length) + sep)
        print(header_box)

        for out in sorted(outlist):
            print(out)

        print("\n")

    return None

def gen_report() -> None:
    print_results(
        header="Found and merged {} duplicate entries.",
        outlist=duplicate_entries,
    )

    print_results(
        header="Found {} entries that are not valid entry types.",
        outlist=invalid_entry_types
    )

    print_results(
        header="Found {} entries that are missing required fields.",
        outlist=missing_required_fields
    )

    print_results(
        header="Found {} entries with invalid fields.",
        outlist=invalid_fields
    )
    
def escape_latex_chars(field: str) -> str:
    return None

def main(filepath=args.filepath, quiet=args.quiet):
    with open(filepath, encoding="utf8") as bib:
        bib_db = bibtexparser.load(bib)

    style_dict, fields_to_titlecase = open_style_guide("aer")
    bib_db.entries = combine_duplicate_entries(bib_db.entries)

    for entry in bib_db.entries:
        entry["ID"] = entry["ID"].lower()
        entry["ENTRYTYPE"] = entry["ENTRYTYPE"].lower()
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
                    correct_word = lowercase_after_dash(word, dash_pos)
                
                corrected_list.append(correct_word)
                
            correct_field = " ".join(corrected_list)
            entry.update({field: correct_field})

    newfilename = f"{Path(filepath).stem}_cleaned.bib"
    newpath = Path(filepath).parent / newfilename
    with open(newpath, "w", encoding="utf8") as f:
        bibtexparser.dump(bib_db, f)

    if quiet == False:
        gen_report()

if __name__ == "__main__":
    main()