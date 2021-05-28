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




# DH = DataHandler()
# DH.load_data()

# with DataHandler() as DH:
#     DH.load_data()
#     DH.tokenize_raw_text_data()
#     DH.clean_sents()
#     pages_len = []
#     print(sum([len(list(p)) for p in DH.cleaned_tokenized_text]))
    # for i, page in enumerate(DH.cleaned_tokenized_text):
    #     p = list(page)
    #     if i == 500:
    #         print(p[0])
    #     pages_len.append(len(p))
    # print(sum(pages_len), end="\n")
    # DH.tokenize_raw_text_data()
    
    
# @with_conn
# def test_func(exec_str, curr=None, **kwds):
#     print(type(curr))
#     curr.execute(exec_str)
#     t = [c[0] for c in curr]
#     return t[1:20]

# t = test_func("""SELECT document_text from public.scrapers_retsinfodocument""")

