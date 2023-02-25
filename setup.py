import setuptools

with open("bibtex_clean/_version.py") as f:
    lines = f.readlines()
    version = lines[0].strip("\n").split("=")[1].strip()

setuptools.setup(
    name="bibtex_clean",
    version="0.0.5",
    author="Cangyuan Li",
    author_email="everest229@gmail.com",
    description="CLI utility to clean bibtex files.",
    url="https://github.com/CangyuanLi/bibtex_fields",
    packages=["bibtex_clean"],
    include_package_data=True,
    install_requires=[
        "bibtexparser",
        "colorama",
        "pycutils",
    ],
    entry_points={
        "console_scripts": [
            "bibtex_clean=bibtex_clean.cli:main"
        ]
    },
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)
