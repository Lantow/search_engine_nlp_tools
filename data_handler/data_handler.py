from data_handler.connection_handler import PostgresConnection
import numpy as np
import nltk
import re
from tqdm import tqdm 


class DataHandler(PostgresConnection):
    
    def load_data(self):
        print("loading data")
        exec_str = "SELECT document_text FROM public.scrapers_retsinfodocument LIMIT 10"
        self.curr.execute(exec_str)
    
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
        tknz = lambda txt: self.tokenizer.tokenize(txt[0])
        try:
            self.tokenized_text = tqdm(map(tknz, self.curr), 
                                       "Tokenizing tekst text into sentances")
        except Exception as E:
            raise E
        
    def clean_sents(self):
        # For now we only remove \r and \n, as we might remove context useable by the BERT model
        pp_special_chars = lambda sent: re.sub("\s+", " ", re.sub("\r|\n|\t", "", sent))
        pp_numbers = lambda sent: sent
        preprocess_sent = lambda sent: pp_special_chars(pp_numbers(sent))
        preprocess_full_txt = lambda full_txt: map(preprocess_sent, full_txt)
        #Do something with the paragraph signs and the numbers etc.
        try:
            self.cleaned_tokenized_text = tqdm(map(preprocess_full_txt, self.tokenized_text),
                                               "cleaning sentances")
        except Exception as E:
            raise E
