from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
from docx2pdf import convert
import socket
from statics import Directories




class DocGenerator:
    def __init__(self):
        self.hostname = socket.gethostname()

    
    def generate_docx(self,email,uuid):
        parsed_email = email.split("@")
        client_identity = parsed_email[1]
        doc = Document()
        doc.add_heading(client_identity).paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_paragraph('%s           %s' %(uuid,self.hostname), style='Intense Quote').paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER        
        doc.add_paragraph("VMESS CDN").paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture(f"{Directories.GENERATED_OUTPUT}/{client_identity}_CDN.PNG",width=Inches(6)) 
        doc.add_page_break()
        doc.add_paragraph("VMESS TLS").paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture(f"{Directories.GENERATED_OUTPUT}/{client_identity}_TLS.PNG",width=Inches(6))
        doc.add_page_break()
        doc.add_paragraph("VMESS TLS CDN").paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture(f"{Directories.GENERATED_OUTPUT}/{client_identity}_TLS-CDN.PNG",width=Inches(6))   
        doc.save(f"{Directories.GENERATED_DOCX}/{client_identity}.docx")
    





