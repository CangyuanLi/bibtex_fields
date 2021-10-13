Python script to clean bibtex files. Relies on bibtexparser.

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

# TODO:

* CLI functionality
* Better acronym handling
* Better pretty-printing
* Colored terminal output (colorama)
* Additional styles
* Additional title case rules
* Better README