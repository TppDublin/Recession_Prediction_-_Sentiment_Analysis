import pandas as pd
import numpy as np
import requests
import time
from PyPDF2 import PdfFileMerger, PdfFileReader, PdfReader
import io
import tabula as tb
import pandas as pd
#import camelot as cl
import fitz
import glob
#from textblob import TextBlob
import re
import os
import create_database as db


def file_read_pdf():
    filename = "your path"
    file = open(filename, "r")
    content = file.read()
    data_into_list = content.replace('\n', ' ').split(",")
    file.close()

    return data_into_list


def file_read_html():
    filename = "your path"
    file = open(filename, "r")
    content = file.read()
    data_into_list = content.replace('\n', ' ').split(",")
    file.close()

    return data_into_list


def date_extract(html_list, pdf_list):
    date_list = []
    html_len = len(html_list)
    pdf_len = len(pdf_list)
    for i in range(0, html_len):
        url = html_list[i]
        suffix = url.split(sep='/')[5]
        date = suffix.split(sep='.')[0]
        date_list.append(date)
    for i in range(0, pdf_len):
        url = pdf_list[i]
        suffix = url.split(sep='/')[5]
        date = suffix.split(sep='.')[0]
        if "fomcminutes" in date:
            MMDDYY = date.split(sep='s')[1]
            date_list.append(MMDDYY)

    return date_list


def quart_list(dates_list):
    quart = []
    for i in range(0, len(dates_list)):
        dts = dates_list[i]
        year = dts[0:4]
        mth = dts[4:6]
        if mth in ('01', '02', '03'):
            quart_var = year + '-03' + '-31'
            quart.append(quart_var)
        if mth in ('04', '05', '06'):
            quart_var = year + '-06' + '-30'
            quart.append(quart_var)
        if mth in ('07', '08', '09'):
            quart_var = year + '-09' + '-30'
            quart.append(quart_var)
        if mth in ('10', '11', '12'):
            quart_var = year + '-12' + '-31'
            quart.append(quart_var)

    return quart


def MOM_dloads_pdf():
    data_list = file_read_pdf()
    cnt = len(data_list)
    print(cnt)
    date_list = []
    for i in range(0, cnt):
        url = data_list[i]
        print(url)
        suffix = url.split(sep='/')[5]
        date = suffix.split(sep='.')[0]

        if "fomcminutes" in date:
            MMDDYY = date.split(sep='s')[1]
            date_list.append(MMDDYY)
        else:
            date_list.append(date)
        url_og = 'https://www.federalreserve.gov/monetarypolicy/files/fomcminutes{}.pdf'.format(
            date_list[i])
        resp = requests.get(url_og)

        with open("your_opath.pdf".format(date_list[i]), "wb") as f:
            f.write(resp.content)
            print("Writing complete for ", date_list[i])


def MOM_dloads_html():
    data_list = file_read_html()
    global cnt
    cnt = len(data_list)
    print(cnt)
    date_list = []
    for i in range(0, cnt):
        url = data_list[i]
        print(url)
        suffix = url.split(sep='/')[5]
        date = suffix.split(sep='.')[0]
        url_og = 'https://www.federalreserve.gov/fomc/minutes/{}.htm'.format(
            date)
        resp = requests.get(url_og)

        with open("your path".format(date), "wb") as f:
            f.write(resp.content)
            print("Writing complete for ", date)


# def htm_pdf_convrtr():
#     renderer = ChromePdfRenderer()
#     # Create a PDF from a HTML string using Python
#     pdf = renderer.RenderHtmlAsPdf("D:\Financial Data Science\Data_Science_Trading\project\FOMC_MOM\FOMC_20070918.html")
#     # Export to a file or Stream
#     pdf.SaveAs("D:\Financial Data Science\Data_Science_Trading\project\FOMC_MOM\FOMC_20070918.pdf")


def pdf_to_df(quart_list):
    path = "your path"
    data = glob.glob(os.path.join(path, '*.pdf'))
    #print(len(data))
    # dfs = [pd.DataFrame(columns=['Articles'])]
    dfs = []
    cnt=1
    for pdf in data:
        artcle = fitz.open(pdf)
        text = ""
        # pattern="Figure\s+\d+[A-Z|a-z]+\d"
        # filter_sent = re.sub('[^a-zA-Z]',' ',sentences[j])
        for page in artcle:
            blocks = page.get_text("blocks")
            for blk in blocks:
                s = re.sub('[^a-zA-Z]', ' ', blk[4])
                text += s
        dfs.append(text)
        print("Pdf no is ",cnt)
        cnt=cnt+1
    print(len(dfs))
    Art_dict={'Date':quart_list,'Article':dfs}    
    Art_df=pd.DataFrame(Art_dict)
    return Art_df


html_list=file_read_html()
pdf_list=file_read_pdf()
dates_list=date_extract(html_list, pdf_list)
q_list=quart_list(dates_list)
# #print(len(q_list))
# print(len(dates_list))
artcle_txt = pdf_to_df(q_list)
print(artcle_txt)
# artcle_txt.describe()
# MOM_dloads_pdf()
# MOM_dloads_html()

db_name = 'Recession_new.db'
table_name = "Fomc_Data"
data_base_obj = db.database(db_name)
data_base_obj.dataframe_to_db(artcle_txt,table_name)