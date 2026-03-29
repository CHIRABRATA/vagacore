from compressor import compress
import json

# Real-world scenario: Financial report paragraph
text = """
Microsoft released its Q4 2024 financial results.
Revenue reached $62 billion, up 16% year-over-year.
Operating income surged 25% to $28 billion.
The company attributed the growth to strong cloud services demand.
Azure revenue more than doubled in the same period.
"""

print("=== Real-World Test: Financial Report with Context ===")
print("Input:")
print(text)
print()
print("Output (with context-aware time propagation):")
results = compress(text)
print(json.dumps(results, indent=2))

print()
print("=== Context Memory in Action ===")
for i, result in enumerate(results, 1):
    time_info = result['time']
    if time_info == "Q4 2024":
        source = "Original extraction"
    elif time_info == "the same period":
        source = "Original (vague reference)"
    else:
        source = "Inherited from context"
    print(f"Sentence {i}: time=\"{time_info}\" ({source})")
