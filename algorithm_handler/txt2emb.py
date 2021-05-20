from danlp.models import load_bert_base_model
from math import ceil
import nltk
import numpy as np

##DATA PREPROCESSING

#Load test data
with open("test_data.txt", "r") as f:
    full_text = f.read()

def load_tokenizer():
    try:
        tokenizer = nltk.data.load("tokenizers/punkt/danish.pickle")
    except LookupError:
        nltk.download('punkt')
        tokenizer = nltk.data.load("tokenizers/punkt/danish.pickle")
    except Exception as E:
        raise E

#SPLIT INTO SENTS
tokenized_text = tokenizer.tokenize(full_text)

#CLEAN SENTS
def clean_sent(sent):
    #Do something with the paragraph signs and the numbers etc.
    return(sent)

cleaned_tokenized_text = [clean_sent(sent) for sent in tokenized_text]

model = load_bert_base_model()
embed_sent = lambda sent: np.array(model.embed_text(sent)[1])

import time
before = time.time()
embeded_all_sents = np.array([embed_sent(sent) for sent in cleaned_tokenized_text])
embedded_full_text = embeded_all_sents.mean(axis=0)
after = time.time()

time_taken = after - before
print(f"it took {time_taken:.2f} seconds")


