import re

def clean_text(text):
    text = re.sub(r'[^a-zA-Z0-9$.,% ]+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def extract_all_entities(doc):
    entities = []
    for ent in doc.ents:
        if ent.label_ in ["ORG", "PERSON"]:
            entities.append(ent.text.strip())
    return entities


def extract_all_values(doc):
    values = []
    for ent in doc.ents:
        if ent.label_ in ["MONEY", "PERCENT"]:
            values.append(ent.text.strip())
    return values


def extract_time(doc):
    for ent in doc.ents:
        if ent.label_ in ["DATE", "TIME"]:
            return ent.text.strip()
    return None


def map_entities_to_values(text, entities, values):
    text_lower = text.lower()
    
    # Handle "respectively"
    if "respectively" in text_lower:
        if len(entities) == len(values):
            return list(zip(entities, values))
    
    # Simple positional mapping
    pairs = []
    for i in range(min(len(entities), len(values))):
        pairs.append((entities[i], values[i]))
    
    return pairs


def extract_facts(text, nlp):
    text = clean_text(text)
    doc = nlp(text)
    
    entities = extract_all_entities(doc)
    values = extract_all_values(doc)
    time = extract_time(doc)
    
    pairs = map_entities_to_values(text, entities, values)
    
    results = []
    
    for entity, value in pairs:
        results.append({
            "entity": entity,
            "event": "reported",
            "value": value,
            "time": time,
            "confidence": 0.9
        })
    
    return results


def compress(text, nlp):
    facts = extract_facts(text, nlp)
    
    return {
        "facts": facts,
        "version": "0.7.0"
    }