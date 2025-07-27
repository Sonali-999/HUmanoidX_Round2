import fitz  # PyMuPDF

def extract_sections_from_pdfs(data_dir, doc_list):
    all_sections = []
    for doc_name in doc_list:
        doc_path = f"{data_dir}/{doc_name}"
        doc = fitz.open(doc_path)
        for page_num, page in enumerate(doc):
            text = page.get_text()
            all_sections.append({
                'document': doc_name,
                'page': page_num + 1,
                'text': text
            })
    return all_sections

