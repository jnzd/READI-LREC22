"""The diversity module contains functions allowing to calculate notions related to text diversity. 
Currently it's only the text token ratio and noun-only version.
These ratios can have variants which can be selected by changing the mode parameter.
For instance, mode == "root" will square the denominator of the ratio, and is supposed to be more robust for longer texts.
"""
import math
import string
from .. import utils
# Lexico-semantic features :
# ~ Difficulty of voc in text, like TTR/RTTR/CTTR.
# need to find something about yule's k it seems to be used sometimes, but what does it mean?
# Other stuff : n-gram lexical features, like word or character n-grams.
# POS based lexical features (i.e ttr but with nouns or other stuff)
# Can also do density (percentage of content words and function words)
# Also need to do word-list based features, 


# The following measures are for text diversity:
def type_token_ratio(text, nlp = None, mode = None):
    """
    Outputs two ratios : ttr and root ttr : number of lexical items / number of words

    :param str text: Content of a text, converted to string if it's already a list of tokens
    :param str mode: Which version of the ttr to return
    :return: text token ratio, mode can be "root", "corrected", and defaults to standard (TTR)
    :rtype: float
    """
    from collections import Counter
    # Convert to string if list/list of lists + handle punctuation.
    doc = utils.convert_text_to_string(text)

    # NOTE: Maybe just use spacy instead to remove punctuation
    doc = doc.translate(str.maketrans('', '', string.punctuation))
    

    nb_unique = len(Counter(doc.split()))
    nb_tokens = len(doc.split())
    #TODO : handle what happens if we receive an empty text as input => nb_unique / tokens = 0
    #Maybe warn the user and send an unusable ratio, such as two? I suppose. 

    if nb_tokens == 0:
        print("WARNING : Current text's content is empty, return value has been set to -1")
        return -1

    if mode == "corrected":
        #print("DEBUG: Returning Corrected TTR ratio = ",nb_unique,"/",math.sqrt(2*nb_tokens),":",nb_unique/math.sqrt(2*nb_tokens))
        return(nb_unique/math.sqrt(2*nb_tokens))
    
    elif mode == "root":
        #print("DEBUG: Returning Root TTR ratio = ",nb_unique,"/",mqth.sqrt(nb_tokens),":",nb_unique/math.sqrt(nb_tokens))
        return(nb_unique/math.sqrt(nb_tokens))
    
    else:
        #print("DEBUG: Returning TTR ratio = ",nb_unique,"/",nb_tokens,":",nb_unique/nb_tokens)
        return(nb_unique/nb_tokens)

# The following methods use a spacy model to recognize lexical items.
def noun_token_ratio(text,nlp=None, mode = None):
    """
    Outputs variant of the type token ratio, the TotalNoun/Noun Ratio.

    :param str text: Content of a text, converted to string if it's already a list of tokens
    :param nlp: What natural language processor to use, currently only spacy is supported.
    :type nlp: spacy.lang
    :param str mode: Which version of the ttr to return
    :return: noun token ratio, mode can be "root", "corrected", and defaults to standard (TTR)
    :rtype: float
    """
    from collections import Counter
    if isinstance(text, str):
        doc = text

    elif any(isinstance(el, list) for el in text):
        doc = ''
        for sentence in text:
            doc = doc + ' ' + ' '.join(sentence)
        
    elif isinstance(text, list):
        doc = ' '.join(text)

    #TODO : check type of current nlp try catch
    nouns = [token.text for token in nlp(doc) if (not token.is_punct and token.pos_ == "NOUN")]
    nb_unique = len(Counter(nouns))
    nb_tokens = len(nouns)

    if nb_tokens == 0:
        print("WARNING : Current text's content is empty or no nouns have been recognized, return value has been set to -1")
        return -1

    if mode == "corrected":
        #print("DEBUG: Returning Corrected TTR ratio = ",nb_unique,"/",math.sqrt(2*nb_tokens),":",nb_unique/math.sqrt(2*nb_tokens))
        return(nb_unique/math.sqrt(2*nb_tokens))
    
    elif mode == "root":
        #print("DEBUG: Returning Root TTR ratio = ",nb_unique,"/",mqth.sqrt(nb_tokens),":",nb_unique/math.sqrt(nb_tokens))
        return(nb_unique/math.sqrt(nb_tokens))
    
    else:
        #print("DEBUG: Returning TTR ratio = ",nb_unique,"/",nb_tokens,":",nb_unique/nb_tokens)
        return(nb_unique/nb_tokens)
    