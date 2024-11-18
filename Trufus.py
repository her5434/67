import os
import requests
import tkinter as tk
from tkinter import messagebox, filedialog
import psutil


def list_usb_devices():
    # Получаем список всех подключенных USB-устройств
    devices = []
    for device in psutil.disk_partitions(all=False):
        if 'removable' in device.opts:  # Фильтруем по типу
            devices.append(device.device)
    return devices


def download_linux_distribution(url):
    try:
        # Загружаем файл дистрибутива
        response = requests.get(url, stream=True)
        filename = url.split("/")[-1]
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return filename
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при загрузке: {e}")
        return None


def write_image_to_usb(image_path, usb_device, volume_label):
    try:
        command = f"dd if={image_path} of={usb_device} bs=4M status=progress conv=fdatasync"
        os.system(command)

        if volume_label:
            label_command = f"sudo e2label {usb_device} {volume_label}"

        messagebox.showinfo("Успех", "Запись завершена.")
        os.remove(image_path)  # Удаление образа после записи
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при записи: {e}")


def select_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.img;*.iso")])
    if file_path:
        image_entry.delete(0, tk.END)
        image_entry.insert(0, file_path)


def update_usb_device_list():
    usb_listbox.delete(0, tk.END)
    usb_devices = list_usb_devices()
    for device in usb_devices:
        usb_listbox.insert(tk.END, device)
    count_label.config(text=f"Подключенные устройства: {len(usb_devices)}")


def start_write():
    image_path = image_entry.get()
    choice = usb_listbox.curselection()
    if choice:
        usb_device = usb_devices[choice[0]]
        volume_label = volume_label_entry.get()
        write_image_to_usb(image_path, usb_device, volume_label)
    else:
        messagebox.showwarning("Предупреждение", "Пожалуйста, выберите USB-устройство.")


# Создание основного окна
root = tk.Tk()
root.title("USB Writer")

# Список USB-устройств
usb_devices = list_usb_devices()
usb_listbox = tk.Listbox(root)
for device in usb_devices:
    usb_listbox.insert(tk.END, device)
usb_listbox.pack(pady=10)

# Ввод URL-адреса дистрибутива Linux
url_label = tk.Label(root, text="Введите URL-адрес дистрибутива Linux:")
url_label.pack()
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)
url_entry.insert(0, "http://tinycorelinux.net/15.x/x86/release/TinyCore-current.iso")  # Вставка URL по умолчанию

# Кнопка загрузки дистрибутива
download_button = tk.Button(root, text="Скачать дистр. Linux", command=lambda: download_linux_distribution(url_entry.get()))
download_button.pack(pady=5)

# Кнопка выбора образа
image_button = tk.Button(root, text="Выбрать образ .img/.iso", command=select_image)
image_button.pack(pady=5)

# Поле для отображения пути к образу
image_entry = tk.Entry(root, width=50)
image_entry.pack(pady=5)

# Ввод метки тома
volume_label_label = tk.Label(root, text="Метка тома (опционально):")
volume_label_label.pack()
volume_label_entry = tk.Entry(root, width=50)
volume_label_entry.pack(pady=5)

# Общая информация о подключенных устройствах
count_label = tk.Label(root, text=f"Подключенные устройства: {len(usb_devices)}")
count_label.pack(pady=10)

# Кнопка записи
write_button = tk.Button(root, text="Записать на USB", command=start_write)
write_button.pack(pady=20)

# Кнопка для перехода на сайт для загрузки дистрибутивов
def open_download_website():
    os.system("start https://distrowatch.com/")  # Для Windows, используйте "xdg-open" для Linux

download_button = tk.Button(root, text="Перейти на сайт для загрузки", command=open_download_website)
download_button.pack(pady=5)

# Запуск приложения
root.mainloop()