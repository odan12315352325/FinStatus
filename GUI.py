import customtkinter as ctk
from tkinter import messagebox, ttk
import pandas as pd
import numpy as np
import random
from keras.models import load_model
from sklearn.preprocessing import StandardScaler

model = load_model('financial_model.h5')

scaler = StandardScaler()
scaler.fit(X)

data = pd.read_csv('./dataINN.csv', delimiter=';')

data.iloc[:, 0] = data.iloc[:, 0].astype(str)
data.iloc[:, 1] = data.iloc[:, 1].astype(str)

def set_placeholder(entry, text):
    entry.insert(0, text)
    entry.configure(text_color='grey')
    entry.bind("<FocusIn>", lambda event: clear_placeholder(entry, text))
    entry.bind("<FocusOut>", lambda event: restore_placeholder(entry, text))

def clear_placeholder(entry, text):
    if entry.get() == text:
        entry.delete(0, ctk.END)
        entry.configure(text_color='white')

def restore_placeholder(entry, text):
    if not entry.get():
        entry.insert(0, text)
        entry.configure(text_color='grey')

def validate_numeric(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def validate_inn(inn):
    return inn.isdigit() and len(inn) == 10

def validate_year(year):
    return year.isdigit() and len(year) == 4

def predict():
    input_data = []
    for entry in entries:
        value = entry.get()
        if value.startswith("x") or not validate_numeric(value):
            messagebox.showerror("Ошибка!", "Все поля должны быть заполнены и содержать только числовые значения!")
            return
        input_data.append(float(value))

    input_data = np.array(input_data).reshape(1, -1)
    input_data_scaled = scaler.transform(input_data)
    regression_output, classification_output = model.predict(input_data_scaled)
    
    result_window = ctk.CTkToplevel(root)
    result_window.title("Результаты")
    
    prediction_labels = [
        "Оценка региональной и отраслевой специфики (Reg)", 
        "Оценка кредитоспособности (Kredit)", 
        "Оценка технической оснащенности (Teh)", 
        "Оценка рыночного потенциала (Market)", 
        "Качество кадрового обеспечения (Staff)", 
        "Оценка морально-психологического климата (Psich)", 
        "Оценка ликвидности (Ability)", 
        "Оценка показателей оборачиваемости (Turn)", 
        "Оценка финансовой устойчивости (Finn)", 
        "Интегральный показатель финансовой устойчивости по 25 переменным (Z25)", 
        "Интегральный показатель финансовой устойчивости по 35 переменным (Z35)"
    ]
    
    results_frame = ctk.CTkFrame(result_window)
    results_frame.pack(anchor='w', padx=20, pady=20)
    
    for i, value in enumerate(regression_output[0]):
        result_label = ctk.CTkLabel(results_frame, text=f"{prediction_labels[i]}: ", font=("Bahnschrift", 24))
        result_label.grid(row=i, column=0, sticky='w', padx=10, pady=2)
        value_label = ctk.CTkLabel(results_frame, text=f"{value:.2f}", font=("Bahnschrift", 28, "bold"))
        value_label.grid(row=i, column=1, sticky='w', padx=10, pady=2)
        
    risk_text = 'высокий риск банкротства' if classification_output[0][0] > 0.5 else 'низкий риск банкротства'
    risk_color = 'red' if classification_output[0][0] > 0.5 else 'green'
    risk_label = ctk.CTkLabel(result_window, text=f"Вероятность банкротства: {risk_text}", font=("Bahnschrift", 28, "bold"), text_color=risk_color)
    risk_label.pack(anchor='w', pady=10, padx=20)

def search_inn_year():
    inn = inn_entry.get().strip()
    year = year_entry.get().strip()
    if not validate_inn(inn):
        messagebox.showerror("Ошибка!", "ИНН должен содержать 10 цифр!")
        return
    if year and not validate_year(year):
        messagebox.showerror("Ошибка!", "Год должен содержать 4 цифры!")
        return

    print(f"Поиск ИНН: {inn}, год: {year}")
    
    if year:
        row = data[(data.iloc[:, 0] == inn) & (data.iloc[:, 1] == year)]
    else:
        row = data[data.iloc[:, 0] == inn].head(1)

    print(f"Найденные строки: {row}")
    
    if row.empty:
        messagebox.showerror("Ошибка!", "Данные для указанного ИНН и года не найдены!")
        return

    values = row.iloc[0, 2:].values
    for i, value in enumerate(values):
        entries[i].delete(0, ctk.END)
        entries[i].insert(0, str(value))
        entries[i].configure(text_color='white')

def random_inn():
    inn = random.choice(data.iloc[:, 0].values)
    inn_entry.delete(0, ctk.END)
    inn_entry.insert(0, inn)
    inn_entry.configure(text_color='white')

root = ctk.CTk()
root.title("Анализ финансового состояния предприятия")

search_frame = ctk.CTkFrame(root)
search_frame.pack(side=ctk.RIGHT, padx=10, pady=10)

inn_label = ctk.CTkLabel(search_frame, text="Поиск по ИНН:", font=("Bahnschrift", 20))
inn_label.pack(anchor='w', pady=2)

inn_entry = ctk.CTkEntry(search_frame, font=("Bahnschrift", 18))
inn_entry.pack(anchor='w', pady=2)

year_label = ctk.CTkLabel(search_frame, text="Поиск по году:", font=("Bahnschrift", 20))
year_label.pack(anchor='w', pady=2)


tab_control = ttk.Notebook(root)

categories = [
    ("Регион. и отрасл. специфика", 5),
    ("Кредитная история", 4),
    ("Техн. оснащенность", 3),
    ("Рыночный потенциал", 5),
    ("Кадровое обеспечение", 7),
    ("Платежеспособность", 6),
    ("Рентабельность", 5)
]

field_labels = [
    "Уровень конкуренции в отрасли региона", "Концентрация отраслевых рисков в регионе", 
    "Доля отрасли, в которой функционирует предприятие в ВРП", "Экономическая ситуация в регионе", 
    "Влияние региональных и макроэкономических рисков", "Качество (наличие/отсутствие) кредитной истории", 
    "Количество полученных кредитов (займов) у предприятия", "Залогоспособность", 
    "Срок функционирования предприятия в регионе", "Коэффициент парка наличного оборудования", 
    "Коэффициент парка установленного оборудования", "Коэффициент интенсивности загрузки оборудования", 
    "Коэффициент выполнения плана (по валовой продукции)", "Оценка средне реализуемых цен предприятия по отрасли", 
    "Удельный вес новой продукции (услуги) в общем выпуске", "Доля крупнейшего поставщика в себестоимости продукции(услуги)", 
    "Доля крупнейшего покупателя в выручке от реализации продукции", 
    "Удельный вес наиболее трудоспособного и квалифицированного персонала", "Общий коэффициент кадрового обеспечения", 
    "Уровень квалификации сотрудников предприятия", "Индекс роста квалификации", 
    "Квалификация кадрового состава в области финансового менеджмента", "Коэффициент текучести кадров", 
    "Обратный коэффициент Кейтца", "Коэффициент текущей ликвидности", 
    "Коэффициент обеспеченности собственными оборотными средствами", "Период оборачиваемости дебиторской задолженности", 
    "Период оборачиваемости кредиторской задолженности", "Отношение периодов оборачиваемости задолженности", 
    "Период оборачиваемости остатков готовой продукции", "Коэффициент финансовой активности", 
    "Коэффициент финансовой независимости", "Коэффициент обеспеченности материальных запасов собственными средствами", 
    "Общая рентабельность", "Коэффициент рентабельности продаж"
]

entries = []
label_index = 0

for category, num_fields in categories:
    tab = ctk.CTkFrame(tab_control)
    tab_control.add(tab, text=category)
    
    for i in range(num_fields):
        label = ctk.CTkLabel(tab, text=f"{label_index + 1}. {field_labels[label_index]}", font=("Bahnschrift", 18))
        label.pack(anchor='w', padx=10, pady=2)
        entry = ctk.CTkEntry(tab, font=("Bahnschrift", 18))
        set_placeholder(entry, f"x{label_index + 1}")
        entry.pack(anchor='w', padx=10, pady=2)
        entries.append(entry)
        label_index += 1

tab_control.pack(expand=1, fill='both')


analyze_button = ctk.CTkButton(root, text="Анализ", command=predict, font=("Bahnschrift", 22, "bold"))
analyze_button.pack(pady=20)

root.mainloop()