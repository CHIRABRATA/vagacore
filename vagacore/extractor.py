def extract_svo(doc):
    """
    Extract Subject, Verb, Object from parsed text.
    IMPROVED: Reliable grammatical extraction with validation.
    
    Uses dependency parsing:
    - nsubj = nominal subject (who/what is doing)
    - ROOT = main verb (what action)
    - dobj/attr = direct object (what they did to)
    
    Returns: (subject, verb, object) with validation
    """
    subject = None
    verb = None
    obj = None
    
    # Step 1: Extract subject (grammatical nsubj)
    for token in doc:
        if token.dep_ == "nsubj" and subject is None:
            # Use the actual subject/actor
            subject = _validate_entity(token.text)
            if subject:
                break
    
    # Fallback: If no nsubj found, look for compound/proper noun combinations
    if not subject:
        for token in doc:
            if token.pos_ in ["PROPN", "NOUN"] and token.dep_ not in ["compound"]:
                potential = _validate_entity(token.text)
                if potential and token.i < 5:  # Early in sentence
                    subject = potential
                    break
    
    # Step 2: Extract verb (main action, normalized)
    for token in doc:
        if token.dep_ == "ROOT" and verb is None:
            # Normalize verb lemma
            verb = _normalize_verb(token.lemma_)
    
    # Step 3: Extract object with quantity handling
    for token in doc:
        if token.dep_ in ["dobj", "attr"] and obj is None:
            if _is_quantity(token.text):
                # Build full quantity phrase
                obj = _build_quantity_phrase(token, doc)
            elif _validate_entity(token.text):
                obj = _validate_entity(token.text)
    
    return subject, verb, obj


def _validate_entity(text):
    """
    Validate if token is a real entity (not generic word, number, etc).
    Returns cleaned text if valid, None otherwise.
    """
    if not text or len(text) < 2:
        return None
    
    # Reject numbers and pure quantities
    reject_patterns = [
        "million", "billion", "trillion", "thousand", "hundred",
        "percent", "%", "percentage",
        "period", "quarter", "year", "time", "date", "day",
        "q1", "q2", "q3", "q4",  # Quarters are times, not entities
        "same", "this", "that", "the", "a", "an",
        "it", "they", "them", "us", "we", "i", "you",
        "amount", "value", "number", "growth", "increase", "decrease",
        "result", "outcome", "change", "rise", "fall", "surge", "decline",
        # Generic nouns that aren't specific entities
        "company", "firm", "business", "corporation", "organization",
        "industry", "sector", "market", "group", "entity", "player",
        "one", "two", "three", "report", "statement",
    ]
    
    lower_text = text.lower()
    
    # Check if it's a rejected pattern
    for pattern in reject_patterns:
        if lower_text == pattern:
            return None
    
    # Reject pure numbers
    if text.replace(".", "").replace(",", "").isdigit():
        return None
    
    # Reject currency symbols only
    if all(c in "$€£¥" for c in text):
        return None
    
    # Valid entity
    return text.strip()


def _normalize_verb(verb_lemma):
    """
    Normalize verb lemma to standard forms for consistency.
    Maps various verbs to standard action terms.
    """
    # Mapping of verbs to standard forms
    verb_map = {
        # Reporting
        "report": "reported",
        "announce": "reported",
        "declare": "reported",
        "reveal": "reported",
        "publish": "reported",
        "release": "reported",
        "state": "reported",
        "say": "reported",
        
        # Having/Possessing (treat as reporting)
        "have": "reported",
        "had": "reported",
        
        # Earnings/Money
        "earn": "earned",
        "make": "earned",
        "generate": "earned",
        "gain": "earned",
        "achieve": "achieved",
        
        # Growth
        "grow": "increased",
        "increase": "increased",
        "expand": "expanded",
        "rise": "increased",
        "surge": "increased",
        "jump": "increased",
        
        # Decline
        "decline": "declined",
        "decrease": "declined",
        "drop": "declined",
        "fall": "declined",
        "slide": "declined",
        
        # Operations
        "reach": "reached",
        "hit": "reached",
        "exceed": "exceeded",
        "meet": "met",
    }
    
    lower_verb = verb_lemma.lower() if verb_lemma else None
    return verb_map.get(lower_verb, verb_lemma)


