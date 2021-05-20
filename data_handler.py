from dataclasses import dataclass
import numpy as np

@dataclass
class DataHandler:
    placeholder: "afhænger af hvordan data hentes fra serveren"

    def clean_sent(self):
        #Do something with the paragraph signs and the numbers etc.
        self.cleaned_tokenized_text = None

