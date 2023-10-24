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
        if os.path.exists(f'{folder.value}\\zips'):
            shutil.rmtree(f'{folder.value}\\zips')
            os.mkdir(f'{folder.value}\\zips')
        else:
            os.mkdir(f'{folder.value}\\zips')
        column.visible = True
        donetext.visible = False
        allsize1, allsize2 = 0, 0
        count1, count2 = 1, 1
        total_size = 0
        current_size = 0
        zip1 = zipfile.ZipFile(f'{folder.value}\\zips\\IT ({count1}).zip', 'w')
        zip2 = zipfile.ZipFile(f'{folder.value}\\zips\\Левитская ({count2}).zip', 'w')

        for file in os.listdir(folder.value):
            if file[-3:] == "pdf":
                total_size += os.path.getsize(f'{folder.value}\\{file}')

        for file in os.listdir(folder.value):
            if file[-3:] == "pdf":
                current_size += os.path.getsize(f'{folder.value}\\zips\\IT ({count1}).zip')
                current_size += os.path.getsize(f'{folder.value}\\zips\\Левитская ({count2}).zip')
                percent = current_size / total_size
                pb.value = percent
                page.update()
                if '-Л_' not in file:
                    size1 = os.path.getsize(f'{folder.value}\\{file}')
                    allsize1 += size1
                    if allsize1 < 600000000:
                        zip1.write(f'{folder.value}\\{file}', os.path.basename(f'{folder.value}\\{file}'))
                    else:
                        count1 += 1
                        zip1.close()
                if '-Л_' in file:
                    size2 = os.path.getsize(f'{folder.value}\\{file}')
                    allsize2 += size2
                    if allsize1 < 600000000:
                        zip2.write(f'{folder.value}\\{file}', os.path.basename(f'{folder.value}\\{file}'))
                    else:
                        count2 += 1
                        zip2.close()

        page.add(donetext)
        column.visible = False
        donetext.visible = True
        page.update()

    page.theme = theme.Theme(color_scheme_seed="orange")
    page.update()
    page.window_width = 500
    page.window_height = 500
    column.visible = False
    donetext.visible = False
    page.add(
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
