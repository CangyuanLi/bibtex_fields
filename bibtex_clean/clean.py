import json
from pathlib import Path

import bibtexparser
import colorama
from colorama import Fore, Style

from .title_styler import ChicagoStyle

# Globals

colorama.init(autoreset=True)

BASE_PATH = Path(__file__).resolve().parents[1]

# Functions

def combine_duplicate_entries(bib: list) -> tuple[list, list]:    
    new_bib = []
    duplicate_entries = []
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

            duplicate_report = (
                f"  {Fore.CYAN}{k} {Style.RESET_ALL}occured {Fore.YELLOW}{num_occurences}" 
                f" {Style.RESET_ALL}times. Automatically merged."
            )
            duplicate_entries.append(duplicate_report)
        else:
            new_bib.append(bib[v[0]])
    
    return new_bib, duplicate_entries

def open_style_guide(style: str) -> tuple[dict, list]:
    with open(BASE_PATH / f"bibtex_clean/style_fields/{style}.json") as style_file:
        style_dict = json.load(style_file)

    fields_to_titlecase = style_dict["FIELDS_TO_TITLECASE"]
    del style_dict["FIELDS_TO_TITLECASE"]

    return style_dict, fields_to_titlecase

def get_base_fields(entry: dict) -> set:
    return {field for field in entry if field.lower() == field}
        
def validate_entry(style_dict: dict, entry: dict) -> dict:
    error_dict = {
        "invalid_entry_types": [],
        "invalid_fields": [],
        "missing_required_fields": []
    }

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
            missing_str2 = (
                f"  {Fore.CYAN}{entry_name} {Style.RESET_ALL}is missing "
                f"{Fore.LIGHTMAGENTA_EX}{missing_str1}"
            )
            error_dict["missing_required_fields"].append(missing_str2)

        invalid_temp = [base_field for base_field in base_fields if base_field not in all_style_fields]

        if len(invalid_temp) != 0:
            invalid_str1 = ", ".join(invalid_temp)
            invalid_str2 = (
                f"  {Fore.CYAN}{entry_name} {Style.RESET_ALL}has invalid fields "
                f"{Fore.LIGHTMAGENTA_EX}{invalid_str1}"
            )
            error_dict["invalid_fields"].append(invalid_str2)

    except KeyError:
        error_dict["invalid_entry_types"].append(f"  {field_id} is not a valid entry type")

    return error_dict

def print_results(header: str, outlist: list, sep: str="*") -> None:
    length = len(outlist)
    if length > 0:
        header_box = sep * (len(header) + 2 - 3 + len(str(length)) + 1)

        print(header_box)
        print(sep + header.format(f"{Fore.YELLOW}{length}{Style.RESET_ALL}") + sep)
        print(header_box)

        for out in sorted(outlist):
            print(out)

        print("\n")

def gen_report(report_dict: dict) -> None:
    print_results(
        header="Found and merged {} duplicate entries.",
        outlist=report_dict["duplicate_entries"]
    )

    print_results(
        header="Found {} entries that are not valid entry types.",
        outlist=report_dict["invalid_entry_types"]
    )

    print_results(
        header="Found {} entries that are missing required fields.",
        outlist=report_dict["missing_required_fields"]
    )

    print_results(
        header="Found {} entries with invalid fields.",
        outlist=report_dict["invalid_fields"]
    )

def clean_file(filepath, style, quiet):
    file = Path(filepath)
    with open(file, encoding="utf8") as bib:
        bib_db = bibtexparser.load(bib)

    style_dict, fields_to_titlecase = open_style_guide(style)
    bib_db.entries, duplicate_entries = combine_duplicate_entries(bib_db.entries)

    error_list = []
    for entry in bib_db.entries:
        # entry["ID"] = entry["ID"].lower()
        entry["ENTRYTYPE"] = entry["ENTRYTYPE"].lower()
        error_dict = validate_entry(style_dict=style_dict, entry=entry)
        error_list.append(error_dict)

        for field in fields_to_titlecase:
            try:
                field_content = entry[field]
            except KeyError:
                continue
            
            correct_field = ChicagoStyle(field_content).get_correct_title()
            entry.update({field: correct_field})

    newfilename = f"{file.stem}_cleaned.bib"
    newpath = file.parent / newfilename
    with open(newpath, "w", encoding="utf8") as f:
        bibtexparser.dump(bib_db, f)

    report_dict = {
        "duplicate_entries": duplicate_entries,
        "invalid_entry_types": [],
        "missing_required_fields": [],
        "invalid_fields": []
    }
    for error_dict in error_list:
        for k in error_dict:
            report_dict[k] += error_dict[k]
            
    if quiet is False:
        gen_report(report_dict)
