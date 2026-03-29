def extract_svo(doc):
    """
    Extract Subject, Verb, Object from parsed text.
    GUARDED: Reliable grammatical extraction with validation and negation/hypothetical skipping.
    
    Uses dependency parsing:
    - nsubj = nominal subject (who/what is doing)
    - ROOT = main verb (what action)
    - dobj/attr = direct object (what they did to)
    
    Returns: (subject, verb, object) with validation
    """
    subject = None
    verb = None
    obj = None

    # Guard against negated or hypothetical statements to avoid hallucinated facts.
    is_negated = any(token.dep_ == "neg" for token in doc)
    is_hypothetical = any(
        token.text.lower() == "if" or (token.pos_ == "AUX" and token.lemma_ in ["will", "would", "could", "might"])
        for token in doc
    )

    if is_negated or is_hypothetical:
        return None, None, None
    
    # Step 1: Extract subject (grammatical nsubj)
    for token in doc:
        if token.dep_ == "nsubj" and subject is None:
            owners = [child.text for child in token.children if child.dep_ == "poss"]
            compounds = [child.text for child in token.children if child.dep_ == "compound"]

            # Prefer possessive owner (e.g., Nvidia's revenue → Nvidia), then compound root (Netflix revenue → Netflix)
            if owners:
                owner_clean = owners[0].replace("'s", "").strip()
                subject = _validate_entity(owner_clean) or _validate_entity(owners[0])
            if not subject and compounds:
                subject = _validate_entity(compounds[0])
            if not subject:
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
        if token.dep_ in ["dobj", "attr", "pobj"] and obj is None:
            if _is_quantity(token.text):
                # Build full quantity phrase
                obj = _build_quantity_phrase(token, doc)
            elif _validate_entity(token.text):
                obj = _validate_entity(token.text)
    
    return subject, verb, obj


def _validate_entity(text):
    """Validate if token is a real entity (not generic word, number, etc)."""
    if not text:
        return None

    # Strip leading single-letter unit prefixes and trailing punctuation (handles "$500M." and "M Profit")
    import re
    text = re.sub(r'^[MB]\s+', '', text)
    text = text.strip().rstrip('.,;:')

    # REJECTION LIST: expanded financial/common non-entity terms
    reject_patterns = [
        "million", "billion", "trillion", "thousand", "hundred", "percent", "%",
        "period", "quarter", "year", "time", "date", "day", "q1", "q2", "q3", "q4",
        "same", "this", "that", "the", "a", "an", "it", "they", "them", "us", "we",
        "amount", "value", "number", "growth", "increase", "decrease", "result",
        "revenue", "profit", "earnings", "sales", "income", "loss", "margin", "eps",
        "company", "firm", "business", "corporation", "one", "two", "lol", "idk"
    ]

    lower_text = text.lower().strip()
    if lower_text in reject_patterns:
        return None

    # Reject pure numbers or currency symbols
    if text.replace(".", "").replace(",", "").isdigit():
        return None
    if all(c in "$€£¥" for c in text):
        return None

    return text if len(text) > 1 else None


def _normalize_verb(verb_lemma):
    """
    Normalize verb lemma to standard forms for consistency.
    Maps various verbs to standard action terms.
    """
    # Mapping of verbs to standard forms
    verb_map = {
        # Reporting / financial result verbs (normalized to a single class)
        "report": "reported",
        "announce": "reported",
        "declare": "reported",
        "reveal": "reported",
        "publish": "reported",
        "release": "reported",
        "state": "reported",
        "say": "reported",
        "have": "reported",
        "had": "reported",
        "earn": "reported",
        "make": "reported",
        "generate": "reported",
        "gain": "reported",
        "post": "reported",
        
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
        "achieve": "achieved",
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
    IMPROVED: Robust extraction with validation and normalization. Skips negated/hypothetical statements.
    
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
    # Guard against negated or hypothetical statements; they are treated as non-facts.
    is_negated = any(token.dep_ == "neg" for token in doc)
    is_hypothetical = any(
        token.text.lower() == "if" or (token.pos_ == "AUX" and token.lemma_ in ["will", "would", "could", "might"])
        for token in doc
    )

    if is_negated or is_hypothetical:
        return None, None, None, 0.0

    value, time, entity = None, None, None
    confidence = 0.5
    all_values = []
    
    # Step 1: NER Pass
    for ent in doc.ents:
        if ent.label_ in ["MONEY", "PERCENT"]:
            all_values.append(ent.text.strip())
            if value is None:
                value = ent.text.strip()
                confidence = 0.9
        elif ent.label_ == "DATE":
            time = _normalize_time(ent.text.strip())
        elif ent.label_ in ["ORG", "PRODUCT", "PERSON"] and entity is None:
            entity = _validate_entity(ent.text.strip())

    # Step 2: POSSESSIVE/COMPOUND FALLBACK (handle Nvidia's revenue → Nvidia; Netflix revenue → Netflix)
    if not entity:
        for token in doc:
            if token.dep_ == "nsubj" or token.pos_ == "NOUN":
                owners = [child.text for child in token.children if child.dep_ == "poss"]
                compounds = [child.text for child in token.children if child.dep_ == "compound"]
                if owners:
                    entity = _validate_entity(owners[0].replace("'s", ""))
                elif compounds:
                    entity = _validate_entity(compounds[0])
                if not entity:
                    entity = _validate_entity(token.text)
                if entity:
                    confidence = 0.9
                    break

    # Step 3: State Correction (keep latest value on later/actually/corrected)
    text_lower = doc.text.lower()
    if len(all_values) > 1 and any(k in text_lower for k in ["later", "actually", "corrected"]):
        value = all_values[-1]

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

