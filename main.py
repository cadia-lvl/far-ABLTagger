
from typing import Optional
from fastapi import FastAPI
from fastapi.responses import Response, JSONResponse, HTMLResponse
from pydantic import BaseModel
from typing import Optional

import traceback
import sys

from colored import fg, attr


__version__ = 0.1

app = FastAPI(
    title="icesum",
    description="Sumerizes icelandic articles"
)


sys.path.insert(0, "./ABLTagger")
from tokenizer import split_into_sentences
from ABLTagger import ABLTagger, Embeddings, Vocab, Utils
import argparse
parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
parser.add_argument("--model", default="Full")
parser.add_argument("--tag_type", default="combined")
parser.add_argument("--tokenize", default='store_true')
args = parser.parse_args(['@'+"model_args.txt"])

# model file names
model_folder = './ABLTagger/models/' + args.model + '/'
chars_file = model_folder + 'characters.txt'
words_file = model_folder + 'words.txt'
tags_coarse_file = model_folder + 'tags_coarse.txt'
tags_fine_file = model_folder + 'tags_fine.txt'
morphlex = model_folder + 'morphlex.txt'
coarse_emb_file = model_folder + 'coarse_tagset.txt'


# load training time model arguments
from tag import read_arguments_from_file
args = argparse.Namespace(**vars(args), **vars(read_arguments_from_file(model_folder + 'args.' + args.tag_type)))

# load words and tagsets used at training time
if args.tag_type in ('combined', 'coarse'):
    VocabTagsCoarse = Utils.build_vocab_tags(tags_coarse_file)

if args.tag_type in ('combined', 'fine'):
    coarse_embeddings = Embeddings(coarse_emb_file)
    VocabTagsFine = Utils.build_vocab_tags(tags_fine_file)

train_words = list(Utils.read(words_file))
char_list = []
for charline in open(chars_file):
    characters = charline.strip().split('\t')
    for c in characters:
        char_list.append(c)

morphlex_embeddings = Embeddings(morphlex)
print("Morphological lexicon embeddings in place")
VocabCharacters = Vocab.from_corpus([char_list])
VocabWords, WordFrequency = Utils.build_word_dict(train_words)

tagger_coarse = ABLTagger(VocabCharacters, VocabWords, VocabTagsCoarse, WordFrequency, morphlex_embeddings, None, args)
print(fg('blue'), "Loading pre-tagger..." + attr('reset') + attr('reset'), end='\r')
tagger_coarse.load_model(model_folder + 'model.combined_coarse')

tagger_fine = ABLTagger(VocabCharacters, VocabWords, VocabTagsFine, WordFrequency, morphlex_embeddings, coarse_embeddings, args)
print(fg('blue'), "Loading tagger...    " + attr('reset') + attr('reset'), end='\r')
tagger_fine.load_model(model_folder + 'model.combined_fine')
"""
for i in args.input:
    tag_simple(i, args.output, tagger_coarse)
    tag_augmented(i+args.output, args.output, tagger_fine)
    os.remove(i+args.output)
    shutil.move(i+args.output+args.output, i+args.output)
"""
print('Done!              ')


@app.get('/', response_class=HTMLResponse)
def home() -> str:
    return """
<html>
    <head><title>icesum API</title></head>
    <body>
        <h1>ABLTagger API Server v{0}</h1>
        <ul><li><a href="/docs">Documentation</a></li></ul>
    </body>
</html>
""".format(__version__)

@app.post('/tag_simple/impl')
def tag(input_text : str):
    global args, tagger_coarse, tagger_fine
    tag_simple = []
    if input_text.strip() != '':
        if args.tokenize:
            simple_tokens = []
            g = split_into_sentences(input_text.strip())
            for sentence in g:
                simple_tokens += sentence.split()
        else:
            simple_tokens = input_text.strip().split()
        print("tagger_coarse:",list(tagger_coarse.tag_sent(simple_tokens)))
        tokens, tags = [], []
        for token, tag in tagger_coarse.tag_sent(simple_tokens):
            tokens.append(token)
            tags.append(tag)
        print("Tokens:",tokens)
        print("Tags:",tags)
        print("Fine:",list(tagger_fine.tag_sent(tokens, tags)))
        arr = []
        for token, tag in tagger_fine.tag_sent(tokens, tags):
            arr += [[token,tag]]
        return JSONResponse(content={"output":arr})
    return ""

