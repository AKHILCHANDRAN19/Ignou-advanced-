import os
from fpdf import FPDF
from PyPDF2 import PdfReader

class PDFGenerator(FPDF):
    def __init__(self):
        super().__init__()
        self.font = None
        self.pen_color = None
        self.margin = 1 * 28.35  # 1 inch in points (1 inch = 28.35 points)
        self.line_height = 4.4  # Set line height to 4.4 points

    def header(self):
        # Draw border on each page
        self.set_draw_color(192, 192, 192)  # Light gray color
        self.rect(self.margin, self.margin, self.w - 2 * self.margin, self.h - 2 * self.margin)

    def set_custom_font(self, font_name, size):
        fonts = {
            "ShadowsIntoLight Regular": "ShadowsIntoLight-Regular.ttf",
            "Satisfy Regular": "Satisfy-Regular.ttf",
            "Caveat Regular": "Caveat-Regular.ttf",
            "PatrickHand Regular": "PatrickHand-Regular.ttf",
            "ReenieBeanie Regular": "ReenieBeanie-Regular.ttf",
            "Sacramento Regular": "Sacramento-Regular.ttf",
            "HomemadeApple Regular": "HomemadeApple-Regular.ttf"
        }
        if font_name in fonts:
            font_path = os.path.join('/storage/emulated/0/fonts', fonts[font_name])
            if os.path.isfile(font_path):
                self.add_font(font_name, '', font_path, uni=True)
                self.set_font(font_name, size=size)
            else:
                raise FileNotFoundError(f"Font file {font_path} not found.")
        else:
            raise ValueError("Font not recognized")

    def set_pen_color(self, color):
        colors = {
            "Black": (0, 0, 0),
            "Blue": (0, 0, 255)
        }
        if color in colors:
            self.pen_color = colors[color]
        else:
            raise ValueError("Color not recognized")

    def add_text(self, text, output_file):
        # Add a new page for text
        self.add_page()
        self.header()  # Draw border on the new page

        # Set font and color for the text
        if self.font:
            self.set_font(self.font, size=16)
        if self.pen_color:
            self.set_text_color(*self.pen_color)

        # Calculate text area
        text_width = self.w - 2 * self.margin

        # Set the initial position within the border
        self.set_xy(self.margin, self.margin + 10)
        y_position = self.get_y()

        # Add text within the border
        lines = text.split('\n')
        for line in lines:
            # If text exceeds the current page, add a new page
            if y_position + self.line_height > self.h - self.margin:
                self.add_page()
                self.header()  # Redraw border on the new page
                y_position = self.margin + 10  # Reset y position

            self.set_xy(self.margin, y_position)
            self.multi_cell(text_width, self.line_height, line, align='L')

            # Update y_position for the next line
            y_position = self.get_y() + self.line_height

        self.output(output_file)

def main():
    try:
        # Ensure output directory exists
        output_folder = '/storage/emulated/0/OUTPUT'
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Font selection
        print("Choose a font:")
        fonts = [
            "ShadowsIntoLight Regular",
            "Satisfy Regular",
            "Caveat Regular",
            "PatrickHand Regular",
            "ReenieBeanie Regular",
            "Sacramento Regular",
            "HomemadeApple Regular"
        ]
        for i, font in enumerate(fonts, 1):
            print(f"{i}. {font}")
        font_choice = int(input("Enter the number corresponding to your choice: "))
        if 1 <= font_choice <= len(fonts):
            font_name = fonts[font_choice - 1]
        else:
            raise ValueError("Invalid font choice")

        # Pen color selection
        print("Choose a pen color:")
        colors = ["Black", "Blue"]
        for i, color in enumerate(colors, 1):
            print(f"{i}. {color}")
        color_choice = int(input("Enter the number corresponding to your choice: "))
        if 1 <= color_choice <= len(colors):
            pen_color = colors[color_choice - 1]
        else:
            raise ValueError("Invalid color choice")

        # PDF selection
        print("Choose how to select PDFs:")
        print("1. Process a single PDF")
        print("2. Process all PDFs")
        pdf_selection = int(input("Enter the number corresponding to your choice: "))

        if pdf_selection == 1:
            # PDF file selection
            pdf_folder = '/storage/emulated/0/INPUT'
            pdf_files = [f for f in os.listdir(pdf_folder) if f.lower().endswith('.pdf')]
            if pdf_files:
                print("Available PDF files in the INPUT folder:")
                for i, pdf_file in enumerate(pdf_files, 1):
                    print(f"{i}. {pdf_file}")
                pdf_choice = int(input("Enter the number corresponding to your choice: "))
                if 1 <= pdf_choice <= len(pdf_files):
                    selected_pdf = pdf_files[pdf_choice - 1]
                    
                    # Extract text from selected PDF
                    pdf_path = os.path.join(pdf_folder, selected_pdf)
                    text = ""
                    with open(pdf_path, 'rb') as file:
                        reader = PdfReader(file)
                        for page in reader.pages:
                            text += page.extract_text() or ""

                    # Create PDF
                    pdf_gen = PDFGenerator()
                    pdf_gen.set_custom_font(font_name, size=16)
                    pdf_gen.set_pen_color(pen_color)

                    # Output file
                    output_file = os.path.join(output_folder, f'{os.path.splitext(selected_pdf)[0]}_Generated.pdf')
                    pdf_gen.add_text(text, output_file)

                    print(f"PDF created successfully: {output_file}")
                else:
                    raise ValueError("Invalid PDF choice")
            else:
                raise FileNotFoundError("No PDF files found in the INPUT folder.")
        elif pdf_selection == 2:
            # Process all PDFs in the folder
            pdf_folder = '/storage/emulated/0/INPUT'
            pdf_files = [f for f in os.listdir(pdf_folder) if f.lower().endswith('.pdf')]
            if pdf_files:
                for pdf_file in pdf_files:
                    pdf_path = os.path.join(pdf_folder, pdf_file)
                    text = ""
                    with open(pdf_path, 'rb') as file:
                        reader = PdfReader(file)
                        for page in reader.pages:
                            text += page.extract_text() or ""

                    # Create PDF
                    pdf_gen = PDFGenerator()
                    pdf_gen.set_custom_font(font_name, size=16)
                    pdf_gen.set_pen_color(pen_color)

                    # Output file
                    output_file = os.path.join(output_folder, f'{os.path.splitext(pdf_file)[0]}_Generated.pdf')
                    pdf_gen.add_text(text, output_file)

                    print(f"PDF created successfully: {output_file}")
            else:
                raise FileNotFoundError("No PDF files found in the INPUT folder.")
        else:
            raise ValueError("Invalid PDF selection method")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
