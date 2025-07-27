
# Project Approach: Persona-Driven Section Extraction and Summarization

## Overview

The goal of this project is to develop a CPU-efficient, offline system that intelligently analyzes a set of diverse PDF documents to extract and prioritize the most relevant sections, tailored to a specific user persona and task (“job to be done”). 

For the demonstration, our persona is a **Travel Planner** organizing a **4-day trip for 10 college friends to the South of France**, using seven richly varied travel-related PDFs.

---

## Methodology

### 1. Persona and Task Parsing

- The system begins by ingesting an input configuration JSON (e.g., `challenge1b_input.json`), which provides:
  - The document list
  - Persona description
  - Job-to-be-done

- These fields are tokenized and concatenated to form an **analysis context** — a unified query that guides relevance determination for subsequent extraction and ranking steps.

---

### 2. PDF Section Extraction

- Using **PyMuPDF**, the system opens each PDF and processes text **page by page**.
- The extractor **does not treat each page as a section**, but instead uses:
  - **Font size heuristics**
  - **Capitalization patterns**
  - **Regex-based rules** (e.g., `^SECTION:`, `^[A-Z][A-Za-z\s]+:$`)

#### For each detected section, the extractor records:
- Source document filename  
- Section title (from heading)  
- Section body (contiguous text beneath heading)  
- Start page number  

This **section-wise granularity** aligns with challenge requirements.

---

### 3. Section Relevance Ranking

- All extracted sections (titles + content) are vectorized using **TF-IDF** (`scikit-learn`).
- The persona and job-to-be-done context string is also vectorized.
- **Cosine similarity** is computed between each section and the persona context.

#### Relevance is boosted by:
- Additional **keyword matching** for the persona/task (e.g., "nightlife", "beach", "budget")

- **Top-ranked** sections are assigned `importance_rank` and carried forward.

---

### 4. Sub-section Analysis

- For each top-ranked section:
  - Further **chunking** and **refined summarization** is applied.
  - Focus is on **persona-relevant details** like:
    - Beach hopping highlights
    - Nightlife suggestions
    - Packing tips for groups

This dual-level analysis ensures depth and output richness.

---

### 5. Output Construction

The system writes a structured JSON file containing:

- **Metadata**:
  - Input documents
  - Persona
  - Job-to-be-done
  - Timestamp

- **extracted_sections**:
  ```json
  [
    {
      "document": "...",
      "section_title": "...",
      "importance_rank": 1,
      "page_number": ...
    }
  ]

