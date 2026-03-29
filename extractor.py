def extract_svo(doc):
    """
    Extract Subject, Verb, Object from parsed text.
    Filters out adjectives and adverbs to reduce noise.
    """
    subject = None
    verb = None
    obj = None
    
    for token in doc:
        # Extract subject (nsubj = nominal subject) - skip if modified by adjective
        if token.dep_ == "nsubj" and subject is None:
            subject = token.text
        
        # Extract main verb (ROOT = primary action)
        if token.pos_ == "VERB" and token.dep_ == "ROOT" and verb is None:
            verb = token.text
        
        # Extract object (dobj = direct object of verb)
        if token.dep_ == "dobj" and obj is None:
            obj = token.text
    
    return subject, verb, obj


def extract_entities(doc):
    """
    Extract Named Entities (NER) from parsed text.
    Uses spacy's built-in entity recognition to identify:
    - PERCENT: Percentages (10%)
    - DATE: Dates and quarters (Q4, 2024)
    - MONEY: Monetary values (50 million)
    - ORG: Organizations (Apple, Microsoft)
    - PERSON: People (Steve Jobs)
    - GPE: Geopolitical entities (countries, cities)
    
    Returns:
        List of tuples: [(entity_text, entity_type), ...]
    """
    entities = []

    for ent in doc.ents:
        entities.append((ent.text, ent.label_))

    return entities


def extract_entities_by_type(doc):
    """
    Extract Named Entities organized by type.
    More structured approach for easier access.
    
    Returns:
        Dict with entity types as keys and lists of entities as values
    """
    entities_by_type = {}
    
    for ent in doc.ents:
        if ent.label_ not in entities_by_type:
            entities_by_type[ent.label_] = []
        entities_by_type[ent.label_].append(ent.text)
    
    return entities_by_type


def extract_details(doc):
    """Extract value, time, and entity from parsed text."""
    value = None
    time = None
    entity = None

    for i, token in enumerate(doc):
        # Extract numbers with percentage (e.g., 10%)
        if token.dep_ == "nummod":
            # Check if next token is a percentage sign
            if i + 1 < len(doc) and doc[i + 1].text == "%":
                value = token.text + "%"
            else:
                value = token.text

        # Extract time (Q1, Q2, Q3, Q4, years, etc.)
        if token.text.upper() in ["Q1", "Q2", "Q3", "Q4"]:
            time = token.text

        # Extract entity (noun after "in") - skip descriptive adjectives
        if token.dep_ == "pobj" and token.head.text == "in":
            # Skip common time/quarter indicators
            if token.text.upper() not in ["Q1", "Q2", "Q3", "Q4"]:
                entity = token.text

    return value, time, entity