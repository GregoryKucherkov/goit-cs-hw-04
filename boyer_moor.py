def build_shift_table(pattern):
    table ={}
    length = len(pattern) 

    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    
    table.setdefault(pattern[-1], length)
    
    return table

def boyer_moor_search(text, pattern):
    shift_table = build_shift_table(pattern)
    i = 0

    # Проходимо по основному тексту, порівнюючи з підрядком
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1     # Починаємо з кінця підрядка
        
        # Порівнюємо символи від кінця підрядка до його початку
        while j >= 0 and text[i+j] == pattern[j]:
            j -= 1

            # Якщо весь підрядок збігається, повертаємо його позицію в тексті
        if j < 0:
            return i    # Підрядок знайдено
            
            # Зсуваємо індекс i на основі таблиці зсувів
            # Це дозволяє "перестрибувати" над неспівпадаючими частинами тексту
        
        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

    return -1


if __name__ == '__main__':
    boyer_moor_search()