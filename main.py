from compressor import compress
import json

# Test with complex financial text using NER-enhanced extraction
text = """
Apple reported $500 million in revenue during Q3 2024 in the Asia-Pacific region.
The profit increased by 15% in the same period.
"""

results = compress(text)

print("=== VagaCore v0.3: Hybrid NER + Rule-Based Extraction ===\n")
print("Input text:")
print(text)
print("\nExtracted facts:")
print(json.dumps(results, indent=2))