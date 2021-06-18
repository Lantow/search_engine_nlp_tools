from algorithm_handler.algorithm_handler import AlgorithmHandler
from psycopg2.extras import execute_batch

class UpdateDbHandler(AlgorithmHandler):
             
    def update_documents(self):
        values = [(emb.tolist(), did) for emb, did in zip(self.embeded_doc, self.doc_id)]
        execute_batch(self.curr, f"""UPDATE public.scrapers_retsinfodocument 
                                SET document_emb_full = %s WHERE doc_id = %s;""", values)
        
    def update_sentences(self):
        values = []
        for emb, txt, sid in zip(self.embeded_sents, self.sent_text, self.doc_id):
            for e, t, in zip(emb, txt):
                values.append((e.tolist(), t, sid))
        execute_batch(self.curr, f"""INSERT INTO public.scrapers_retsinfosentences(sentence_emb_full, 
                                    sentence_text, doc_id) VALUES (%s, %s, %s)""", values)
        
        

   

with UpdateDbHandler() as AH:
    AH.
    AH.load_data()
    AH.tokenize_raw_text_data()
    AH.clean_sents()
    AH.embed_text()
    AH.merge_embsent_to_docsent()
    values = []
    for emb, txt, sid in zip(AH.embeded_sents, AH.sent_text, AH.doc_id):
        for e, t, in zip(emb, txt):
            values.append((e.tolist(), t, sid))
    # AH.update_sentences()
    
        
        #s = list(AH.embeded_doc)
        
        # AH.reduce_dim()
        #t1 = [(a, mean_of_emb(c)) for (a, b), c in zip(AH.curr, AH.embeded_text, AH.tokenized_text)]
        # mean_of_emb = lambda x: np.array([t.numpy() for t in x]).mean(axis=0)
        # generate_values = lambda did_and_text, emb: (did_and_text[0], mean_of_emb(emb))
        # t = list(map(generate_values, zip(AH.curr, AH.embeded_text)))
        # from psycopg2.extras import execute_batch
        # print("opdaterer DB")
        # execute_batch(AH.curr, f"""UPDATE public.scrapers_retsinfodocument 
        #                     SET document_emb_full = %s WHERE doc_id = %s;""",
        #                     values)
        