import os
import sys
import copy
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable, Flowable, Preformatted
)
from reportlab.pdfgen import canvas

# Import modular dissertation generators
from dissertation_src.front_matter import generate_front_matter
from dissertation_src.chapter1_intro import generate_chapter_1
from dissertation_src.chapter2_lit import generate_chapter_2
from dissertation_src.chapter3_method import generate_chapter_3
from dissertation_src.chapter4_impl import generate_chapter_4
from dissertation_src.chapter5_results import generate_chapter_5
from dissertation_src.chapter6_disc import generate_chapter_6
from dissertation_src.chapter7_concl import generate_chapter_7
from dissertation_src.appendices import generate_appendices

def to_roman(n):
    """Convert integer to lowercase roman numerals for front matter."""
    if n <= 0:
        return ""
    roman_map = [
        (1000, 'm'), (900, 'cm'), (500, 'd'), (400, 'cd'),
        (100, 'c'), (90, 'xc'), (50, 'l'), (40, 'xl'),
        (10, 'x'), (9, 'ix'), (5, 'v'), (4, 'iv'), (1, 'i')
    ]
    result = ""
    for val, numeral in roman_map:
        while n >= val:
            result += numeral
            n -= val
    return result

class PageTarget(Flowable):
    """Zero-size flowable that records its render page during the build pass."""
    def __init__(self, key, directory):
        super().__init__()
        self.key = key
        self.directory = directory
        self.width = 0
        self.height = 0

    def draw(self):
        self.directory[self.key] = self.canv._pageNumber

