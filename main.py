import flet as ft

def main(page: ft.Page):
    # Configuration de la fenêtre
    page.title = "Ma To-Do List Moderne"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK  # Mode sombre par défaut
    page.window_width = 450
    page.window_height = 600

    # Champ de saisie pour les nouvelles tâches
    new_task = ft.TextField(hint_text="Qu'avez-vous à faire ?", expand=True)

    # Fonction pour supprimer une tâche
    def delete_task(task_row):
        tasks_view.controls.remove(task_row)
        page.update()

    # Fonction pour ajouter une tâche
    def add_clicked(e):
        if new_task.value != "":
            # Création d'une ligne de tâche style "Compose"
            task_row = ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Checkbox(label=new_task.value, check_color="white"),
                    ft.IconButton(
                        icon=ft.Icons.DELETE_OUTLINE,
                        icon_color="red700",
                        on_click=lambda _: delete_task(task_row)
                    ),
                ],
            )
            tasks_view.controls.append(task_row)
            new_task.value = ""
            page.update()

    # Conteneur pour la liste des tâches (Scrollable)
    tasks_view = ft.Column()

    # Mise en page principale
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

# Lancer l'application
if __name__ == "__main__":
    ft.app(target=main)