import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import re
import os
import shutil
import fitz
from PyPDF2 import PdfReader
import PyPDF2
from dotenv import dotenv_values, load_dotenv



# Загрузка переменных окружения из файла .env
load_dotenv('.env')
poppler_path = os.getenv("poppler_path")
tesseract_path = os.getenv("tesseract_path")
log_path = os.getenv("log_path")
pdf_files = os.getenv("input_directory")
folder_path = os.getenv("output_directory")
print(pdf_files,folder_path)

def read_text_from_pdf(file_path):
    with open(file_path, "rb") as file:
        pdf_reader = PdfReader(file)
        num_pages = len(pdf_reader.pages)

        text = ""
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()

        return text

def find_pdf_files(folder_path):
    pdf_files = []
    # для чтения в подкаталогах тоже
    # for root, dirs, files in os.walk(folder_path):
    #     for file in files:
    #         if file.endswith(".pdf"):
    #             pdf_files.append(os.path.join(root, file))
    # return pdf_files
    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            pdf_files.append(os.path.join(folder_path, file))
    return pdf_files
folder_path = os.getenv('input_directory')



# print("Найденные PDF-файлы:")
# for file_path in pdf_files:
#     print(file_path)
#     get_aku_name(file_path)

#path = "IMG_0001.pdf" #path to a pdf file
def get_aku_name(path):
    def remove_first_page(input_pdf, output_pdf):
        with open(input_pdf, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            writer = PyPDF2.PdfWriter()

            for page_num in range(0,1):
                page = reader.pages[page_num]
                writer.add_page(page)

            with open(output_pdf, 'wb') as output_file:
                writer.write(output_file)


        
    remove_first_page(path,"output.pdf")
    images = convert_from_path("output.pdf", 500, poppler_path='poppler-23.11.0/Library/bin/')
    pattern = r"AKU[.,\s]\S{4}[.,\s]\S{2}\S{3}[.,\s]\S{1,3}[.,\s]RK[.,\s]\S{1,6}"
    pattern2 = r"[,\s]"
        
    pytesseract.pytesseract.tesseract_cmd = r"Tesseract-OCR/tesseract.exe"

    match = re.findall(pattern,pytesseract.image_to_string(images[0], lang='eng'))
    print(match)
    if match:
        print(f"Код '{match[0]}' соответствует формату.")
        replaced_text = re.sub(pattern2, ".", match[0])
        print(replaced_text)
        return replaced_text
    else:
        match = re.findall(pattern,read_text_from_pdf(path))
        if match:
            print(f"Код '{match[0]}' соответствует формату.")
            replaced_text = re.sub(pattern2, ".", match[0])
            print(replaced_text)
            return replaced_text
        else:
            print(f"Код  не соответствует формату.")
            return "unknown"
        
if not os.path.exists(folder_path):
        os.mkdir(folder_path)
def save_file_with_new_name(file_path, new_file_path):
    shutil.copyfile(file_path, new_file_path)

print("PDF-файлы:")
num = 1
for file_path in pdf_files: 
    print(file_path)
    buf = get_aku_name(file_path) 
    buf = str(num)+"_"+buf+".pdf"
    new_file_path = os.path.join(folder_path , buf)
    save_file_with_new_name(file_path, new_file_path )
    print("Файл сохранен под новым именем:", buf)
    num+=1