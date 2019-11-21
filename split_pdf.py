import sys
import fitz
import cloudconvert

def convert(filename):
    print("CONVERTING .........")
    api = cloudconvert.Api(
        '2R83XvhTuELfut2PvQbv0rRgPRSlTGA2wICqnQRUdnJL7YVua17xrHHpufJzqQtC')
    process = api.convert({
        'inputformat': 'txt',
        'outputformat': 'pdf',
        'input': 'upload',
        'file': open(filename, 'rb')
    })
    process.wait()  # wait until conversion finished
    pdf_file_name = filename[:len(filename)-4]+".pdf"
    process.download(pdf_file_name)
    return pdf_file_name

def mark_word(page, text):
    """
    Highlight each word that contains 'text'.
    """
    found = 0
    wlist = page.getTextWords()        # make the word list
    #print(wlist)
    for w in wlist:                    # scan through all words on page
        if text in w[4]:               # w[4] is the word's string
            found += 1                 # count
            r = fitz.Rect(w[:4])       # make rect from word bbox
            page.addHighlightAnnot(r)  # underline
    return found

def highlight(fname,text):
    doc = fitz.open(fname)

    #print("underlining words containing '%s' in document '%s'" % (text, doc.name))
    new_doc = False                        
    for page in doc: 
        found = mark_word(page,text)                      
        if found:                          
            new_doc = True
            #print("found '%s' %i times on page %i" % (text, found, page.number + 1))
    if new_doc:
        doc.save("Highlighted/HIGLIGHTED_" + doc.name)
