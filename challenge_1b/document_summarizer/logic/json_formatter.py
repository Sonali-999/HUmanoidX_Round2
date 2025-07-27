def format_output_json(documents, persona, task, extracted_sections, timestamp):
    output = {
        "metadata": {
            "documents": documents,
            "persona": persona,
            "job_to_be_done": task,
            "processing_timestamp": timestamp.isoformat()
        },
        "extracted_sections": []
    }
    for sec in extracted_sections:
        output["extracted_sections"].append({
            "document": sec["document"],
            "page_number": sec["page_number"],
            "section_title": sec["section_title"],
            "importance_rank": sec["importance_rank"],
            "refined_text": sec["refined_text"]
        })
    return output

