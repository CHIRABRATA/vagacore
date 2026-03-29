from compressor import compress
import json

# Most critical scenario: sentences with NO time data at all
# Context memory prevents complete loss of temporal information

text = """
Apple released Q3 2024 earnings.
Profit margins expanded by 200 basis points.
Operating expenses were well controlled.
Cash flow generation remained robust.
"""

print("=== CRITICAL: Context Memory Prevents Data Loss ===")
print()
print("Input (sentences 2-4 have NO explicit time reference):")
for i, line in enumerate(text.strip().split('\n'), 1):
    if line.strip():
        print(f"  {i}: {line.strip()}")
print()

results = compress(text)
print("Output (with context memory):")
print(json.dumps(results, indent=2))

print()
print("=== Why This Matters ===")
print()
print("USE CASE: Retrieval-Augmented Generation (RAG)")
print("  When processing a financial document...")
print("  You want ALL facts tied to the reporting period")
print()
print("❌ Without context memory:")
print("  Only sentence 1 has time")
print("  Sentences 2-4 lose temporal context")
print("  RAG system can't properly link facts to time period")
print()
print("✅ With context memory (VagaCore):")
for i, result in enumerate(results, 1):
    if result['time']:
        print(f"  Sentence {i}: Preserves time='{result['time']}'")
print()
print("🔥 This is how industry systems work!")
print("🔥 Used in LLM pipelines, RAG systems, and knowledge bases!")
