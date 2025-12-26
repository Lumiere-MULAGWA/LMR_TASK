import flet as ft

def main(page: ft.Page):
    page.title = "Application Multi-Vues"

    def route_change(e):
        page.views.clear()
        # Vue principale
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(title=ft.Text("Accueil"), bgcolor=ft.Colors.ON_SURFACE_VARIANT),
                    ft.ElevatedButton("Ouvrir les réglages", on_click=lambda _: page.go("/settings")),
                ],
            )
        )
        # Vue des réglages
        if page.route == "/settings":
            page.views.append(
                ft.View(
                    "/settings",
                    [
                        ft.AppBar(title=ft.Text("Réglages"), bgcolor=ft.Colors.ON_SURFACE_VARIANT),
                        ft.Text("Ici vous pouvez modifier vos préférences."),
                        ft.ElevatedButton("Retour", on_click=lambda _: page.go("/")),
                    ],
                )
            )
        page.update()

    page.on_route_change = route_change
    page.go(page.route)

ft.app(target=main)
#modification du code pour prendre une interface plus simple 
