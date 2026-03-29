# Parser module for VagaCore
import spacy

# Load model once
nlp = spacy.load("en_core_web_sm")

def parse_text(text):
    doc = nlp(text)
    return doc