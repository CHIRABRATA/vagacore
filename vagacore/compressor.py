# Compressor module for VagaCore
from .parser import parse_text
from .extractor import extract_svo, extract_details, _normalize_verb, _normalize_time
from .utils import remove_noise


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
    doc = parse_text(text)
    
    results = []
    last_time = None
    
    # Process each sentence separately for better context
    for sent in doc.sents:
        # Extract subject, verb, object
        subject, verb, obj = extract_svo(sent)
        
        # Extract details with confidence scoring
        value, time, entity, confidence = extract_details(sent)
        
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
            results.append(fact)
    
    # Deduplicate facts (remove duplicates and conflicting facts)
    results = deduplicate_facts(results)
    
    # Format output based on mode
    if mode == "json":
        return {"facts": results, "version": "0.6.0"}
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


