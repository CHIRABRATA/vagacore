def extract_svo(doc):
    """
    Extract Subject, Verb, Object from parsed text.
    Uses verb lemmas for normalized action forms.
    Improves object extraction: preserves numbers + values with units.
    """
    subject = None
    verb = None
    obj = None
    quantity_phrase = None  # Track complete quantity phrase like "$500 million"
    
    for token in doc:
        # Extract subject (nsubj = nominal subject)
        if token.dep_ == "nsubj" and subject is None:
            subject = token.text
        
        # Extract main verb using LEMMA (normalized form: reported -> report)
        if token.dep_ == "ROOT" and verb is None:
            verb = token.lemma_
        
        # Extract object with smart handling for quantities
        if token.dep_ in ["dobj", "attr"] and obj is None:
            # Build full quantity phrase with units (e.g., "$500 million")
            if token.text[0] in "$€£" or token.text.replace(".", "").replace(",", "").isdigit():
                # Found number/currency, look ahead for unit words
                quantity_phrase = _build_quantity_phrase(token, doc)
                obj = quantity_phrase
            elif token.text.lower() not in ["million", "billion", "thousand", "hundred"]:
                obj = token.text
    
    return subject, verb, obj


def _build_quantity_phrase(token, doc):
    """Build complete quantity phrase including units (e.g., '$500 million')."""
    phrase_tokens = [token.text]
    
    # Look at following tokens for unit words
    idx = token.i + 1
    while idx < len(doc) and idx < token.i + 4:
        next_token = doc[idx]
        if next_token.text.lower() in ["million", "billion", "trillion", "thousand", "percent", "%"]:
            phrase_tokens.append(next_token.text)
            idx += 1
        elif next_token.pos_ == "NUM":
            phrase_tokens.append(next_token.text)
            idx += 1
        else:
            break
    
    return " ".join(phrase_tokens)


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
    """
    Extract value, time, and entity from parsed text.
    IMPROVED: Better preservation of numbers, times, and entity separation.
    
    Entity Priority:
    1. Domain keywords (revenue, profit, earnings) - highest priority
    2. Organizations/Persons (but not generic, not dates)
    3. Fallback to extracted organization entities
    
    Returns: (value, time, entity)
        value: Monetary or percentage with full units (e.g., "$500 million", "15%")
        time: Date expression (e.g., "Q3 2024", "2024-01-15")
        entity: Company/person name (e.g., "Apple", "Microsoft")
    """
    value = None
    time = None
    entity = None
    org_entity = None
    money_entity = None
    percent_entity = None

    # Step 1: Extract using NER - preserve full entity text
    for ent in doc.ents:
        # Preserve monetary values with full text
        if ent.label_ == "MONEY":
            money_entity = ent.text.strip()
            if value is None:
                value = money_entity

        # Preserve percentage with % sign
        elif ent.label_ == "PERCENT":
            percent_entity = ent.text.strip()
            if value is None:
                value = percent_entity

        # Extract temporal information - KEEP FULL EXPRESSIONS like "Q3 2024"
        elif ent.label_ == "DATE":
            time = ent.text.strip()

        # Store organizations/persons - ONLY trust them if not temporal
        elif ent.label_ in ["ORG", "PRODUCT", "PERSON", "LOC"]:
            # Filter out temporal false positives
            if ent.text.upper() not in ["Q1", "Q2", "Q3", "Q4", "Q1 2024", "Q2 2024", "Q3 2024", "Q4 2024"]:
                if ent.label_ in ["ORG", "PRODUCT"]:
                    org_entity = ent.text.strip()
                elif ent.label_ == "PERSON":
                    entity = ent.text.strip()
                    return value, time, entity

    # Step 2: Domain keywords for entity - prioritize over generic orgs
    domain_keywords = ["revenue", "profit", "earnings", "sales", "income", "loss", 
                       "growth", "increase", "decline", "margin", "margin", "eps"]
    filter_words = ["period", "time", "quarter", "year", "date"]
    
    for token in doc:
        if token.dep_ == "pobj" and token.head.text in ["in", "of"]:
            lower_text = token.text.lower()
            
            # Domain keywords take highest priority
            if lower_text in domain_keywords:
                entity = token.text.strip()
                return value, time, entity
            
            # Non-generic, non-filtered words as fallback
            elif lower_text not in filter_words and lower_text not in ["q1", "q2", "q3", "q4"]:
                if entity is None:
                    entity = token.text.strip()

    # Use ORG as last resort if no domain noun found
    if entity is None and org_entity is not None:
        entity = org_entity

    # Ensure value preserves full precision
    if value is None and money_entity is not None:
        value = money_entity
    if value is None and percent_entity is not None:
        value = percent_entity

    return value, time, entity

