import flet as ft
from database.models import MoldelAdmin
from database.admin import Admin
import time
import random
from tools.email import send_email 
class forgot(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        # Campo para ingresar el código
        self.code_field = ft.TextField(
            text_align=ft.TextAlign.CENTER,
            label="Código",
            visible=False,
            border_color=ft.colors.LIGHT_BLUE_900,
            border_width=1,
            color=ft.colors.LIGHT_BLUE_900,
            width=100
        )
        # Botón para confirmar el código
        self.save_code = ft.Container(
            alignment=ft.alignment.center,
            bgcolor=ft.colors.LIGHT_BLUE_900,
            visible=False,
            height=40,
            ink=True,
            on_click=self.verify_code,
            ink_color=ft.colors.ORANGE_ACCENT_700,
            content=ft.Text("Confirmar Código", color=ft.colors.WHITE),
        )
        self.send_check=ft.Container(
            alignment=ft.alignment.center,
            bgcolor=ft.colors.ORANGE_ACCENT_700,
            height=40,
            ink=True,
            on_click=self.check_and_send_email,
            ink_color=ft.colors.LIGHT_BLUE_900,
            content=ft.Text("Enviar Correo de Recuperación",color=ft.colors.WHITE),
        )
        self.email=None
        self.sent_code = None  # Variable para almacenar el código enviado
        # Variables para controlar el tiempo de envío
        self.last_sent_time = 0  # Almacena el tiempo del último envío
        self.cooldown_period = 60  # Tiempo de espera en segundos
        #Validation
        self.error_field=ft.Text(value="",color=ft.colors.YELLOW_ACCENT_700, visible=False,weight=ft.FontWeight.BOLD,size=15)
        self.error_border=ft.border.all(color=ft.colors.YELLOW_ACCENT_700,width=1)
        self.error_divider=ft.Divider(height=9, thickness=3,color = ft.colors.YELLOW_ACCENT_700,visible=False)
        #EndValidation
        page.theme=ft.Theme(color_scheme_seed=ft.colors.ORANGE_ACCENT_700)
        self.expand=True
        self.text_email=ft.TextField(
            label="Email",
            border_color=ft.colors.LIGHT_BLUE_900,
            border_width=1,
            color= ft.colors.LIGHT_BLUE_900
        )
        
        self.content=ft.Row(
            controls=[
                ft.Container(
                    expand=3,
                    content=ft.Stack(
                        fit=ft.StackFit.EXPAND,
                        controls=[
                            ft.Image(
                                src="images/cruz.png",
                                fit=ft.ImageFit.COVER
                            ), 
                        ]
                    )
                ),
                ft.Container(
                    expand=2,
                    margin=ft.margin.only(top=20),
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
                                content=ft.Text("Recuperar Contraseña",
                                    text_align=ft.TextAlign.CENTER,
                                    color=ft.colors.ORANGE_ACCENT_700,
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
                                            color = ft.colors.ORANGE_ACCENT_700
                                        ),
                                        ft.Container(
                                            alignment=ft.alignment.center,
                                            content=self.error_field
                                        ),
                                        self.error_divider,
                                        self.text_email,
                                        ft.Row(
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            controls=[
                                                self.code_field,
                                            ]
                                        )
                                    ]
                                )
                            ),
                            self.save_code,
                            self.send_check,
                            ft.Container(
                                alignment=ft.alignment.center,
                                height=40,
                                content=ft.Text("Volver Atras",
                                    color=ft.colors.LIGHT_BLUE_900,
                                    weight=ft.FontWeight.BOLD
                                ),
                                on_click=lambda e: page.go("/login")
                            )
                        ]
                    )
                ),
            ]
        )
    def check_and_send_email(self,e):
        self.send_check.on_click=None
        #Comprobacion de Email Y Contraseña
        current_time = time.time()  # Obtiene el tiempo actual en segundos
        # Verifica si han pasado 60 segundos desde el último envío
        if current_time - self.last_sent_time < self.cooldown_period:
            error_handler(self, "Por favor, espera antes de enviar otro correo.")
            self.send_check.on_click=self.check_and_send_email
            return
        email=self.text_email.value
        if email:
            someone = Admin(0,email,"",'')
            admin=MoldelAdmin.login(someone)
            if admin:
                self.code_field.visible = True  # Muestra el campo para ingresar el código
                self.save_code.visible = True  # Muestra el botón para confirmar el código
                self.last_sent_time = current_time 
                self.sent_code=''.join(random.choices('0123456789', k=4))
                self.email=email
                send_email(admin.email,self.sent_code)
                self.send_check.content=ft.Text("Enviar de Nuevo",color=ft.colors.WHITE)
                self.send_check.on_click=self.check_and_send_email
                print("enviado")
                self.page.update()
            else:
                error_handler(self,"Email no encontrado")
                self.send_check.on_click=self.check_and_send_email
        else:
            error_handler(self,"Debe completar el campo!")
            self.send_check.on_click=self.check_and_send_email
    
    def verify_code(self, e):
        entered_code = self.code_field.value  # Obtiene el código ingresado
        if entered_code == self.sent_code:  # Compara con el código enviado
            # Código correcto, puedes proceder con la recuperación de contraseña
            admin=MoldelAdmin.login(Admin(None,self.email,"",""))
            self.page.data={
                "Admin_id": admin.id,
                "Admin_name": admin.name,
            }
            self.page.go("/home")
            # Aquí puedes agregar la lógica para permitir al usuario restablecer su contraseña
        else:
            error_handler(self, "Código incorrecto")
    




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