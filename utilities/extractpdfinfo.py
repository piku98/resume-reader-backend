from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.pdffont import PDFFont
from pdfminer.converter import PDFPageAggregator
import pdfminer
import tabula
import io



def parse_obj(objs, fonts):
    for obj in objs:
        if isinstance(obj, pdfminer.layout.LTTextBox):
            for o in obj._objs:
                if isinstance(o,pdfminer.layout.LTTextLine):
                    text=o.get_text()
                    if text.strip():
                        for c in  o._objs:
                            if isinstance(c, pdfminer.layout.LTChar):
                                if c.fontname not in fonts:
                                    fonts.append(c.fontname)
        # if it's a container, recurse
        elif isinstance(obj, pdfminer.layout.LTFigure):
            parse_obj(obj._objs, fonts)
        else:
            pass




def extract_pdf_info(pdf):
    text = ''
    n_images = 0
    fonts = []
    linkedin = ''
    n_tables = 0


    #no. of tables
    try:
        tables = tabula.read_pdf(pdf, multiple_tables=True, pages='all')
        n_tables = len(tables)
    except:
        pass

    for page in PDFPage.get_pages(pdf, check_extractable=True, caching=True):
        #extract text
        resource_manager = PDFResourceManager()
        fake_file_handle = io.StringIO()
        converter = TextConverter(resource_manager, fake_file_handle)
        page_interpreter = PDFPageInterpreter(resource_manager, converter)
        page_interpreter.process_page(page)
        t = fake_file_handle.getvalue()
        text = text + '\n' + t

        #extract fonts
        device = PDFPageAggregator(resource_manager, laparams=LAParams())
        device_interpretor = PDFPageInterpreter(resource_manager, device)
        device_interpretor.process_page(page)
        layout = device.get_result()
        parse_obj(layout._objs, fonts)
        

        #no. of images
        try:

            for key in page.resources['XObject'].keys():
                if key.startswith('Im'):
                    n_images += 1
        except KeyError:
            pass

        

        #linkedIn link
        if page.annots and linkedin == '':
            for annotation in page.annots:
                annotationDict = annotation.resolve()
                if str(annotationDict['Subtype']) == "/'Link'":
                    if str(annotationDict['A']['URI'])[2:-1].startswith('http://www.linkedin.com'):
                        linkedin = str(annotationDict['A']['URI'])[2:-1]

    

    return {"linkedin": linkedin, "n_tables": n_tables, "fonts": fonts, "n_images": n_images, "text": text}





#file = open('../../../resume-test/Resume_1.pdf', 'rb')
#print(extract_pdf_info(file))
