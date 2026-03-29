# Compressor module for VagaCore
from .parser import parse_text
from .extractor import extract_svo, extract_details, _normalize_verb, _normalize_time, _validate_entity
from .utils import remove_noise, clean_text


class ContextManager:
    """Track last proper entity to resolve generic subjects like "the company"."""

    def __init__(self):
        self.last_proper_entity = None

    def resolve_subject(self, current_subject):
        generic_terms = {"company", "firm", "it", "they", "giant", "startup", "business", "organization"}
        if current_subject and current_subject.lower() in generic_terms:
            return self.last_proper_entity or current_subject

        if current_subject:
            self.last_proper_entity = current_subject
        return current_subject


def compress(text, mode="json"):
    """
    Compress text into structured facts with intelligent extraction.
    IMPROVED: More robust with validation, normalization, and confidence scoring.
    
    Args:
        text (str): Input text to process
        mode (str): Output format
            - "json": Structured JSON (API-friendly, default)
            - "text": Human-readable format
            - "llm": Optimized for LLM consumption
    
    Returns:
        dict or str: Depending on mode
    
    Processing Pipeline:
    1. Parse text with spaCy (NER + dependency parsing)
    2. Extract facts with validation
    3. Normalize verbs, times, numbers
    4. Filter low-confidence extractions
    5. Format output based on mode
    """
    cleaned_text = clean_text(text)
    doc = parse_text(cleaned_text)
    
    results = []
    last_time = None
    last_entity = None  # Subject memory for generic references
    context = ContextManager()
    
    # Process each sentence separately for better context
    for sent in doc.sents:
        # Skip sentences that look like pure noise (no entities, no capitalized tokens)
        if not sent.ents and not any(tok.is_alpha and tok.text[:1].isupper() for tok in sent):
            continue

        # First, handle explicit pairing patterns (e.g., "respectively")
        paired_facts = _extract_respective_facts(sent) or _extract_parallel_pairs(sent)
        if paired_facts:
            # Update memory with last paired entity
            last_entity = paired_facts[-1]["entity"] if paired_facts else last_entity
            results.extend(paired_facts)
            continue

        # Structured list-style fallback (e.g., "Revenue: $50M; Profit: $10M")
        list_facts = _extract_list_pattern(sent)
        if list_facts:
            time = _extract_time_from_sentence(sent) or last_time
            for fact in list_facts:
                fact["time"] = time
                if fact.get("entity"):
                    fact["entity"] = context.resolve_subject(fact["entity"])
                    last_entity = fact["entity"]
                results.append(fact)
            if time:
                last_time = time
            continue

        # Extract subject, verb, object
        subject, verb, obj = extract_svo(sent)
        subject = context.resolve_subject(subject)
        
        # Extract details with confidence scoring
        value, time, entity, confidence = extract_details(sent)

        if entity:
            entity = context.resolve_subject(entity)
            last_entity = entity
        elif last_entity and any(t.text.lower() in ["company", "firm", "it", "giant", "startup", "business", "organization"] for t in sent):
            entity = last_entity
            confidence = max(confidence, 0.85)
        elif subject:
            entity = context.resolve_subject(subject)
            if entity:
                last_entity = entity
        
        # Normalize time and apply context memory
        if time:
            time = _normalize_time_format(time)
            last_time = time
        elif last_time:
            # Use previously seen time if current is missing
            time = last_time
        
        # Normalize verb
        if verb:
            verb = _normalize_verb(verb)
        
        # Only include facts with meaningful content and reasonable confidence
        if confidence >= 0.5 and (subject or entity or value):
            fact = {
                "entity": entity or subject or "Unknown",
                "event": verb or "N/A",
                "value": value,
                "time": time,
                "confidence": round(confidence, 2)
            }
            if _is_meaningful_fact(fact):
                results.append(fact)
    
    # Deduplicate facts (remove duplicates and conflicting facts)
    results = deduplicate_facts(results)
    
    # Format output based on mode
    if mode == "json":
        return {"facts": results, "version": "1.0.1"}
    elif mode == "text":
        return _format_text(results)
    elif mode == "llm":
        return _format_llm(results)
    else:
        raise ValueError(f"Unknown mode: {mode}. Use 'json', 'text', or 'llm'")


def _normalize_time_format(time_str):
    """Ensure consistent time format."""
    if not time_str:
        return None
    import re
    # Q3 2024, Q3/2024 → Q3 2024
    match = re.search(r'(Q[1-4])\s*/?-?\s*(\d{4})', time_str.upper())
    if match:
        return f"{match.group(1)} {match.group(2)}"
    return time_str


