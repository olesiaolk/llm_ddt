# LLM Attribute Extraction Tool

A lightweight Python project for testing and validating LLM output using structured attribute extraction from unstructured chat history.

## Purpose

The tool loads chat transcripts, sends them to an LLM using a fixed system prompt, extracts attributes, and compares them to expected values to calculate accuracy.

## What It Does

* Reads test cases from a CSV
* Sends each conversation to an LLM
* Extracts:

  * Email
  * Phone number
  * Move date
* Compares predictions with ground truth
* Outputs overall accuracy

## How to Run (Step-by-Step)

### **1. Open the project in PyCharm**

### **2. Create a virtual environment**

```
python3 -m venv .venv
```

### **3. Activate the virtual environment**

**macOS / PyCharm Terminal:**

```
source .venv/bin/activate
```

### **4. Install dependencies**

```
pip install -r requirements.txt
```

If there is no `requirements.txt`, install manually:

```
pip install pandas openai python-dotenv
```

### **5. Add your API key**

Create a `.env` file in the project root:

```
OPENAI_API_KEY=your_key_here
```

### **6. Run the program**

```
python main.py
```

Or in PyCharm:
**Right-click `main.py` → Run 'main'**

## Output Example

```
Test completed. Accuracy: 87.5%
```
