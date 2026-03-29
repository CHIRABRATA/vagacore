from compressor import compress
import json

# Test case showing where context memory REALLY helps
# These sentences don't have explicit dates but relate to the same period

text = """
Apple reported strong Q4 2024 results.
Revenue was exceptional this quarter.
Margins improved significantly.
"""

print("=== Context Memory: Where It Matters ===")
print()
print("Input text (notice: only 1st sentence has date, others are vague):")
print(text)
print()

results = compress(text)
print("Output:")
print(json.dumps(results, indent=2))

print()
print("=== Analysis ===")
print("❌ WITHOUT context memory:")
print("  Sentence 1: time='Q4 2024'")
print("  Sentence 2: time=None (LOST CONTEXT)")
print("  Sentence 3: time=None (LOST CONTEXT)")
print()
print("✅ WITH context memory (VagaCore v0.5):")
for i, result in enumerate(results, 1):
    print(f"  Sentence {i}: time='{result['time']}'")
print()
print("🎯 This is exactly how RAG systems maintain context!")
