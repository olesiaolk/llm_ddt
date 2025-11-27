# LLM Attribute Extraction Tool

A lightweight Python project for testing and validating LLM output using structured attribute extraction from unstructured chat history.

## 🚀 Purpose

The tool loads chat transcripts, sends them to an LLM using a fixed system prompt, receives extracted attributes, and compares them to expected values to measure accuracy.

## 🧩 What It Does

* Reads test cases from a CSV file
* Sends each conversation to an LLM
* Extracts three attributes:

  * **Email**
  * **Phone number**
  * **Move date**
* Normalizes formatting
* Compares model output with ground truth
* Calculates overall accuracy

## ▶️ How to Run

1. Create a virtual environment
2. Install dependencies
3. Add your API key
4. Run:

```
python main.py
```

## 📊 Output Example

```
Test completed. Accuracy: 87.5%
```
