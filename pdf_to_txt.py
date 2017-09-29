#!/usr/bin/python
#-*- coding: utf-8 -*-

from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
from pdfminer.converter import TextConverter
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.layout import *
import re

def pdf_2_txt(filepath, outpath):
    try:
        fp = open(filepath, 'rb')
        outfp=open(outpath,'wb')
        rsrcmgr = PDFResourceManager(caching = False)
        laparams = LAParams()
        device = TextConverter(rsrcmgr, outfp, codec='utf-8', laparams=laparams,imagewriter=None)

        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.get_pages(fp, pagenos = set(),maxpages=0,
                                      password='',caching=False, check_extractable=True):
            page.rotate = page.rotate % 360
            interpreter.process_page(page)

        fp.close()
        device.close()
        outfp.flush()
        outfp.close()
        print ('Successfully converted pdf to txt')
        
    except Exception:
         print ("Fail to convert pdf")