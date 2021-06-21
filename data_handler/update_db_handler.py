from algorithm_handler.algorithm_handler import AlgorithmHandler
from psycopg2.extras import execute_batch

class UpdateDbHandler(AlgorithmHandler):
             
    def update_documents(self):
        print("updating document embeddings")
        values = zip([i.tolist() for i in self.embeded_doc_map], self.doc_id)
        #values = [(emb.tolist(), did) for emb, did in zip(self.embeded_doc, self.doc_id)]
        execute_batch(self.curr, f"""UPDATE public.scrapers_retsinfodocument 
                                SET document_emb_full = %s WHERE doc_id = %s;""", values)
        
    def update_sentences(self):        
        print("updating sentance embeddings")
        values = []
        for emb, txt, sid in zip(self.embeded_sents, self.sent_text, self.doc_id):
            for e, t, in zip(emb, txt):
                values.append((e.tolist(), t, sid))
        execute_batch(self.curr, f"""INSERT INTO public.scrapers_retsinfosentences(sentence_emb_full, 
                                    sentence_text, doc_id) VALUES (%s, %s, %s)""", values)
           
    def update_all(self):
        
        try:
            self.update_documents()
        except Exception as E:
            print(E)        
        try:
            self.update_sentences()
        except Exception as E:
            print(E)
        