import flet as ft
import time
from database.models import MoldelAdmin
from database.admin import Admin


class login(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        #Validation
        self.error_field=ft.Text(value="",color=ft.colors.YELLOW_ACCENT_700, visible=False,weight=ft.FontWeight.BOLD,size=15)
        self.error_border=ft.border.all(color=ft.colors.YELLOW_ACCENT_700,width=1)
        self.error_divider=ft.Divider(height=9, thickness=3,color = ft.colors.YELLOW_ACCENT_700,visible=False)
        #EndValidation
        page.theme=ft.Theme(color_scheme_seed=ft.colors.ORANGE_ACCENT_700)
        self.expand=True
        self.text_email=ft.TextField(
            label="Email",
            border_color=ft.colors.ORANGE_ACCENT_700,
            border_width=1,
            color= ft.colors.ORANGE_ACCENT_700
        )
        self.text_password=ft.TextField(
            label="Password",
            password=True,
            can_reveal_password=True,
            cursor_color=ft.colors.ORANGE_ACCENT_700,
            border_color=ft.colors.ORANGE_ACCENT_700,
            border_width=1,
            color= ft.colors.ORANGE_ACCENT_700
        )
        self.content=ft.Row(
            controls=[
                ft.Container(
                    expand=2,
                    padding=ft.padding.all(40),
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.START,
                        controls=[
                            ft.Container(
                                alignment=ft.alignment.center,
                                content=ft.Image(
                                    src="images/logo_tabernaculo.png",
                                    width=175,
                                    height=175,
                                ),
                            ),
                            ft.Container(
                                alignment=ft.alignment.center,
                                content=ft.Text("Tabernáculo DB",
                                    text_align=ft.TextAlign.CENTER,
                                    color=ft.colors.LIGHT_BLUE_900,
                                    size=40,
                                    weight=ft.FontWeight.BOLD
                                )
                            ),
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Divider(
                                            height=9, 
                                            thickness=3,
                                            color = ft.colors.LIGHT_BLUE_900
                                        ),
                                        ft.Container(
                                            alignment=ft.alignment.center,
                                            content=self.error_field
                                        ),
                                        self.error_divider,
                                        self.text_email,
                                        self.text_password
                                    ]
                                )
                            ),
                            ft.Container(
                                alignment=ft.alignment.center,
                                bgcolor=ft.colors.LIGHT_BLUE_900,
                                height=40,
                                ink=True,
                                ink_color=ft.colors.ORANGE_ACCENT_700,
                                content=ft.Text("Entrar",color=ft.colors.WHITE),
                                on_click=self.log
                                
                            ),
                            ft.Container(
                                alignment=ft.alignment.center,
                                height=40,
                                content=ft.Text("Olvide la Contraseña",
                                    color=ft.colors.ORANGE_ACCENT_700,
                                    weight=ft.FontWeight.BOLD
                                ),
                                on_click=lambda e: page.go("/forgot")
                            )
                        ]
                    )
                ),
                ft.Container(
                    expand=3,
                    content=ft.Stack(
                        fit=ft.StackFit.EXPAND,
                        controls=[
                            ft.Image(
                                src="images/familia.png",
                                fit=ft.ImageFit.COVER
                            ),
                            ft.Column(
                                alignment=ft.MainAxisAlignment.START,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=0,
                                controls=[
                                    ft.Icon(
                                        name=ft.icons.LOCK_PERSON_ROUNDED,
                                        size=90,
                                        color=ft.colors.ORANGE_ACCENT_700
                                    ),
                                    ft.Text(
                                        "Inicio de Sesión",
                                        color=ft.colors.ORANGE_ACCENT_700,
                                        size=20,
                                        weight=ft.FontWeight.BOLD
                                    ),
                                ] 
                            ) 
                        ]
                    )
                ),
            ]
        )
    
    def log(self,e):
        #Comprobacion de Email Y Contraseña
        email=self.text_email.value
        password=self.text_password.value
        if email and password:
            someone = Admin(0,email,password,'')
            admin=MoldelAdmin.login(someone)
            if admin:
                if admin.password:
                    self.page.data={
                        "Admin_id": admin.id,
                        "Admin_name": admin.name,
                        }
                    self.page.go("/home")
                else:
                    error_handler(self, "Contraseña Incorrecta")
            else:
                error_handler(self,"Email no encontrado")
        else:
            error_handler(self,"Debe completar todos los campos!")


def error_handler(self,message):
    #resibe como argumento el mensaje de error y hace visible el mensaje de error en en login
    self.error_field.visible=True
    self.error_field.value= message
    self.error_divider.visible=True
    self.error_field.update()
    self.error_divider.update()
    time.sleep(1.5)
    self.error_field.visible= False
    self.error_divider.visible=False
    self.error_field.update()
    self.error_divider.update()