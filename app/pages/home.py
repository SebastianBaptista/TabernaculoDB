import flet as ft
from components.sidebar import sidebar
from components.topbar import topbar
from components.general_table import panel

class home(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        # tema de esta ruta
        page.theme=ft.Theme(
            color_scheme_seed=ft.colors.ORANGE_ACCENT_700,
            scrollbar_theme=ft.ScrollbarTheme(
                track_color={
                    ft.ControlState.HOVERED: ft.colors.ORANGE_ACCENT_700,
                    ft.ControlState.DEFAULT: ft.colors.TRANSPARENT
                },
            )
        )
        self.search=ft.TextField(
            width=600,
            content_padding=ft.padding.only(bottom=5),
            height=45,
            border_radius=ft.border_radius.all(0),
            text_size=17,
            border=ft.InputBorder.OUTLINE,
            bgcolor=ft.colors.WHITE,
            text_style=ft.TextStyle(color=ft.colors.ORANGE_ACCENT_700),
            text_vertical_align=0,
            prefix_icon=ft.icons.SEARCH,
        )
        # titulo,icono y contenido que varia segun el sidebar
        self.addicon=ft.IconButton(icon=ft.icons.ADD_BOX_OUTLINED,icon_color=ft.colors.ORANGE_ACCENT_700,icon_size=40)
        
        self.presentation=ft.Column(
            expand=True,
            controls=[panel(page,self.search,self.addicon)]
        )
        
        self.topic=ft.Text(
            value='Dashboard',
            color=ft.colors.LIGHT_BLUE_900,
            size=20,
            weight=ft.FontWeight.BOLD,
        )
        # sidebar y topbar con argumentos para cambiar los atributos del contenedor correspondiente
        self.menu=sidebar(page,self.presentation,self.topic,self.addicon,self.search)
        
        self.nav=topbar(page,self.menu,self.search)
        # caracteristicas de home
        self.bgcolor=ft.colors.WHITE
        self.expand=True
        self.content=ft.Row(
            expand=True,
            spacing=0,
            controls=[
                self.menu,
                ft.Container(
                    expand=True,
                    content=ft.Column(
                        expand=True,
                        controls=[
                            self.nav,
                            ft.Container(
                                expand=1,
                                padding=ft.padding.only(left=10,right=15),
                                content=ft.Column(
                                    controls=[
                                        ft.Row(
                                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                            controls=[
                                                ft.Container(
                                                    bgcolor=ft.colors.WHITE,
                                                    padding=ft.padding.all(20),
                                                    content=self.topic
                                                ),
                                                self.addicon
                                            ]
                                        ),
                                        ft.Divider(
                                            color=ft.colors.BLACK,
                                            height=0.5,
                                            thickness=0.5
                                        )
                                    ]
                                )
                                
                            ),
                            ft.Container(
                                expand=7,
                                content=ft.Column(
                                    expand=True,
                                    controls=[
                                        ft.Container(
                                            expand=True,
                                            content=self.presentation
                                        )
                                    ]
                                )
                            )
                        ]
                    )
                )
            ]
        )