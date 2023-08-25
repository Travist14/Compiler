from dataclasses import dataclass

class Tokenizer():
    def __init__(self, text):
        self.text = text

    def tokenize(self):
        return self.text.split()