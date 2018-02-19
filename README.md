# Name Extraction
Use NLP methods to extract the names of all people mentions from text content and their roles (when available).

Output is tuple of
People names, role, and name of the file


## Requirements

beside install requirments.txt,

    pip install -r requirements.txt
user should install spacy model:

    python -m spacy download en_core_web_lg

## How to run the code

    python name_extraction.py --directory=[directory name] > [results.txt]
e.g.

    python name_extraction.py --directory='data/' >results.txt

## Evaluation and issues
In general finding the role has less accuracy comparing to finding a name
The role is extracted by chunking the part of text where the name is extracted
The model can be extended by considering POS for finding role and better preprocessing the text

No preprocessing has been done on the input text,
e.g.,
    sometimes “Don t” is considered as a name because of lack of punctuation and the model confuses with name “Don”

Adding hard rule may increase the accuracy of role detection.
e.g., words between semicolon after name is a role!

Also it considered couple of brand names like “youtube” or “Android” as a name which can be solve by assigning a predefined dictionary to remove them.

By analyzing 7 text files (+8000 words) the model extracted 21 names, one of them are completely wrong (e.g. “Don t”) 3 names had added prefix, and 2 roles are not selected
### Model accuracy ~ 67%



