Tired of going through your bibtex files and manually applying weird title rules? Is the file getting messy, with many duplicate entries, missing or invalid fields? Bibtex_clean (bibtex_clean) is a CLI tool to clean bibtex files.

# Supported Rules:

* [Chicago](https://titlecaseconverter.com/rules/#CMOS)
# Supported Styles:

* [aer.bst](https://www.bibtex.com/s/bibliography-style-economic-aer/)

# Features:

* Merge duplicate entries
* Capitalize appropriate fields
    * Rules applied are naive. For example, "on" could be a preposition or an adjective, but "on" is always treated as a preposition.
* Warn if entry type is invalid
* Warn if entry is missing required fields
* Warn if entry has unsupported fields

# Usage:

## Requirements

A valid Python 3 installation.

## Installing

The easiest way is to install bibtex_clean from PyPI using pip:

```
pip install bibtex_clean
```

## Running

After installation, a bibtex_clean command should be exposed to anywhere on the command line.

```
bibtex_clean ./path/to/your/file
```

Will then output a file named "yourfile_clean.bib" in the same directory as your file. By default, bibtex_clean follows the AER style guide and uses Chicago Title Case. In the future, command line switches in the style of

```
bibtex_clean ./path/to/your/file -style="{style}"
```

will be supported.

# TODO:

* Additional styles
* Additional title case rules