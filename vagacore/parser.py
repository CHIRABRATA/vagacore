# Parser module for VagaCore
import spacy

def load_model():
    """
    Load spaCy model with automatic fallback download.
    Removes friction: users just pip install vagacore and go.
    """
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        # Model not found, auto-download it
        print("📥 Downloading spaCy model (first time only)...")
        from spacy.cli import download
        download("en_core_web_sm")
        return spacy.load("en_core_web_sm")

# Load model once at module level
nlp = load_model()

def parse_text(text):
    """Parse text using spaCy NLP pipeline."""
    doc = nlp(text)
    return doc
