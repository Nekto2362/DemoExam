import psycopg2
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter import *
from PIL import Image, ImageTk
import os
import time
import connect_bd  # импортируем наши функции работы с БД

def add_tovar(parent):
    add_win = tk.Toplevel(parent)
    add_win.title("ООО «Обувь» Добавление Товара")
    add_win.geometry("600x700")
    add_win.resizable(False, False)
    icon = PhotoImage(file = "import/Icon.png")
    add_win.iconphoto(False, icon)

    style = ttk.Style()
    style.configure('TLabel', font=('Times New Roman', 10))
    style.configure('TButton', font=('Times New Roman', 10))

    # --- Переменные для полей ввода ---
    artikul_var = tk.StringVar()
    name_var = tk.StringVar()
    category_var = tk.StringVar()
    manufacturer_var = tk.StringVar()
    postavshchik_var = tk.StringVar()
    price_var = tk.StringVar()
    unit_var = tk.StringVar()
    quantity_var = tk.StringVar()
    discount_var = tk.StringVar()
    photo_path_var = tk.StringVar()          # временный путь к выбранному файлу
    description_text = None                   # будет создан позже

    # --- Получаем списки для выпадающих списков ---
    categories = connect_bd.get_categories()
    manufacturers = connect_bd.get_manufacturers()

    # --- Создание виджетов ---
    row = 0

    # Артикул (добавлено для идентификации, хотя явно не указано в задании)
    ttk.Label(add_win, text="Артикул:").grid(row=row, column=0, sticky='w', padx=5, pady=5)
    ttk.Entry(add_win, textvariable=artikul_var).grid(row=row, column=1, sticky='ew', padx=5, pady=5)
    row += 1

    # Наименование товара
    ttk.Label(add_win, text="Наименование товара:").grid(row=row, column=0, sticky='w', padx=5, pady=5)
    ttk.Entry(add_win, textvariable=name_var).grid(row=row, column=1, sticky='ew', padx=5, pady=5)
    row += 1

    # Категория товара (выпадающий список)
    ttk.Label(add_win, text="Категория товара:").grid(row=row, column=0, sticky='w', padx=5, pady=5)
    category_combo = ttk.Combobox(add_win, textvariable=category_var, values=categories, state='readonly')
    category_combo.grid(row=row, column=1, sticky='ew', padx=5, pady=5)
    row += 1

    # Описание товара (многострочное)
    ttk.Label(add_win, text="Описание товара:").grid(row=row, column=0, sticky='nw', padx=5, pady=5)
    description_text = tk.Text(add_win, height=4, width=30)
    description_text.grid(row=row, column=1, sticky='ew', padx=5, pady=5)
    row += 1

    # Производитель (выпадающий список)
    ttk.Label(add_win, text="Производитель:").grid(row=row, column=0, sticky='w', padx=5, pady=5)
    manufacturer_combo = ttk.Combobox(add_win, textvariable=manufacturer_var, values=manufacturers, state='readonly')
    manufacturer_combo.grid(row=row, column=1, sticky='ew', padx=5, pady=5)
    row += 1

    # Поставщик
    ttk.Label(add_win, text="Поставщик:").grid(row=row, column=0, sticky='w', padx=5, pady=5)
    ttk.Entry(add_win, textvariable=postavshchik_var).grid(row=row, column=1, sticky='ew', padx=5, pady=5)
    row += 1

    # Цена (может содержать сотые)
    ttk.Label(add_win, text="Цена:").grid(row=row, column=0, sticky='w', padx=5, pady=5)
    ttk.Entry(add_win, textvariable=price_var).grid(row=row, column=1, sticky='ew', padx=5, pady=5)
    row += 1

    # Единица измерения
    ttk.Label(add_win, text="Единица измерения:").grid(row=row, column=0, sticky='w', padx=5, pady=5)
    unit_combo = ttk.Combobox(add_win, textvariable=unit_var, values=['шт.', 'пара'], state='readonly')
    unit_combo.grid(row=row, column=1, sticky='ew', padx=5, pady=5)
    row += 1

    # Количество на складе (целое неотрицательное)
    ttk.Label(add_win, text="Количество на складе:").grid(row=row, column=0, sticky='w', padx=5, pady=5)
    ttk.Entry(add_win, textvariable=quantity_var).grid(row=row, column=1, sticky='ew', padx=5, pady=5)
    row += 1

    # Действующая скидка (%)
    ttk.Label(add_win, text="Действующая скидка (%):").grid(row=row, column=0, sticky='w', padx=5, pady=5)
    ttk.Entry(add_win, textvariable=discount_var).grid(row=row, column=1, sticky='ew', padx=5, pady=5)
    row += 1

    # --- Фото товара ---
    ttk.Label(add_win, text="Фото товара:").grid(row=row, column=0, sticky='nw', padx=5, pady=5)
    photo_label = ttk.Label(add_win, text="Загрузите фото")
    photo_label.grid(row=row, column=1, padx=5, pady=5)

    # Функция показа заглушки
    def show_placeholder():
        try:
            placeholder = "picture.png"
            if os.path.exists(placeholder):
                img = Image.open(placeholder)
                img = img.resize((300, 200), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                photo_label.config(image=photo, text='')
                photo_label.image = photo
            else:
                photo_label.config(text="picture.png не найден")
        except Exception as e:
            photo_label.config(text="Ошибка заглушки")

    # Функция загрузки изображения
    def load_image():
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")])
        if file_path:
            try:
                img = Image.open(file_path)
                img = img.resize((300, 200), Image.LANCZOS)   # приводим к требуемому размеру
                photo = ImageTk.PhotoImage(img)
                photo_label.config(image=photo, text='')
                photo_label.image = photo
                photo_path_var.set(file_path)                 # запоминаем исходный путь
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить изображение:\n{e}")
        else:
            show_placeholder()   # если отмена, показываем заглушку

    btn_load = ttk.Button(add_win, text="Загрузить фото", command=load_image)
    btn_load.grid(row=row, column=2, padx=5, pady=5)

    # Показываем заглушку при запуске
    show_placeholder()
    row += 1

    # --- Кнопки управления ---
    btn_frame = ttk.Frame(add_win)
    btn_frame.grid(row=row, column=0, columnspan=3, pady=10)

    def save_tovar():
        # Сбор данных
        artikul = artikul_var.get().strip()
        name = name_var.get().strip()
        category = category_var.get().strip()
        description = description_text.get("1.0", tk.END).strip()
        manufacturer = manufacturer_var.get().strip()
        postavshchik = postavshchik_var.get().strip()
        price_str = price_var.get().strip()
        unit = unit_var.get().strip()
        quantity_str = quantity_var.get().strip()
        discount_str = discount_var.get().strip()

        # Валидация числовых полей
        try:
            price = float(price_str)
            if price < 0:
                messagebox.showerror("Ошибка", "Цена не может быть отрицательной")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Цена должна быть числом (можно с сотыми)")
            return

        try:
            quantity = int(quantity_str)
            if quantity < 0:
                messagebox.showerror("Ошибка", "Количество не может быть отрицательным")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Количество должно быть целым числом")
            return

        try:
            discount = int(discount_str)
            if discount < 0:
                messagebox.showerror("Ошибка", "Скидка не может быть отрицательной")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Скидка должна быть целым числом")
            return

        # --- Обработка фото ---
        photo_db_path = None
        selected_photo = photo_path_var.get()
        if selected_photo:
            # Создаём папку для изображений, если её нет
            if not os.path.exists("images"):
                os.makedirs("images")
            # Генерируем имя файла: артикул + временная метка (для уникальности)
            ext = os.path.splitext(selected_photo)[1]
            filename = f"{artikul}_{int(time.time())}{ext}"
            dest_path = os.path.join("images", filename)
            try:
                # Открываем, изменяем размер и сохраняем
                img = Image.open(selected_photo)
                img = img.resize((300, 200), Image.LANCZOS)
                img.save(dest_path)
                photo_db_path = dest_path   # относительный путь для БД
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить изображение:\n{e}")
                return
        # Если фото не выбрано, в БД пойдёт NULL

        # --- Вставка в БД ---
        success, msg = connect_bd.insert_tovar(
            artikul, name, unit, price, postavshchik,
            manufacturer, category, discount, quantity,
            description, photo_db_path
        )
        if success:
            messagebox.showinfo("Успех", "Товар успешно добавлен")
            add_win.destroy()
        else:
            messagebox.showerror("Ошибка БД", f"Не удалось добавить товар:\n{msg}")

    ttk.Button(btn_frame, text="Сохранить", command=save_tovar).pack(side=tk.LEFT, padx=5)
    ttk.Button(btn_frame, text="Отмена", command=add_win.destroy).pack(side=tk.LEFT, padx=5)

    # Настройка растяжения колонок
    add_win.columnconfigure(1, weight=1)

    add_win.grab_set()
    parent.wait_window(add_win)

    return add_win