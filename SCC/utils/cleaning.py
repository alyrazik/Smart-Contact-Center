import re
import string

from camel_tools.disambig.mle import MLEDisambiguator
from camel_tools.tagger.default import DefaultTagger
from camel_tools.tokenizers.word import simple_word_tokenize


def clean_text_1(text):
    '''Make text lowercase, remove text in square brackets, remove punctuation and remove words containing numbers.'''
    text = text.lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\w*\d\w*', '', text)
    return text


def clean_text_2(text):
    '''Get rid of some additional punctuation and non-sensical text that was missed the first time around.'''
    text = re.sub('[‘’“”…]', '', text)
    text = re.sub('\n', '', text)
    return text

def nouns_adj(text):
    '''Given a string of text, tokenize the text and pull out only the nouns and adjectives.'''

    mled = MLEDisambiguator.pretrained()
    tagger = DefaultTagger(mled, 'pos')

    is_noun_adj = lambda pos: pos == 'noun'
    tokenized = simple_word_tokenize(text)
    tags = tagger.tag(tokenized)
    nouns_adj = [word for (word, pos) in zip(tokenized, tags) if is_noun_adj(pos)]
    return ' '.join(nouns_adj)