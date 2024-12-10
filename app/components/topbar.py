import flet as ft

def topbar(page,menu,nav):
        
    def animate(e):
        menu.width = 0 if menu.width == 230 else 230
        menu.update()
    top=ft.Container(
        margin=0,
        height=60,
        content=ft.Container(
            bgcolor=ft.colors.LIGHT_BLUE_900,
            margin=0,
            padding=ft.padding.only(left=20,right=20),
            content=ft.Row( 
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.IconButton(icon=ft.icons.MENU_OPEN,icon_color=ft.colors.WHITE,on_click=animate),
                    ft.Container(
                        alignment=ft.alignment.center,
                        height=65,
                        content= nav
                    ),
                    ft.SubmenuButton(
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Icon(
                                        name=ft.icons.PERSON,
                                        color=ft.colors.WHITE,
                                    ),
                                    ft.Text(
                                        f"Admin: {page.data['Admin_name']}",
                                        color=ft.colors.WHITE,
                                    )
                                ]
                            )
                        )
                    )
                ]
            )
        )
    )
    return top

