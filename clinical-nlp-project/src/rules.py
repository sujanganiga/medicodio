# src/rules.py
import re
import spacy

# Load spaCy tokenizer (not an LLM)
nlp = spacy.load("en_core_web_sm")

# ---------- Regex Dictionaries ---------- #

# Common procedures
PROCEDURE_TERMS = [
    "colonoscopy", "polypectomy", "biopsy", "EGD",
    "esophagogastroduodenoscopy", "snare", "retroflexion"
]

# Anatomy terms
ANATOMY_TERMS = [
    "rectum", "cecum", "sigmoid colon", "ascending colon", "descending colon",
    "transverse colon", "ileocecal valve", "appendiceal orifice",
    "esophagus", "stomach", "duodenum", "antrum", "pylorus"
]

# Modifiers (e.g., anesthesia terms)
MODIFIER_TERMS = [
    "ASA", "Monitored Anesthesia Care", "MAC", "General Anesthesia",
    "Lactated Ringers", "Propofol", "Lidocaine"
]

# ICD-10 and CPT regex patterns
ICD_PATTERN = r"\b[A-TV-Z][0-9]{2}(?:\.[0-9A-Za-z]{1,4})?\b"
CPT_PATTERN = r"\b[0-9]{5}\b"

# ---------- Extraction Functions ---------- #

def extract_procedures(text):
    matches = []
    for term in PROCEDURE_TERMS:
        found = re.findall(rf"\b{re.escape(term)}\b", text, flags=re.IGNORECASE)
        matches.extend(found)
    return sorted(set(m.title() for m in matches))


def extract_anatomy(text):
    matches = []
    for term in ANATOMY_TERMS:
        found = re.findall(rf"\b{re.escape(term)}\b", text, flags=re.IGNORECASE)
        matches.extend(found)
    return sorted(set(m.title() for m in matches))


def extract_modifiers(text):
    matches = []
    for term in MODIFIER_TERMS:
        found = re.findall(rf"\b{re.escape(term)}\b", text, flags=re.IGNORECASE)
        matches.extend(found)
    return sorted(set(matches))


def extract_icd10(text):
    return sorted(set(re.findall(ICD_PATTERN, text)))


def extract_cpt(text):
    return sorted(set(re.findall(CPT_PATTERN, text)))

HCPCS_PATTERN = r"\b[A-Z]\d{4}\b"  # e.g., J3010, G0105

def extract_hcpcs(text):
    return sorted(set(re.findall(HCPCS_PATTERN, text)))



def extract_diagnoses(text):
    pattern = (
        r"(?i)(Diagnosis|Impression|Post[-\s]*operative Diagnosis|"
        r"Pre[-\s]*operative Diagnosis)[:\-]?\s*(.*?)(?=\n[A-Z][a-zA-Z ]{2,}:|\Z)"
    )
    matches = re.findall(pattern, text, flags=re.DOTALL)

    diagnoses = []
    for _, block in matches:
        lines = [l.strip(" -•·") for l in block.split("\n") if len(l.strip()) > 2]
        for line in lines:
            # Keep only relevant diagnosis text
            if re.search(r"\b(K|R|Z)[0-9]{2}", line) or "[" in line or len(line.split()) <= 6:
                diagnoses.append(line)

    clean = [
        d for d in diagnoses
        if not any(x in d.lower() for x in [
            "patient", "procedure", "colonoscopy", "egd", "indication",
            "tolerated", "uneventful", "impression", "codes", "diagnosis"
        ])
    ]

    return sorted(set(clean))



def extract_all(text, report_id="Unknown"):
    data = {
        "ReportID": report_id,
        "Clinical Terms": sorted(set(extract_procedures(text) + extract_modifiers(text))),
        "Anatomical Locations": extract_anatomy(text),
        "Diagnosis": extract_diagnoses(text),
        "Procedures": extract_procedures(text),
        "ICD-10": extract_icd10(text),
        "CPT": extract_cpt(text),
        "HCPCS": extract_hcpcs(text),
        "Modifiers": extract_modifiers(text)
    }
    # Remove empty lists for cleaner JSON (optional)
    return {k: v for k, v in data.items() if v}

