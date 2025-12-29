import flet as ft
import json
import os

TASKS_FILE = os.path.join(
    os.environ.get("SNAP_USER_DATA", "."),
    "tasks.json"
)



def main(page: ft.Page):
    # -------------------------
    # CONFIG PAGE
    # -------------------------
    page.title = "Ma To-Do List Moderne"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 420
    page.window_min_width = 320

    page.theme_mode = ft.ThemeMode.DARK
    page.adaptive = True


    # Thème par défaut
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE)

    new_task = ft.TextField(hint_text="Qu'avez-vous à faire ?", expand=True)
    tasks_view = ft.Column(
    scroll=ft.ScrollMode.AUTO,
    expand=True
)


    # -------------------------
    # SAUVEGARDE
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
    # GESTION TACHES
    # -------------------------
    def delete_task(task_row):
        tasks_view.controls.remove(task_row)
        save_tasks()
        page.update()

    def create_task(label, checked=False):
        checkbox = ft.Checkbox(
            label=label,
            value=checked,
            on_change=lambda _: save_tasks()
        )

        task_row = ft.Row(
            wap=True,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
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
        if new_task.value.strip():
            create_task(new_task.value)
            new_task.value = ""
            save_tasks()
            page.update()

    # -------------------------
    # THEME & COULEUR
    # -------------------------
    def change_theme(e):
        page.theme_mode = (
            ft.ThemeMode.DARK
            if e.control.value == "Sombre"
            else ft.ThemeMode.LIGHT
        )
        page.update()

    def change_color(e):
        page.theme = ft.Theme(color_scheme_seed=e.control.value)
        page.update()

    theme_selector = ft.Dropdown(
        label="Thème",
        value="Sombre",
        width=180,
        options=[
            ft.dropdown.Option("Sombre"),
            ft.dropdown.Option("Clair"),
        ],
        on_change=change_theme,
    )

    color_selector = ft.Dropdown(
        label="Couleur",
        value=ft.Colors.BLUE,
        width=180,
        options=[
            ft.dropdown.Option(ft.Colors.BLUE),
            ft.dropdown.Option(ft.Colors.GREEN),
            ft.dropdown.Option(ft.Colors.PURPLE),
            ft.dropdown.Option(ft.Colors.ORANGE),
            ft.dropdown.Option(ft.Colors.RED),
            ft.dropdown.Option(ft.Colors.TEAL),
        ],
        on_change=change_color,
    )

    # -------------------------
    # UI
    # -------------------------
    page.add(
        ft.Text("Mes Tâches 2025", size=30, weight=ft.FontWeight.BOLD),
        ft.Row([theme_selector, color_selector], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row(
            controls=[
                new_task,
                ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=add_clicked),
            ],
        ),
        ft.Divider(height=20),
        tasks_view,
    )

    load_tasks()
    page.update()


if __name__ == "__main__":
    ft.app(target=main)
