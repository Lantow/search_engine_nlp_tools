from algorithm_handler.algorithm_handler import AlgorithmHandler
from dotenv import load_dotenv

load_dotenv()

if __name__ == '__main__':
    with AlgorithmHandler() as AH:
        AH.load_data()
        AH.tokenize_raw_text_data()
        AH.clean_sents()
        AH.embed_text()
        this = [list(i) for i in list(AH.embeded_text)]