from danlp.models import load_bert_base_model
import numpy as np
from data_handler.data_handler import DataHandler
from tqdm import tqdm 
from torch import from_numpy
from sklearn.decomposition import PCA

#https://www.psycopg.org/docs/cursor.html#cursor-iterable

class AlgorithmHandler(DataHandler):
    
    def embed_text(self):
        model = load_bert_base_model()
        def embed_sent(sent):
            # the DAnlp bert base model cant handle more than X tokens
            # the following try/except solves the symptom but not the root cause.
            # OBS! when root cause is solved the folowing code may be used instead:              
            # embed_sent = lambda sent: model.embed_text(sent)
            try:
                return model.embed_text(sent)[1]
            except Exception as E:
                if "The size of tensor a" and "must match the size of tensor b" in str(E):
                    #n is an arbitrary low number. OBS! This will still fail, if each char becomes a token
                    # TODO: this partially be solved with a better word tokenizer  
                    n= 800
                    # Here the long sentance is split and embedded, whereafter an average is returned
                    split_sent_on_idx = lambda i: model.embed_text(sent[i:i+n])[1].numpy()
                    split_points = range(0, len(sent), n)
                    split_sent_obj = map(split_sent_on_idx, split_points)
                    split_sent_np = np.array(list(split_sent_obj)).mean(axis=0)
                    #A PyTorch tensor is returned to type match the rest of the sents
                    return from_numpy(split_sent_np)
                else: 
                    raise E
                
        embed_sent_l = lambda sent: embed_sent(sent)
        embed_full_txt = lambda full_txt: map(embed_sent_l, full_txt)
        try:
            self.embeded_sents_map = tqdm(map(embed_full_txt, self.cleaned_tokenized_map), 
                                    "embedding all sents with BERT")
        except Exception as E:
            raise E
            
    def merge_embsent_to_docsent(self):
        #OBS! look into using reduce instead of np.mean
        self.embeded_sents = []
        def mean_of_emb_and_keep_sents(emb_sents):
            emb_sents = list(emb_sents)
            self.embeded_sents.append(emb_sents)
            return np.array([t.numpy() for t in emb_sents]).mean(axis=0)
        try:
            self.embeded_doc_map = tqdm(map(mean_of_emb_and_keep_sents, self.embeded_sents_map),
                                "reducing sentences to a single doc embeding")
        except Exception as E:
            raise E
       
    # def reduce_dim(self):
    #     pca = PCA(n_components=100, svd_solver="auto")
        
    #     to_100_dim = lambda emb_doc: pca.fit_transform(np.array(list(emb_doc)))
    #     self.embedded_reduced_doc = to_100_dim(self.embeded_doc))
        
# if __name__ == "__main__":
#     with AlgorithmHandler() as AH:
#         AH.load_data()
#         AH.tokenize_raw_text_data()
#         AH.clean_sents()
#         AH.embed_text()
#         AH.merge_embsent_to_docsent()
        
#         values = [(emb.tolist(), did) for emb, did in zip(AH.embeded_doc_map, AH.doc_id)]
        
#         #s = list(AH.embeded_doc)
        
#         # AH.reduce_dim()
#         #t1 = [(a, mean_of_emb(c)) for (a, b), c in zip(AH.curr, AH.embeded_text, AH.tokenized_text)]
#         # mean_of_emb = lambda x: np.array([t.numpy() for t in x]).mean(axis=0)
#         # generate_values = lambda did_and_text, emb: (did_and_text[0], mean_of_emb(emb))
#         # t = list(map(generate_values, zip(AH.curr, AH.embeded_text)))
#         from psycopg2.extras import execute_batch
#         print("opdaterer DB")
#         execute_batch(AH.curr, f"""UPDATE public.scrapers_retsinfodocument 
#                             SET document_emb_full = %s WHERE doc_id = %s;""",
#                             values)
        
        # for (did,txt), emb in zip(AH.curr, AH.embeded_text):
        #     doc_values.append((did, mean_of_emb(emb))
        

 
        
#TODO: lave embeded_text om til embeded_doc ved at tage gennemsnit
#Itterer gennem zip-objectet og udtræk også sætninger