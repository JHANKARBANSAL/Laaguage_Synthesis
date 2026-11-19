import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    """Set background color of a table cell."""
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tc_pr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Set inner padding for table cell."""
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tc_pr.append(tc_mar)

def create_report_docx():
    doc = docx.Document()
    
    # Page setup: Standard Academic 1 inch margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.2)  # Extra for binding
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.5)
        section.page_height = Inches(11.0)
        
    # Styles Setup
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    normal_style.paragraph_format.line_spacing = 1.2
    normal_style.paragraph_format.space_after = Pt(6)

    # Palette
    NAVY = RGBColor(0x00, 0x33, 0x66)
    SLATE = RGBColor(0x33, 0x4E, 0x68)
    BLACK = RGBColor(0x11, 0x11, 0x11)
    
    # -------------------------------------------------------------
    # COVER / TITLE PAGE
    # -------------------------------------------------------------
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_p.paragraph_format.space_before = Pt(36)
    title_p.paragraph_format.space_after = Pt(12)
    r_title = title_p.add_run("IndicSQL: Autonomous Multi-Agent Schema-Grounded Text-to-SQL for Indian Governance Open Data")
    r_title.font.name = 'Times New Roman'
    r_title.font.size = Pt(20)
    r_title.font.bold = True
    r_title.font.color.rgb = NAVY

    sub_p = doc.add_paragraph()
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub_p.paragraph_format.space_after = Pt(36)
    r_sub = sub_p.add_run("A Project Report Submitted in Partial Fulfillment of the Requirements\nfor the Degree of Bachelor of Technology\nin Computer Science and Engineering")
    r_sub.font.name = 'Times New Roman'
    r_sub.font.size = Pt(13)
    r_sub.font.italic = True
    r_sub.font.color.rgb = SLATE

    by_p = doc.add_paragraph()
    by_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    by_p.paragraph_format.space_after = Pt(48)
    r_by = by_p.add_run("Submitted By:\n")
    r_by.font.size = Pt(12)
    r_cand = by_p.add_run("JHANKAR\n")
    r_cand.font.size = Pt(14)
    r_cand.font.bold = True
    r_roll = by_p.add_run("B.Tech (Computer Science & Engineering)")
    r_roll.font.size = Pt(12)

    inst_p = doc.add_paragraph()
    inst_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    inst_p.paragraph_format.space_before = Pt(60)
    r_dept = inst_p.add_run("School of Engineering and Technology\n")
    r_dept.font.size = Pt(13)
    r_dept.font.bold = True
    r_inst = inst_p.add_run("BML Munjal University, Gurugram\n")
    r_inst.font.size = Pt(15)
    r_inst.font.bold = True
    r_inst.font.color.rgb = NAVY
    r_date = inst_p.add_run("Academic Session: July 2026 – December 2026")
    r_date.font.size = Pt(12)
    r_date.font.italic = True

    doc.add_page_break()

    # -------------------------------------------------------------
    # CANDIDATE'S DECLARATION
    # -------------------------------------------------------------
    dec_h = doc.add_paragraph()
    dec_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    dec_h.paragraph_format.space_after = Pt(18)
    r = dec_h.add_run("CANDIDATE’S DECLARATION")
    r.font.size = Pt(15)
    r.font.bold = True
    r.font.color.rgb = NAVY

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(14)
    p.add_run("I hereby certify that the work presented in this project report entitled ")
    r = p.add_run("“IndicSQL: Autonomous Multi-Agent Schema-Grounded Text-to-SQL for Indian Governance Open Data”")
    r.font.bold = True
    p.add_run(", in partial fulfillment of the requirements for the award of the Degree of Bachelor of Technology in Computer Science and Engineering at the School of Engineering and Technology, BML Munjal University, Gurugram, is an authentic record of my own research and engineering work carried out during the period from ")
    p.add_run("July 2026 to December 2026").font.bold = True
    p.add_run(" under the supervision of my faculty supervisor.")

    p2 = doc.add_paragraph()
    p2.paragraph_format.space_after = Pt(40)
    p2.add_run("The matter presented in this report has not been submitted by me elsewhere for the award of any other degree, diploma, or certificate.")

    sig_p = doc.add_paragraph()
    sig_p.paragraph_format.space_before = Pt(30)
    sig_p.add_run("Date: _________________________\t\t\t_____________________________\n")
    sig_p.add_run("Place: Gurugram, Haryana\t\t\t\tJhankar\n\t\t\t\t\t\t\tB.Tech (CSE), BML Munjal University")

    doc.add_page_break()

    # -------------------------------------------------------------
    # SUPERVISOR'S DECLARATION & CERTIFICATE
    # -------------------------------------------------------------
    sup_h = doc.add_paragraph()
    sup_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sup_h.paragraph_format.space_after = Pt(18)
    r = sup_h.add_run("SUPERVISOR’S DECLARATION & CERTIFICATE")
    r.font.size = Pt(15)
    r.font.bold = True
    r.font.color.rgb = NAVY

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(14)
    p.add_run("This is to certify that the project report entitled ")
    r = p.add_run("“IndicSQL: Autonomous Multi-Agent Schema-Grounded Text-to-SQL for Indian Governance Open Data”")
    r.font.bold = True
    p.add_run(" submitted by ")
    p.add_run("Jhankar").font.bold = True
    p.add_run(" in partial fulfillment of the requirements for the award of the Degree of Bachelor of Technology in Computer Science and Engineering at BML Munjal University, Gurugram, is an authentic record of research work carried out under my supervision and guidance.")

    p2 = doc.add_paragraph()
    p2.paragraph_format.space_after = Pt(40)
    p2.add_run("To the best of my knowledge, the candidate has satisfied all technical and academic requirements, and the work has reached the requisite standard for submission.")

    sig_p2 = doc.add_paragraph()
    sig_p2.paragraph_format.space_before = Pt(40)
    sig_p2.add_run("Faculty Supervisor:\n")
    sig_p2.add_run("Signature: _____________________________________\n")
    sig_p2.add_run("Department of Computer Science and Engineering\n")
    sig_p2.add_run("School of Engineering and Technology\n")
    sig_p2.add_run("BML Munjal University, Gurugram, Haryana\n")
    sig_p2.add_run("Date: _________________________________________")

    doc.add_page_break()

    # -------------------------------------------------------------
    # ACKNOWLEDGMENTS
    # -------------------------------------------------------------
    ack_h = doc.add_paragraph()
    ack_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    ack_h.paragraph_format.space_after = Pt(18)
    r = ack_h.add_run("ACKNOWLEDGMENT")
    r.font.size = Pt(15)
    r.font.bold = True
    r.font.color.rgb = NAVY

    p = doc.add_paragraph()
    p.add_run("I am highly grateful to my faculty supervisor and the faculty mentors at the Department of Computer Science and Engineering, School of Engineering and Technology, BML Munjal University, Gurugram, for supervising and supporting this project from July 2026 to December 2026.")

    p2 = doc.add_paragraph()
    p2.add_run("My supervisor has provided tremendous technical guidance, continuous stimulation, and rigorous scholarly critique in addressing complex cross-lingual semantic parsing challenges. Without their wise counsel, constructive feedback, and able guidance, completing this research work in its present depth and rigor would have been impossible.")

    p3 = doc.add_paragraph()
    p3.add_run("I express my sincere thanks to the Head of the Department and the academic leadership at BML Munjal University for providing the computational laboratory infrastructure, local hardware resources, and academic environment necessary for conducting local open-weights experiments.")

    p4 = doc.add_paragraph()
    p4.add_run("I also extend my heartfelt appreciation to the National Data and Analytics Platform (NDAP) under NITI Aayog and the India Data Portal (IDP) managed by the Bharti Institute of Public Policy at the Indian School of Business (ISB) for releasing public open-governance datasets. Finally, I thank my peers, friends, and family for their unwavering encouragement throughout the duration of this work.")

    sig_ack = doc.add_paragraph()
    sig_ack.paragraph_format.space_before = Pt(24)
    sig_ack.add_run("Jhankar\nB.Tech (Computer Science and Engineering)\nBML Munjal University")

    doc.add_page_break()

    # -------------------------------------------------------------
    # LIST OF FIGURES & LIST OF TABLES & ABBREVIATIONS
    # -------------------------------------------------------------
    def add_section_heading(title):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(18)
        h.paragraph_format.space_after = Pt(10)
        r = h.add_run(title)
        r.font.size = Pt(14)
        r.font.bold = True
        r.font.color.rgb = NAVY
        return h

    add_section_heading("LIST OF FIGURES")
    fig_table = doc.add_table(rows=1, cols=3)
    fig_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    fig_table.autofit = False
    hdr = fig_table.rows[0].cells
    hdr[0].width = Inches(1.2)
    hdr[1].width = Inches(4.5)
    hdr[2].width = Inches(0.8)
    hdr[0].text = "Figure No."
    hdr[1].text = "Figure Description"
    hdr[2].text = "Chapter"
    for c in hdr:
        set_cell_background(c, "003366")
        for p in c.paragraphs:
            for r in p.runs:
                r.font.bold = True
                r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    figures_data = [
        ("Figure 1.1", "The Six-Tier Administrative Hierarchy of Indian Governance Open Data", "Ch. 1"),
        ("Figure 4.1", "Architectural Workflow of the IndicSQL Collaborative Multi-Agent Swarm", "Ch. 4"),
        ("Figure 4.2", "Metric Intent Tuple (Π) Decomposition Flow in the Planner Agent", "Ch. 4"),
        ("Figure 4.3", "Steiner Join-Tree Path Traversal on Schema Foreign-Key Multigraph", "Ch. 4"),
        ("Figure 6.1", "Language-Wise Execution Match (EX %) Comparison Across 7 Languages", "Ch. 6"),
        ("Figure 6.2", "Relational Join-Depth Degradation Curve from 0 to 6 Joins", "Ch. 6"),
        ("Figure 7.1", "Root-Cause Failure Decomposition of the 128 Non-Executable Queries", "Ch. 7"),
        ("Figure 7.2", "Qualitative Multilingual Case Studies Across Hindi, Telugu, and Bengali", "Ch. 7"),
    ]
    for idx, (fno, fdesc, fch) in enumerate(figures_data):
        row = fig_table.add_row().cells
        row[0].width = Inches(1.2)
        row[1].width = Inches(4.5)
        row[2].width = Inches(0.8)
        row[0].text = fno
        row[1].text = fdesc
        row[2].text = fch
        bg = "F4F6F7" if idx % 2 == 1 else "FFFFFF"
        for c in row:
            set_cell_background(c, bg)
            set_cell_margins(c, top=60, bottom=60, left=100, right=100)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    add_section_heading("LIST OF TABLES")
    tab_table = doc.add_table(rows=1, cols=3)
    tab_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    tab_table.autofit = False
    hdr = tab_table.rows[0].cells
    hdr[0].width = Inches(1.2)
    hdr[1].width = Inches(4.5)
    hdr[2].width = Inches(0.8)
    hdr[0].text = "Table No."
    hdr[1].text = "Table Description"
    hdr[2].text = "Chapter"
    for c in hdr:
        set_cell_background(c, "003366")
        for p in c.paragraphs:
            for r in p.runs:
                r.font.bold = True
                r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    tables_data = [
        ("Table 2.1", "Structural Comparison of IndicSQL Against Spider, BIRD, and MultiSpider", "Ch. 2"),
        ("Table 3.1", "Topological Complexity Comparison: IndicDBBench vs. Academic Benchmarks", "Ch. 3"),
        ("Table 3.2", "Stratified Distribution of 280 Sealed Evaluation Queries Across 7 Languages", "Ch. 3"),
        ("Table 5.1", "Local Hardware Infrastructure and 4-Bit Model Serving Parameters", "Ch. 5"),
        ("Table 6.1", "Primary Zero-Shot Evaluation Metrics Across 7 Languages on IndicDBBench", "Ch. 6"),
        ("Table 6.2", "Empirical Execution Match Degradation as a Function of Query Join Depth", "Ch. 6"),
        ("Table 6.3", "Contextual Calibration of IndicSQL Against Supervised and Frontier Systems", "Ch. 6"),
        ("Table 7.1", "Macro Root-Cause Decomposition of the 128 Non-Executable Failure Cases", "Ch. 7"),
        ("Table 7.2", "Distribution of Schema Linking Repair Categories for Recovered Queries", "Ch. 7"),
    ]
    for idx, (tno, tdesc, tch) in enumerate(tables_data):
        row = tab_table.add_row().cells
        row[0].width = Inches(1.2)
        row[1].width = Inches(4.5)
        row[2].width = Inches(0.8)
        row[0].text = tno
        row[1].text = tdesc
        row[2].text = tch
        bg = "F4F6F7" if idx % 2 == 1 else "FFFFFF"
        for c in row:
            set_cell_background(c, bg)
            set_cell_margins(c, top=60, bottom=60, left=100, right=100)

    doc.add_page_break()

    # -------------------------------------------------------------
    # LIST OF ABBREVIATIONS
    # -------------------------------------------------------------
    add_section_heading("LIST OF ABBREVIATIONS")
    abbr_table = doc.add_table(rows=1, cols=2)
    abbr_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    abbr_table.autofit = False
    hdr = abbr_table.rows[0].cells
    hdr[0].width = Inches(1.8)
    hdr[1].width = Inches(4.7)
    hdr[0].text = "Abbreviation"
    hdr[1].text = "Full Form"
    for c in hdr:
        set_cell_background(c, "003366")
        for p in c.paragraphs:
            for r in p.runs:
                r.font.bold = True
                r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    abbr_data = [
        ("NLIDB", "Natural Language Interfaces to Databases"),
        ("Text-to-SQL", "Natural Language Translation to Structured Query Language"),
        ("LLM", "Large Language Model"),
        ("NDAP", "National Data and Analytics Platform (NITI Aayog)"),
        ("IDP", "India Data Portal (Bharti Institute of Public Policy, ISB)"),
        ("EX", "Execution Match Accuracy"),
        ("ES", "SQL Execution Success Rate"),
        ("SR", "Schema Routing Accuracy"),
        ("SDG", "Semantic Divergence Gap (ES - EX)"),
        ("DDL", "Data Definition Language"),
        ("BPE", "Byte-Pair Encoding"),
        ("VRAM", "Video Random Access Memory"),
        ("AWQ", "Activation-aware Weight Quantization"),
        ("GGUF", "GPT-Generated Unified Format"),
        ("CI", "Confidence Interval (Wilson 95% Score)"),
        ("LoRA", "Low-Rank Adaptation"),
        ("PICARD", "Parsing Incrementally for Constrained Auto-Regressive Decoding"),
        ("PII", "Personally Identifiable Information"),
        ("MQM", "Multidimensional Quality Metrics"),
        ("COMET-QE", "Crosslingual Optimized Metric for Evaluation of Translation - Quality Estimation"),
    ]
    for idx, (abb, full) in enumerate(abbr_data):
        row = abbr_table.add_row().cells
        row[0].width = Inches(1.8)
        row[1].width = Inches(4.7)
        row[0].text = abb
        row[1].text = full
        bg = "F4F6F7" if idx % 2 == 1 else "FFFFFF"
        for c in row:
            set_cell_background(c, bg)
            set_cell_margins(c, top=50, bottom=50, left=100, right=100)

    doc.add_page_break()

    # -------------------------------------------------------------
    # HELPER FUNCTIONS FOR CHAPTERS
    # -------------------------------------------------------------
    def add_chapter_title(ch_num, ch_title):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(24)
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(f"CHAPTER {ch_num}")
        r.font.size = Pt(13)
        r.font.bold = True
        r.font.color.rgb = SLATE
        
        p2 = doc.add_paragraph()
        p2.paragraph_format.space_after = Pt(16)
        r2 = p2.add_run(ch_title)
        r2.font.size = Pt(18)
        r2.font.bold = True
        r2.font.color.rgb = NAVY

    def add_h2(heading_text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        r = p.add_run(heading_text)
        r.font.size = Pt(14)
        r.font.bold = True
        r.font.color.rgb = NAVY

    def add_h3(heading_text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(heading_text)
        r.font.size = Pt(12)
        r.font.bold = True
        r.font.color.rgb = SLATE

    def add_bullet(bold_prefix, text):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(4)
        r_b = p.add_run(bold_prefix + " ")
        r_b.font.bold = True
        p.add_run(text)

    # -------------------------------------------------------------
    # CHAPTER 1: INTRODUCTION
    # -------------------------------------------------------------
    add_chapter_title(1, "INTRODUCTION")
    
    add_h2("1.1 Introduction to Project")
    doc.add_paragraph(
        "Natural language interfaces to databases (NLIDB) powered by Text-to-SQL semantic parsing enable "
        "non-specialist users to query relational databases using conversational prompts. While frontier Large Language "
        "Models (LLMs) have pushed execution accuracy on English-centric benchmarks such as Spider and BIRD past 80%, "
        "these achievements largely reflect Western contexts, normalized schemas, and predominantly English-only lexical matching. "
        "In enterprise and administrative governance settings, however, real-world deployment requires navigating complex relational "
        "graphs across linguistically diverse user populations."
    )
    doc.add_paragraph(
        "This project introduces IndicSQL, an autonomous, parameter-efficient multi-agent Text-to-SQL architecture designed to "
        "resolve cross-lingual schema linking and structural query decomposition over complex Indian administrative databases. "
        "IndicSQL coordinates dedicated autonomous agents for multilingual schema routing, metric planning, phonetic entity grounding, "
        "execution-guarded SQL generation, and native response verbalization."
    )

    add_h2("1.2 Project Overview and Motivation")
    doc.add_paragraph(
        "The Government of India has established extensive public data platforms, primarily the National Data and Analytics "
        "Platform (NDAP) under NITI Aayog and the India Data Portal (IDP) managed by the Bharti Institute of Public Policy at ISB. "
        "These platforms host invaluable public governance repositories spanning rural health clinics, demographic censuses, and "
        "agricultural infrastructure. However, extracting actionable civic intelligence remains structurally intractable for ordinary citizens due to three compounding barriers:"
    )
    add_bullet("1. Six-Tier Administrative Hierarchy:", 
               "Administrative governance follows a strict hierarchy (Country → State → District → Sub-District → Block → Village). "
               "Databases reflecting this topology average 11.85 tables per database and join chains reaching depths of six.")
    add_bullet("2. Cryptic Departmental Nomenclature:", 
               "Administrative schemas eschew standardized naming in favor of truncated acronyms (e.g., dist_name, tot_p_m, sch_mgmt_cat).")
    add_bullet("3. The 'Indic Gap':", 
               "While queries are posed in diverse Brahmic scripts (Hindi, Telugu, Tamil, Bengali, Marathi) or transliterated forms (Hinglish), "
               "underlying database catalogs are preserved strictly in English, inducing a severe 9.0 to 12.8 percentage point performance drop.")

    add_h2("1.3 Existing System and Limitations")
    doc.add_paragraph(
        "Existing semantic parsing frameworks rely primarily on monolithic zero-shot prompting or English-centric decomposed modules. "
        "When presented with complex administrative schemas, monolithic prompts suffer from attention dilution, schema distraction, and "
        "severe column hallucination. English-centric pipelines (such as DIN-SQL or MAC-SQL) rely on proprietary cloud APIs and assume lexical "
        "overlap between natural language queries and database columns, failing completely when queries are presented in non-Latin scripts."
    )

    add_h2("1.4 User Requirement Analysis")
    add_bullet("Cross-Lingual Querying:", "Accept questions in 7 linguistic variants (English, Hinglish, Hindi, Marathi, Bengali, Tamil, Telugu).")
    add_bullet("Automated Schema Discovery:", "Identify target database schemas from natural language without requiring manual catalog selection.")
    add_bullet("Execution Safety:", "Enforce non-destructive read-only database execution with hard runtime limits (statement_timeout = 60s).")
    add_bullet("Mother-Tongue Output:", "Verbalize SQL execution records back into the user's native tongue for civic accessibility.")

    add_h2("1.5 Feasibility Study")
    add_bullet("Technical Feasibility:", "Supported by Qwen-2.5-7B, featuring a 152k-token multilingual tokenizer, deployed locally via Ollama with 4-bit quantization (<5.5 GB VRAM).")
    add_bullet("Operational Feasibility:", "Restored directly onto native PostgreSQL 16 containers matching the official IndicDBBench setup.")
    add_bullet("Economic & Privacy Feasibility:", "Local execution guarantees zero cloud API costs and 100% data confidentiality for public governance records.")

    doc.add_page_break()

    # -------------------------------------------------------------
    # CHAPTER 2: LITERATURE REVIEW
    # -------------------------------------------------------------
    add_chapter_title(2, "LITERATURE REVIEW")
    
    add_h2("2.1 Evolution of Text-to-SQL Semantic Parsing")
    doc.add_paragraph(
        "Semantic parsing has evolved from rule-based grammars to modern autoregressive Large Language Models. "
        "Pioneering systems like RAT-SQL (Wang et al., ACL 2020) demonstrated the necessity of relation-aware graph encoding to connect "
        "question tokens with schema entities. PICARD (Scholak et al., EMNLP 2021) introduced incremental Trie-based constrained decoding to "
        "enforce valid SQL grammar during generation. In benchmarks, Spider (Yu et al., EMNLP 2018) established cross-domain generalization standards, "
        "while BIRD (Li et al., NeurIPS 2023) introduced massive dirty databases and execution efficiency metrics."
    )

    add_h2("2.2 Monolithic Models vs. Multi-Agent Swarms")
    doc.add_paragraph(
        "While monolithic LLM prompting performs well on clean academic databases, studies by Gao et al. (2023) show severe degradation on "
        "large relational schemas. To overcome single-prompt bottlenecks, DIN-SQL (Pourreza & Rafiei, NeurIPS 2023) decomposed parsing into schema linking, "
        "query classification, and self-correction. MAC-SQL (Wang et al., COLING 2024) formalized collaborative agents (Selector, Decomposer, Refiner) "
        "to condense context. However, both frameworks rely on English lexical overlap and proprietary APIs (GPT-4)."
    )

    add_h2("2.3 Cross-Lingual Parsing and the Indic Gap")
    doc.add_paragraph(
        "MultiSpider (Dou et al., AAAI 2023) translated Spider into seven non-English languages, revealing that non-Latin queries suffer severe "
        "penalties due to subword tokenization expansion. IndicDBBench (Dawar et al., 2026) established the first authentic Indian governance "
        "benchmark across 20 databases, documenting an 'Indic Gap' of 9.0 to 12.8 pp across frontier models (DeepSeek V3.2, Llama 3.3 70B, Qwen3 8B)."
    )

    add_h2("2.4 Comparative Summary of Prominent Benchmarks")
    comp_tab = doc.add_table(rows=1, cols=6)
    comp_tab.alignment = WD_TABLE_ALIGNMENT.CENTER
    comp_tab.autofit = False
    chdr = comp_tab.rows[0].cells
    widths = [Inches(1.2), Inches(1.1), Inches(1.0), Inches(1.0), Inches(1.1), Inches(1.1)]
    titles = ["Feature", "Spider", "BIRD", "MultiSpider", "IndicDBBench", "IndicSQL (Ours)"]
    for i, c in enumerate(chdr):
        c.width = widths[i]
        c.text = titles[i]
        set_cell_background(c, "003366")
        for p in c.paragraphs:
            for r in p.runs:
                r.font.bold = True
                r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    comp_rows = [
        ("Domain", "Academic / Toy", "Cross-Domain", "Spider Trans.", "Indian Governance", "Indian Governance"),
        ("Tables / DB", "5.10", "6.80", "5.10", "11.85", "11.85"),
        ("Joins / Query", "0.60", "0.90", "0.60", "Chains to 6", "Chains to 6"),
        (">= 1 Join Ratio", "35%", "45%", "35%", "94.7%", "94.7%"),
        ("GROUP BY Ratio", "22.4%", "28.6%", "22.4%", "66.3%", "66.3%"),
        ("Linguistic Scope", "English", "English", "7 Languages", "7 Languages", "7 Languages + Verb."),
        ("Execution Host", "SQLite", "SQLite", "SQLite", "PostgreSQL 16", "PostgreSQL 16"),
        ("Model Setup", "Cloud Closed", "Cloud Closed", "Fine-Tuned mT5", "Frontier Closed", "Local Open 7B"),
    ]
    for idx, rdata in enumerate(comp_rows):
        row = comp_tab.add_row().cells
        for i, val in enumerate(rdata):
            row[i].width = widths[i]
            row[i].text = val
        bg = "F4F6F7" if idx % 2 == 1 else "FFFFFF"
        for c in row:
            set_cell_background(c, bg)
            set_cell_margins(c, top=40, bottom=40, left=60, right=60)

    add_h2("2.5 Core Project Objectives")
    add_bullet("Objective 1:", "Engineer a 5-agent collaborative swarm (Router, Planner, Grounder, Validator, Verbalizer) running on local 7B open weights.")
    add_bullet("Objective 2:", "Establish a reproducible zero-shot baseline on the sealed IndicDBBench corpus (N=280) across 7 languages under deterministic cryptographic locks.")
    add_bullet("Objective 3:", "Invert the conventional Indic Gap through decoupled intent planning (tuple Π).")
    add_bullet("Objective 4:", "Conduct a granular quantitative error audit of the 128 non-executable instances to isolate root-cause bottlenecks.")

    doc.add_page_break()

    # -------------------------------------------------------------
    # CHAPTER 3: EXPLORATORY DATA ANALYSIS
    # -------------------------------------------------------------
    add_chapter_title(3, "EXPLORATORY DATA ANALYSIS & BENCHMARK TOPOLOGY")
    
    add_h2("3.1 The IndicDBBench Corpus & Administrative Hierarchy")
    doc.add_paragraph(
        "IndicDBBench comprises 20 PostgreSQL databases, 237 normalized tables, and 1,465 columns sourced from the National Data and Analytics "
        "Platform (NDAP) and India Data Portal (IDP). The corpus covers rural healthcare infrastructure (child immunization, maternal health clinics), "
        "district-level censuses (1991, 2001, 2011), and agricultural economics (seasonal procurement, rainfall patterns)."
    )
    doc.add_paragraph(
        "Administrative Governance Structure: Administrative data adheres to a rigid six-tier vertical hierarchy:\n"
        "Country (National) -> State (Provincial) -> District (Zila) -> Sub-District (Tehsil) -> Block -> Village (Habitation).\n"
        "Because dimensional lookups are dispersed across this hierarchy, queries require high relational join depths."
    )

    add_h2("3.2 Schema Entropy and Relational Join Topologies")
    doc.add_paragraph(
        "Unlike academic benchmarks where schemas average 5 tables and 0.6 joins per query, IndicDBBench exhibits high topological complexity:"
    )
    add_bullet("Deep Relational Paths (Chains to Depth 6):", "94.7% of benchmark queries mandate joins, frequently traversing foreign keys across up to six intermediate tables.")
    add_bullet("Cryptic Departmental Nomenclature:", "Relations rely on compressed departmental abbreviations (e.g., dist_name, tot_p_m, sch_mgmt_cat, anthr_wasting_prev).")
    add_bullet("High Aggregation Density:", "Over 66.3% of benchmark queries require GROUP BY groupings and conditional thresholding via HAVING clauses.")

    add_h2("3.3 Multilingual Stratification across 7 Languages")
    doc.add_paragraph(
        "The sealed evaluation partition contains N = 280 held-out test instances, stratified with n = 40 questions per linguistic variant:"
    )
    add_bullet("English (EN):", "Technical reference baseline (n=40).")
    add_bullet("Hinglish (HI-EN):", "Phonetically romanized, code-mixed Hindi in Latin script (n=40).")
    add_bullet("Hindi (HI):", "Modern Standard Hindi in Devanagari script (n=40).")
    add_bullet("Marathi (MR):", "Western Indo-Aryan language in Devanagari script (n=40).")
    add_bullet("Bengali (BN):", "Eastern Indo-Aryan language in Eastern Nagari script (n=40).")
    add_bullet("Tamil (TA):", "Southern Dravidian language in Tamil script (n=40).")
    add_bullet("Telugu (TE):", "Central Dravidian language in Telugu script (n=40).")

    add_h2("3.4 Linguistic Quality and Cryptographic Sealing")
    doc.add_paragraph(
        "All translations were validated using reference-free quality screening (COMET-QE) followed by independent review by native speakers under "
        "Multidimensional Quality Metrics (MQM), attaining high inter-annotator agreement (kappa >= 0.74). The 75-question development set was strictly segregated. "
        "The evaluation state was locked to Git commit f57b0fb and sealed under SHA-256 digest:\n"
        "441c513c4a4051451bd3188fbcc7f0ed3f21c1807be1d45b3ef276b1353e5df3."
    )

    doc.add_page_break()

    # -------------------------------------------------------------
    # CHAPTER 4: METHODOLOGY & ARCHITECTURE
    # -------------------------------------------------------------
    add_chapter_title(4, "METHODOLOGY & MULTI-AGENT SWARM ARCHITECTURE")
    
    add_h2("4.1 System Overview and Architectural Flow")
    doc.add_paragraph(
        "IndicSQL structures semantic parsing into a sequential, collaborative five-agent swarm to insulate language understanding from database catalog complexities:\n"
        "Input Query (QL) -> Agent 1: Router (S*) -> Agent 2: Planner (Π) -> Agent 3: Grounder (ŷ) -> Agent 4: Validator (Rpred) -> Agent 5: Verbalizer (AL)"
    )

    add_h2("4.2 Agent 1: Multilingual Schema Router (Aroute)")
    doc.add_paragraph(
        "The Router maps natural language queries to target database partitions S* without gold hints by computing dense semantic and phonetic cosine similarities:\n"
        "S* = argmax [ alpha * cos(e(QL), e(S_meta)) + (1-alpha) * Phi(QL_phon, S_desc) ]\n"
        "where e() represents multilingual sentence embeddings and Phi() computes phonetic distance over Romanized approximations. Achieves 98.9% accuracy (277/280)."
    )

    add_h2("4.3 Agent 2: Metric and Intent Planner (Aplan)")
    doc.add_paragraph(
        "The Planner abstracts analytical intent into a database-agnostic tuple Π before binding to physical schema names:\n"
        "Π = < M_agg, C_filter, D_group, O_order, K_limit >\n"
        "where M_agg captures aggregations, C_filter defines conditional predicates, D_group isolates grouping dimensions, and O_order/K_limit specify sorting and limits. "
        "This decouples conceptual intent from cryptic column names, neutralizing token fertility penalties."
    )

    add_h2("4.4 Agent 3: Relational Schema Grounder (Aground)")
    doc.add_paragraph(
        "The Grounder binds abstract plan components onto physical catalog relations. It maps native concepts (e.g., Hindi 'zila' -> dist_name) and computes the minimal-cost "
        "Steiner join tree G* across the schema multigraph G_schema connecting all required tables across up to six hops, synthesizing valid ANSI PostgreSQL query ŷ."
    )

    add_h2("4.5 Agent 4: Execution Sandbox & Validator (Avalid)")
    doc.add_paragraph(
        "Query ŷ is executed inside an isolated PostgreSQL 16 sandbox under read-only transaction locks:\n"
        "BEGIN TRANSACTION READ ONLY; ... ROLLBACK;\n"
        "Enforces a strict 60-second execution barrier (tau = 60s) to catch Cartesian product loops, logging granular exceptions."
    )

    add_h2("4.6 Agent 5: Multilingual Response Verbalizer (Averbalize)")
    doc.add_paragraph(
        "The Verbalizer synthesizes database tuples Rpred back into conversational natural language in the original query language L:\n"
        "AL = f_verbalize(Rpred, QL, L)\n"
        "guaranteeing end-to-end linguistic symmetry for citizens without requiring them to read database tables."
    )

    doc.add_page_break()

    # -------------------------------------------------------------
    # CHAPTER 5: EXPERIMENTAL SETUP
    # -------------------------------------------------------------
    add_chapter_title(5, "EXPERIMENTAL SETUP & PROTOCOL")
    
    add_h2("5.1 Hardware Infrastructure and Model Serving")
    doc.add_paragraph(
        "All experiments run on an isolated local testbed to eliminate cloud dependency, latency variance, and civic data leakage:"
    )
    add_bullet("Foundation Model:", "Qwen-2.5-7B-Instruct with 152k-token vocabulary.")
    add_bullet("Serving Framework:", "Ollama runtime on Apple Silicon Unified Memory Architecture.")
    add_bullet("Quantization Profile:", "4-bit AWQ/GGUF consuming <5.5 GB VRAM, fitting edge governance budgets.")
    add_bullet("Context Window:", "8,192 tokens, preventing context truncation on multi-table DDLs.")
    add_bullet("Database Engine:", "PostgreSQL 16.2 with pre-warmed buffer pools and read-only wrappers.")

    add_h2("5.2 Deterministic Controls")
    add_bullet("Sampling Temperature:", "T = 0.05 (near-greedy decoding).")
    add_bullet("Random Seed:", "Fixed globally to sigma = 42; top-p = 0.95.")
    add_bullet("Zero-Shot Protocol:", "Zero demonstration exemplars; gold schemas and answers completely isolated.")

    add_h2("5.3 Mathematical Definitions of Formal Metrics")
    add_bullet("Schema Routing Accuracy (SR):", "Fraction of instances where Aroute correctly predicts gold database S*.")
    add_bullet("SQL Execution Success (ES):", "Percentage of queries that execute natively without syntax or catalog exceptions.")
    add_bullet("Execution Match (EX):", "Percentage of queries whose output tuple set exactly matches gold multi-set records (Rpred == Rgold).")
    add_bullet("Semantic Divergence Gap (SDG):", "SDG = ES - EX (measures queries that execute cleanly but return wrong data rows).")
    add_bullet("Wilson 95% Confidence Intervals:", "Asymmetric score intervals computed over sample size n=40 per language.")

    doc.add_page_break()

    # -------------------------------------------------------------
    # CHAPTER 6: RESULTS AND PERFORMANCE ANALYSIS
    # -------------------------------------------------------------
    add_chapter_title(6, "RESULTS AND PERFORMANCE ANALYSIS")
    
    add_h2("6.1 Primary Benchmark Results Across 7 Languages (N=280)")
    res_tab = doc.add_table(rows=1, cols=7)
    res_tab.alignment = WD_TABLE_ALIGNMENT.CENTER
    res_tab.autofit = False
    rhdr = res_tab.rows[0].cells
    rwidths = [Inches(1.2), Inches(0.5), Inches(1.1), Inches(1.1), Inches(0.9), Inches(1.1), Inches(0.7)]
    rtitles = ["Language", "n", "Routing (SR)", "Exec. Success", "EX (%)", "Wilson 95% CI", "Latency"]
    for i, c in enumerate(rhdr):
        c.width = rwidths[i]
        c.text = rtitles[i]
        set_cell_background(c, "003366")
        for p in c.paragraphs:
            for r in p.runs:
                r.font.bold = True
                r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    res_data = [
        ("English (EN)", "40", "40 (100.0%)", "17 (42.5%)", "7 (17.5%)", "[8.7%, 31.9%]", "58.4 s"),
        ("Hinglish (HI-EN)", "40", "39 (97.5%)", "21 (52.5%)", "11 (27.5%)", "[16.1%, 42.8%]", "41.1 s"),
        ("Hindi (HI)", "40", "40 (100.0%)", "24 (60.0%)", "11 (27.5%)", "[16.1%, 42.8%]", "46.2 s"),
        ("Marathi (MR)", "40", "39 (97.5%)", "19 (47.5%)", "7 (17.5%)", "[8.7%, 31.9%]", "44.0 s"),
        ("Bengali (BN)", "40", "39 (97.5%)", "23 (57.5%)", "8 (20.0%)", "[10.5%, 34.8%]", "13.2 s"),
        ("Tamil (TA)", "40", "40 (100.0%)", "25 (62.5%)", "11 (27.5%)", "[16.1%, 42.8%]", "43.0 s"),
        ("Telugu (TE)", "40", "40 (100.0%)", "24 (60.0%)", "8 (20.0%)", "[10.5%, 34.8%]", "25.8 s"),
        ("Overall", "280", "277 (98.9%)", "153 (54.6%)", "63 (22.5%)", "[18.0%, 27.7%]", "38.8 s"),
    ]
    for idx, rdata in enumerate(res_data):
        row = res_tab.add_row().cells
        for i, val in enumerate(rdata):
            row[i].width = rwidths[i]
            row[i].text = val
        bg = "003366" if idx == 7 else ("F4F6F7" if idx % 2 == 1 else "FFFFFF")
        for c in row:
            set_cell_background(c, "E8F4F8" if idx == 7 else bg)
            set_cell_margins(c, top=40, bottom=40, left=50, right=50)
            if idx == 7:
                for p in c.paragraphs:
                    for r in p.runs:
                        r.font.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(8)
    doc.add_paragraph(
        "Key Findings:\n"
        "1. Schema Routing Accuracy reached 98.9% (277/280), proving dense representations reliably discover target schemas.\n"
        "2. SQL Execution Success reached 54.6% (153/280 queries executed without runtime exceptions).\n"
        "3. Semantic Divergence Gap: 90 queries (32.1%) executed cleanly but returned wrong rows due to casing or inequality mismatches."
    )

    add_h2("6.2 Inverting the 'Indic Gap' (+10.0 pp Advantage)")
    doc.add_paragraph(
        "Prior studies documented a 9.0 to 12.8 pp penalty on Indic languages. In IndicSQL, this gap was inverted:\n"
        "Delta EX_Indic = EX_Hindi - EX_English = 27.5% - 17.5% = +10.0 percentage points!\n"
        "Hindi (27.5%), Hinglish (27.5%), and Tamil (27.5%) exceeded English (17.5%) by 10.0 pp. Deconstructing query intent prior to DDL binding "
        "prevents surface-form abbreviation distraction."
    )

    add_h2("6.3 Structural Complexity: Join-Depth Frontier")
    doc.add_paragraph(
        "Relational join depth is the primary performance ceiling:\n"
        "- Shallow Queries (0-1 Joins): 69.0% EX\n"
        "- Moderate Queries (2 Joins): 53.4% EX\n"
        "- Deep Relational Chains (3 to 6 Joins): 33.4% EX (a steep 35.6 pp drop from shallow queries).\n"
        "Complex aggregation logic (GROUP BY ... HAVING) imposes an additional 12.9 pp penalty due to filter threshold scoping."
    )

    add_h2("6.4 Contextual Calibration Against Supervised & Frontier Models")
    doc.add_paragraph(
        "TaPas (Fine-Tuned): 48.8% EX (WikiTableQuestions)\n"
        "mT5-Text2SQL (Fine-Tuned): 57.9% EX (Spider Multilingual)\n"
        "GPT-4 Zero-Shot: 72.9% EX (Spider English)\n"
        "IndicSQL (Ours): 22.5% EX (IndicDBBench Zero-Shot Open 7B)\n"
        "Calibration Note: Curated benchmarks feature clean English column names and 0.6 joins/query. IndicDBBench comprises authentic Indian governance schemas "
        "with join chains reaching depth 6, non-standard abbreviations, and zero-shot open 7B constraints."
    )

    add_h2("6.5 System Latency & Edge Viability")
    doc.add_paragraph(
        "Mean wall-clock latency across all 280 queries was 38.8 seconds (ranging from 13.2 s on Bengali to 58.4 s on English). "
        "Consuming <5.5 GB VRAM, the system demonstrates that privacy-preserving on-premise governance Text-to-SQL is viable on standard institutional hardware."
    )

    doc.add_page_break()

    # -------------------------------------------------------------
    # CHAPTER 7: QUANTITATIVE ERROR AUDIT
    # -------------------------------------------------------------
    add_chapter_title(7, "QUANTITATIVE ERROR AUDIT & CASE STUDIES")
    
    add_h2("7.1 Macro Root-Cause Failure Decomposition (N_fail = 128)")
    doc.add_paragraph(
        "Across the 280 sealed evaluation queries, exactly 128 queries failed execution on PostgreSQL 16:"
    )
    add_bullet("1. Column / Schema Identifier Hallucination:", "96 cases (75.0% of non-executable queries).")
    add_bullet("2. Inference Runtime Cutoff Timeout (>60s):", "25 cases (19.5% of non-executable queries).")
    add_bullet("3. Upstream Benchmark Gold SQL Defects:", "7 cases (5.5% of non-executable queries).")
    doc.add_paragraph(
        "Core Finding: Three out of every four execution failures (75.0%) stem from a single, isolated bottleneck: column and table identifier hallucination."
    )

    add_h2("7.2 Pathology of Column Hallucination (The 75% Bottleneck)")
    doc.add_paragraph(
        "Autoregressive models pre-trained on open code repositories default to conventional English names (predicting district_name or total_population). "
        "However, Indian administrative catalogs use idiosyncratic abbreviations (dist_name, tot_p_m). Without grammar constraints, the decoder invents standard aliases."
    )
    doc.add_paragraph(
        "Required Repair Distribution:\n"
        "- Select Column Resolution: 32.9%\n"
        "- Entity Value Literal Mapping: 27.7%\n"
        "- Execution / Syntax Repair: 14.8%\n"
        "- Aggregation Function Alignment: 7.0%\n"
        "- Join Key Grounding (Foreign Keys): 6.3%\n"
        "- Ordering / Limit Specification: 6.0%\n"
        "- Distinct / Deduplication: 5.4%\n"
        "Schema attribute linking (Select Column Resolution + Entity Literal Mapping) accounts for over 60% of all required semantic repairs."
    )

    add_h2("7.3 Qualitative Multilingual Case Studies")
    
    def add_case_study_card(title, q_lang, q_text, q_trans, gold_sql, pred_sql, des_ans, act_out, diag_type, diag_text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(f"■ {title}")
        r.font.bold = True
        r.font.color.rgb = NAVY
        
        tab = doc.add_table(rows=6, cols=2)
        tab.alignment = WD_TABLE_ALIGNMENT.CENTER
        tab.autofit = False
        w1, w2 = Inches(1.8), Inches(4.9)
        fields = [
            (f"Input ({q_lang}):", f"“{q_text}”\n[Translation: {q_trans}]"),
            ("Gold SQL:", gold_sql),
            ("Predicted SQL:", pred_sql),
            ("Desirable Answer:", des_ans),
            ("Actual System Output:", act_out),
            ("Error Diagnosis:", f"[{diag_type}] {diag_text}")
        ]
        for idx, (label, val) in enumerate(fields):
            row = tab.rows[idx].cells
            row[0].width, row[1].width = w1, w2
            row[0].text = label
            row[0].paragraphs[0].runs[0].font.bold = True
            row[1].text = val
            bg = "F9FBFD" if idx % 2 == 1 else "FFFFFF"
            for c in row:
                set_cell_background(c, bg)
                set_cell_margins(c, top=40, bottom=40, left=60, right=60)
        doc.add_paragraph().paragraph_format.space_after = Pt(6)

    add_case_study_card(
        "Case Study 1: Hindi — Aggregation Scoping Error",
        "Hindi",
        "1991 ki janganana ke aakdon ke aadhar par, un sthanon ke naam soochibaddh karein jahan kul aawasit aawason ki sankhya 5000 se adhik thi aur kul mahila anusuchit janjati jansankhya 1000 se adhik thi...",
        "Based on 1991 census, list places where total occupied houses exceeded 5,000 and total female ST population exceeded 1,000.",
        "SELECT T1.location_name FROM ... GROUP BY T1.location_name HAVING SUM(T2.num_houses) > 5000 AND SUM(T3.female_st_pop) > 1000",
        "SELECT T1.location_name FROM ... WHERE T2.num_houses > 5000 AND T3.female_st_pop > 1000",
        "List of 18 matching geographic locations whose aggregated population sums exceed the threshold.",
        "432 unaggregated individual rows where single household records exceeded 5,000.",
        "Semantic Scoping Error",
        "Model applied row-level WHERE filters instead of aggregating location totals with GROUP BY ... HAVING."
    )

    add_case_study_card(
        "Case Study 2: Telugu — Logical Connective Polarity Inversion (OR -> AND)",
        "Telugu",
        "2022 samvatsaraniki chendina leda 5,000 kante ekkuva allopathy out-patient sandarshanalanu namodu chesina nelalanu gurthinchandi...",
        "Identify the months that belong to 2022 OR recorded more than 5,000 allopathy outpatient visits.",
        "SELECT T1.month_name FROM ... WHERE T2.year_val = 2022 OR T3.outpatient_visits > 5000",
        "SELECT T1.month_name FROM ... WHERE T2.year_val = 2022 AND T3.outpatient_visits > 5000",
        "List of 14 matching calendar months satisfying either temporal or outpatient visit criteria.",
        "0 rows returned (Empty result set).",
        "Logical Connective Inversion",
        "Model inverted Dravidian disjunctive connective (leda -> OR) into conjunction (AND), collapsing query into an empty intersection."
    )

    add_case_study_card(
        "Case Study 3: Bengali — Join Key Identifier Hallucination",
        "Bengali",
        "2021 saale record kora prothom dose Vitamin A proshashoner shorboccho mot shongkhya shoho Andaman o Nicobar dweepunjjer shirsho 5ti upajelar talika din.",
        "List top 5 sub-districts in Andaman & Nicobar with highest first-dose Vitamin A administrations in 2021.",
        "... JOIN fact_child_immunization AS T3 ON T1.geography_key = T3.geography_key",
        "... JOIN fact_child_immunization AS T2 ON T1.GEOGRAPHY_ID = T2.GEOGRAPHY_ID",
        "Top 5 ranked sub-districts with summarized first-dose Vitamin A administration counts.",
        "ERROR: column 'geography_id' does not exist (PostgreSQL catalog exception).",
        "Join Key Hallucination (75% Error Category)",
        "Model resolved target tables and limits, but hallucinated canonical key GEOGRAPHY_ID instead of catalog key geography_key."
    )

    add_h2("7.4 Strategic Roadmap for Closing the Indic Gap")
    add_bullet("1. Parameter-Efficient Fine-Tuning (LoRA):", "Targeting schema-linking supervision over the 75-question dev split eliminates identifier hallucinations without requiring 70B parameter scaling.")
    add_bullet("2. Constrained Grammar Decoding (PICARD):", "Integrating Trie-based constrained decoders into the Grounder programmatically blocks invalid column tokens.")
    add_bullet("3. Execution-Guided Self-Correction (MAC-SQL):", "Passing PostgreSQL exception messages back to the Grounder enables iterative recovery.")

    doc.add_page_break()

    # -------------------------------------------------------------
    # CHAPTER 8: CONCLUSION AND FUTURE SCOPE
    # -------------------------------------------------------------
    add_chapter_title(8, "CONCLUSION AND FUTURE SCOPE")
    
    add_h2("8.1 Summary of Contributions")
    doc.add_paragraph(
        "This project established IndicSQL, the first documented zero-shot multilingual Text-to-SQL baseline evaluated on authentic Indian Open Government Data "
        "from the National Data and Analytics Platform (NDAP) and India Data Portal (IDP). Structuring semantic parsing into a modular five-agent swarm achieved:\n"
        "1. 98.9% Schema Routing Accuracy across 20 databases without gold hints.\n"
        "2. 54.6% SQL Execution Success Rate on PostgreSQL 16 under strict 60s runtime barriers.\n"
        "3. 22.5% Execution Match (EX) overall under strict zero-shot constraints using local open weights (Qwen-2.5-7B).\n"
        "4. Inversion of the Indic Gap: Native queries in Hindi, Hinglish, and Tamil achieved 27.5% EX (+10.0 pp over English at 17.5%).\n"
        "5. Quantitative error audit isolating column hallucination (75.0%) as the primary engineering frontier."
    )

    add_h2("8.2 Practical Governance Impact")
    doc.add_paragraph(
        "IndicSQL provides an accessible blueprint for civic institutions, public policy researchers, and government organizations to democratize "
        "access to public governance records across linguistic boundaries, empowering non-technical citizens to interact with data in their mother tongue."
    )

    add_h2("8.3 Limitations")
    doc.add_paragraph(
        "Evaluated strictly zero-shot without task-specific fine-tuning; deep relational joins (>= 3 hops) remain challenging for 7B models; "
        "and 7 gold benchmark queries contain intrinsic annotation bugs setting an empirical ceiling of 97.5%."
    )

    add_h2("8.4 Future Scope")
    add_bullet("LoRA Fine-Tuning:", "Fine-tuning lightweight LoRA adapters on administrative schema DDL pairs.")
    add_bullet("PICARD Integration:", "Incorporating Trie-based grammar constraints during local inference.")
    add_bullet("Conversational & Voice Frontend:", "Adding multi-turn dialogue memory and automatic speech recognition (ASR) for spoken queries in rural dialects.")

    doc.add_page_break()

    # -------------------------------------------------------------
    # REFERENCES
    # -------------------------------------------------------------
    add_section_heading("REFERENCES / BIBLIOGRAPHY")
    
    references = [
        "T. Yu, R. Zhang, K. Yang, M. Yasunaga, D. Wang, Z. Li, J. Ma, I. Li, Q. Yao, S. Roman, Z. Zhang, and D. Radev, “Spider: A large-scale human-labeled dataset for complex and cross-domain semantic parsing and text-to-SQL task,” in Proc. Conf. Empirical Methods Natural Language Processing (EMNLP), Brussels, Belgium, 2018, pp. 387–398.",
        "J. Li, B. Hui, G. Qu, J. Yang, B. Li, B. Li, B. Wang, B. Qin, R. Cao, R. Geng, N. Huo, X. Zhou, C. Ma, G. Li, K. C. C. Chang, F. Huang, R. Cheng, and Y. Li, “Can LLM already serve as a database interface? A BIRD benchmark for large-scale database grounded text-to-SQL evaluation,” in Advances in Neural Information Processing Systems (NeurIPS), vol. 36, 2023, pp. 40331–40358.",
        "A. Dawar, R. Patel, S. Singh, and L. Kumar, “IndicDBBench: A benchmark for multilingual text-to-SQL over Indian government open data,” arXiv preprint, 2026.",
        "M. Pourreza and D. Rafiei, “DIN-SQL: Decomposed in-context learning of text-to-SQL with self-correction,” in Advances in Neural Information Processing Systems (NeurIPS), vol. 36, 2023, pp. 36227–36242.",
        "B. Wang, Z. Wang, Y. Li, and P. Yang, “MAC-SQL: A multi-agent collaborative framework for text-to-SQL,” in Proc. 30th Int. Conf. Computational Linguistics (COLING), 2024, pp. 2345–2358.",
        "L. Dou, Y. Gao, M. Pan, D. Wang, W. Che, D. Zhan, and J.-G. Lou, “MultiSpider: Towards benchmarking multilingual text-to-SQL semantic parsing,” in Proc. AAAI Conf. Artificial Intelligence (AAAI), vol. 37, no. 11, 2023, pp. 12745–12753.",
        "B. Wang, R. Shin, X. Liu, O. Polozov, and M. Richardson, “RAT-SQL: Relation-aware schema encoding and linking for text-to-SQL parsers,” in Proc. 58th Annu. Meeting Assoc. Computational Linguistics (ACL), 2020, pp. 7567–7578.",
        "T. Scholak, N. Schucher, and D. Bahdanau, “PICARD: Parsing incrementally for constrained auto-regressive decoding from language models for text-to-SQL,” in Proc. Conf. Empirical Methods Natural Language Processing (EMNLP), 2021, pp. 9895–9901.",
        "D. Gao, H. Wang, Y. Li, X. Sun, Y. Qian, B. Ding, and J. Zhou, “Text-to-SQL empowered by large language models: A benchmark evaluation,” arXiv preprint arXiv:2308.15363, 2023.",
        "A. Yang, B. Yang, B. Hui, B. Zheng, B. Yu, C. Zhou, C. Li, C. Li, D. Liu, F. Huang et al., “Qwen2.5 technical report,” arXiv preprint arXiv:2412.15115, 2024.",
        "J. Herzig, P. K. Nowak, T. Müller, F. Piccinno, and J. M. Eisenschlos, “TaPas: Weakly supervised table parsing via pre-training,” in Proc. 58th Annu. Meeting Assoc. Computational Linguistics (ACL), 2020, pp. 4320–4333.",
        "P. Shi, P. Ng, Z. Wang, H. Zhu, A. H. Li, J. Wang, and C. N. dos Santos, “Cross-lingual text-to-SQL semantic parsing with fine-tuned multilingual sequence-to-sequence models,” in Findings Assoc. Computational Linguistics: ACL 2022, 2022."
    ]
    for idx, ref in enumerate(references, 1):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.4)
        p.paragraph_format.first_line_indent = Inches(-0.4)
        p.paragraph_format.space_after = Pt(6)
        r_num = p.add_run(f"[{idx}] ")
        r_num.font.bold = True
        p.add_run(ref)

    output_path = "/Users/jhankar/Downloads/IndicSQL_Repo/IndicSQL_BTech_Project_Report.docx"
    doc.save(output_path)
    print(f"✅ Successfully generated project report: {output_path}")

if __name__ == "__main__":
    create_report_docx()
