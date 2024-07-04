import re
import pandas as pd
import os

def save_to_sql(file_path, sql):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(sql)

def transform_date(date_str):
    if not isinstance(date_str, str):
        print(f"Значение не строка: {date_str}")
        return None
    
    # Проверка на формат "MM.YYYY"
    if re.match(r'^\d{1,2}\.\d{4}$', date_str):
        date_str = '01.' + date_str  # Добавляем день "01"
        # print(f"Формат MM.YYYY: преобразуем {date_str}")
        try:
            date_obj = pd.to_datetime(date_str, format='%d.%m.%Y')
            return date_obj.strftime('%Y-%m-%d')
        except ValueError:
            print(f"Ошибка преобразования даты: {date_str}")
            return None
    
    # Проверка на формат "DD.MM.YY"
    if re.match(r'^\d{1,2}\.\d{1,2}\.\d{2}$', date_str):
        # print(f"Формат DD.MM.YY: преобразуем {date_str}")
        try:
            date_obj = pd.to_datetime(date_str, format='%d.%m.%y')
            return date_obj.strftime('%Y-%m-%d')
        except ValueError:
            print(f"Ошибка преобразования даты: {date_str}")
            return None
    
    # Проверка на формат "DD.MM.YYYY"
    if re.match(r'^\d{1,2}\.\d{1,2}\.\d{4}$', date_str):
        # print(f"Формат DD.MM.YYYY: преобразуем {date_str}")
        try:
            date_obj = pd.to_datetime(date_str, format='%d.%m.%Y')
            return date_obj.strftime('%Y-%m-%d')
        except ValueError:
            print(f"Ошибка преобразования даты: {date_str}")
            return None
    
    # Если формат не соответствует ни одному из вышеуказанных
    print(f"Неверный формат даты: {date_str}")
    return None


def clean_text(text):
    """
    Очищает текст от знаков препинания и специальных символов, а также удаляет пробелы в начале и в конце строки.

    :param text: исходный текст
    :return: очищенный текст
    """
    text = text.lower().strip()
    text = text.replace("\n", " ")
    # text = re.sub(r'[^\w\s]', '', text)
    return text

def csv_normalize_columns_names(df):
    df.columns = [clean_string(str(col)) for col in df.columns]
    return df

def clean_string(s):
    return re.sub(r'[^a-zA-Zа-яА-ЯёЁ]', '', s).lower()

# не подошел тк удалять значения из шапки не нужно тк это может повлиять на отображения таблицы
# def remove_empty_values(array_of_arrays):
#     """
#     Удаляет все пустые значения из массива массивов и удаляет пустые массивы.

#     :param array_of_arrays: исходный массив массивов
#     :return: массив массивов без пустых значений и пустых массивов
#     """
#     # Удаление пустых значений из вложенных массивов
#     cleaned_array_of_arrays = [[value for value in subarray if value != ''] for subarray in array_of_arrays]
#     # Удаление пустых массивов
#     cleaned_array_of_arrays = [subarray for subarray in cleaned_array_of_arrays if subarray]
#     return cleaned_array_of_arrays


# Не подошел тк процент сходства почему-то показывает меньше
# def calculate_jaccard_score(list1, list2):
#     """
#     Вычисляет коэффициент Жаккара между двумя списками с использованием scikit-learn.

#     :param list1: первый список
#     :param list2: второй список
#     :return: коэффициент Жаккара
#     """
#     # Преобразуем списки в строки для использования CountVectorizer
#     str1 = ' '.join(list1)
#     str2 = ' '.join(list2)

#     # Преобразуем строки в бинарные вектора
#     vectorizer = CountVectorizer(binary=True)
#     X = vectorizer.fit_transform([str1, str2]).toarray()
    
#     # Вычисляем коэффициент Жаккара
#     return jaccard_score(X[0], X[1])