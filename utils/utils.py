import re

def extract_filename_substring(input_string):
    # Шаблон для имени файла: допустим, это имя файла с расширением
    pattern = r'\b\w+\.\w+\b'
    
    # Поиск совпадений в строке
    match = re.search(pattern, input_string)
    
    if match:
        return match.group(0)  # Возвращаем найденное имя файла
    else:
        return None  # Если совпадений нет, возвращаем None

# # Пример использования
# input_str = "Путь к файлу: /папка/файл_пример.txt"
# result = extract_filename_substring(input_str)
# print(result)  # Выведет: файл_пример.txt
