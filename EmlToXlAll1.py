import os
import re
import chardet
import csv
from email import policy
from email.parser import BytesParser

# Функция для чтения и разбора .eml файла
def parse_eml(file_path):
    with open(file_path, 'rb') as file:
        email_message = BytesParser(policy=policy.default).parse(file)

    # Извлекаем и объединяем все текстовые части
    text_parts = []
    if email_message.is_multipart():
        for part in email_message.walk():
            content_type = part.get_content_type()
            if content_type in ['text/plain', 'text/html']:
                charset = part.get_content_charset() or 'utf-8'
                text = part.get_payload(decode=True).decode(charset, errors='replace')
                text_parts.append(text)
    else:
        # Для не multipart сообщений сразу читаем содержимое
        charset = email_message.get_content_charset() or 'utf-8'
        text_parts.append(email_message.get_payload(decode=True).decode(charset, errors='replace'))

    return '\n'.join(text_parts)

# Функция для обработки строки, аналогичная вашей предыдущей
def process_line(line):
    line = re.sub(r"(\d{2}:\d{2})(\w)", r"\1;\2", line)
    line = re.sub(r"(\d{2}\.\d{2}\.\d{4})", r";\1", line)
    return line

# Функция для обработки всех .eml файлов в папке
def process_eml_files_in_folder(folder_path, output_csv):
    with open(output_csv, mode='w', newline='', encoding='utf-8-sig') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_NONE, escapechar='\\')

        for file_name in os.listdir(folder_path):
            if file_name.endswith('.eml'):
                file_path = os.path.join(folder_path, file_name)
                content = parse_eml(file_path)
                modified_content = process_line(content)
                row_data = modified_content.split(';')
                csv_writer.writerow(row_data)

current_folder_path = os.path.dirname(os.path.abspath(__file__))
output_csv = os.path.join(current_folder_path, 'output_utf8.csv')
process_eml_files_in_folder(current_folder_path, output_csv)
print(current_folder_path, output_csv, 'Обработано')