def _format_text(facts):
    """Human-readable text format for documentation and reports."""
    if not facts:
        return "No facts extracted."
    
    output = []
    output.append("📊 Extracted Facts:\n")
    
    for i, fact in enumerate(facts, 1):
        entity = fact.get('entity') or 'Unknown'
        event = fact.get('event') or 'N/A'
        lines = [f"{i}. {entity} {event}"]
        
        if fact.get('value'):
            lines.append(f"   • Value: {fact['value']}")
        if fact.get('time'):
            lines.append(f"   • Time: {fact['time']}")
        
        # Add confidence only if below threshold
        confidence = fact.get('confidence', 0)
        if confidence < 0.8:
            lines.append(f"   • Confidence: {confidence:.0%}")
        
        output.append("\n".join(lines))
    
    return "\n".join(output)


def _format_llm(facts):
    """LLM-optimized format - concise, unambiguous, structured."""
    if not facts:
        return ""
    
    lines = []
    for fact in facts:
        # Build concise fact string: "Apple reported $500M (Q3 2024)."
        entity = (fact.get('entity') or '').strip()
        event = (fact.get('event') or '').strip()
        value = (fact.get('value') or '').strip()
        time = (fact.get('time') or '').strip()
        
        if not entity:
            continue
        
        # Build main statement
        parts = [entity, event]
        if value:
            parts.append(value)
        main = " ".join(filter(None, parts)) + "."
        
        # Add temporal context
        if time:
            main = f"{main[:-1]} ({time})."
        
        lines.append(main)
    
    return " ".join(lines)


def deduplicate_facts(facts):
    """
    Remove duplicate and conflicting facts intelligently.
    
    Strategy:
    - Group facts by (entity, semantic_type, time, value)
    - Keep only highest-confidence fact per group
    - Handle verb variations (reported/stated/announced all mean same thing)
    - Group similar reporting verbs (reported, earned, generated all report financial facts)
    
    Args:
        facts (list): List of fact dicts
    
    Returns:
        list: Deduplicated facts
    """
    if not facts:
        return []
    
    def get_semantic_event_type(event):
        """Map event to semantic type for smarter deduplication."""
        if not event or event == "N/A":
            return "unknown"
        
        event_lower = event.lower()
        
        # Financial reporting verbs (all equivalent)
        if any(v in event_lower for v in ["report", "state", "announce", "declare", "publish", "earn", "make", "generate", "gain", "have"]):
            return "financial_report"
        
        # Growth verbs
        if any(v in event_lower for v in ["grow", "increase", "expand", "rise", "surge"]):
            return "growth"
        
        # Decline verbs
        if any(v in event_lower for v in ["decline", "decrease", "drop", "fall"]):
            return "decline"
        
        return event_lower
    
    seen = {}
    deduplicated = []
    
    for fact in facts:
        # Create key with semantic event type
        semantic_type = get_semantic_event_type(fact.get('event', 'N/A'))
        key = (
            fact.get('entity', 'Unknown'),
            semantic_type,
            fact.get('time') or 'Unknown',
            fact.get('value') or 'Unknown'  # Include value for more specific dedup
        )
        
        if key not in seen:
            # First occurrence
            seen[key] = fact
            deduplicated.append(fact)
        else:
            # Check if this is higher confidence
            existing_confidence = seen[key].get('confidence', 0)
            new_confidence = fact.get('confidence', 0)
            
            if new_confidence > existing_confidence:
                # Replace with higher confidence version
                idx = deduplicated.index(seen[key])
                deduplicated[idx] = fact
                seen[key] = fact
    
    return deduplicated


def _extract_respective_facts(sent):
    """Handle sentences with explicit "respectively" alignment.

    Pattern: A and B ... X and Y respectively → map A→X, B→Y
    Returns a list of fact dicts or empty list.
    """
    if "respectively" not in sent.text.lower():
        return []

    entities = _collect_entities(sent)
    values = _collect_money_values(sent)

    if len(entities) < 2 or len(values) < 2:
        return []

    entities = [text for _, text in sorted(entities, key=lambda x: x[0])]
    values = [text for _, text in sorted(values, key=lambda x: x[0])]

    # Align by order
    pairs = list(zip(entities, values))
    if not pairs:
        return []

    verb = None
    for token in sent:
        if token.dep_ == "ROOT":
            verb = _normalize_verb(token.lemma_)
            break

    time = None
    for ent in sent.ents:
        if ent.label_ == "DATE":
            normalized_time = _normalize_time(ent.text) or ent.text
            time = _normalize_time_format(normalized_time)
            break

    facts = []
    for entity, value in pairs:
        fact = {
            "entity": entity,
            "event": verb or "reported",
            "value": value,
            "time": time,
            "confidence": 0.9
        }
        if _is_meaningful_fact(fact):
            facts.append(fact)

    return facts


