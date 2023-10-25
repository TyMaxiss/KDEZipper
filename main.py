import shutil

import flet as ft
import tkinter as tk
from tkinter import filedialog
import os
import sys
import zipfile
from pathlib import Path

from flet_core import Theme, theme


def main(page: ft.Page):
    folder = ft.Text()
    folder.value = ''
    pb = ft.ProgressBar(width=400)
    column = ft.Column([ft.Text("Выполняется..."), pb])
    donetext = ft.Text("Готово!")

    def pick_folder_result(e):
        folder.value = (filedialog.askdirectory())
        folder.update()

    def start(e):
        if folder.value == '' or folder.value == 'Вы не выбрали папку!':
            folder.value = 'Вы не выбрали папку!'
            folder.update()
            return
        column.visible = True
        donetext.visible = False
        if os.path.exists(f'{folder.value}\\zips'):
            shutil.rmtree(f'{folder.value}\\zips')
            os.mkdir(f'{folder.value}\\zips')
        else:
            os.mkdir(f'{folder.value}\\zips')
        count1, count2 = 1, 1
        total_size = 0

        zip1 = zipfile.ZipFile(f'{folder.value}\\zips\\IT ({count1}).zip', 'w')
        zip2 = zipfile.ZipFile(f'{folder.value}\\zips\\Левитская ({count2}).zip', 'w')

        for file in os.listdir(folder.value):
            if file[-3:] == "pdf":
                total_size += os.path.getsize(f'{folder.value}\\{file}') / 1000000

        for file in os.listdir(folder.value):
            if file[-3:] == "pdf":
                current_size = 0
                for sizeAllZips in os.listdir(f'{folder.value}\\zips'):
                    current_size += os.path.getsize(f'{folder.value}\\zips\\{sizeAllZips}') / 1000000
                pb.value = current_size / total_size
                page.update()
                if '-Л_' not in file:
                    allsize1 = os.path.getsize(f'{folder.value}\\zips\\IT ({count1}).zip') / 1000000
                    if (allsize1 + os.path.getsize(f'{folder.value}\\{file}') / 1000000) < int(field.value):
                        zip1.write(f'{folder.value}\\{file}', os.path.basename(f'{folder.value}\\{file}'))
                        current_size += os.path.getsize(f'{folder.value}\\zips\\IT ({count1}).zip') / 1000000
                    else:
                        count1 += 1
                        zip1.close()
                        zip1 = zipfile.ZipFile(f'{folder.value}\\zips\\IT ({count1}).zip', 'w')
                        zip1.write(f'{folder.value}\\{file}', os.path.basename(f'{folder.value}\\{file}'))
                        current_size += os.path.getsize(f'{folder.value}\\zips\\IT ({count1}).zip') / 1000000
                if '-Л_' in file:
                    allsize2 = os.path.getsize(f'{folder.value}\\zips\\Левитская ({count2}).zip') / 1000000
                    if (allsize2 + os.path.getsize(f'{folder.value}\\{file}') / 1000000) < int(field.value):
                        zip2.write(f'{folder.value}\\{file}', os.path.basename(f'{folder.value}\\{file}'))
                        current_size += os.path.getsize(f'{folder.value}\\zips\\Левитская ({count2}).zip') / 1000000
                    else:
                        count2 += 1
                        zip2.close()
                        zip2 = zipfile.ZipFile(f'{folder.value}\\zips\\Левитская ({count2}).zip', 'w')
                        zip2.write(f'{folder.value}\\{file}', os.path.basename(f'{folder.value}\\{file}'))
                        current_size += os.path.getsize(f'{folder.value}\\zips\\Левитская ({count2}).zip') / 1000000

        page.add(donetext)
        column.visible = False
        donetext.visible = True
        page.update()

    page.theme = theme.Theme(color_scheme_seed="orange")
    field = ft.TextField(label="Максимальный вес zip (Mb)", value="600")
    page.update()
    page.window_width = 500
    page.window_height = 500
    column.visible = False
    donetext.visible = False
    page.add(
        ft.Row(
            [
                field
            ]
        ),
        ft.Row(
            [
                ft.ElevatedButton(
                    "Выбрать папку",
                    icon=ft.icons.FOLDER,
                    on_click=pick_folder_result),
                folder
            ]
        ),
        ft.Row(
            [
                ft.ElevatedButton(
                    "Начать",
                    icon=ft.icons.DONE,
                    on_click=start)
            ]
        ),
        ft.Row(
            [
                column
            ]
        ),
        ft.Row(
            [
                donetext
            ]
        )
    )


ft.app(target=main)
