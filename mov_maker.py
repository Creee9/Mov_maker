import os
import subprocess

FOLDER_PATH = "Путь_до_материалов"


def find_jpg_files(directory: str) -> list[str]:
    """
    Функция для нахождения всех jpg файлов в папке и подпапках.

    :param directory: путь до рабочей директории
    :return: список всех путей до найденных jpg-файлов
    """

    jpg_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".jpg"):
                jpg_files.append(os.path.join(root, file))

    return jpg_files


def create_a_folder(directory: str) -> str:
    """
    Функция для создания папки.

    :param directory: путь до рабочей директории
    :return: путь директории, куда будут сохранены mov-файлы
    """

    output_folder = os.path.join(directory, "output_videos")
    os.makedirs(output_folder, exist_ok=True)

    return output_folder


def create_a_mov_files():
    """
    Функция для создания mov-файлов из jpg-файлов.

    # 1 - Список всех путей файлов.
    # 2 - Извлекаем имя файла.
    # 3 - Раскомментировать в случае наличия копий jpg-файлов.
    # 4 - Блок кода, отвечающий за поиск индекса сеппаратора.
    # 5 - Сеппаратор имени секвенции и номера фрейма (Например, ' ', '.', '_').
    # 6 - Чем выше значение -b:v (25М), тем тяжелее mov-файл
          и выше качество изображения.
    """

    jpg_files = find_jpg_files(FOLDER_PATH)  # 1
    jpg_files.sort()

    for jpg_file in jpg_files:
        filename = os.path.splitext(os.path.basename(jpg_file))[0]  # 2

        # if not filename[-1].isdigit():  # 3
        #     continue

        sep_index = -1
        for char in filename[::-1]:  # 4
            if char.isdigit():
                sep_index -= 1
            else:
                break
        separator = filename[sep_index]  # 5
        sequence_name = filename[:sep_index]
        frame_number = filename[sep_index + 1:]
        path_with_seq_name = os.path.join(
            os.path.dirname(jpg_file),
            sequence_name
        )
        output_file = os.path.join(
            create_a_folder(FOLDER_PATH),
            f"{sequence_name}.mov"
        )

        cmd = (
            f'ffmpeg -framerate 24 -start_number {frame_number} '
            f'-i "{path_with_seq_name}{separator}%{len(frame_number)}d.jpg"'
            f' -c:v mjpeg -b:v 25M "{output_file}"'  # 6
        )
        if not os.path.exists(output_file):
            subprocess.run(cmd, shell=True)


if __name__ == "__main__":
    create_a_mov_files()
