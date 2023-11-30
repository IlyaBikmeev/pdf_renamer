import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import re
import os
import shutil
from PyPDF2 import PdfReader
import traceback
import PyPDF2
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv('.env')
poppler_path = os.getenv("poppler_path")
tesseract_path = os.getenv("tesseract_path")
log_path = os.getenv("log_path")
input_path = os.getenv("input_directory")
output_path = os.getenv("output_directory")
pytesseract.pytesseract.tesseract_cmd = tesseract_path

def save_first_page(input_pdf, output_pdf):
    with open(input_pdf, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        writer = PyPDF2.PdfWriter()
        writer.add_page(reader.pages[0])

        with open(output_pdf, 'wb') as output_file:
            writer.write(output_file)

def read_text_from_pdf(file_path):
    with open(file_path, "rb") as file:
        pdf_reader = PdfReader(file)
        return '\n'.join([page.extract_text() for page in pdf_reader.pages[::2]])

def get_aku_name(path):
    save_first_page(path, 'buf.pdf')
    images = convert_from_path("buf.pdf", 500, poppler_path=poppler_path)
    os.remove('buf.pdf')
    pattern_1 = r"AKU[.,\s]\S{4}[.,\s]\S{2}\S{3}[.,\s]\S{1,3}[.,\s]RK[.,\s]\S{1,6}"
    pattern_2 = r"[,\s]"

    text = read_text_from_pdf(path)
    match_1 = re.findall(pattern_1, text)
    match_2 = re.findall(pattern_1,pytesseract.image_to_string(images[0], lang='eng'))
    

    if not match_1 and not match_2:
        print(f'Не получилось достать код для файла {path} :(')
        raise ValueError("Doesn't match any regexp")

    if match_1:
        print('Найдено совпадение в тексте.')
        return re.sub(pattern_2, ".", match_1[0])
    else:
        print('Найдено совпадение в картинке.')
        return re.sub(pattern_2, ".", match_2[0])

if not os.path.exists(output_path):
    os.mkdir(output_path)

num = 1
success = 0
failed = 0
for file in os.listdir(input_path):
    if file.endswith('.pdf'):
        try:
            path = f'{input_path}/{file}'
            aku_name = get_aku_name(path)
            print('Идентификатор для файла: ' + aku_name)
            new_path = f'{output_path}/{num}_{aku_name}.pdf'
            shutil.copyfile(path, new_path)
            num += 1
            success += 1

            print('Успешно обработан файл ' + file)
        except Exception as e:
            failed += 1
            print(f'Не получилось обработать файл {file}. Ошибка: {e}.')
            print(traceback.print_exc())

print(f'Успешно обработано файлов: {success} из {success + failed}. Ошибок: {failed}')