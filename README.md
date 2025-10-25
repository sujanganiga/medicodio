# 🧠 Clinical NLP Extraction

## 📘 Overview

This project is part of the **Medicodio AI Engineer recruitment assignment**, focused on **rule-based NLP extraction** of structured clinical information from real-world reports.

The task demonstrates how to extract **diagnoses, procedures, ICD-10 codes, anatomical locations, and modifiers** from unstructured clinical text — **without using any Large Language Models (LLMs)**.

---

## 🚫 No LLM Usage

> ⚠️ **Important:**
> This solution does **not** use any LLMs, APIs, or generative models (e.g., GPT, Claude, Gemini, Mistral, etc.).
> All entity extraction is performed using:
>
> - Python regex (`re`)
> - Deterministic pattern rules
> - `spaCy` (only for tokenization & sentence segmentation)
> - Lookup dictionaries for anatomy, modifiers, and procedures
>
> The pipeline is **fully interpretable and compliant** with Medicodio's assignment constraints.

---

## ⚙️ Environment Setup

### 1️⃣ Create & activate conda environment

```bash
conda create -n clinical-nlp python=3.10
conda activate clinical-nlp
```

### 2️⃣ Install required dependencies

```bash
pip install pandas numpy regex nltk spacy scikit-learn pdfminer.six jupyterlab
python -m spacy download en_core_web_sm
```

---

## 📂 Folder Structure

```
clinical-nlp-project/
├─ data/
│   ├─ report1.txt
│   ├─ report2.txt
│   ├─ report3.txt
│   └─ report4.txt
├─ src/
│   └─ rules.py                  # All regex and rule-based extraction logic
├─ notebooks/
│   └─ clinical_extraction.ipynb # Jupyter notebook to run extraction
├─ outputs/
│   ├─ reports_extracted.json    # Final structured output (Medicodio format)
│   └─ reports_extracted.csv     # Optional readable version
└─ README.md
```

---

## 🧹 How to Run

1. **Open Jupyter Lab**

   ```bash
   jupyter lab
   ```

2. **Open and run** `notebooks/clinical_extraction.ipynb`

   - The notebook reads all `.txt` reports from `/data/`
   - Extracts entities using `src/rules.py`
   - Saves results to `/outputs/reports_extracted.json`

3. **Verify output**

   ```bash
   cat outputs/reports_extracted.json
   ```

   Example snippet:

   ```json
   [
     {
       "ReportID": "Report 1",
       "Clinical Terms": ["Colonoscopy", "Propofol", "Lidocaine"],
       "Anatomical Locations": ["Rectum", "Cecum"],
       "Diagnosis": ["Personal history of colonic polyps"],
       "Procedures": ["Colonoscopy"],
       "ICD-10": ["K64.8"],
       "CPT": [],
       "HCPCS": [],
       "Modifiers": ["Monitored Anesthesia Care"]
     }
   ]
   ```

---

## 🧠 Methodology

| Component            | Technique Used           | Description                              |
| -------------------- | ------------------------ | ---------------------------------------- |
| **Text Parsing**     | `pdfminer.six` / `.txt`  | Extracted raw text from PDF reports      |
| **Tokenization**     | `spaCy`                  | Used for sentence segmentation only      |
| **Entity Detection** | `regex`, `lookup tables` | Identifies terms, anatomy, and modifiers |
| **Codes**            | `regex` patterns         | Extracts ICD-10 and CPT codes            |
| **Output**           | `JSON`                   | Follows structured Medicodio format      |

---

## 💡 Notes

- No external APIs or internet calls are made.
- Only local deterministic NLP is used.
- Easily extendable for more patterns, custom ontologies, or datasets.

---
