def determine_type(data):

    try:
        int(data)
        return int
    except ValueError:
        pass

    try:
        float(data)
        return float
    except ValueError:
        pass

    if data.lower() in ("да", "нет"):
        return bool
    else:
        return str

questions = [
    "Введите название вакансии:",
    "Введите описание вакансии:",
    "Введите город для вакансии:",
    "Введите требуемый опыт работы (лет):",
    "Введите нижнюю границу оклада вакансии:",
    "Введите верхнюю границу оклада вакансии:",
    "Нужен свободный график (да / нет):",
    "Является ли данная вакансия премиум-вакансией (да / нет):"
]

data = []

for question in questions:
    user_input = input(question + " ")
    data.append(user_input)

for i, item in enumerate(data):
    item_type = type(item).__name__  # Если правильно понял замечание
    if item_type == "str" and item.lower() == "да":
        print(f"True (bool)")
    elif item_type == "str" and item.lower() == "нет":
        print(f"False (bool)")
    else:
        print(f"{item} ({item_type})")