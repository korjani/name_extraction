## Author: Mehdi Korjani, korjani@gmail.com
## extract the names of all people mentions from contents and their roles (when available)

from __future__ import unicode_literals
import spacy
import pdb
import os
import sys
import glob
import argparse
import datefinder


# Load English tokenizer, tagger, parser, NER and word vectors
nlp = spacy.load('en_core_web_lg')


def remove_from_text(text, patern):
    patern_list = patern.split()
    text_list = text.split()
    result_words = [word for word in text_list if word not in patern_list]
    return result_words

# Find named entities and phrases

def extract_name(doc, tail):
    ## find entities from files
    for ent in doc.ents:

        ## if the entity is "preson" and the whole entity is in the same line
        if ent.label_ == 'PERSON' and ent.text.find('\n') == -1 and not ent.text.isspace():
            role = ''

            ## extract chunks from sentence
            for chunk in ent.sent.noun_chunks:

                ## find the correcponding chunk of entity and remove the entity from it to
                ## extract role (if any available)
                if chunk.text.find(ent.text) != -1:
                    ## remove ent from chunk
                    result = remove_from_text(chunk.text, ent.text)
                    result = ' '.join(result)

                    ## remove any date from results if result is not empty
                    ## TODO:
                    ## find other aspects that does not make sense and remove them
                    matches = datefinder.find_dates(result, source=True)
                    match = [w for w in matches]
                    if len(result) != 0 and len(match) != 0:
                        ## assume only one date in the reuslts
                        result = remove_from_text(result, match[0][1])
                        result = ' '.join(result)

                    role = result

            ## don't print if the role is only one character
            if len(role) > 2 or len(role) == 0:
                print(ent, role, tail)




def check_arg(args=None):
    parser = argparse.ArgumentParser(description='extract name and role from docs')

    parser.add_argument('-d', '--directory', default='data/', help='directory')
    results = parser.parse_args(args)
    return results.directory


if __name__ == '__main__':
    dir_path = check_arg(sys.argv[1:])

    ## iterate through all files in the directory
    ## Process whole documents
    for file_path in glob.iglob(os.path.join(dir_path, '*')):
        ## extract file names from path
        head, tail = os.path.split(file_path)

        ## read files
        text = open(file_path).read()

        ## make spacy doc
        doc = nlp(text.decode('utf8'))

        ## extract name and role and print the along side file name
        extract_name(doc, tail)