def _normalize_time(time_str):
    """
    Normalize time expressions to consistent format.
    Q3 2024, 2024-Q3, Q3/2024 → Q3 2024
    """
    if not time_str:
        return None
    
    # Map variations to standard format
    time_str = time_str.strip()
    
    # Q3 2024, Q3/2024, Q32024 → Q3 2024
    import re
    
    # Handle quarter format
    match = re.search(r'(Q[1-4])\s*/?-?\s*(\d{4})', time_str.upper())
    if match:
        return f"{match.group(1)} {match.group(2)}"
    
    # Handle full date format (Jan 1, 2024 → January 1, 2024)
    match = re.search(r'(january|february|march|april|may|june|july|august|september|october|november|december)\s+\d+,?\s+(\d{4})', 
                     time_str.lower(), re.IGNORECASE)
    if match:
        return time_str
    
    # Return as-is if recognized format
    if any(q in time_str.upper() for q in ["Q1", "Q2", "Q3", "Q4"]) or any(c.isdigit() for c in time_str):
        return time_str
    
    return None


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


def _is_quantity(text):
    """Check if token represents a numeric quantity or currency."""
    if not text:
        return False
    
    # Check for currency symbols
    if text[0] in "$€£¥":
        return True
    
    # Check for number-like patterns
    if text[0].isdigit():
        return True
    
    # Check for percentage
    if "%" in text:
        return True
    
    # Check for quantity words (but not all, only numeric-related)
    quantity_words = ["million", "billion", "trillion", "thousand", "percent", "thousand", "k", "m"]
    if text.lower() in quantity_words:
        return True
    
    return False