def _extract_parallel_pairs(sent):
    """Pair multiple entities with multiple values in order when counts match.

    This covers sentences like "Apple and Microsoft reported $500M and $300M" even
    without the explicit "respectively" keyword.
    """
    entities = _collect_entities(sent)
    values = _collect_money_values(sent)

    if len(entities) < 2 or len(values) < 2:
        return []

    entities = [text for _, text in sorted(entities, key=lambda x: x[0])]
    values = [text for _, text in sorted(values, key=lambda x: x[0])]

    verb = None
    for token in sent:
        if token.dep_ == "ROOT":
            verb = _normalize_verb(token.lemma_)
            break

    time = None
    for ent in sent.ents:
        if ent.label_ == "DATE":
            normalized_time = _normalize_time(ent.text) or ent.text
            time = _normalize_time_format(normalized_time)
            break

    facts = []
    for entity, value in zip(entities, values):
        fact = {
            "entity": entity,
            "event": verb or "reported",
            "value": value,
            "time": time,
            "confidence": 0.85
        }
        if _is_meaningful_fact(fact):
            facts.append(fact)

    return facts


def _collect_entities(sent):
    """Collect ordered entity texts (ORG/PRODUCT/PERSON) with position info."""
    base_offset = sent.start_char
    entities = [(ent.start_char - base_offset, ent.text.strip()) for ent in sent.ents if ent.label_ in ("ORG", "PRODUCT", "PERSON")]
    # Fallback: use proper nouns only if NER missed entirely
    if not entities:
        for token in sent:
            if token.pos_ == "PROPN" and token.text[:1].isupper():
                entities.append((token.idx - base_offset, token.text))
    # Deduplicate while preserving order
    seen = set()
    ordered = []
    for idx, text in sorted(entities, key=lambda x: x[0]):
        if text not in seen:
            seen.add(text)
            ordered.append((idx, text))
    return ordered


def _collect_money_values(sent):
    """Collect ordered monetary/percentage values with regex fallback."""
    base_offset = sent.start_char
    values = [(ent.start_char - base_offset, ent.text.strip()) for ent in sent.ents if ent.label_ in ("MONEY", "PERCENT", "QUANTITY")]

    # Regex fallback to capture patterns like $500M and $300M with strict suffix binding
    import re
    pattern = re.compile(r"(\$?\d[\d.,]*\s?(?:million|billion|trillion|m|b|bn|k|%))", re.IGNORECASE)
    for match in pattern.finditer(sent.text):
        val_text = match.group().strip().rstrip('.,;:')
        values.append((match.start(), val_text))

    # Deduplicate: keep longest match when overlaps/duplicates occur
    values = sorted(values, key=lambda x: (x[0], -len(x[1])))
    filtered = []
    for idx, text in values:
        if any(existing_text.startswith(text) or text.startswith(existing_text) for _, existing_text in filtered):
            continue
        filtered.append((idx, text))

    # Preserve original order by index
    filtered = sorted(filtered, key=lambda x: x[0])
    return filtered


def _extract_list_pattern(sent):
    """Extract key/value pairs from list-style sentences like "Revenue: $50M; Profit: $10M"."""
    import re

    matches = re.findall(r"([A-Za-z][A-Za-z0-9_ ]+):\s*([$€£¥]?\d[\d.,]*\s*(?:million|billion|trillion|m|b|bn|k|%)?)", sent.text)
    facts = []
    for key, val in matches:
        cleaned_key = key.strip()
        cleaned_val = val.strip()
        if not cleaned_key or not cleaned_val:
            continue
        facts.append({
            "entity": cleaned_key,
            "event": "reported",
            "value": cleaned_val,
            "time": None,
            "confidence": 0.9
        })
    return facts


def _extract_time_from_sentence(sent):
    """Get first DATE entity from the sentence, normalized if possible."""
    for ent in sent.ents:
        if ent.label_ == "DATE":
            normalized_time = _normalize_time(ent.text) or ent.text
            return _normalize_time_format(normalized_time)
    return None


def _is_meaningful_fact(fact):
    """Filter out low-signal/noisy facts (e.g., garbage tokens without values)."""
    entity = (fact.get("entity") or "").strip()
    value = fact.get("value")
    time = fact.get("time")

    # If we have a value or time, ensure entity is also valid (to avoid garbage subjects)
    if value or time:
        return bool(_validate_entity(entity) or entity == "Unknown")

    # Require entity to be alphabetic and capitalized to avoid noisy lowercase tokens
    if entity and entity[0].isalpha() and entity[0].isupper() and len(entity) > 2:
        return bool(_validate_entity(entity))

    return False


