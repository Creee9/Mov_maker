import os
import subprocess
from pprint import pprint


# Функция для нахождения всех jpg файлов в папке и подпапках
def find_jpg_files(directory):
    jpg_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".jpg"):
                jpg_files.append(os.path.join(root, file))
    # pprint(jpg_files)
    return jpg_files


# Путь до папки с материалами
folder_path = "C:\\Dev\\Test"
# folder_path = "C:\Dev\Algous Studio\source"

# Находим все jpg файлы
jpg_files = find_jpg_files(folder_path)
# # pprint(jpg_files)

# Создаем отдельную папку для сохранения видео файлов
output_folder = os.path.join(folder_path, "output_videos")
os.makedirs(output_folder, exist_ok=True)

# Создаем mov файлы из секвенций jpg файлов
for jpg_file in jpg_files:
    # pprint(jpg_file)
    filename = os.path.splitext(os.path.basename(jpg_file))[0]
    # pprint(filename)
    if not filename[-1].isdigit():
        continue
    index = -1
    for char in filename[::-1]:
        if char.isdigit():
            index -= 1
        else:
            break
    separator = filename[index]
    # pprint(separator)
    # pprint(filename)

    sequence_name, frame_numbers = filename[:index], filename[index + 1:]

    output_file = os.path.join(output_folder, f"{sequence_name}.mov")

    if not os.path.exists(output_file):
        subprocess.run(f'ffmpeg -framerate 24 -start_number {frame_numbers} -i "{os.path.join(os.path.dirname(jpg_file), sequence_name)}{separator}%{len(frame_numbers)}d.jpg" -c:v mjpeg "{output_file}"', shell=True)

print("Mov файлы успешно созданы и сохранены в папке output_videos.")
