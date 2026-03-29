# Compressor module for VagaCore
from .parser import parse_text
from .extractor import extract_svo, extract_details
from .utils import remove_noise


def compress(text):
    """
    Compress text into structured JSON with key information.
    Handles multiple sentences and returns a list of extracted facts.
    
    Strategy:
    - Extract from ORIGINAL text (NER + syntax parsing work best)
    - Implement context memory for temporal info propagation
    
    Context Awareness (Industry Trick):
    - Track last_time seen
    - If current sentence has no time, use previous time
    - Handles "in the same period" and vague references
    """
    doc = parse_text(text)

    results = []
    last_time = None  # Context memory: store last time for propagation

    # Process each sentence separately
    for sent in doc.sents:
        # Extract from ORIGINAL sentence for best accuracy
        subject, verb, obj = extract_svo(sent)
        value, time, entity = extract_details(sent)

        # Context Awareness: Propagate time from previous sentence
        if time is None or "period" in str(time).lower():
            # Use previously seen time if current is missing or vague
            time = last_time
        else:
            # Update context memory with new time
            last_time = time

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
