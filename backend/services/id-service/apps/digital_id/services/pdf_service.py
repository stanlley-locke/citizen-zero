import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch, mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# Kenyan Flag Colors
KENYA_BLACK = colors.black
KENYA_RED = colors.Color(0.75, 0.05, 0.05) # Blood Red
KENYA_GREEN = colors.Color(0.0, 0.4, 0.0)  # Forest Green
KENYA_GOLD = colors.Color(0.85, 0.65, 0.13) # Gold for Arms
KENYA_WHITE = colors.white

class PDFService:
    @staticmethod
    def _draw_guilloche_pattern(c, x, y, width, height, color=colors.lightgrey):
        """Draws a simulated guilloche security pattern."""
        c.saveState()
        c.setStrokeColor(color)
        c.setLineWidth(0.3)
        c.setDash([1, 2])
        # Draw intersecting sine-like waves
        for i in range(0, int(height/mm), 4):
            path = c.beginPath()
            path.moveTo(x, y + i*mm)
            path.curveTo(x + width/3, y + (i+5)*mm, x + 2*width/3, y + (i-5)*mm, x + width, y + i*mm)
            c.drawPath(path, stroke=1, fill=0)
        c.restoreState()

    @staticmethod
    def _draw_kenyan_flag_strip(c, x, y, width, height):
        """Draws a horizontal Kenyan flag strip."""
        c.saveState()
        stripe_h = height / 3
        # Black
        c.setFillColor(KENYA_BLACK)
        c.rect(x, y + 2*stripe_h, width, stripe_h, stroke=0, fill=1)
        # Red + White separators
        c.setFillColor(KENYA_WHITE)
        c.rect(x, y + stripe_h - 0.5*mm, width, stripe_h + 1*mm, stroke=0, fill=1)
        c.setFillColor(KENYA_RED)
        c.rect(x, y + stripe_h, width, stripe_h, stroke=0, fill=1)
        # Green
        c.setFillColor(KENYA_GREEN)
        c.rect(x, y, width, stripe_h, stroke=0, fill=1)
        c.restoreState()

    @staticmethod
    def generate_national_id(citizen_data):
        """
        Generates a Premium National ID Card PDF (Front and Back).
        Format: ID-1 (85.60 × 53.98 mm)
        """
        buffer = io.BytesIO()
        card_width = 85.6 * mm
        card_height = 53.98 * mm
        c = canvas.Canvas(buffer, pagesize=(card_width, card_height))
        
        # --- FRONT ---
        # 1. Background (Light Blue-Grey gradient simulation)
        c.setFillColor(colors.Color(0.96, 0.98, 1.0))
        c.rect(0, 0, card_width, card_height, fill=1, stroke=0)
        PDFService._draw_guilloche_pattern(c, 0, 0, card_width, card_height, colors.Color(0.8, 0.85, 0.9, alpha=0.5))

        # 2. Top Banner (Kenyan Flag + Republic Text)
        c.setFillColor(colors.Color(0.9, 0.9, 0.95)) # Header background
        c.rect(0, card_height - 12*mm, card_width, 12*mm, fill=1, stroke=0)
        
        # Flag Strip on top edge
        PDFService._draw_kenyan_flag_strip(c, 0, card_height - 3*mm, card_width, 3*mm)
        
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(KENYA_BLACK)
        c.drawCentredString(card_width/2, card_height - 7*mm, "REPUBLIC OF KENYA")
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(KENYA_RED)
        c.drawCentredString(card_width/2, card_height - 10*mm, "NATIONAL IDENTITY CARD")

        # 3. Photo & Chip
        # Photo Frame
        c.setStrokeColor(KENYA_BLACK)
        c.setLineWidth(0.5)
        c.setFillColor(colors.white)
        c.rect(3*mm, 10*mm, 26*mm, 32*mm, fill=1, stroke=1)
        
        # Ghost Photo text
        c.setFont("Helvetica", 6)
        c.setFillColor(colors.lightgrey)
        c.drawCentredString(16*mm, 26*mm, "PHOTO")

        # Gold Chip
        c.setFillColor(KENYA_GOLD)
        c.setStrokeColor(colors.darkgoldenrod)
        c.roundRect(5*mm, 22*mm, 11*mm, 10*mm, 2*mm, fill=1, stroke=1)
        # Chip Contacts
        c.setStrokeColor(colors.black)
        c.setLineWidth(0.2)
        c.line(5*mm, 25*mm, 16*mm, 25*mm)
        c.line(5*mm, 29*mm, 16*mm, 29*mm)
        c.line(8.5*mm, 22*mm, 8.5*mm, 32*mm)
        c.line(12.5*mm, 22*mm, 12.5*mm, 32*mm)

        # 4. Data Fields (Aligned)
        x_labels = 32*mm
        x_values = 58*mm
        y_cursor = 37*mm
        
        # ID Number Highlight
        c.setFont("Helvetica-Bold", 11)
        KENYA_BLUE = colors.darkblue
        c.setFillColor(KENYA_BLUE) # Official Blue
        c.drawString(x_labels, 42*mm, f"ID: {citizen_data.get('national_id', 'N/A')}")
        
        # Helper for rows
        def draw_row(label, value):
            nonlocal y_cursor
            c.setFont("Helvetica-Bold", 6)
            c.setFillColor(colors.darkslategrey)
            c.drawString(x_labels, y_cursor, label)
            
            c.setFont("Helvetica-Bold", 7)
            c.setFillColor(KENYA_BLACK)
            # Use fixed positioning for better alignment than simple offset
            c.drawString(x_labels + 20*mm, y_cursor, str(value).upper())
            y_cursor -= 4.2*mm

        draw_row("FULL NAMES", f"{citizen_data.get('last_name', '')}")
        draw_row("GIVEN NAMES", f"{citizen_data.get('first_name', '')}")
        draw_row("DATE OF BIRTH", str(citizen_data.get('date_of_birth', '')))
        draw_row("SEX", citizen_data.get('gender', 'M'))
        draw_row("DISTRICT", citizen_data.get('county_of_birth', 'NAIROBI').split('-')[-1].strip().upper())
        draw_row("DATE OF ISSUE", "03.02.2026")

        # 5. Coat of Arms (Right Watermark)
        c.saveState()
        c.translate(card_width - 12*mm, card_height - 18*mm)
        c.setFillColor(colors.gold)
        c.circle(0, 0, 8*mm, fill=1, stroke=0)
        c.setFont("Times-Bold", 20)
        c.setFillColor(KENYA_BLACK)
        c.drawCentredString(0, -2*mm, "K")
        c.restoreState()

        # Serial Number (Bottom Right)
        c.setFont("Courier-Bold", 6)
        c.setFillColor(KENYA_RED)
        c.drawRightString(card_width - 3*mm, 3*mm, "SERIAL 94837261")

        c.showPage()
        
        # --- BACK ---
        c.setFillColor(colors.Color(0.96, 0.98, 1.0))
        c.rect(0, 0, card_width, card_height, fill=1, stroke=0)
        PDFService._draw_guilloche_pattern(c, 0, 0, card_width, card_height, colors.Color(0.8, 0.85, 0.9, alpha=0.5))

        # PDF417 Area
        c.setFillColor(colors.white)
        c.rect(2*mm, card_height - 20*mm, card_width - 4*mm, 15*mm, fill=1, stroke=1)
        # Mock Barcode
        c.setFillColor(KENYA_BLACK)
        c.rect(5*mm, card_height - 18*mm, card_width - 10*mm, 10*mm, fill=1, stroke=0) 
        c.setFillColor(colors.white)
        c.setFont("Courier-Bold", 10)
        c.drawCentredString(card_width/2, card_height - 14*mm, f"<{citizen_data.get('national_id', 'ID')}>")

        # District/Location
        c.setFillColor(KENYA_BLACK)
        c.setFont("Helvetica-Bold", 6)
        c.drawString(5*mm, 20*mm, "DISTRICT OF BIRTH:")
        c.setFont("Helvetica", 6)
        c.drawString(30*mm, 20*mm, citizen_data.get('county_of_birth', 'NAIROBI').upper())

        c.setFont("Helvetica-Bold", 6)
        c.drawString(5*mm, 16*mm, "PLACE OF ISSUE:")
        c.setFont("Helvetica", 6)
        c.drawString(30*mm, 16*mm, "NAIROBI")

        # Footer
        c.setFont("Helvetica-Oblique", 5)
        c.drawCentredString(card_width/2, 5*mm, "Property of the Government of Kenya. If found, return to nearest authority.")

        c.save()
        buffer.seek(0)
        return buffer.getvalue()

    @staticmethod
    def generate_passport(citizen_data):
        """
        Generates a Passport Bio Page PDF (ICAO 9303 Compliant Layout).
        """
        buffer = io.BytesIO()
        p_width = 125*mm
        p_height = 88*mm
        c = canvas.Canvas(buffer, pagesize=(p_width, p_height))
        
        # 1. Background Pattern (Detailed)
        c.setFillColor(colors.Color(0.98, 0.96, 0.98)) # Off-white pinkish
        c.rect(0, 0, p_width, p_height, fill=1, stroke=0)
        PDFService._draw_guilloche_pattern(c, 0, 0, p_width, p_height, colors.Color(0.9, 0.8, 0.8, alpha=0.5))

        # 2. Header
        c.setFont("Times-Bold", 10)
        c.setFillColor(KENYA_BLACK)
        c.drawCentredString(p_width/2, p_height - 7*mm, "REPUBLIC OF KENYA")
        c.setFont("Times-Roman", 8)
        c.drawCentredString(p_width/2, p_height - 11*mm, "PASSPORT / PASSEPORT")
        
        # Coat of Arms (Center Top)
        c.setFillColor(KENYA_GOLD)
        c.circle(p_width/2, p_height - 7*mm, 2*mm, fill=1, stroke=0) # Tiny dot simulation

        # 3. Top Right Codes
        c.setFont("Helvetica", 6)
        c.drawString(5*mm, p_height - 16*mm, "Type/Type")
        c.drawString(20*mm, p_height - 16*mm, "Country Code/Code du pays")
        c.drawString(55*mm, p_height - 16*mm, "Passport No./No du passeport")
        
        c.setFont("Helvetica-Bold", 8)
        c.drawString(5*mm, p_height - 19*mm, "P")
        c.drawString(20*mm, p_height - 19*mm, "KEN")
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(KENYA_RED)
        c.drawString(55*mm, p_height - 19*mm, "AK029384")
        c.setFillColor(KENYA_BLACK)

        # 4. Photo (Left)
        c.setStrokeColor(colors.grey)
        c.setFillColor(colors.white)
        c.rect(5*mm, 23*mm, 28*mm, 35*mm, fill=1, stroke=1)
        c.setFont("Helvetica", 6)
        c.setFillColor(colors.grey)
        c.drawCentredString(19*mm, 40*mm, "PHOTO")

        # 5. Data Fields (Grid Layout)
        x_col = 38*mm
        y_cur = p_height - 25*mm
        
        def draw_pass_field(label, value, x, y, width=40*mm):
            c.setFont("Helvetica", 5)
            c.setFillColor(colors.darkgrey)
            c.drawString(x, y, label)
            c.setFont("Helvetica-Bold", 7.5)
            c.setFillColor(KENYA_BLACK)
            c.drawString(x, y - 3*mm, str(value).upper())

        draw_pass_field("Surname / Nom", citizen_data.get('last_name', ''), x_col, y_cur)
        y_cur -= 7.5*mm
        draw_pass_field("Given Names / Prenoms", citizen_data.get('first_name', ''), x_col, y_cur)
        y_cur -= 7.5*mm
        draw_pass_field("Nationality / Nationalite", "KENYAN", x_col, y_cur)
        y_cur -= 7.5*mm
        draw_pass_field("Date of Birth / Date de naissance", str(citizen_data.get('date_of_birth', '')), x_col, y_cur)
        draw_pass_field("Sex / Sexe", citizen_data.get('gender', 'M'), x_col + 35*mm, y_cur) # Inline
        y_cur -= 7.5*mm
        draw_pass_field("Place of Birth / Lieu de naissance", citizen_data.get('place_of_birth', ''), x_col, y_cur)
        y_cur -= 7.5*mm
        draw_pass_field("Date of Issue / Date de delivrance", "03 FEB 2026", x_col, y_cur)
        draw_pass_field("Date of Expiry / Date d'expiration", "03 FEB 2036", x_col + 35*mm, y_cur) # Inline

        # 6. MRZ Zone (Strict Typography)
        c.setFont("Courier-Bold", 10) # Monospace is critical
        c.setFillColor(KENYA_BLACK)
        
        # MRZ Logic
        last_name = citizen_data.get('last_name', '').upper().replace(' ', '<')
        first_name = citizen_data.get('first_name', '').upper().replace(' ', '<')
        mrz_1 = f"P<KEN{last_name}<<{first_name}"
        mrz_1 = mrz_1.ljust(44, '<')[:44]
        
        p_no = "AK029384<"
        nat = "KEN"
        dob = "950101" # Mock
        sex = citizen_data.get('gender', 'M')
        exp = "300101" # Mock
        mrz_2 = f"{p_no}4{nat}{dob}8{sex}{exp}2<<<<<<<<<<<<<<02"
        mrz_2 = mrz_2.ljust(44, '<')[:44]

        c.drawString(5*mm, 10*mm, mrz_1)
        c.drawString(5*mm, 5*mm, mrz_2)

        c.save()
        buffer.seek(0)
        return buffer.getvalue()

    @staticmethod
    def generate_birth_certificate(citizen_data):
        """
        Generates a Ceremonial Birth Certificate PDF (A4) with Kenyan Theme.
        """
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        
        # 1. Kenyan Flag Border
        border_w = 4*mm
        # Top = Black, Bottom = Green, Sides = Red (Stylized)
        
        # Outer Gold Frame
        c.setStrokeColor(KENYA_GOLD)
        c.setLineWidth(1)
        c.rect(10*mm, 10*mm, width - 20*mm, height - 20*mm)
        
        # Inner Content Box
        c.rect(15*mm, 15*mm, width - 30*mm, height - 30*mm)

        # 2. Header
        y_cursor = height - 40*mm
        c.setFont("Times-Bold", 26)
        c.setFillColor(KENYA_BLACK)
        c.drawCentredString(width/2, y_cursor, "CERTIFICATE OF BIRTH")
        
        y_cursor -= 12*mm
        c.setFont("Times-Bold", 16)
        c.setFillColor(KENYA_RED)
        c.drawCentredString(width/2, y_cursor, "REPUBLIC OF KENYA")
        
        y_cursor -= 8*mm
        c.setFont("Times-Italic", 12)
        c.setFillColor(KENYA_BLACK)
        c.drawCentredString(width/2, y_cursor, "The Births and Deaths Registration Act")

        # 3. Watermark
        c.saveState()
        c.translate(width/2, height/2)
        c.rotate(30)
        c.setFont("Helvetica-Bold", 80)
        c.setFillColor(colors.Color(0.8, 0.8, 0.8, alpha=0.15))
        c.drawCentredString(0, 0, "KENYA")
        c.restoreState()

        # 4. Form Data (Table Layout with Dotted Lines)
        y_start = height - 85*mm
        row_h = 14*mm
        left_margin = 35*mm
        label_w = 60*mm

        data = [
            ("Birth Entry Number", "129038475"),
            ("Name of Child", f"{citizen_data.get('first_name', '')} {citizen_data.get('last_name', '')}"),
            ("Date of Birth", str(citizen_data.get('date_of_birth', ''))),
            ("Sex", "Male" if citizen_data.get('gender') == 'M' else "Female"),
            ("Place of Birth", citizen_data.get('place_of_birth', 'Nairobi').title()),
            ("Name of Mother", "Jane Doe (Mock)"),
            ("Name of Father", "John Doe (Mock)"),
            ("Date of Registration", "02 Feb 2026"),
        ]

        for label, val in data:
            # Label
            c.setFont("Times-Bold", 12)
            c.setFillColor(colors.darkslategrey)
            c.drawString(left_margin, y_start, label + ":")
            
            # Value
            c.setFont("Courier-Bold", 13) # Monospace for data looks official
            c.setFillColor(KENYA_BLACK)
            c.drawString(left_margin + label_w, y_start, str(val).upper())
            
            # Dotted Underline
            c.setStrokeColor(colors.grey)
            c.setLineWidth(0.5)
            c.setDash([1, 2])
            c.line(left_margin + label_w, y_start - 2*mm, width - 35*mm, y_start - 2*mm)
            
            y_start -= row_h

        # 5. Seal & Signatures
        y_sig = 40*mm
        
        # Seal (Left)
        c.setStrokeColor(KENYA_RED)
        c.setLineWidth(2)
        c.setDash([]) # Solid
        c.circle(50*mm, y_sig, 18*mm)
        c.setFont("Times-Bold", 10)
        c.setFillColor(KENYA_RED)
        c.drawCentredString(50*mm, y_sig + 12*mm, "OFFICIAL SEAL")
        c.drawCentredString(50*mm, y_sig - 12*mm, "REGISTRAR OF BIRTHS")

        # Signature (Right)
        c.setStrokeColor(KENYA_BLACK)
        c.setLineWidth(1)
        c.line(width - 80*mm, y_sig - 5*mm, width - 30*mm, y_sig - 5*mm)
        c.setFont("Times-Roman", 10)
        c.setFillColor(KENYA_BLACK)
        c.drawCentredString(width - 55*mm, y_sig - 10*mm, "District Registrar")

        # 6. Bottom Border Strip (Kenyan Flag Colors)
        PDFService._draw_kenyan_flag_strip(c, 10*mm, 10*mm, width - 20*mm, 4*mm)

        c.save()
        buffer.seek(0)
        return buffer.getvalue()

