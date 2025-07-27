from extract.extractor import extract_sections_from_pdfs
from extract.section_ranker import rank_sections
from logic.persona_matching import filter_relevant_sections
from logic.json_formatter import format_output_json
import json
from datetime import datetime
import os

# Configuration
DATA_DIR = "data"
DOCUMENTS = [f for f in os.listdir(DATA_DIR) if f.endswith(".pdf")]
PERSONA = "Travel Planner"
TASK = "Plan a trip of 4 days for a group of 10 college friends."

if __name__ == "__main__":
    raw_sections = extract_sections_from_pdfs(DATA_DIR, DOCUMENTS)
    
    scored_sections = rank_sections(raw_sections, persona=PERSONA, task=TASK)
    
    filtered_subsections = filter_relevant_sections(scored_sections, group_type="college", trip_length=4)
    
    output_json = format_output_json(DOCUMENTS, PERSONA, TASK, filtered_subsections, datetime.now())
    
    with open("output/challenge1b_output.json", "w", encoding="utf-8") as f:
        json.dump(output_json, f, indent=2, ensure_ascii=False)
    
    print("Output written to output/challenge1b_output.json")

