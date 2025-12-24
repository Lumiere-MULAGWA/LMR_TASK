import flet as ft

class StatsCard(ft.Container):
    def __init__(self, title, value, icon, color):
        super().__init__(
            content=ft.Column([
                ft.Icon(icon, color=color, size=30),
                ft.Text(value, size=25, weight="bold"),
                ft.Text(title, color=ft.Colors.GREY_500),
            ]),
            bgcolor=ft.Colors.ON_SURFACE_VARIANT,
            padding=20,
            border_radius=15,
            expand=True
        )

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 30
    
    page.add(
        ft.Text("Tableau de Bord Système", size=32, weight="bold"),
        ft.Row([
            StatsCard("CPU", "24%", ft.Icons.MEMORY, ft.Colors.BLUE),
            StatsCard("RAM", "6.2 GB", ft.Icons.TERMINAL, ft.Colors.GREEN),
            StatsCard("Disque", "1.2 TB", ft.Icons.STORAGE, ft.Colors.ORANGE),
        ], spacing=20),
        ft.Container(height=20),
        ft.Text("Processus Actifs", size=20, weight="bold"),
        ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nom")),
                ft.DataColumn(ft.Text("Statut")),
            ],
            rows=[
                ft.DataRow(cells=[ft.DataCell(ft.Text("1")), ft.DataCell(ft.Text("Python")), ft.DataCell(ft.Text("Actif"))]),
                ft.DataRow(cells=[ft.DataCell(ft.Text("2")), ft.DataCell(ft.Text("Flet")), ft.DataCell(ft.Text("Actif"))]),
            ],
            expand=True
        )
    )

ft.app(target=main)
#launch a application 
