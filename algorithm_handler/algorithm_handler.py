from danlp.models import load_bert_base_model
import numpy as np
from data_handler.data_handler import DataHandler
from tqdm import tqdm 

#https://www.psycopg.org/docs/cursor.html#cursor-iterable

class AlgorithmHandler(DataHandler):

    def embed_text(self):
        model = load_bert_base_model()
        
        def embed_sent(sent):
            # the DAnlp bert base model cant handle more than 512 tokens
            # the following try/except solves the symptom but not the root cause.
            # OBS! when root cause is solved the folowing code may be used instead:              
            # embed_sent = lambda sent: model.embed_text(sent)
            try:
                return model.embed_text(sent)
            except Exception as E:
                if "The size of tensor a" and "must match the size of tensor b" in str(E):
                    #n is an arbitrary low number. OBS! This will still fail, if each char becomes a token
                    # TODO: this partially be solved with a better word tokenizer  
                    n= 800
                    # Here the long sentance is split and embedded, whereafter an average is returned
                    return np.array([model.embed_text(sent[i:i+n])[1].numpy() 
                                for i in range(0, len(sent), n)]).mean(axis=0)
                else: 
                    raise E
                
        embed_sent_l = lambda sent: embed_sent(sent)
        embed_full_txt = lambda full_txt: map(embed_sent_l, full_txt)
        self.embeded_text = tqdm(map(embed_full_txt, self.cleaned_tokenized_text), 
                                 "embedding all sents with BERT")       

with AlgorithmHandler() as AH:
    AH.load_data()
    AH.tokenize_raw_text_data()
    AH.clean_sents()
    AH.embed_text()
    this = [list(i) for i in list(AH.embeded_text)] 
    
    
    # ext = list(list(AH.cleaned_tokenized_text)[38])
    # ex = [list(i) for i in list(AH.embeded_text)[38]]
    # print(sum([len(list(p)) for p in DH.cleaned_tokenized_text]))
        

# for i, sent in enumerate(ext):
#     try:
#         t = model.embed_text(sent)
#     except Exception as E:
#         if "The size of tensor a" and "must match the size of tensor b" in str(E):
#             print(str(E))

# for i, sent in enumerate(ext):
#     try:
#         print(i)
#         t1 = model.embed_text(sent)
#     except Exception as E:
#         print(E)
#         if "The size of tensor a" and "must match the size of tensor b" in str(E):
#             #n is an arbitrary low number. OBS! This will still fail, if each char becomes a token
#             # TODO: this partially be solved with a better word tokenizer  
#             n= 800
#             # Here the long sentance is split and embedded, whereafter an average is returned
#             t = np.array([model.embed_text(sent[i:i+n])[1].numpy() 
#                           for i in range(0, len(sent), n)]).mean(axis=0)
#         else: 
#             raise E