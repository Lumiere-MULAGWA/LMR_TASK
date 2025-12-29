import flet as ft
import json
import os

TASKS_FILE = "tasks.json"


def main(page: ft.Page):
    # Configuration de la fenêtre
    page.title = "Ma To-Do List Moderne"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 450
    page.window_height = 600

    new_task = ft.TextField(hint_text="Qu'avez-vous à faire ?", expand=True)
    tasks_view = ft.Column(scroll=ft.ScrollMode.AUTO)

    # -------------------------
    # GESTION DU FICHIER
    # -------------------------

    def save_tasks():
        tasks = []
        for row in tasks_view.controls:
            checkbox = row.controls[0]
            tasks.append({
                "label": checkbox.label,
                "checked": checkbox.value
            })
        with open(TASKS_FILE, "w", encoding="utf-8") as f:
            json.dump(tasks, f, ensure_ascii=False, indent=4)

    def load_tasks():
        if not os.path.exists(TASKS_FILE):
            return

        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            tasks = json.load(f)

        for task in tasks:
            create_task(task["label"], task["checked"])

    # -------------------------
    # FONCTIONS UI
    # -------------------------

    def delete_task(task_row):
        tasks_view.controls.remove(task_row)
        save_tasks()
        page.update()

    def create_task(label, checked=False):
        checkbox = ft.Checkbox(
            label=label,
            value=checked,
            check_color="white",
            on_change=lambda _: save_tasks()
        )

        task_row = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                checkbox,
                ft.IconButton(
                    icon=ft.Icons.DELETE_OUTLINE,
                    icon_color="red700",
                    on_click=lambda _: delete_task(task_row)
                ),
            ],
        )
        tasks_view.controls.append(task_row)

    def add_clicked(e):
        if new_task.value.strip() == "":
            return

        create_task(new_task.value)
        new_task.value = ""
        save_tasks()
        page.update()

    # -------------------------
    # UI
    # -------------------------

    page.add(
        ft.Text("Mes Tâches 2025", size=30, weight=ft.FontWeight.BOLD, color="blueaccent"),
        ft.Row(
            controls=[
                new_task,
                ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=add_clicked),
            ],
        ),
        ft.Divider(height=20, thickness=1),
        tasks_view
    )

    # Charger les tâches sauvegardées
    load_tasks()
    page.update()


if __name__ == "__main__":
    ft.app(target=main)
