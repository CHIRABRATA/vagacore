from parser import parse_text
from extractor import extract_entities, extract_entities_by_type
import json

text = "The company reported a 10% increase in revenue in Q4."

doc = parse_text(text)

print("=== Test 1: Extract entities as list ===")
print(extract_entities(doc))
print()

print("=== Test 2: Extract entities by type ===")
print(json.dumps(extract_entities_by_type(doc), indent=2))
print()

print("=== Test 3: Complex text with multiple entity types ===")
text2 = "Apple reported $500 million in revenue during Q3 2024 in the Asia-Pacific region."
doc2 = parse_text(text2)
print(f"Text: {text2}")
print("Entities:")
print(json.dumps(extract_entities_by_type(doc2), indent=2))