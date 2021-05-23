from dataclasses import dataclass
import numpy as np
from data_handler.connection_handler import PostgresConnection

from os import getenv 
from math import ceil
import nltk



# @with_conn
# def test_func(exec_str, curr=None, **kwds):
#     print(type(curr))
#     curr.execute(exec_str)
#     t = [c[0] for c in curr]
#     return t[1:20]

# t = test_func("""SELECT document_text from public.scrapers_retsinfodocument""")

class DataHandler(PostgresConnection):
    
    # def __init__(self, raw_text_data):
    #     super(DataHandler, self).__init__()
    
    def load_data(self):
        exec_str = "SELECT document_text from public.scrapers_retsinfodocument"
        self.raw_text_data = self.curr.execute(exec_str)
    
    def load_tokenizer(self):
        try:
            self.tokenizer = nltk.data.load("tokenizers/punkt/danish.pickle")
        except LookupError:
            nltk.download('punkt')
            self.tokenizer = nltk.data.load("tokenizers/punkt/danish.pickle")
        except Exception as E:
            raise E
        
    def tokenize_raw_text_data(self):
        if not hasattr(self, "tokenizer"): self.load_tokenizer()
        self.tokenized_text = map(self.tokenizer.tokenize, self.raw_text_data)
        
    def clean_sents(self):
        self.tokenize_raw_text_data()
        pp_special_chars = lambda sent: sent
        pp_numbers = lambda sent: sent
        preprocess = lambda sent: pp_special_chars(pp_numbers(sent))
        #Do something with the paragraph signs and the numbers etc.
        self.cleaned_tokenized_text = map(preprocess, self.tokenized_text)




# DH = DataHandler(raw_text_data=np.array([1,2,3]))
with DataHandler(raw_text_data=np.array([1,2,3])) as DH: 
    DH.load_data()
    # DH.tokenize_raw_text_data()