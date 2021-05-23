from danlp.models import load_bert_base_model
import numpy as np
from data_handler import Data_handler


#https://www.psycopg.org/docs/cursor.html#cursor-iterable

class AlgorithmHandler(DataHandler):

    def load_tokenizer(self):
        try:
            self.tokenizer = nltk.data.load("tokenizers/punkt/danish.pickle")
        except LookupError:
            nltk.download('punkt')
            self.tokenizer = nltk.data.load("tokenizers/punkt/danish.pickle")
        except Exception as E:
            raise E

    def tokenize(self):
        tokenized_text = self.tokenizer.tokenize(full_text)