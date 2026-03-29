#!/usr/bin/env python3
"""Debug script to understand dependency parsing."""

from vagacore.parser import parse_text

text = "Apple reported $500 million in revenue for Q3 2024."
doc = parse_text(text)

print(f"Text: {text}")
print("\nDependency Tree:")
for token in doc:
    print(f"{token.i:2d}. {token.text:12} {token.pos_:8} {token.dep_:10} head={token.head.text}")

print("\n")

# Try another sentence
text2 = "Amazon grew by 25% compared to last quarter in Q2 2024."
doc2 = parse_text(text2)

print(f"Text: {text2}")
print("\nDependency Tree:")
for token in doc2:
    print(f"{token.i:2d}. {token.text:12} {token.pos_:8} {token.dep_:10} head={token.head.text}")
