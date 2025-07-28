# Approach

The core objective of this solution is to transform a static PDF document into a structured, machine-understandable JSON format. To achieve this, we designed a lightweight, offline, and fast system that extracts the document's title and a hierarchical outline consisting of heading levels H1, H2, and H3.

We used the Python library **PyMuPDF (imported as `fitz`)**, which provides fast and flexible tools to read and analyze PDF documents. The solution is fully offline and adheres to all Adobe Hackathon constraints like CPU-only execution, ≤10s runtime, and ≤200MB model size (no ML models used here).

Step-by-Step Process:

1. **Reading the PDF:**
   - We open the PDF using PyMuPDF and process it page by page.
   - For each page, we extract text blocks in "dict" mode to access low-level layout information, including font sizes and positions.

2. **Title Extraction:**
   - We treat the first non-empty line of the first page as the document title.
   - This assumption holds true in most formal documents and avoids hardcoding.

3. **Heading Detection using Font Size:**
   - Each line of text is analyzed based on the font size of its components (`span["size"]`).
   - We use font size as an **approximate indicator** of heading level. Based on empirical observation:
     - Font size ≥ 18 → classified as `H1`
     - Font size ≥ 14 and < 18 → classified as `H2`
     - Font size ≥ 11 and < 14 → classified as `H3`
   - This logic avoids relying on tags or styles, making it robust across a variety of PDF layouts.

4. **Structuring the Output:**
   - For every detected heading, we store:
     - Level (H1/H2/H3)
     - The heading text
     - The page number (1-indexed)
   - All this is saved in a clean JSON format like:

     ```json
     {
       "title": "Sample Document",
       "outline": [
         { "level": "H1", "text": "Introduction", "page": 1 },
         { "level": "H2", "text": "Background", "page": 2 }
       ]
     }
     ```

5. **Automation Across Files:**
   - The script automatically reads all `.pdf` files from the `/app/input` directory and writes a `.json` file for each into `/app/output`, as required by Adobe’s Docker execution model.

6. **Performance and Modularity:**
   - The entire pipeline runs in <10 seconds for a 50-page PDF on CPU.
   - The code is modular and easily reusable for future rounds (e.g., Round 1B).

 Why This Approach Works Well:

- It avoids file-specific logic and hardcoding.
- It requires no internet access or external services.
- It runs offline, fast, and works well for structured documents like research papers, textbooks, or reports.
- It’s general enough to be extended later with NLP for smarter heading classification.
- It’s general enough to be extended later with NLP for smarter heading classification.
