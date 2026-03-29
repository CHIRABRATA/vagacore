def extract_svo(doc):
    """
    Extract Subject, Verb, Object from parsed text.
    Uses verb lemmas for normalized action forms.
    Intelligent object extraction: prioritizes meaningful nouns over quantities.
    """
    subject = None
    verb = None
    obj = None
    quantity_obj = None  # Track if object is just a quantity (e.g., "million")
    
    for token in doc:
        # Extract subject (nsubj = nominal subject)
        if token.dep_ == "nsubj" and subject is None:
            subject = token.text
        
        # Extract main verb using LEMMA (normalized form: reported -> report)
        if token.dep_ == "ROOT" and verb is None:
            verb = token.lemma_
        
        # Extract object with special handling for quantities
        if token.dep_ in ["dobj", "attr"] and obj is None:
            # Check if this is just a quantity word (million, billion, etc.)
            if token.text.lower() in ["million", "billion", "thousand", "hundred"]:
                quantity_obj = token.text
            else:
                obj = token.text
    
    # If we only found a quantity object, look for a more meaningful object
    if obj is None and quantity_obj is not None:
        # Try to find a meaningful noun that goes with the quantity
        for token in doc:
            if token.dep_ == "pobj" and token.head.text in ["in", "of"]:
                if token.text.lower() not in ["period", "time", "quarter", "year"]:
                    obj = token.text
                    break
        # Fallback to quantity if no better object found
        if obj is None:
            obj = quantity_obj
    
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
    """
    Extract value, time, and entity from parsed text.
    Intelligent hybrid approach: ML-based NER + rule-based syntax.
    
    Entity Priority:
    1. Domain keywords (revenue, profit, earnings) from rule-based
    2. NER organizations/locations (but not times) as fallback
    3. Filter out common non-domain and temporal words
    """
    value = None
    time = None
    entity = None
    org_entity = None  # Store ORG as fallback

    # Step 1: Extract using NER
    for ent in doc.ents:
        # Extract monetary or percentage values
        if ent.label_ in ["PERCENT", "MONEY"]:
            value = ent.text.strip()

        # Extract temporal information
        elif ent.label_ in ["DATE", "TIME"]:
            time = ent.text.strip()

        # Store organizations/locations as fallback (but not if they're dates)
        elif ent.label_ in ["ORG", "PRODUCT", "LOC"]:
            # Don't use quarters/dates as entities
            if ent.text.upper() not in ["Q1", "Q2", "Q3", "Q4"]:
                org_entity = ent.text.strip()

    # Step 2: Prioritize domain-specific nouns over generic entities
    domain_keywords = ["revenue", "profit", "earnings", "sales", "income", "loss", "growth", "increase", "decline"]
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

    return value, time, entity