class BlackBookCanvas(canvas.Canvas):
    """
    Two-pass canvas that formats pages according to NMIMS MPSTME Capstone guidelines:
    - Cover page & Inner title: No headers or footers
    - Front matter (Certificate, Ack, Abstract, TOC, Lists): Lowercase Roman numerals (i, ii, iii...)
    - Main body (Chapters 1-7, References, Appendices): Arabic numerals (1, 2, 3...)
    """
    first_arabic_page = 14

    def __init__(self, *args, **kwargs):
        super(BlackBookCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        first_arabic = getattr(BlackBookCanvas, 'first_arabic_page', 14)

        for state in self._saved_page_states:
            self.__dict__.update(state)
            current_page = self._pageNumber

            # Cover (1) and Inner Cover (2) have no headers or footers
            if current_page > 2:
                self.saveState()
                self.setFont("Times-Roman", 9)
                self.setFillColor(colors.HexColor("#475569"))

                # Running Header
                if current_page < first_arabic:
                    self.drawString(90, 745, "Mukesh Patel School of Technology Management & Engineering | Capstone Project")
                else:
                    self.drawString(90, 745, "Ultimate Precision AI: Automated Video Surveillance & Violence Detection System")
                
                self.setStrokeColor(colors.HexColor("#94a3b8"))
                self.setLineWidth(0.6)
                self.line(90, 737, 540, 737)

                # Running Footer
                self.line(90, 52, 540, 52)
                self.drawString(90, 40, "Department of Computer Engineering, MPSTME Shirpur")

                if current_page < first_arabic:
                    page_str = to_roman(current_page - 2)
                else:
                    arabic_num = current_page - first_arabic + 1
                    page_str = str(arabic_num)

                self.drawRightString(540, 40, f"Page {page_str}")
                self.restoreState()

            super(BlackBookCanvas, self).showPage()
        super(BlackBookCanvas, self).save()


def get_styles():
    styles = getSampleStyleSheet()
    PRIMARY = colors.HexColor("#0f172a")     # Deep Charcoal Black
    SECONDARY = colors.HexColor("#1e3a8a")   # Academic Navy
    MUTED_TEXT = colors.HexColor("#334155")  # Dark Slate
    CARD_BORDER = colors.HexColor("#cbd5e1") # Slate 300
    BG_LIGHT = colors.HexColor("#f8fafc")    # Slate 50

    styles.add(ParagraphStyle(
        name='BBTitle24',
        fontName='Times-Bold',
        fontSize=22,
        leading=28,
        textColor=PRIMARY,
        alignment=1,
        spaceAfter=15,
    ))

    styles.add(ParagraphStyle(
        name='BBSubtitle14',
        fontName='Times-Roman',
        fontSize=13,
        leading=18,
        textColor=MUTED_TEXT,
        alignment=1,
        spaceAfter=15,
    ))

    styles.add(ParagraphStyle(
        name='BBCenter12',
        fontName='Times-Roman',
        fontSize=11,
        leading=16,
        textColor=PRIMARY,
        alignment=1,
        spaceAfter=6,
    ))

    styles.add(ParagraphStyle(
        name='BBCenter14Bold',
        fontName='Times-Bold',
        fontSize=13,
        leading=18,
        textColor=PRIMARY,
        alignment=1,
        spaceAfter=6,
    ))

    styles.add(ParagraphStyle(
        name='BBChapterHeader',
        fontName='Times-Bold',
        fontSize=16,
        leading=21,
        textColor=PRIMARY,
        spaceBefore=14,
        spaceAfter=10,
        keepWithNext=True
    ))

    styles.add(ParagraphStyle(
        name='BBSectionHeader',
        fontName='Times-Bold',
        fontSize=12.5,
        leading=16.5,
        textColor=PRIMARY,
        spaceBefore=12,
        spaceAfter=5,
        keepWithNext=True
    ))

    styles.add(ParagraphStyle(
        name='BBSubSectionHeader',
        fontName='Times-Bold',
        fontSize=11,
        leading=15,
        textColor=PRIMARY,
        spaceBefore=9,
        spaceAfter=4,
        keepWithNext=True
    ))

    styles.add(ParagraphStyle(
        name='BBSubSubSectionHeader',
        fontName='Times-Italic',
        fontSize=10.5,
        leading=14.5,
        textColor=SECONDARY,
        spaceBefore=7,
        spaceAfter=3,
        keepWithNext=True
    ))

    styles.add(ParagraphStyle(
        name='BBBody',
        fontName='Times-Roman',
        fontSize=10,
        leading=15.5,
        textColor=PRIMARY,
        alignment=4,
        spaceAfter=7,
    ))

    styles.add(ParagraphStyle(
        name='BBBodyIndent',
        fontName='Times-Roman',
        fontSize=10,
        leading=15.5,
        textColor=PRIMARY,
        alignment=4,
        firstLineIndent=20,
        spaceAfter=7,
    ))

    styles.add(ParagraphStyle(
        name='BBBullet',
        fontName='Times-Roman',
        fontSize=9.5,
        leading=14.5,
        textColor=PRIMARY,
        leftIndent=24,
        firstLineIndent=-14,
        spaceAfter=4,
        alignment=4,
    ))

    styles.add(ParagraphStyle(
        name='BBCode',
        fontName='Courier',
        fontSize=7.5,
        leading=10.5,
        textColor=colors.HexColor("#0f172a"),
    ))

    styles.add(ParagraphStyle(
        name='BBTableHeader',
        fontName='Times-Bold',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.white,
        alignment=1,
    ))

    styles.add(ParagraphStyle(
        name='BBTableCell',
        fontName='Times-Roman',
        fontSize=8.5,
        leading=12,
        textColor=PRIMARY,
    ))

    styles.add(ParagraphStyle(
        name='BBTableCellBold',
        fontName='Times-Bold',
        fontSize=8.5,
        leading=12,
        textColor=PRIMARY,
    ))

    styles.add(ParagraphStyle(
        name='BBCallout',
        fontName='Times-Italic',
        fontSize=9.5,
        leading=14.5,
        textColor=SECONDARY,
        alignment=4,
    ))

    return styles


def assemble_story(styles, page_lookup, target_dir):
    story = []
    
    # 1. Front Matter (13 pages)
    story.extend(generate_front_matter(styles, page_lookup, PageTarget, target_dir))

    # 2. Main Body: Chapters 1 to 7
    story.extend(generate_chapter_1(styles, PageTarget, target_dir))
    story.extend(generate_chapter_2(styles, PageTarget, target_dir))
    story.extend(generate_chapter_3(styles, PageTarget, target_dir))
    story.extend(generate_chapter_4(styles, PageTarget, target_dir))
    story.extend(generate_chapter_5(styles, PageTarget, target_dir))
    story.extend(generate_chapter_6(styles, PageTarget, target_dir))
    story.extend(generate_chapter_7(styles, PageTarget, target_dir))

    # 3. Appendices A to D
    story.extend(generate_appendices(styles, PageTarget, target_dir))

    return story


def build_full_dissertation(output_pdf_path):
    styles = get_styles()

    # Pass 1: Dry run to record page targets
    print("Executing Pass 1: Calculating exact page layout and target indices...")
    pass1_target_dir = {}
    pass1_story = assemble_story(styles, None, pass1_target_dir)

    temp_pass1_pdf = "temp_pass1_measure.pdf"
    doc_pass1 = SimpleDocTemplate(
        temp_pass1_pdf,
        pagesize=letter,
        leftMargin=90,  # 1.25 in binding gutter
        rightMargin=72, # 1.0 in
        topMargin=72,   # 1.0 in
        bottomMargin=72 # 1.0 in
    )
    doc_pass1.build(pass1_story, canvasmaker=BlackBookCanvas)

    first_arabic = pass1_target_dir.get("ch1_start", 14)
    BlackBookCanvas.first_arabic_page = first_arabic
    print(f"Pass 1 Complete. First Arabic page identified at physical page: {first_arabic}")

    # Convert physical page numbers to formal formatted strings (Roman / Arabic)
    page_lookup = {}
    for key, phys_page in pass1_target_dir.items():
        if phys_page < first_arabic:
            page_lookup[key] = to_roman(phys_page - 2)
        else:
            page_lookup[key] = str(phys_page - first_arabic + 1)

    # Pass 2: Final build with synchronized TOC and List indices
    print("Executing Pass 2: Building final 50+ page Capstone Dissertation with synchronized TOC...")
    pass2_target_dir = {}
    pass2_story = assemble_story(styles, page_lookup, pass2_target_dir)

    doc_final = SimpleDocTemplate(
        output_pdf_path,
        pagesize=letter,
        leftMargin=90,
        rightMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    doc_final.build(pass2_story, canvasmaker=BlackBookCanvas)

    if os.path.exists(temp_pass1_pdf):
        try:
            os.remove(temp_pass1_pdf)
        except Exception:
            pass

    print(f"SUCCESS: Capstone Black Book Dissertation successfully generated at: {output_pdf_path}")


if __name__ == "__main__":
    out_file = "Capstone_Project_Report_Black_Book.pdf"
    if len(sys.argv) > 1:
        out_file = sys.argv[1]
    build_full_dissertation(out_file)
