import nltk
import re
stp = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]



def checkint(ch):
    try:
        int(ch)
        return True
    except:
        return False


def getnouns(document):
    names = []
    stp_document = ' '.join([i for i in document.split() if i not in stp])
    sentences = nltk.sent_tokenize(stp_document)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    for tagged_sentence in sentences:
        for chunk in nltk.ne_chunk(tagged_sentence):
            if type(chunk) == nltk.tree.Tree:
                if chunk.label() == 'PERSON' or chunk.label() == 'ORGANIZATION':
                    names.append(' '.join([c[0] for c in chunk]))
    return names


def get_personal_details(text):

    #extract name
    names = getnouns(text)
    name = ''
    if names[0].lower() != 'resume':
        name = names[0]
    else:
        name = names[1]
    
    
    #extract phone number
    phone = ''
    """ phone_labels = ['mob', 'Mob', 'MOB',  'ph', 'Ph', 'PH', 'mobile', 'Mobile', 'phone', 'Phone']
    for pl in phone_labels:
        idx = text.find(pl)
        if idx != -1:
            i = idx + len(pl)
            while text[i] != '+' and not checkint(text[i]):
                i += 1
            
            while text[i] != ' ' and text[i] != '\n':
                phone = phone + text[i]
                i += 1
            phone = phone.strip()
            break """
    
    """ if phone == '':
        numbers = re.findall(re.compile(r'(?:(?:\+?([1-9]|[0-9][0-9]|[0-9][0-9][0-9])\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([0-9][1-9]|[0-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?'), text)
        if numbers:
            phone = ''.join(numbers[0])
            if len(phone) > 10:
                phone =  '+' + phone

 """
    numbers = []
    numbers = re.findall(re.compile(r'\+(9[976]\d|8[987530]\d|6[987]\d|5[90]\d|42\d|3[875]\d|2[98654321]\d|9[8543210]|8[6421]|6[6543210]|5[87654321]|4[987654310]|3[9643210]|2[70]|7|1)\d{1,14}$'), text)
    if len(numbers) == 0:
        numbers = re.findall(re.compile(r'\+(9[976]\d|8[987530]\d|6[987]\d|5[90]\d|42\d|3[875]\d|2[98654321]\d|9[8543210]|8[6421]|6[6543210]|5[87654321]|4[987654310]|3[9643210]|2[70]|7|1)\W*\d\W*\d\W*\d\W*\d\W*\d\W*\d\W*\d\W*\d\W*(\d{1,2})$'), text)
    if len(numbers) == 0:
        numbers = re.findall(re.compile(r'((?:\+|00)[17](?: |\-)?|(?:\+|00)[1-9]\d{0,2}(?: |\-)?|(?:\+|00)1\-\d{3}(?: |\-)?)?(0\d|\([0-9]{3}\)|[1-9]{0,3})(?:((?: |\-)[0-9]{2}){4}|((?:[0-9]{2}){4})|((?: |\-)[0-9]{3}(?: |\-)[0-9]{4})|([0-9]{7}))'), text)
    if len(numbers) == 0:
        numbers = re.findall(re.compile(r'(?:(?:\+?([1-9]|[0-9][0-9]|[0-9][0-9][0-9])\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([0-9][1-9]|[0-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?'), text)
    if len(numbers) == 0:
        numbers = re.findall(re.compile(r'^\d{3}-\d{2}-\d{4}$|^\d{2}-\d{7}$'), text)
    if len(numbers) > 0:
        phone = ''.join(numbers[0])


    
    #extract email
    email = ''
    emails = re.findall("([^@|\s]+@[^@]+\.[^@|\s]+)", text)
    if emails:
        try:
            email = emails[0].split()[0].strip(';')
        except IndexError:
            pass

    
    return {"name": name, "email": email, "phone": phone}


#file = open('../../../resume-test/Resume_2.pdf', 'rb')
#from extractpdfinfo import extract_pdf_info
#print(get_personal_details(extract_pdf_info(file)['text']))

