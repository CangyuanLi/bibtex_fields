# bibtex_clean: simple way to format and validate .bib files
![PyPI - Downloads](https://img.shields.io/pypi/dm/bibtex_clean)

## What is it?

Tired of going through your bibtex files and manually applying weird title rules? Is the file getting messy, with many duplicate entries, missing or invalid fields? **bibtex_clean** is a CLI tool to clean bibtex files.

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

## Dependencies

- [bibtexparser - Parses your bibtex file]
- [colorama - Pretty terminal output]

## Installing

The easiest way is to install bibtex_clean from PyPI using pip:

```
pip install bibtex_clean
```

## Running

After installation, a bibtex_clean command should be exposed to anywhere on the command line.

```shell
bibtex_clean /path/to/your/file
```

Will then output a file named "yourfile_clean.bib" in the same directory as your file. By default, bibtex_clean follows the AER style guide and uses Chicago Title Case. In the future, command line switches in the style of

```shell
bibtex_clean /path/to/your/file -style="{style}"
```

will be supported.

To specify the name of the cleaned .bib file, simply do

```shell
bibtex_clean /path/to/your/file /path/to/new/file
```

# TODO:

* Additional styles
* Additional title case rules