# Compressor module for VagaCore
from parser import parse_text
from extractor import extract_svo, extract_details
from utils import remove_noise


def compress(text):
    """
    Compress text into structured JSON with key information.
    Handles multiple sentences and returns a list of extracted facts.
    Removes noise (adjectives, adverbs, stop words) before extraction.
    Extracts subject, verb, object, entity, value, and time from each sentence.
    """
    doc = parse_text(text)

    results = []

    # Process each sentence separately
    for sent in doc.sents:
        # Clean text by removing adjectives, adverbs, and stop words
        cleaned_text = remove_noise(sent)
        
        # Re-parse cleaned sentence for better extraction
        sent_doc = parse_text(cleaned_text)

        subject, verb, obj = extract_svo(sent_doc)
        value, time, entity = extract_details(sent_doc)

        result = {
            "subject": subject,
            "action": verb,
            "object": obj,
            "entity": entity,
            "value": value,
            "time": time
        }

        results.append(result)

    return results
