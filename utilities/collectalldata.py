import os
os.chdir('..')
from utilities.extractdocxinfo import extract_docx_info
from utilities.extractpdfinfo import extract_pdf_info
from utilities.getpersondetails import get_personal_details

def collect_details(file, ext):
    details = {}
    if ext == 'docx':
        docxinfo = extract_docx_info(file)
        personinfo = get_personal_details(docxinfo['text'])
        if docxinfo['email'] != '':
            details['email'] = docxinfo['email']
        else:
            details['email'] = personinfo['email']
        
        for key in docxinfo.keys():
            if key != 'email' and key != 'text':
                details[key] = docxinfo[key]
        
        for key in personinfo.keys():
            if key != 'email' and key != 'text':
                details[key] = personinfo[key]
    
    elif ext == 'pdf':
        pdfinfo = extract_pdf_info(file)
        personinfo = get_personal_details(pdfinfo['text'])
        
        for key in pdfinfo.keys():
            if key != 'text':
                details[key] = pdfinfo[key]
        
        for key in personinfo.keys():
            if key != 'text':
                details[key] = personinfo[key]


    return details



#file = open('../../../resume-test/testme.docx', 'rb')
#print(collect_details(file, 'docx'))