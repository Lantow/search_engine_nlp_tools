from data_handler.update_db_handler import UpdateDbHandler
# from dotenv import load_dotenv, find_dotenv
# load_dotenv(find_dotenv())

if __name__ == '__main__':
    with UpdateDbHandler() as AH:
        AH.load_data()
        AH.tokenize_raw_text_data()
        AH.clean_sents()
        AH.embed_text()
        AH.merge_embsent_to_docsent()
        AH.update_all() 