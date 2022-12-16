import setuptools

setuptools.setup(
    name="bibtex_clean",
    version="0.0.1",
    author="Cangyuan Li",
    author_email="everest229@gmail.com",
    description="CLI utility to clean bibtex files.",
    url="https://github.com/CangyuanLi/bibtex_fields",
    packages=["bibtex_clean"],
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
