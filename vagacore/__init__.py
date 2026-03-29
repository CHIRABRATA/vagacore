"""
VagaCore - Intelligent Text Compression & Fact Extraction Engine

A production-ready NLP system combining:
- Named Entity Recognition (NER)
- Dependency Parsing
- Context-Aware Processing

Features:
- Multi-sentence processing with context memory
- Hybrid ML + Rule-based extraction
- Structured JSON output
"""

__version__ = "0.6.0"
__author__ = "VagaCore Team"

from .compressor import compress

__all__ = ["compress"]
