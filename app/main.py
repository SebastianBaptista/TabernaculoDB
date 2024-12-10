import flet as ft
from pages.login import login
from pages.forgot import forgot
from pages.home import home

def main(page: ft.Page):
    page.title = "TABERNACULO DB"
    page.window.icon = "images/logo_ico.ico"
    page.window_width = 1275
    page.window_height = 725
    page.window_min_width = 1275
    page.window_min_height = 725
    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                bgcolor="white",
                padding=ft.padding.all(0),
                controls=[login(page)]
            )
        )
        if page.route == "/forgot":
            page.views.append(
                ft.View(
                    "/forgot",
                    bgcolor=ft.colors.GREY_100,padding=ft.padding.all(0),
                    controls=[forgot(page)]
                )
            )
        if page.route == "/home":
            page.views.append(
                ft.View(
                    "/home",
                    padding=ft.padding.all(0),
                    controls=[home(page)]
                )
            )
        page.update()
        
    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
    
    page.on_route_change=route_change
    page.on_view_pop = view_pop
    page.go(page.route)

ft.app(target=main, assets_dir="assets", upload_dir="database")