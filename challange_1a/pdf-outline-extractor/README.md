# PDF Outline Extraction - Project Explanation

## Goal

The program processes PDF files placed in the input/ directory and extracts structured document outlines (like headings and paragraphs), then saves them as JSON files in the output/ directory.

## High-Level Workflow

1. Read PDF files from /app/input
2. Extract and process text spans (lines, paragraphs, headings, title)
3. Analyze the document structure
4. Export results to JSON in /app/output

## Detailed Step-by-Step Breakdown

### 1. The main() Function

* Ensures the output directory exists.
* Scans the input/ folder for .pdf files.
* Calls process_pdf() on each file.

### 2. The process_pdf(pdf_path) Function

This is the core logic for PDF processing:

#### a. Extract text spans

* Likely extracts raw text blocks and their layout metadata (bounding boxes, font size, etc.).

#### b. Group into lines

* Converts the low-level spans into logical text lines using spatial proximity.

#### c. Group lines into paragraphs

* Clusters lines into coherent paragraphs.

#### d. Compute stats

* Gathers statistical data (font size distribution, indentation, etc.) for later analysis.

#### e. Detect heading candidates

* Uses heuristics to find potential headings.

#### f. Score and filter heading candidates

* Assigns scores based on confidence and filters weak candidates.

#### g. Assign hierarchical levels to headings

* Determines heading levels (H1, H2, etc.) for document outline.

#### h. Select document title

* Picks the main document title using heading info and maybe font styles or position.

#### i. Export the final structured data

* Saves structured outline (title + headings) as a JSON file in the output/ directory.

## Example Output

Each processed PDF will result in a JSON file that may look like this:

json
{
  "title": "Some Document Title",
  "outline": [
    { "level": 1, "text": "Section 1" },
    { "level": 2, "text": "Subsection 1.1" }
  ]
}


## Ideal Use Case

This is designed for use in a Docker container with:

* Mounted volumes for input and output
* No internet/network access
* Execution via a CMD like python your_script.py in the Dockerfile