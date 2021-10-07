# imports

from pathlib import Path

import bibtexparser

# globals

base_path = Path(__file__).parent.parent

articles = [
    "a",
    "an",
    "the"
]

conjunctions = [
    "and",
    "but",
    "for",
    "nor",
    "or",
    "so",
    "yet"
]

prepositions = [
      'a',
      'abaft',
      'aboard',
      'about',
      'above',
      'absent',
      'across',
      'afore',
      'after',
      'against',
      'along',
      'alongside',
      'amid',
      'amidst',
      'among',
      'amongst',
      'an',
      'apropos',
      'apud',
      'around',
      'as',
      'aside',
      'astride',
      'at',
      'athwart',
      'atop',
      'barring',                                                                                                                                                                                                                             
      'before',
      'behind',
      'below',
      'beneath',
      'beside',
      'besides',
      'between',
      'beyond',
      'but',
      'by',
      'circa',
      'concerning',
      'despite',
      'down',
      'during',
      'except',
      'excluding',
      'failing',
      'following',
      'for',
      'from',
      'given',
      'in',
      'including',
      'inside',
      'into',
      'lest',
      'like',
      'mid',
      'midst',
      'minus',
      'modulo',
      'near',
      'next',
      'notwithstanding',
      'of',
      'off',
      'on',
      'onto',
      'opposite',
      'out',
      'outside',
      'over',
      'pace',
      'past',
      'per',
      'plus',
      'pro',
      'qua',
      'regarding',
      'round',
      'sans',
      'save',
      'since',
      'than',
      'through',
      'thru',
      'throughout',
      'thruout',
      'till',
      'times',
      'to',
      'toward',
      'towards',                                                                                                                                                                                                                             
      'under',
      'underneath',
      'unlike',
      'until',
      'unto',
      'up',
      'upon',
      'versus',
      'vs\.',
      'vs',
      'v\.',
      'v',
      'via',
      'vice',
      'with',
      'within',
      'without',
      'worth'
]

with open(base_path / "test_files/cl_sg_bib.bib", encoding="utf8") as bib:
    bib_db = bibtexparser.load(bib)




