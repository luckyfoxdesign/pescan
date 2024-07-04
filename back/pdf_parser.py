import pdfplumber
import logging
import csv
import utils
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def group_columns_by_table(metadata):
    """
    Группирует метаданные колонок по таблицам.

    :param metadata: список кортежей с метаданными колонок
    :return: словарь, где ключ - имя таблицы, значение - список описаний колонок
    """
    tables = {}
    for table_name, column_name, description in metadata:
        if table_name not in tables:
            tables[table_name] = []
        tables[table_name].append(utils.clean_text(description) if description else "")
    return tables


# def group_columns_by_table(metadata):
#     grouped_columns = {}
#     for row in metadata:
#         if len(row) == 3:
#             table_name, column_name, description = row
#             if table_name not in grouped_columns:
#                 grouped_columns[table_name] = []
#             grouped_columns[table_name].append((column_name, description))
#         else:
#             raise ValueError("Expected 3 values in metadata tuple, got {}".format(len(row)))
#     return grouped_columns

def normalize_headers(headers):
    """
    Нормализует заголовки таблиц.

    :param headers: список заголовков
    :return: нормализованный список заголовков
    """
    new_headers = [[utils.clean_text(col) if col else "" for col in header] for header in headers]
    return new_headers

def calculate_jaccard_score(list1, list2):
    """
    Вычисляет коэффициент Жаккара между двумя списками.

    :param list1: первый список
    :param list2: второй список
    :return: коэффициент Жаккара
    """
    set1 = set(list1)
    set2 = set(list2)
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    return len(intersection) / len(union) if len(union) > 0 else 0

def extract_tables_from_pdf(pdf, page_number):
    """
    Извлекает таблицы из PDF-файла на указанной странице.

    :param pdf_path: путь к PDF-файлу
    :param page_number: номер страницы
    :return: список таблиц
    """
    # with pdfplumber.open(pdf_path) as pdf:
    #     page = pdf.pages[page_number - 1]
    #     tables = page.extract_tables()
    #     return tables if tables else None

    page = pdf.pages[page_number - 1]
    tables = page.extract_tables()
    return tables if tables else None

def save_table_to_csv(header, data, output_path):
    """
    Сохраняет таблицу в CSV файл.

    :param header: заголовок таблицы
    :param data: данные таблицы
    :param output_path: путь для сохранения CSV файла
    """
    with open(output_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(data)

def save_results_to_csv(results, output_path):
    """
    Сохраняет результаты в CSV файл.

    :param results: список словарей с результатами
    :param output_path: путь для сохранения CSV файла
    """
    keys = results[0].keys()
    with open(output_path, mode='w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(results)

def extract_table_headers(tables):
    """
    Извлекает заголовки таблиц.

    :param tables: список таблиц
    :return: список заголовков
    """
    return [table[0] for table in tables]

def match_tables_with_metadata(tables, grouped_columns):
    """
    Сопоставляет таблицы из PDF с метаданными из базы данных.

    :param tables: список таблиц из PDF
    :param grouped_columns: сгруппированные метаданные колонок
    :return: список результатов и список совпадающих таблиц
    """
    headers = extract_table_headers(tables)
    normalized_headers = normalize_headers(headers)
    
    results = []
    matched_tables = []
    for table_name, db_headers in grouped_columns.items():
        for idx, pdf_header in enumerate(normalized_headers):
            match_percentage = calculate_jaccard_score(pdf_header, db_headers)
            if match_percentage > 0:
                results.append({
                    "pdf_table": f"pdf_table_{idx + 1}.csv",
                    "db_table": f"{table_name}",
                    "similarity": f"{match_percentage * 100:.2f}%"
                })
                matched_tables.append((table_name, idx, tables[idx]))
    return results, matched_tables

def extract_text_as_paragraphs(pdf):
    paragraphs = []
    current_paragraph = ""

    for page in pdf.pages:
        text = page.extract_text()
        if text:
            lines = text.split('\n')
            for line in lines:
                if line.strip():  # если строка не пустая
                    current_paragraph += " " + line.strip()
                else:
                    if current_paragraph:  # если текущий параграф не пуст
                        paragraphs.append(current_paragraph.strip())
                        current_paragraph = ""
    
    # Добавляем последний параграф, если он не пуст
    if current_paragraph:
        paragraphs.append(current_paragraph.strip())

    return paragraphs

def save_matched_tables_and_results(results, matched_tables): #path
    """
    Сохраняет совпадающие таблицы и результаты в CSV файлы и возвращает данные в формате DataFrame.

    :param results: список результатов
    :param matched_tables: список совпадающих таблиц
    :return: результаты в формате DataFrame и совпадающие таблицы в формате DataFrame
    """
    # results_df = pd.DataFrame(results)
    # results_df.to_csv("similarity_results.csv", index=False)

    matched_tables_dfs = {}
    for table_name, table_index, table in matched_tables:
        header = table[0]
        data = table[1:]
        df = pd.DataFrame(data, columns=header)
        # csv_output_path = f"./res/{table_name}.csv"
        # df.to_csv(csv_output_path, index=False)
        matched_tables_dfs[table_name] = df

    # return results_df, matched_tables_dfs   
    return matched_tables_dfs   

def process(pdf, db_columns_metadata):
    """
    Основная функция, которая выполняет все шаги от извлечения метаданных до сохранения результатов.

    :param pdf_path: путь к PDF-файлу
    :param page_number: номер страницы для обработки
    :return: результаты и совпадающие таблицы
    """
    page_number = 0

    grouped_columns = group_columns_by_table(db_columns_metadata)
    tables = extract_tables_from_pdf(pdf, page_number)

    if tables:
        results, matched_tables = match_tables_with_metadata(tables, grouped_columns)
        
        # logger.info(results)
        
        mtd = save_matched_tables_and_results(results, matched_tables)
        
        # logger.info("\n\n\n---------\n\n\n")
        return mtd
    else:
        logger.info(f"Не удалось найти таблицы на странице {page_number}")
    
    return None