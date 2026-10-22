"""
Generate Comprehensive Playthrough Guide, Solution Walkthrough & DSA Manual for SOCIAL DETECTIVE.
Builds a publication-quality multi-page PDF using ReportLab.
"""
import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class SolutionGuideNumberedCanvas(canvas.Canvas):
    """Two-pass canvas for dynamic running header and page numbering."""
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
        self.setFillColor(colors.HexColor("#78716c"))

        # Don't draw running header on cover/page 1
        if self._pageNumber > 1:
            self.drawString(54, 750, "SOCIAL DETECTIVE — Playthrough Guide & DSA Architecture Manual")
            self.drawRightString(612 - 54, 750, "Case #001: The Vanishing File")
            self.setStrokeColor(colors.HexColor("#ded4c0"))
            self.setLineWidth(0.6)
            self.line(54, 742, 612 - 54, 742)

        # Running Footer
        self.setStrokeColor(colors.HexColor("#ded4c0"))
        self.setLineWidth(0.6)
        self.line(54, 45, 612 - 54, 45)

        self.setFont("Helvetica", 8)
        self.drawString(54, 32, "Computer Science & Engineering · DSA Lab & Viva Walkthrough")
        self.drawRightString(612 - 54, 32, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()


def build_solution_guide_pdf(filename="Social_Detective_Playthrough_and_DSA_Guide.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=50,
        rightMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    # Editorial Forensic Palette
    c_primary = colors.HexColor("#1c1917")    # Deep carbon ink
    c_secondary = colors.HexColor("#57534e")  # Muted charcoal
    c_navy = colors.HexColor("#1e40af")       # Academic navy
    c_cerulean = colors.HexColor("#0284c7")   # Forensic cyan/blue
    c_emerald = colors.HexColor("#15803d")    # Verified green
    c_amber = colors.HexColor("#b45309")      # Warning amber
    c_crimson = colors.HexColor("#b91c1c")    # Culprit red
    c_purple = colors.HexColor("#6d28d9")     # Docket purple
    c_bg_card = colors.HexColor("#faf6ee")    # Crisp ivory card
    c_border = colors.HexColor("#ded4c0")     # Linen border
    c_bg_dark = colors.HexColor("#292524")    # Dark carbon header

    # Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=c_primary,
        alignment=0,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=c_cerulean,
        textTransform='uppercase',
        spaceAfter=10
    )

    h1_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=c_navy,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SubSectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=c_primary,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=c_secondary,
        spaceAfter=5
    )

    body_bold = ParagraphStyle(
        'BodyDarkBold',
        parent=body_style,
        fontName='Helvetica-Bold',
        textColor=c_primary
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11.5,
        textColor=c_primary
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white,
        alignment=1
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=c_primary
    )

    table_cell_code = ParagraphStyle(
        'TableCellCode',
        parent=styles['Normal'],
        fontName='Courier-Bold',
        fontSize=7.2,
        leading=9.5,
        textColor=c_navy
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10,
        textColor=c_primary
    )

    story = []

    # =========================================================================
    # DOCUMENT COVER HEADER
    # =========================================================================
    header_table_data = [
        [
            Paragraph("SOCIAL DETECTIVE: THE COMPLETE PLAYTHROUGH & DSA MANUAL", title_style),
            Paragraph("CASE FILE: #001<br/><b>STATUS: CONVICTED</b><br/>SCORE: 1000/1000 PTS", ParagraphStyle(
                'CaseBadge', parent=styles['Normal'], fontName='Courier-Bold', fontSize=8, leading=11, textColor=c_crimson, alignment=2
            ))
        ],
        [
            Paragraph("Comprehensive Reference: Every Data Structure Used & Step-by-Step Solution Walkthrough", subtitle_style),
            Paragraph("CRIME: CORPORATE ESPIONAGE<br/>FACILITY: APEX BIO-INFORMATICS LAB", ParagraphStyle(
                'CaseSub', parent=styles['Normal'], fontName='Helvetica', fontSize=7.5, leading=10, textColor=c_secondary, alignment=2
            ))
        ]
    ]

    header_table = Table(header_table_data, colWidths=[370, 142])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_navy, spaceBefore=2, spaceAfter=8))

    # =========================================================================
    # SECTION 1: CASE BRIEFING & FORENSIC PROBLEM STATEMENT
    # =========================================================================
    story.append(Paragraph("1. Incident Briefing & Forensic Problem Statement", h1_style))
    story.append(Paragraph(
        "<b>The Crime:</b> On the evening of October 6, 2026, at precisely <b>19:42 PM</b>, the breakthrough CRISPR-Cas9 sequencing file "
        "<code>PROJECT_CHIMERA_GENOME.enc</code> was exfiltrated via high-speed USB from Workstation #04 inside Apex Bio-Informatics Lab. "
        "The primary database backups were deliberately wiped. Principal Investigator <b>Dr. Maya Rao</b> discovered the theft upon returning "
        "from the cafeteria at 20:45 PM. Initial access logs show that Dr. Rao's physical keycard (<code>KC-9021</code>) unlocked Door #3 at 19:38 PM. "
        "However, physical witnesses and cafeteria camera registers place Dr. Rao on the 1st floor from 19:30 to 20:45 PM. "
        "Thirteen suspects had access to campus credentials. The detective must reconstruct the case using <b>12 custom Python data structures</b>.",
        body_style
    ))

    # Key Facts Callout Box
    facts_data = [[
        Paragraph(
            "<b>CORE MYSTERY CONTRADICTION:</b><br/>"
            "• Physical Keycard <b>KC-9021</b> accessed high-security Door #3 at <b>19:38 PM</b>.<br/>"
            "• Owner <b>Dr. Maya Rao</b> was eating dinner in the cafeteria from <b>19:30 to 20:45 PM</b> (Verified by 3 witnesses).<br/>"
            "• Therefore, <b>someone stole Dr. Rao's badge</b> between 19:30 and 19:38 PM and executed the theft while fabricating their own alibi.",
            callout_style
        )
    ]]
    facts_table = Table(facts_data, colWidths=[512])
    facts_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#fef2f2")),
        ('BOX', (0,0), (-1,-1), 1, c_crimson),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(facts_table)
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 2: DATA STRUCTURES & ALGORITHMS (WHAT IS USED WHERE)
    # =========================================================================
    story.append(Paragraph("2. Master DSA Architecture — What Data Structure is Used Where", h1_style))
    story.append(Paragraph(
        "Social Detective does not rely on third-party libraries for its algorithmic logic. All 12 data structures are implemented from scratch in pure Python.",
        body_style
    ))

    # Master Table of Data Structures
    dsa_table_data = [
        [
            Paragraph("Data Structure", table_header),
            Paragraph("Module Path", table_header),
            Paragraph("Practical Role in Investigation", table_header),
            Paragraph("Time Complexity", table_header),
            Paragraph("Space", table_header)
        ],
        [
            Paragraph("<b>Hash Table</b><br/>Separate Chaining", table_cell),
            Paragraph("<code>structures/<br/>hash_table.py</code>", table_cell_code),
            Paragraph("Fast keycard ID, username (e.g. <code>@ryan_47</code>), and clue SHA-256 hash lookup.", table_cell),
            Paragraph("Search: <b>O(1)</b> avg<br/>Insert: <b>O(1)</b> avg", table_cell),
            Paragraph("O(n + k)", table_cell)
        ],
        [
            Paragraph("<b>Graph</b><br/>Adjacency List", table_cell),
            Paragraph("<code>structures/<br/>graph.py</code>", table_cell_code),
            Paragraph("Represents 13 suspects (vertices) and 18 communication/credential links (edges).", table_cell),
            Paragraph("Add Vertex: <b>O(1)</b><br/>Add Edge: <b>O(1)</b>", table_cell),
            Paragraph("O(V + E)", table_cell)
        ],
        [
            Paragraph("<b>Breadth-First Search (BFS)</b>", table_cell),
            Paragraph("<code>services/<br/>social_network.py</code>", table_cell_code),
            Paragraph("Finds shortest path (degrees of separation) between Maya and Ryan using FIFO Queue.", table_cell),
            Paragraph("Traversal: <b>O(V + E)</b><br/>Guarantees shortest hops", table_cell),
            Paragraph("O(V)", table_cell)
        ],
        [
            Paragraph("<b>Depth-First Search (DFS)</b>", table_cell),
            Paragraph("<code>services/<br/>social_network.py</code>", table_cell_code),
            Paragraph("Deep recursive exploration to discover conspirator sub-networks and clusters.", table_cell),
            Paragraph("Traversal: <b>O(V + E)</b><br/>Via Call Stack", table_cell),
            Paragraph("O(V)", table_cell)
        ],
        [
            Paragraph("<b>Doubly Linked List</b>", table_cell),
            Paragraph("<code>structures/<br/>doubly_linked_list.py</code>", table_cell_code),
            Paragraph("Incident timeline stepper. Supports forward (<code>node.next</code>) and backward (<code>node.prev</code>) traversal.", table_cell),
            Paragraph("Next/Prev Step: <b>O(1)</b><br/>Full Search: O(n)", table_cell),
            Paragraph("O(n)", table_cell)
        ],
        [
            Paragraph("<b>Singly Linked List</b>", table_cell),
            Paragraph("<code>structures/<br/>linked_list.py</code>", table_cell_code),
            Paragraph("Chain of custody pipeline linking 7 sequential evidence items from theft to exit.", table_cell),
            Paragraph("Append: <b>O(1)</b><br/>Traverse: O(n)", table_cell),
            Paragraph("O(n)", table_cell)
        ],
        [
            Paragraph("<b>Binary Search Tree (BST)</b>", table_cell),
            Paragraph("<code>structures/<br/>bst.py</code>", table_cell_code),
            Paragraph("Hierarchical index of 15 evidence records by numerical ID (e.g. #1047 CCTV, #1061 USB).", table_cell),
            Paragraph("Search: <b>O(log n)</b><br/>Worst (skewed): O(n)", table_cell),
            Paragraph("O(n)", table_cell)
        ],
        [
            Paragraph("<b>BST Inorder Traversal</b>", table_cell),
            Paragraph("<code>structures/<br/>bst.py</code>", table_cell_code),
            Paragraph("Recursively traverses Left-Root-Right to output all evidence records in sorted ascending order.", table_cell),
            Paragraph("Traversal: <b>O(n)</b><br/>Produces sorted list", table_cell),
            Paragraph("O(h)", table_cell)
        ],
        [
            Paragraph("<b>Max-Heap</b><br/>Priority Queue", table_cell),
            Paragraph("<code>structures/<br/>heap.py</code>", table_cell_code),
            Paragraph("Always keeps highest-credibility clue at root (index 0). Bubbles down upon extraction.", table_cell),
            Paragraph("Peek Root: <b>O(1)</b><br/>Extract Max: <b>O(log n)</b>", table_cell),
            Paragraph("O(n)", table_cell)
        ],
        [
            Paragraph("<b>LIFO Stack</b>", table_cell),
            Paragraph("<code>structures/<br/>stack.py</code>", table_cell_code),
            Paragraph("Investigation history ledger. Backtracking ('Undo') pops latest hypothesis in O(1) time.", table_cell),
            Paragraph("Push: <b>O(1)</b><br/>Pop: <b>O(1)</b>", table_cell),
            Paragraph("O(n)", table_cell)
        ],
        [
            Paragraph("<b>Circular Queue</b><br/>Ring Buffer", table_cell),
            Paragraph("<code>structures/<br/>circular_queue.py</code>", table_cell_code),
            Paragraph("Fixed-size (capacity 5) CCTV surveillance monitor buffer. Overwrites oldest frame when full.", table_cell),
            Paragraph("Enqueue: <b>O(1)</b><br/>Dequeue: <b>O(1)</b>", table_cell),
            Paragraph("O(K)", table_cell)
        ],
        [
            Paragraph("<b>Merge Sort & Quick Sort</b>", table_cell),
            Paragraph("<code>structures/<br/>sorting.py</code>", table_cell_code),
            Paragraph("Sorting suspect risk scores (Merge Sort: stable O(n log n); Quick Sort: in-place pivot partitioning).", table_cell),
            Paragraph("Avg: <b>O(n log n)</b><br/>Live swap trace", table_cell),
            Paragraph("O(n) / O(log n)", table_cell)
        ],
        [
            Paragraph("<b>Binary Search (Array)</b>", table_cell),
            Paragraph("<code>structures/<br/>searching.py</code>", table_cell_code),
            Paragraph("Divide-and-conquer on sorted evidence ID array using low/mid/high boundary pointers.", table_cell),
            Paragraph("Search: <b>O(log n)</b><br/>Requires sorted list", table_cell),
            Paragraph("O(1)", table_cell)
        ]
    ]

    dsa_table = Table(dsa_table_data, colWidths=[90, 85, 175, 110, 52])
    dsa_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_card]),
    ]))
    story.append(dsa_table)
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 3: STEP-BY-STEP PLAYTHROUGH & SOLUTION WALKTHROUGH
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("3. Step-by-Step Playthrough Guide (100% Score Solution)", h1_style))
    story.append(Paragraph(
        "Follow this exact sequence to navigate all 6 investigation stages and secure a conviction against Ryan Mehta.",
        body_style
    ))

    # Stage 1
    story.append(Paragraph("STAGE 1: Suspect Roster & Alibi Verification ('Who Had Access?')", h2_style))
    story.append(Paragraph(
        "<b>1. Navigate to Playthrough:</b> Click <b>'Start Investigation'</b> or visit <code>/case</code>.<br/>"
        "<b>2. Inspect Dr. Maya Rao:</b> Click row #01 (Dr. Maya Rao). Note her statement: she went to the cafeteria at 19:30. "
        "Her keycard <code>KC-9021</code> went missing from her bag. Alibi is confirmed by 3 faculty witnesses. "
        "Click <b>'Tag Suspect' ➔ 'Clear'</b>.<br/>"
        "<b>3. Inspect Ryan Mehta:</b> Click row #02 (Ryan Mehta). Statement: claims he was studying alone in the university library. "
        "Has no keycard assigned (<code>KC-NONE</code>). Risk score: <b>88/100</b>. Notice: he has NO alibi witnesses. "
        "Click <b>'Tag Suspect' ➔ 'Critical'</b>.<br/>"
        "<b>4. Advance:</b> Click the dominant green banner button: <b>'INVESTIGATE RYAN MEHTA ➔'</b> to advance to Stage 2.",
        body_style
    ))

    # Stage 2
    story.append(Paragraph("STAGE 2: Social Network Tracing ('Something Doesn't Add Up')", h2_style))
    story.append(Paragraph(
        "<b>1. Objective:</b> Ryan claimed he barely knew Dr. Maya Rao. We will disprove this using BFS.<br/>"
        "<b>2. Execute BFS Trace (Maya ➔ Ryan):</b> Under the graph canvas, verify <b>Start: Dr. Maya Rao</b> and <b>Target: Ryan Mehta</b>. "
        "Click <b>'TRACE BFS SHORTEST PATH'</b>.<br/>"
        "<b>3. Algorithmic Output:</b> The FIFO Queue visits vertex <code>maya_rao</code>, inspects neighbors, and immediately identifies "
        "an edge to <code>ryan_mehta</code> in <b>1 hop</b> (Co-authorship on Project Chimera; shared server cluster access). "
        "Ryan's claim of having no connection is falsified.<br/>"
        "<b>4. Bonus Trace (Ryan ➔ Sam):</b> Click <b>'Trace Ryan ➔ Sam'</b>. BFS identifies a 3-hop connection through lab systems logs. "
        "Sam Verma is the Linux systems administrator with root privileges.<br/>"
        "<b>5. Advance:</b> Click the action banner button <b>'TRACE CONNECTION ➔'</b> to advance to Stage 3.",
        body_style
    ))

    # Stage 3
    story.append(Paragraph("STAGE 3: Chronological Timeline ('What Happened That Night?')", h2_style))
    story.append(Paragraph(
        "<b>1. Objective:</b> Traverse the Doubly Linked List forward (<code>node.next</code>) and backward (<code>node.prev</code>).<br/>"
        "<b>2. Step Through Events:</b> Click <b>'NEXT EVENT (node.next)'</b> repeatedly.<br/>"
        "<b>3. Key Contradiction Trigger (19:38 PM):</b> When you land on Event #04 (<b>19:38 PM: Door #3 Access</b>), a red alert box triggers: "
        "<i>'ALIBI CONTRADICTION: Keycard KC-9021 scanned into Door #3, but owner Maya Rao was at Cafeteria Station 4.'</i><br/>"
        "<b>4. Subsequent Events:</b> Advance through <b>19:42 PM</b> (Terminal 04 USB dump) and <b>19:47 PM</b> (CCTV Camera #1047 captures hooded figure in navy jacket exiting fire stairs).<br/>"
        "<b>5. Advance:</b> Click <b>'FOLLOW THE EVIDENCE ➔'</b> to move to Stage 4.",
        body_style
    ))

    # Stage 4
    story.append(Paragraph("STAGE 4: Forensic Evidence Vault ('Follow the Evidence')", h2_style))
    story.append(Paragraph(
        "<b>1. Examine Clue Chain (Singly Linked List):</b> Click <b>'EXAMINE NEXT CLUE IN CHAIN ➔'</b>. "
        "Observe the pointer advance through Nodes 1 through 7, ending at the NULL pointer.<br/>"
        "<b>2. Search BST Record #1047:</b> In the BST Search box, ensure <b>1047</b> is entered (or click badge <code>#1047 CCTV</code>). "
        "Click <b>'FIND RECORD ➔'</b>. The BST traverses: Root #1075 ➔ Left Child #1047 in <b>2 comparisons</b> (O(log n)), "
        "retrieving the footage of the hooded figure in the navy jacket.<br/>"
        "<b>3. Max-Heap Extraction:</b> Click <b>'EXTRACT STRONGEST EVIDENCE (O(log n))'</b>. "
        "The Max-Heap extracts Root #1190 (<b>99% Credibility</b>: Sandisk USB drive serial number registered to Ryan Mehta's student email). "
        "Bubble-down swaps restore the heap invariant.<br/>"
        "<b>4. Advance:</b> Click <b>'BUILD YOUR THEORY ➔'</b> to advance to Stage 5.",
        body_style
    ))

    # Stage 5
    story.append(Paragraph("STAGE 5: Prosecution Theory & Stack Backtracking ('Put the Pieces Together')", h2_style))
    story.append(Paragraph(
        "<b>1. Suspect Classification:</b> In the suspect tagging roster:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• Click <b>'Critical'</b> next to <b>Ryan Mehta</b> (marks him as prime culprit).<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• Click <b>'Clear'</b> next to <b>Dr. Maya Rao</b> (verifies her exonerated victim status).<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• Click <b>'Relevant'</b> next to <b>Sam Verma</b> (accomplice proxy).<br/>"
        "<b>2. Stack Backtracking Demo:</b> Click <b>'UNDO (POP)'</b> to pop the last hypothesis off the LIFO Stack in O(1) time. "
        "Re-tag Ryan Mehta as <b>'Critical'</b>.<br/>"
        "<b>3. Advance:</b> Click <b>'MAKE FINAL ACCUSATION ➔'</b> to proceed to Stage 6.",
        body_style
    ))

    # Stage 6
    story.append(Paragraph("STAGE 6: Final Accusation & Verdict ('Court of Forensics')", h2_style))
    story.append(Paragraph(
        "<b>1. Select Perpetrator:</b> In the accusation grid, click on <b>Ryan Mehta (Research Fellow · Risk: 88%)</b>. "
        "A confirmation card appears outlining the 3 pillars of proof (Stolen Keycard + Fabricated Alibi + USB Drive #1190).<br/>"
        "<b>2. Submit Accusation:</b> Click the red <b>'SUBMIT ACCUSATION'</b> button.<br/>"
        "<b>3. Verdict:</b> The system redirects to <code>/case-solved</code> with victory fanfare: "
        "<i>'100% Case Solved! Ryan Mehta convicted of research espionage ($150,000 crypto payout). Sam Verma cited as accomplice.'</i><br/>"
        "<b>4. Final Score:</b> <b>1000 / 1000 PTS</b> (All data structures explored, zero penalties).",
        body_style
    ))

    # =========================================================================
    # SECTION 4: VIVA VOCE & ACADEMIC EVALUATION CHEAT SHEET
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("4. Academic Viva Voce & Evaluation Cheat Sheet", h1_style))
    story.append(Paragraph(
        "Be prepared to answer these common oral examination questions during your practical project presentation:",
        body_style
    ))

    viva_qa = [
        (
            "Q1: Why use an Adjacency List instead of an Adjacency Matrix for the social network?",
            "<b>Answer:</b> The social network is <i>sparse</i> (13 vertices and 18 edges; E << V^2). "
            "An Adjacency Matrix requires O(V^2) space (169 cells) regardless of density. "
            "An Adjacency List requires only O(V + E) space and allows BFS/DFS to traverse neighbors in O(V + E) "
            "time instead of O(V^2)."
        ),
        (
            "Q2: How does the Hash Table handle collisions, and what is its Big-O performance?",
            "<b>Answer:</b> It uses <i>Separate Chaining</i> with Singly Linked Lists at each bucket. "
            "The hash function computes a polynomial rolling hash modulo table size (default 17). "
            "Average time complexity for Search, Insert, and Delete is <b>O(1)</b> assuming uniform hashing. "
            "Worst-case is O(n) if all keys hash to the same bucket."
        ),
        (
            "Q3: Why is a Doubly Linked List ideal for the incident timeline?",
            "<b>Answer:</b> Detectives must navigate chronologically forward (<code>node.next</code>) to reconstruct events "
            "and backward (<code>node.prev</code>) to verify alibis without reallocating arrays. "
            "Stepping between adjacent events is strictly <b>O(1)</b> pointer manipulation, compared to array slicing or re-indexing."
        ),
        (
            "Q4: What is the difference between BFS and DFS in this investigation?",
            "<b>Answer:</b> BFS uses a FIFO Queue to traverse level-by-level, guaranteeing the <i>shortest degree of separation</i> "
            "(minimum hops) between Maya and Ryan. DFS uses a LIFO Call Stack to traverse deeply into one branch, "
            "which is useful for uncovering cyclic conspiracy chains and sub-group cliques."
        ),
        (
            "Q5: How does the Max-Heap guarantee O(1) peek time for the highest credibility clue?",
            "<b>Answer:</b> A binary Max-Heap maintains the <i>Heap Invariant</i> where every parent node has a credibility "
            "greater than or equal to its children. Therefore, the maximum element is always at index 0 (root). "
            "Extracting the root takes <b>O(log n)</b> because the last leaf moves to root and bubbles down."
        ),
        (
            "Q6: Why use a Circular Queue for CCTV monitoring instead of a standard dynamic array?",
            "<b>Answer:</b> CCTV monitors need a bounded ring buffer (e.g. last 5 camera snapshots). "
            "A standard array requires O(n) shift operations when removing the oldest element. "
            "A Circular Queue uses modulo arithmetic (<code>rear = (rear + 1) % capacity</code>) to achieve "
            "strictly <b>O(1)</b> enqueue and dequeue with zero memory reallocation."
        ),
        (
            "Q7: What is the time complexity of searching Evidence #1047 in the BST versus Linear Search?",
            "<b>Answer:</b> Linear search scans every element in O(n) (15 comparisons). "
            "A balanced BST halves the search space at each step based on numerical comparison, "
            "finding Evidence #1047 in O(log_2 15) ≈ <b>3 to 4 comparisons</b>."
        ),
        (
            "Q8: What happens during Stack Backtracking (LIFO)?",
            "<b>Answer:</b> Every investigation action (tagging a suspect, dismissing an alibi) is pushed onto the Stack. "
            "When the detective clicks 'Undo', the top hypothesis is popped in <b>O(1)</b> time, "
            "reverting the case board to the exact previous state."
        )
    ]

    for q, a in viva_qa:
        q_box = [
            [Paragraph(f"<b>{q}</b>", ParagraphStyle('QTitle', parent=body_bold, textColor=c_navy))],
            [Paragraph(a, ParagraphStyle('AnsText', parent=body_style, leading=11))]
        ]
        q_table = Table(q_box, colWidths=[512])
        q_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), c_bg_card),
            ('BOX', (0,0), (-1,-1), 0.5, c_border),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(q_table)
        story.append(Spacer(1, 4))

    doc.build(story, canvasmaker=SolutionGuideNumberedCanvas)
    print(f"Successfully generated solution guide: {filename}")
    return filename


if __name__ == "__main__":
    out_file = sys.argv[1] if len(sys.argv) > 1 else "Social_Detective_Playthrough_and_DSA_Guide.pdf"
    build_solution_guide_pdf(out_file)
