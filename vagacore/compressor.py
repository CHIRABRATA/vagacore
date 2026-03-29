# Compressor module for VagaCore
from .parser import parse_text
from .extractor import extract_svo, extract_details
from .utils import remove_noise


def compress(text, mode="json"):
    """
    Compress text into structured facts with intelligent extraction.
    
    Args:
        text (str): Input text to process
        mode (str): Output format
            - "json": Structured JSON (API-friendly, default)
            - "text": Human-readable format
            - "llm": Optimized for LLM consumption
    
    Returns:
        dict or str: Depending on mode
            - "json": {"facts": [...]}
            - "text": Markdown-formatted summary
            - "llm": LLM-optimized string
    
    Strategy:
    - Extract from ORIGINAL text (NER + parsing work best on unclean text)
    - Implement context memory for temporal info propagation
    - Preserve numbers, values, and full time expressions
    - Use subject (company name) as entity
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
        
        # Use subject as entity if it looks like a company/person name and entity isn't meaningful
        if subject and (not entity or entity.lower() in ["revenue", "profit", "sales", "income", "earnings"]):
            entity = subject
        
        # Only add facts with meaningful content
        if subject or value or entity:
            fact = {
                "entity": entity or subject or "Unknown",      # Company/person name
                "event": verb or "N/A",                        # Action taken
                "value": value,                                # Numeric or percentage
                "time": time,                                  # When it happened
                "reason": obj                                  # Context/reason
            }
            results.append(fact)
    
    # Format output based on mode
    if mode == "json":
        return {"facts": results}
    
    elif mode == "text":
        return _format_text(results)
    
    elif mode == "llm":
        return _format_llm(results)
    
    else:
        raise ValueError(f"Unknown mode: {mode}. Use 'json', 'text', or 'llm'")


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
        if fact.get('reason'):
            lines.append(f"   • Reason: {fact['reason']}")
        
        output.append("\n".join(lines))
    
    return "\n".join(output)


def _format_llm(facts):
    """LLM-optimized format - concise, unambiguous, structured."""
    if not facts:
        return ""
    
    lines = []
    for fact in facts:
        # Build concise fact string: "Apple reported $500M (Q3 2024). Reason: iPhone sales."
        entity = (fact.get('entity') or '').strip()
        event = (fact.get('event') or '').strip()
        value = (fact.get('value') or '').strip()
        time = (fact.get('time') or '').strip()
        reason = (fact.get('reason') or '').strip()
        
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
        
        # Add reason
        if reason and reason.lower() not in ["n/a", "unknown"]:
            main = f"{main[:-1]} Reason: {reason}."
        
        lines.append(main)
    
    return " ".join(lines)

