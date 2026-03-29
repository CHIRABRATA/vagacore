# Utilities module for VagaCore

def remove_noise(doc):
    """
    Remove adjectives, adverbs, and stop words from parsed text.
    Keeps prepositions to preserve relationships (in, by, of, etc.)
    Keeps only meaningful structural elements (nouns, verbs, numbers).
    """
    # Important prepositions to keep for relationships
    keep_prepositions = {"in", "of", "by", "at", "on", "for", "from", "to", "with"}
    
    clean_tokens = []

    for token in doc:
        # Remove adjectives (descriptive words: very, significant, happy)
        if token.pos_ == "ADJ":
            continue
        
        # Remove adverbs (modifying words: extremely, quickly, very)
        if token.pos_ == "ADV":
            continue
        
        # Remove most stop words but keep important prepositions
        if token.is_stop:
            if token.text.lower() not in keep_prepositions:
                continue

        clean_tokens.append(token.text)

    return " ".join(clean_tokens)


def clean_text(text):
    """Lightweight preprocessing to remove noisy characters before parsing.

    - Keeps alphanumerics, whitespace, basic punctuation, currency and percent symbols
    - Collapses consecutive whitespace
    - Preserves casing so spaCy can leverage capitalization for entities
    """
    import re

    if not text:
        return ""

    # Remove obvious noise (emoji, symbols) but keep $, %, ., commas and hyphens
    cleaned = re.sub(r"[^A-Za-z0-9$%.,:/\-\s]+", " ", text)
    # Collapse multiple spaces
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned
