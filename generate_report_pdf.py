"""
Generate Comprehensive Academic Project Report PDF for SOCIAL DETECTIVE.
Uses ReportLab with high aesthetic typography, tables, and structured sections.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable, Image
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute and draw total page numbers and running headers/footers."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#64748b"))

        # Don't draw running header on cover/first page
        if self._pageNumber > 1:
            # Running Header
            self.drawString(54, 750, "SOCIAL DETECTIVE — Project Summary & Academic Viva Report")
            self.drawRightString(612 - 54, 750, "Case #001: The Vanishing File")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(54, 742, 612 - 54, 742)

        # Running Footer
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(54, 45, 612 - 54, 45)

        self.setFont("Helvetica", 8)
        self.drawString(54, 32, "Computer Science & Engineering · Data Structures & Algorithms Project")
        self.drawRightString(612 - 54, 32, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()


def build_pdf(filename="Social_Detective_Project_Report.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom Palette
    c_primary = colors.HexColor("#0f172a")    # Deep Slate
    c_accent = colors.HexColor("#0284c7")     # Cyan / Deep Sky Blue
    c_secondary = colors.HexColor("#475569")  # Slate Gray
    c_dark = colors.HexColor("#1e293b")
    c_bg_light = colors.HexColor("#f8fafc")
    c_border = colors.HexColor("#e2e8f0")
    c_code_bg = colors.HexColor("#f1f5f9")
    c_green = colors.HexColor("#059669")
    c_amber = colors.HexColor("#d97706")
    c_red = colors.HexColor("#dc2626")

    # Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=c_primary,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=c_accent,
        spaceAfter=14
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=c_primary,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=c_dark,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#334155"),
        spaceAfter=6
    )

    body_bold = ParagraphStyle(
        'Body_Bold_Custom',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    callout_style = ParagraphStyle(
        'Callout_Text',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=c_dark
    )

    code_style = ParagraphStyle(
        'Code_Snippet',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#0f172a")
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#1e293b")
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=table_cell_style,
        fontName='Helvetica-Bold'
    )

    caption_style = ParagraphStyle(
        'FigureCaption',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=c_primary,
        alignment=1,
        spaceBefore=4,
        spaceAfter=2
    )

    figure_desc_style = ParagraphStyle(
        'FigureDesc',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=7.5,
        leading=10,
        textColor=c_secondary,
        alignment=1,
        spaceAfter=8
    )

    story = []

    # =========================================================================
    # 1. HEADER & META BANNER
    # =========================================================================
    story.append(Paragraph("🕵️‍♂️ SOCIAL DETECTIVE: Every Connection Is Evidence", title_style))
    story.append(Paragraph("Comprehensive Academic Project Report, System Architecture & Viva Guide", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_accent, spaceBefore=0, spaceAfter=10))

    meta_table_data = [
        [
            Paragraph("<b>Project Domain:</b> Data Structures & Algorithms / Web Forensics", table_cell_style),
            Paragraph("<b>Implementation Language:</b> Python 3.8+ (Pure Custom DSA)", table_cell_style),
        ],
        [
            Paragraph("<b>Architecture:</b> Flask MVC + Vanilla JS + Web Audio", table_cell_style),
            Paragraph("<b>Case Narrative:</b> Case #001 — The Vanishing File", table_cell_style),
        ],
        [
            Paragraph("<b>Data Structures Implemented:</b> 12 Custom Data Structures", table_cell_style),
            Paragraph("<b>Academic Scope:</b> Mini/Major Project, Viva Presentation, Lab Portfolio", table_cell_style),
        ]
    ]
    meta_table = Table(meta_table_data, colWidths=[250, 254])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_bg_light),
        ('BOX', (0, 0), (-1, -1), 0.5, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # =========================================================================
    # 2. EXECUTIVE SUMMARY & ABSTRACT
    # =========================================================================
    story.append(Paragraph("1. Executive Summary & Project Motivation", h1_style))
    story.append(Paragraph(
        "<b>SOCIAL DETECTIVE</b> is an interactive cyber forensics mystery web application designed to demonstrate the practical, real-world utility of fundamental <b>Data Structures and Algorithms (DSA)</b>. In traditional computer science curricula, data structures such as Graphs, Binary Search Trees, Max-Heaps, and Linked Lists are often taught in isolation using abstract mathematical exercises. Social Detective solves this educational disconnect by embedding <b>12 fully functional, custom-built Python data structures</b> directly into the core mechanics of a detective murder/theft investigation.",
        body_style
    ))
    story.append(Paragraph(
        "The player assumes the role of a digital forensics detective investigating the theft of a high-security genomic research file (<code>PROJECT_CHIMERA_GENOME.enc</code>) from Apex Bio-Informatics Lab. Rather than using pre-packaged high-level standard libraries, <b>every single investigative tool in the system is directly driven by custom pointer-manipulation and graph-traversal code written from scratch</b> in Python.",
        body_style
    ))

    # =========================================================================
    # 3. COMPLETE MASTER COMPLEXITY & DATA STRUCTURE MAPPING TABLE
    # =========================================================================
    story.append(Spacer(1, 6))
    story.append(Paragraph("2. Master Data Structures & Algorithms Complexity Mapping", h1_style))
    story.append(Paragraph(
        "The following table provides an exhaustive summary of all 12 custom DSA components implemented in the project, including their time complexities, space complexities, underlying memory models, and exact role in the detective game:",
        body_style
    ))

    dsa_rows = [
        [
            Paragraph("Data Structure / Algorithm", table_header_style),
            Paragraph("Primary Operation", table_header_style),
            Paragraph("Avg Time", table_header_style),
            Paragraph("Worst Time", table_header_style),
            Paragraph("Space", table_header_style),
            Paragraph("Detective Mystery Use-Case", table_header_style),
        ],
        [
            Paragraph("<b>Hash Table</b> (Chaining)", table_cell_bold),
            Paragraph("<code>search(key)</code>", table_cell_style),
            Paragraph("O(1)", table_cell_bold),
            Paragraph("O(n)", table_cell_style),
            Paragraph("O(C + n)", table_cell_style),
            Paragraph("Instant lookup for suspect usernames, Evidence IDs, and Keycards.", table_cell_style),
        ],
        [
            Paragraph("<b>Graph</b> (Adjacency List)", table_cell_bold),
            Paragraph("<code>get_neighbors()</code>", table_cell_style),
            Paragraph("O(1)", table_cell_bold),
            Paragraph("O(1)", table_cell_style),
            Paragraph("O(V + E)", table_cell_style),
            Paragraph("Social network modeling for 13 suspects and 24 relationship edges.", table_cell_style),
        ],
        [
            Paragraph("<b>Breadth-First Search</b>", table_cell_bold),
            Paragraph("<code>bfs(start, target)</code>", table_cell_style),
            Paragraph("O(V + E)", table_cell_bold),
            Paragraph("O(V + E)", table_cell_style),
            Paragraph("O(V)", table_cell_style),
            Paragraph("Guarantees shortest connection path between victim and culprit.", table_cell_style),
        ],
        [
            Paragraph("<b>Depth-First Search</b>", table_cell_bold),
            Paragraph("<code>dfs(start)</code>", table_cell_style),
            Paragraph("O(V + E)", table_cell_bold),
            Paragraph("O(V + E)", table_cell_style),
            Paragraph("O(V)", table_cell_style),
            Paragraph("Deep conspiracy exploration with call stack backtrack trail.", table_cell_style),
        ],
        [
            Paragraph("<b>Doubly Linked List</b>", table_cell_bold),
            Paragraph("<code>prev / next</code>", table_cell_style),
            Paragraph("O(1) step", table_cell_bold),
            Paragraph("O(n) scan", table_cell_style),
            Paragraph("O(n)", table_cell_style),
            Paragraph("Incident timeline forward/backward navigation for alibi verification.", table_cell_style),
        ],
        [
            Paragraph("<b>Binary Search Tree</b>", table_cell_bold),
            Paragraph("<code>search(key)</code>", table_cell_style),
            Paragraph("O(log n)", table_cell_bold),
            Paragraph("O(n)", table_cell_style),
            Paragraph("O(n)", table_cell_style),
            Paragraph("Numeric Evidence ID indexing; Inorder yields sorted clues.", table_cell_style),
        ],
        [
            Paragraph("<b>Max-Heap</b> (Priority Queue)", table_cell_bold),
            Paragraph("<code>extract_max()</code>", table_cell_style),
            Paragraph("O(log n)", table_cell_bold),
            Paragraph("O(log n)", table_cell_style),
            Paragraph("O(n)", table_cell_style),
            Paragraph("Surfaces highest-credibility forensic evidence items first (O(1) peek).", table_cell_style),
        ],
        [
            Paragraph("<b>LIFO Stack</b>", table_cell_bold),
            Paragraph("<code>push() / pop()</code>", table_cell_style),
            Paragraph("O(1)", table_cell_bold),
            Paragraph("O(1)", table_cell_style),
            Paragraph("O(n)", table_cell_style),
            Paragraph("Investigation breadcrumb history & instant Backtrack undo.", table_cell_style),
        ],
        [
            Paragraph("<b>Circular Queue</b>", table_cell_bold),
            Paragraph("<code>cycle() (i+1)%cap</code>", table_cell_style),
            Paragraph("O(1)", table_cell_bold),
            Paragraph("O(1)", table_cell_style),
            Paragraph("O(cap)", table_cell_style),
            Paragraph("Fixed-capacity CCTV rotating surveillance camera buffer.", table_cell_style),
        ],
        [
            Paragraph("<b>Singly Linked List</b>", table_cell_bold),
            Paragraph("<code>traverse()</code>", table_cell_style),
            Paragraph("O(n)", table_cell_bold),
            Paragraph("O(n)", table_cell_style),
            Paragraph("O(n)", table_cell_style),
            Paragraph("Sequential clue pipeline linking clue 1 to clue 2, 3, etc.", table_cell_style),
        ],
        [
            Paragraph("<b>Merge Sort</b>", table_cell_bold),
            Paragraph("<code>merge_sort()</code>", table_cell_style),
            Paragraph("O(n log n)", table_cell_bold),
            Paragraph("O(n log n)", table_cell_style),
            Paragraph("O(n)", table_cell_style),
            Paragraph("Guaranteed stable sorting of suspects by threat/risk score.", table_cell_style),
        ],
        [
            Paragraph("<b>Quick Sort</b>", table_cell_bold),
            Paragraph("<code>partition()</code>", table_cell_style),
            Paragraph("O(n log n)", table_cell_bold),
            Paragraph("O(n²)", table_cell_style),
            Paragraph("O(log n)", table_cell_style),
            Paragraph("Pivot-based partition sorting of evidence credibility.", table_cell_style),
        ],
        [
            Paragraph("<b>Binary Search</b>", table_cell_bold),
            Paragraph("<code>binary_search()</code>", table_cell_style),
            Paragraph("O(log n)", table_cell_bold),
            Paragraph("O(log n)", table_cell_style),
            Paragraph("O(1)", table_cell_style),
            Paragraph("Logarithmic lookup on sorted evidence IDs with Low/Mid/High pointers.", table_cell_style),
        ],
    ]

    dsa_table = Table(dsa_rows, colWidths=[100, 75, 55, 55, 45, 174])
    dsa_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light]),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(dsa_table)

    # =========================================================================
    # 4. CASE NARRATIVE & SOLUTION MATRIX
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("3. Case Dossier & Forensics Investigation Matrix", h1_style))
    story.append(Paragraph(
        "<b>Case 001: The Vanishing File</b> features an interconnected narrative designed to test hypothesis formulation, alibi cross-examination, and timestamp contradiction analysis:",
        body_style
    ))

    case_details = [
        [Paragraph("<b>Incident:</b>", table_cell_bold), Paragraph("CRISPR-AI genomic algorithm <code>PROJECT_CHIMERA_GENOME.enc</code> purged from server.", table_cell_style)],
        [Paragraph("<b>Incident Window:</b>", table_cell_bold), Paragraph("19:00 PM — 21:00 PM on October 6, 2026 at Apex Bio-Informatics Lab.", table_cell_style)],
        [Paragraph("<b>Victim:</b>", table_cell_bold), Paragraph("<b>Dr. Maya Rao</b> (Principal Investigator). Stepped out to cafeteria 19:30 - 20:45 (Verified).", table_cell_style)],
        [Paragraph("<b>Prime Culprit:</b>", table_cell_bold), Paragraph("<b>Ryan Mehta</b> (Junior Researcher). Fabricated library alibi; stolen keycard KC-9021 used at 19:38.", table_cell_style)],
        [Paragraph("<b>Accomplice:</b>", table_cell_bold), Paragraph("<b>Sam Verma</b> (Systems Admin). Configured SSH jump-box & wiped switch mirrors for 20% cut.", table_cell_style)],
        [Paragraph("<b>Financial Motive:</b>", table_cell_bold), Paragraph("$150,000 cryptocurrency bounty offered by rival corporate firm NexaGen.", table_cell_style)],
        [Paragraph("<b>Smoking Gun Clues:</b>", table_cell_bold), Paragraph("CCTV #1047 (19:47 exit) + Terminal Log #1061 (19:42 exfiltration) + Badge Scan #1075 (19:38 Door 3).", table_cell_style)],
    ]
    t_case = Table(case_details, colWidths=[110, 394])
    t_case.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_bg_light),
        ('BOX', (0, 0), (-1, -1), 0.5, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_case)
    story.append(Spacer(1, 10))

    # =========================================================================
    # 5. STEP-BY-STEP PLAYTHROUGH ARCHITECTURE (STAGES 0 - 6)
    # =========================================================================
    story.append(Paragraph("4. Guided Investigation Playthrough Architecture", h1_style))
    story.append(Paragraph(
        "The application organizes the investigation into a progressive 7-stage state machine that enforces logical deduction while tracking detective score and discoveries:",
        body_style
    ))

    stages_data = [
        [
            Paragraph("Stage", table_header_style),
            Paragraph("Stage Name", table_header_style),
            Paragraph("Active DSA Engine", table_header_style),
            Paragraph("Investigative Objective & Milestone", table_header_style)
        ],
        [
            Paragraph("<b>Stage 0</b>", table_cell_bold),
            Paragraph("Briefing", table_cell_style),
            Paragraph("Case Metadata", table_cell_style),
            Paragraph("Review crime scene parameters, victim statement, and initial incident scope.", table_cell_style)
        ],
        [
            Paragraph("<b>Stage 1</b>", table_cell_bold),
            Paragraph("Suspects", table_cell_style),
            Paragraph("Hash Table O(1)", table_cell_style),
            Paragraph("Inspect 13 personnel files. Uncover Ryan Mehta's fabricated library alibi.", table_cell_style)
        ],
        [
            Paragraph("<b>Stage 2</b>", table_cell_bold),
            Paragraph("Connections", table_cell_style),
            Paragraph("Graph BFS O(V + E)", table_cell_style),
            Paragraph("Trace shortest path: Dr. Maya Rao ➔ Ryan Mehta ➔ Sam Verma (3 degrees).", table_cell_style)
        ],
        [
            Paragraph("<b>Stage 3</b>", table_cell_bold),
            Paragraph("Timeline", table_cell_style),
            Paragraph("Doubly Linked List", table_cell_style),
            Paragraph("Step forward/backward: Uncover Door 3 scan at 19:38 & Terminal 04 at 19:42.", table_cell_style)
        ],
        [
            Paragraph("<b>Stage 4</b>", table_cell_bold),
            Paragraph("Evidence", table_cell_style),
            Paragraph("BST & Max-Heap", table_cell_style),
            Paragraph("Traverse Singly Linked List clue chain, search BST for #1047, extract Max-Heap root.", table_cell_style)
        ],
        [
            Paragraph("<b>Stage 5</b>", table_cell_bold),
            Paragraph("Theory", table_cell_style),
            Paragraph("LIFO Stack Undo", table_cell_style),
            Paragraph("Classify suspects: Mark Ryan Mehta as CRITICAL, clear Maya, maintain undo history.", table_cell_style)
        ],
        [
            Paragraph("<b>Stage 6</b>", table_cell_bold),
            Paragraph("Accusation", table_cell_style),
            Paragraph("Verification Engine", table_cell_style),
            Paragraph("Submit indictment against Ryan Mehta. Cross-check alibis & generate final score debrief.", table_cell_style)
        ],
    ]
    t_stages = Table(stages_data, colWidths=[48, 80, 110, 266])
    t_stages.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light]),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_stages)

    # =========================================================================
    # 6. SYSTEM ARCHITECTURE & CODE MODULES
    # =========================================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("5. Technical Implementation & Directory Architecture", h1_style))
    story.append(Paragraph(
        "The codebase is structured following strict separation of concerns into <b>Structures</b>, <b>Services</b>, <b>REST APIs</b>, and <b>Presentation Views</b>:",
        body_style
    ))

    arch_rows = [
        [Paragraph("<b>Directory / File</b>", table_header_style), Paragraph("Architectural Responsibility", table_header_style), Paragraph("Key Data Structures Contained", table_header_style)],
        [Paragraph("<code>structures/graph.py</code>", table_cell_style), Paragraph("Social network graph representation and pathfinding.", table_cell_style), Paragraph("Adjacency List, BFS (Queue), DFS (Stack)", table_cell_style)],
        [Paragraph("<code>structures/bst.py</code>", table_cell_style), Paragraph("Binary Search Tree for indexing forensic records by ID.", table_cell_style), Paragraph("BST Insert, Search, Inorder/Preorder/Postorder", table_cell_style)],
        [Paragraph("<code>structures/heap.py</code>", table_cell_style), Paragraph("Max-Heap Priority Queue for clue credibility rankings.", table_cell_style), Paragraph("Array-based Complete Tree, Bubble-Up/Down", table_cell_style)],
        [Paragraph("<code>structures/hash_table.py</code>", table_cell_style), Paragraph("Hash Table with polynomial hashing and collision chaining.", table_cell_style), Paragraph("Separate Chaining, Linked List Buckets", table_cell_style)],
        [Paragraph("<code>structures/doubly_linked_list.py</code>", table_cell_style), Paragraph("Bi-directional linked list for incident timeline stepping.", table_cell_style), Paragraph("DoublyNode (prev, next), Forward/Backward", table_cell_style)],
        [Paragraph("<code>structures/stack.py</code> & <code>queue.py</code>", table_cell_style), Paragraph("LIFO breadcrumb history and FIFO evidence pipeline.", table_cell_style), Paragraph("Node-based Stack & Node-based FIFO Queue", table_cell_style)],
        [Paragraph("<code>structures/circular_queue.py</code>", table_cell_style), Paragraph("Modulo wrap-around buffer for CCTV camera monitors.", table_cell_style), Paragraph("Fixed Array <code>(index + 1) % capacity</code>", table_cell_style)],
        [Paragraph("<code>structures/sorting.py</code> & <code>searching.py</code>", table_cell_style), Paragraph("Pure algorithmic sort & search implementations.", table_cell_style), Paragraph("Merge Sort, Quick Sort, Binary & Linear Search", table_cell_style)],
        [Paragraph("<code>services/case_engine.py</code>", table_cell_style), Paragraph("Master facade coordinating investigations, theory, and scoring.", table_cell_style), Paragraph("Case state machine, accusation verification", table_cell_style)],
        [Paragraph("<code>app.py</code>", table_cell_style), Paragraph("Flask web server exposing 26 REST API endpoints and views.", table_cell_style), Paragraph("HTTP Routing, JSON serialization, Session state", table_cell_style)],
    ]
    t_arch = Table(arch_rows, colWidths=[140, 194, 170])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_dark),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light]),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_arch)

    # =========================================================================
    # 7. COLLEGE VIVA VOCE QUESTIONS & ANSWERS (TOP 10 EXAMINER QUESTIONS)
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("6. Academic Viva Voce / Presentation Q&A Guide", h1_style))
    story.append(Paragraph(
        "This section prepares students for oral defense, project viva, and technical review by detailing the top 10 questions frequently asked by academic examiners:",
        body_style
    ))

    viva_qa = [
        (
            "Q1: Why did you choose an Adjacency List over an Adjacency Matrix for the Social Graph?",
            "Social networks are sparse graphs where the number of edges |E| is significantly less than |V|² (e.g. 13 suspects with 24 relationships vs 169 potential matrix cells). An Adjacency List uses optimal O(V + E) space compared to O(V²) for an Adjacency Matrix and enables iterating over a suspect's direct neighbors in O(degree(v)) time rather than O(V)."
        ),
        (
            "Q2: How does Breadth-First Search (BFS) guarantee the shortest connection path between victim and suspect?",
            "BFS explores nodes level-by-level in order of their hop distance from the root vertex using a FIFO Queue. In an unweighted graph, the very first time a target vertex is dequeued, the path traversed is mathematically guaranteed to contain the minimum number of edge hops."
        ),
        (
            "Q3: Why is a Doubly Linked List necessary for the case timeline instead of a simple Array?",
            "Timeline reconstruction requires continuous bi-directional transitions: stepping forward to analyze future consequences (node.next) and backtracking backward to verify alibis (node.prev). A Doubly Linked List provides O(1) step transitions with localized pointer updates without memory re-allocations or index shifting."
        ),
        (
            "Q4: What is the significance of BST Inorder Traversal in your Evidence Vault?",
            "In a Binary Search Tree where Left < Root < Right, an Inorder traversal (Left Subtree -> Root -> Right Subtree) visits keys in strictly ascending numerical order in O(n) time. In Social Detective, running BST Inorder traversal transforms arbitrary evidence intake records into a perfectly sorted forensic register."
        ),
        (
            "Q5: How does the Max-Heap prioritize forensic evidence in O(1) time?",
            "A Max-Heap satisfies the heap-order property where every parent node has a priority score greater than or equal to its children. Consequently, the highest-credibility clue is always situated at index 0 (the root). Peeking takes O(1) time, and extracting the max clue takes O(log n) time via bubble-down (heapify)."
        ),
        (
            "Q6: How does your Hash Table handle hash collisions?",
            "The Hash Table uses Separate Chaining. When two distinct keys hash to the same bucket index via the polynomial hash function, they are inserted into a Singly Linked List housed at that bucket. On average, if the load factor λ = n / capacity is kept small, search and insertion execute in O(1) time."
        ),
        (
            "Q7: Why use a Circular Queue with modulo arithmetic for surveillance CCTV feeds?",
            "Surveillance monitors rotate continuously through a fixed buffer of cameras (CAM 1 to 5). Using a Circular Queue with modulo arithmetic (rear + 1) % capacity eliminates memory fragmentation and avoids shifting array elements upon dequeue, maintaining strict O(1) rotation."
        ),
        (
            "Q8: Why is Merge Sort preferred for sorting suspect risk scores?",
            "Merge Sort is a Divide-and-Conquer algorithm with guaranteed O(n log n) time complexity across best, average, and worst cases. Unlike basic Quick Sort, Merge Sort is stable, meaning suspects with identical risk scores retain their original relative order."
        ),
        (
            "Q9: What role does the LIFO Stack play in the investigation engine?",
            "The Stack models the detective's exploratory breadcrumb trail. Pushing records when a new suspect or clue is inspected allows instant O(1) backtracking (undoing the last action via Stack Pop) to return to the previous decision point."
        ),
        (
            "Q10: How do you verify the correctness of all your custom data structures?",
            "The system includes an automated PyTest test suite (tests/test_all_structures.py) comprising 12 unit tests verifying edge cases, empty states, boundary conditions, heap property restoration, tree traversals, and graph connectivity."
        )
    ]

    for q, a in viva_qa:
        story.append(Paragraph(f"<b>{q}</b>", h2_style))
        story.append(Paragraph(a, body_style))
        story.append(Spacer(1, 2))

    # =========================================================================
    # 8. TESTING, VERIFICATION & CONCLUSION
    # =========================================================================
    story.append(Spacer(1, 6))
    story.append(Paragraph("7. Test Verification & Conclusion", h1_style))
    story.append(Paragraph(
        "<b>Automated Test Suite:</b> The project underwent rigorous test-driven validation using <code>pytest</code>. All 12 custom structures passed 100% of unit tests verifying edge cases, boundary pointers, and Big-O invariants.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Conclusion:</b> Social Detective demonstrates that complex computer science concepts can be taught engagingly through gamified simulation. By uniting authentic algorithmic rigor with interactive cyber forensics, the application provides an exemplary model for college coursework, viva presentations, and portfolio demonstration.",
        body_style
    ))

    # =========================================================================
    # 9. PHOTOGRAPHIC CASE WALKTHROUGH & FORENSIC UI SCREENSHOTS
    # =========================================================================
    screenshot_dir = os.path.join(os.path.dirname(__file__), "screenshots")
    if os.path.exists(screenshot_dir):
        story.append(PageBreak())
        story.append(Paragraph("8. Photographic Case Walkthrough & Forensic UI Screenshots", h1_style))
        story.append(Paragraph(
            "The following high-resolution figures capture the complete end-to-end playthrough of Case #001 (The Vanishing File), demonstrating the practical synergy between the detective narrative and the underlying custom Data Structures & Algorithms (DSA):",
            body_style
        ))
        story.append(Spacer(1, 6))

        figures = [
            (
                "01_stage0_case_briefing.png",
                "Figure 1: Stage 0 — Incident Briefing & Dossier",
                "Case parameter review showing theft time (19:42 PM), victim Dr. Maya Rao's statement, and initial scope."
            ),
            (
                "02_stage1_suspects_roster.png",
                "Figure 2: Stage 1 — Suspect Roster & Hash Table Lookup",
                "Suspect profile inspection via O(1) Separate-Chaining Hash Table uncovering Ryan Mehta's fake library alibi."
            ),
            (
                "03b_stage2_network_explorer.png",
                "Figure 3: Stage 2 — Social Network Graph Explorer & BFS Traversal",
                "Live Breadth-First Search (BFS) graph traversal showing the shortest conspiracy path: Maya Rao ➔ Sam Verma ➔ Ryan Mehta."
            ),
            (
                "04_stage3_timeline_stepper.png",
                "Figure 4: Stage 3 — Chronological Timeline (Doubly Linked List)",
                "Bi-directional stepping (node.next / node.prev) exposing Door #3 keycard scan at 19:38 and Terminal 04 theft at 19:42."
            ),
            (
                "05_stage4_evidence_vault.png",
                "Figure 5: Stage 4 — Forensic Evidence Vault (BST & Max-Heap)",
                "Binary Search Tree ID indexing for Clue #1047 and Max-Heap priority extraction of Terminal 04 SSH logs (#1061)."
            ),
            (
                "06_stage5_theory_board.png",
                "Figure 6: Stage 5 — Theory Board & LIFO Stack Undo",
                "Hypothesis formulation marking Ryan Mehta as CRITICAL and Maya as CLEARED with instant LIFO Stack undo."
            ),
            (
                "07_stage6_case_solved.png",
                "Figure 7: Stage 6 — Formal Accusation & Victory Debrief",
                "Successful indictment of Ryan Mehta revealing the $150k cryptocurrency bounty and 100% Case Solved rating."
            ),
            (
                "09_algorithm_lab_viva.png",
                "Figure 8: Algorithm Lab — Academic Viva Presentation Hub",
                "Interactive live testing hub for all 12 custom Python data structures with time/space complexity meters."
            )
        ]

        for i, (fname, title, desc) in enumerate(figures):
            fpath = os.path.join(screenshot_dir, fname)
            if os.path.exists(fpath):
                img = Image(fpath, width=440, height=255)
                fig_block = [
                    Spacer(1, 4),
                    img,
                    Paragraph(f"<b>{title}</b>", caption_style),
                    Paragraph(desc, figure_desc_style),
                    Spacer(1, 6)
                ]
                story.append(KeepTogether(fig_block))
                # Add page break every 2 figures
                if (i % 2 == 1) and (i < len(figures) - 1):
                    story.append(PageBreak())

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[SUCCESS] Academic Project Report generated: {filename}")
    return filename


if __name__ == "__main__":
    build_pdf()