def extract_numeric_value(doc):
    """
    Extract numeric value with unit from sentence.
    Returns: (value_str, raw_number) or (None, None)
    
    Example: "$500 million" → ("$500 million", 500000000)
    """
    for token in doc:
        if token.pos_ == "NUM" or (token.text and token.text[0] in "$€£¥"):
            value_str = _build_quantity_phrase(token, doc)
            
            # Parse numeric portion
            import re
            match = re.search(r'(\d+(?:,\d{3})?(?:\.\d+)?)', value_str)
            if match:
                number = float(match.group(1).replace(",", ""))
                
                # Apply unit multiplier
                if "billion" in value_str.lower():
                    number *= 1_000_000_000
                elif "million" in value_str.lower():
                    number *= 1_000_000
                elif "trillion" in value_str.lower():
                    number *= 1_000_000_000_000
                elif "thousand" in value_str.lower() or "k" in value_str.lower():
                    number *= 1_000
                
                return (value_str, number)
    
    return (None, None)



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
    IMPROVED: Robust extraction with validation and normalization.
    
    Strategy:
    1. Extract using NER (high confidence)
    2. Validate extracted values (reject garbage)
    3. Normalize to standard formats (time, verb, numbers)
    4. Fall back to rule-based extraction if needed
    
    Returns: (value, time, entity, confidence)
        value: Monetary or percentage with units ("$500 million", "15%")
        time: Normalized time ("Q3 2024", "January 15, 2024")
        entity: Validated entity name ("Apple", not "million")
        confidence: Score 0-1 for reliability
    """
    value = None
    time = None
    entity = None
    confidence = 0.5
    
    org_entity = None
    money_entity = None
    percent_entity = None
    
    # Step 1: Extract using NER with validation
    for ent in doc.ents:
        # Extract monetary values - VALIDATE
        if ent.label_ == "MONEY":
            money_entity = ent.text.strip()
            if value is None:
                value = money_entity
                confidence = 0.9

        # Extract percentage - VALIDATE
        elif ent.label_ == "PERCENT":
            percent_entity = ent.text.strip()
            if value is None:
                value = percent_entity
                confidence = 0.9

        # Extract temporal information - NORMALIZE
        elif ent.label_ == "DATE":
            normalized_time = _normalize_time(ent.text.strip())
            if normalized_time:
                time = normalized_time
                confidence = min(1.0, confidence + 0.2)

        # Extract organizations/entities - VALIDATE
        elif ent.label_ in ["ORG", "PRODUCT", "PERSON"]:
            validated_entity = _validate_entity(ent.text.strip())
            if validated_entity:
                if ent.label_ in ["ORG", "PRODUCT"]:
                    org_entity = validated_entity
                elif ent.label_ == "PERSON":
                    entity = validated_entity
                    confidence = 0.95
    
    # Step 2: Use domain keywords for entity - higher confidence than generic ORG
    domain_keywords = [
        "revenue", "profit", "earnings", "sales", "income", 
        "loss", "growth", "increase", "decline", "margin",
        "earnings per share", "eps"
    ]
    
    # IMPORTANT: Check ORG entity FIRST - it's usually the subject actor
    if entity is None and org_entity is not None:
        entity = org_entity
        confidence = 0.9  # ORG from NER is usually the subject
    
    # Step 3: Use domain keywords only as fallback
    for token in doc:
        if entity is None and token.dep_ == "pobj" and token.head.text in ["in", "of"]:
            lower_text = token.text.lower()
            
            # Domain keywords are high-confidence entities only if no ORG found
            if lower_text in domain_keywords:
                entity = token.text.strip()
                confidence = 0.85
                break
    
    # Step 4: Extract subject from dependency parsing if still missing
    if entity is None:
        for token in doc:
            if token.dep_ == "nsubj":
                valid = _validate_entity(token.text)
                if valid:
                    entity = valid
                    confidence = 0.9
                    break
    if value is None:
        if money_entity:
            value = money_entity
        elif percent_entity:
            value = percent_entity
    
    return value, time, entity, confidence


def analyze_numeric_comparison(doc):
    """
    Analyze numeric comparisons in text.
    Handles patterns like:
    - "up 25%", "down 10%"
    - "growth of 15%"
    - "increased by $2M"
    - "declined to $50B"
    - "grew by 25%"
    
    Returns: {
        "direction": "up" | "down",
        "magnitude": numeric value,
        "percent": True if percentage, False if absolute,
        "comparison_text": description
    }
    """
    import re
    
    comparison = {
        "direction": None,
        "magnitude": None,
        "percent": False,
        "comparison_text": None
    }
    
    text = doc.text
    
    # Patterns for growth/decline with percentage
    growth_patterns = [
        r'(?:up|grow|grew|growth|increase|increased|expand|expanded|rise|rose|surge|surged|jump|jumped)\s+(?:by\s+)?(\d+(?:\.\d+)?)\s*%',
        r'(?:down|decline|declined|decrease|decreased|drop|dropped|fall|fell)\s+(?:by\s+)?(\d+(?:\.\d+)?)\s*%',
    ]
    
    # Patterns for growth/decline with absolute values
    absolute_patterns = [
        r'(?:grow|grew|growth|increase|increased|expand|expanded|rise|rose|surge)\s+(?:by\s+)?\$?(\d+(?:,\d{3})*(?:\.\d+)?)\s*(?:million|billion|trillion|thousand)?',
    ]
    
    # Check for growth/decline keywords
    if re.search(r'\b(grow|grew|growth|increase|increased|expand|expanded|rise|rose|surge|surged|jump|jumped|gain|gained)\b', text, re.IGNORECASE):
        comparison["direction"] = "up"
    elif re.search(r'\b(decline|declined|decrease|decreased|drop|dropped|fall|fell|slide|slid|lose|lost)\b', text, re.IGNORECASE):
        comparison["direction"] = "down"
    
    # Extract magnitude from growth patterns
    for pattern in growth_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            magnitude = float(match.group(1).replace(",", ""))
            comparison["magnitude"] = magnitude
            comparison["percent"] = "%" in match.group(0)
            comparison["comparison_text"] = match.group(0)
            return comparison
    
    # Extract magnitude from absolute patterns
    for pattern in absolute_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            magnitude = float(match.group(1).replace(",", ""))
            comparison["magnitude"] = magnitude
            comparison["percent"] = False
            comparison["comparison_text"] = match.group(0)
            return comparison
    
    return None if comparison["magnitude"] is None else comparison

