import flet as ft
from database.models import MoldelAdmin
from database.admin import Admin
from components.general_table import restriction
import time
import re
def config_panel(page):
    
    def validar_email(email):
        # Expresión regular para validar el email
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(patron, email) is not None
        
    
    def close_dlg(e):
        page.dialog.open=False
        page.update()
        
    def save_new_admin(no_complete,invalid,no_allow,key,admin):
        if admin.name and admin.email and admin.password:
            if validar_email(admin.email):
                password_hashed=MoldelAdmin.get_admin_by_id(1).password
                if Admin.check_password(password_hashed,key):
                    admin.password=Admin.generate_hash(admin.password)
                    page.dialog.open=False
                    MoldelAdmin.create_admin(admin)
                    update_panel()
                    page.update()
                else:
                    no_allow.visible=True
                    no_allow.update()
                    time.sleep(1.5)
                    no_allow.visible= False
                    no_allow.update()
            else:
                invalid.visible=True
                invalid.update()
                time.sleep(1.5)
                invalid.visible= False
                invalid.update()
        else:
            no_complete.visible=True
            no_complete.update()
            time.sleep(1.5)
            no_complete.visible= False
            no_complete.update()
            
    
    def delete_admin(id):
        MoldelAdmin.delete_admin(id)
        update_panel()
        page.dialog.open=False
        page.update()
    
    def open_delete(e):
        id=e.control.data
        dialog=ft.AlertDialog(
            modal=True,
            title=ft.Text("ESTAS SEGURO DE ELIMINAR ESTE USUARIO?",
                color=ft.colors.RED,
                weight=ft.FontWeight.BOLD
            ),
            
            bgcolor=ft.colors.WHITE,
            shadow_color=ft.colors.BLACK,
            shape=ft.RoundedRectangleBorder(radius=0),
            actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            actions=[
                ft.ElevatedButton("Cancelar", on_click=close_dlg, bgcolor=ft.colors.RED,color=ft.colors.WHITE,style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=0))),
                ft.ElevatedButton("Aceptar", on_click=lambda e: delete_admin(id), bgcolor=ft.colors.LIGHT_BLUE_900,color=ft.colors.WHITE,style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=0))),
            ],
        )
        page.dialog=dialog
        page.dialog.open=True
        page.update()
    def save_edit(user, email, password):
        new_admin=Admin(page.data['Admin_id'],email,Admin.generate_hash(password),user)
        MoldelAdmin.edit_admin(new_admin)
        close_dlg
        page.update()
        page.data={}
        page.go("/login")
        
    
    def open_change(user,email,password):
        if user and email and password:
            if validar_email(email):
                dialog=ft.AlertDialog(
                    modal=True,
                    title=ft.Text("Estas Seguro?",
                        color=ft.colors.ORANGE_ACCENT_700,
                        weight=ft.FontWeight.BOLD
                    ),
                    
                    bgcolor=ft.colors.WHITE,
                    shadow_color=ft.colors.BLACK,
                    shape=ft.RoundedRectangleBorder(radius=0),
                    content=ft.Container(
                        content=ft.Text("Al aceptar deberas iniciar sesion nuevamente",color=ft.colors.BLACK, weight=ft.FontWeight.BOLD, size=20),
                    ),
                    actions=[
                        ft.ElevatedButton("Guardar", on_click=lambda e: save_edit(user,email,password), bgcolor=ft.colors.LIGHT_BLUE_900,color=ft.colors.WHITE,style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=0))),
                        ft.ElevatedButton("Cancelar", on_click=close_dlg, bgcolor=ft.colors.RED,color=ft.colors.WHITE,style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=0)))
                    ],
                )
            else:
                dialog=ft.AlertDialog(
                    title=ft.Text("El EMAIL NO ES VALIDO",
                        color=ft.colors.ORANGE_ACCENT_700,
                        weight=ft.FontWeight.BOLD
                    ),
                    
                    bgcolor=ft.colors.WHITE,
                    shadow_color=ft.colors.BLACK,
                    shape=ft.RoundedRectangleBorder(radius=0),
                )
        else:
            dialog=ft.AlertDialog(
                    title=ft.Text("DEBES COMPLETAR TODOS LOS CAMPOS",
                        color=ft.colors.RED,
                        weight=ft.FontWeight.BOLD
                    ),
                    
                    bgcolor=ft.colors.WHITE,
                    shadow_color=ft.colors.BLACK,
                    shape=ft.RoundedRectangleBorder(radius=0),
                )
        page.dialog=dialog
        page.dialog.open=True
        page.update()
    
    def open_add_admin(e):
        other_name=ft.TextField(
            label="Nombre de usuario:",
            label_style=ft.TextStyle(color=ft.colors.BLACK,weight=ft.FontWeight.BOLD),
            color=ft.colors.BLACK,
            border_color=ft.colors.ORANGE_ACCENT_700,
            max_length=50,
            height=73,
            width=350,
            helper_style=ft.TextStyle(color=ft.colors.ORANGE_ACCENT_700),
            on_change=restriction
        )
        other_email=ft.TextField(
            label="Email:",
            label_style=ft.TextStyle(color=ft.colors.BLACK,weight=ft.FontWeight.BOLD),
            color=ft.colors.BLACK,
            border_color=ft.colors.ORANGE_ACCENT_700,
            max_length=50,
            width=350,
            height=73,
            helper_style=ft.TextStyle(color=ft.colors.ORANGE_ACCENT_700),
            on_change=restriction
        )
        other_password=ft.TextField(
            label="Nueva Contraseña:",
            label_style=ft.TextStyle(color=ft.colors.BLACK,weight=ft.FontWeight.BOLD),
            color=ft.colors.BLACK,
            border_color=ft.colors.ORANGE_ACCENT_700,
            max_length=30,
            height=73,
            width=350,
            helper_style=ft.TextStyle(color=ft.colors.ORANGE_ACCENT_700),
            on_change=restriction
        )
        
        key=ft.TextField(
            label="Contraseña Maestra",
            label_style=ft.TextStyle(color=ft.colors.BLACK,weight=ft.FontWeight.BOLD),
            color=ft.colors.BLACK,
            border_color=ft.colors.ORANGE_ACCENT_700,
            max_length=30,
            height=73,
            width=350,
            helper_style=ft.TextStyle(color=ft.colors.ORANGE_ACCENT_700),
            on_change=restriction
        )
        
        no_complete= ft.Container(
            visible=False,
            width=250,
            alignment=ft.alignment.center,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(
                        "DEBE COMPLETAR TODOS LOS CAMPOS",
                        color=ft.colors.RED,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Divider(
                        height=9,
                        thickness=3,
                        color = ft.colors.RED,
                    )
                ]
            )
        )
        invalid= ft.Container(
            visible=False,
            width=250,
            alignment=ft.alignment.center,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(
                        "EL EMAIL DEBE SER VALIDO",
                        color=ft.colors.YELLOW_ACCENT_700,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Divider(
                        height=9,
                        thickness=3,
                        color = ft.colors.YELLOW_ACCENT_700,
                    )
                ]
            )
        )
        no_allow= ft.Container(
            visible=False,
            width=250,
            alignment=ft.alignment.center,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(
                        "LA CONTRASEÑA MAESTRA NO ES VALIDA",
                        color=ft.colors.YELLOW_ACCENT_700,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Divider(
                        height=9,
                        thickness=3,
                        color = ft.colors.YELLOW_ACCENT_700,
                    )
                ]
            )
        )
        
        dialog=ft.AlertDialog(
            modal=True,
            title=ft.Text("Añadir un Nuevo Administrador",
                color=ft.colors.ORANGE_ACCENT_700,
                weight=ft.FontWeight.BOLD
            ),
            
            bgcolor=ft.colors.WHITE,
            shadow_color=ft.colors.BLACK,
            shape=ft.RoundedRectangleBorder(radius=0),
            content=ft.Column(
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    no_complete,
                    invalid,
                    ft.Column(
                        controls=[
                            other_name,
                            other_email,
                            other_password,
                        ]
                    ),
                    ft.Column(
                        expand=True,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.END,
                        controls=[
                            no_allow,
                            key
                        ]
                    )
                    
                    
                ],
                
            ),
            actions=[
                ft.ElevatedButton("Guardar", on_click=lambda e: save_new_admin(no_complete,invalid,no_allow,key.value,Admin(None,other_email.value,other_password.value,other_name.value)), bgcolor=ft.colors.LIGHT_BLUE_900,color=ft.colors.WHITE,style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=0))),
                ft.ElevatedButton("Cancelar", on_click=close_dlg, bgcolor=ft.colors.RED,color=ft.colors.WHITE,style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=0)))
            ],
        )
        page.dialog=dialog
        page.dialog.open=True
        page.update()
    
    admin=MoldelAdmin.get_admin_by_id(page.data['Admin_id'])
    
    list_admins=ft.Column(
        spacing=10,
        width=370,
        scroll=ft.ScrollMode.ALWAYS,
        controls=[
            
        ]
    )
    
    def del_icon(data):
        
        delete_icon=ft.IconButton(
            icon=ft.icons.DELETE_FOREVER,
            icon_color=ft.colors.RED,
            data=data,
            on_click=open_delete
        )
        if page.data['Admin_id'] == 1:
            delete_icon.visible=True
        else:
            delete_icon.visible=False
        return delete_icon
    
    def update_panel():
        list_admins.controls.clear()
        admins=MoldelAdmin.get_all_admins(page.data['Admin_id'])
        for admin_feature in admins:
            people=ft.Container(
                padding=ft.padding.only(left=15,bottom=5),
                border=ft.border.only(bottom=ft.BorderSide(0.5,color=ft.colors.RED)),
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                    controls=[
                        ft.Text(
                            f"{admin_feature.name}",
                            color=ft.colors.BLACK,
                            weight=ft.FontWeight.BOLD,
                            size=14,
                            width=300
                        ),
                        del_icon(admin_feature.id)
                    ]
                )
            )
            
            list_admins.controls.append(people)
    
    
    admins=MoldelAdmin.get_all_admins(page.data['Admin_id'])
    
    for admin_feature in admins:
        people=ft.Container(
            padding=ft.padding.only(left=15,bottom=5),
            border=ft.border.only(bottom=ft.BorderSide(0.5,color=ft.colors.RED)),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                controls=[
                    ft.Text(
                        f"{admin_feature.name}",
                        color=ft.colors.BLACK,
                        weight=ft.FontWeight.BOLD,
                        size=14,
                        width=300
                    ),
                    del_icon(admin_feature.id)
                ]
            )
        )
        
        list_admins.controls.append(people)
    
    new_user=ft.TextField(
        label="Nombre de usuario:",
        label_style=ft.TextStyle(color=ft.colors.BLACK,weight=ft.FontWeight.BOLD),
        color=ft.colors.BLACK,
        border_color=ft.colors.LIGHT_BLUE_900,
        max_length=50,
        height=73,
        width=350,
        helper_style=ft.TextStyle(color=ft.colors.LIGHT_BLUE_900,),
        on_change=restriction
    )
    new_email=ft.TextField(
        label="Email:",
        label_style=ft.TextStyle(color=ft.colors.BLACK,weight=ft.FontWeight.BOLD),
        color=ft.colors.BLACK,
        border_color=ft.colors.LIGHT_BLUE_900,
        max_length=50,
        width=350,
        height=73,
        helper_style=ft.TextStyle(color=ft.colors.LIGHT_BLUE_900),
        on_change=restriction
    )
    new_password=ft.TextField(
        label="Nueva Contraseña:",
        label_style=ft.TextStyle(color=ft.colors.BLACK,weight=ft.FontWeight.BOLD),
        color=ft.colors.BLACK,
        border_color=ft.colors.LIGHT_BLUE_900,
        max_length=30,
        password=True,
        height=73,
        width=350,
        helper_style=ft.TextStyle(color=ft.colors.LIGHT_BLUE_900),
        on_change=restriction
    )
    
    panel=ft.Column(
        expand=True,
        height=100,
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.Container(
                expand=True,
                content=ft.Column(
                    expand=True,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            vertical_alignment=ft.CrossAxisAlignment,
                            height=65,
                            controls=[
                                ft.Container(
                                    expand=True,
                                    bgcolor=ft.colors.ORANGE_ACCENT_700,
                                    alignment=ft.alignment.center,
                                    content=ft.Text(
                                        "Ajustes de Cuenta",
                                        size=25,
                                        color=ft.colors.WHITE,
                                        weight=ft.FontWeight.BOLD,
                                        text_align=ft.TextAlign.CENTER,
                                    )
                                )
                            ]
                        ),
                        ft.Row(
                            expand=True,
                            controls=[
                                ft.Column(
                                    expand=1,
                                    controls=[
                                        ft.Column(
                                            
                                            controls=[
                                                ft.Row(
                                                    alignment=ft.MainAxisAlignment.CENTER,
                                                    height=45,
                                                    controls=[
                                                        ft.Container(
                                                            margin=ft.margin.only(left=20),
                                                            expand=True,
                                                            alignment=ft.alignment.center,
                                                            content=ft.Text(
                                                                "Datos Actuales",
                                                                size=25,
                                                                color=ft.colors.LIGHT_BLUE_900,
                                                                weight=ft.FontWeight.BOLD,
                                                            )
                                                        )
                                                    ]
                                                    
                                                )
                                            ]
                                        ),
                                        ft.Row(
                                            controls=[
                                                ft.Container(
                                                    padding=ft.padding.only(left=20),
                                                    content=ft.Text(
                                                        "Usuario:",
                                                        size=20,
                                                        color=ft.colors.LIGHT_BLUE_900,
                                                        weight=ft.FontWeight.BOLD,
                                                    )
                                                ),
                                                ft.Container(
                                                    content=ft.Text(
                                                        f"{admin.name}",
                                                        size=20,
                                                        color=ft.colors.BLACK,
                                                        weight=ft.FontWeight.BOLD,
                                                    )
                                                ),
                                            ]
                                        ),
                                        ft.Row(
                                            controls=[
                                                ft.Container(
                                                    padding=ft.padding.only(left=20),
                                                    content=ft.Text(
                                                        "Email:",
                                                        size=20,
                                                        color=ft.colors.LIGHT_BLUE_900,
                                                        weight=ft.FontWeight.BOLD,
                                                    )
                                                ),
                                                ft.Container(
                                                    content=ft.Text(
                                                        f"{admin.email}",
                                                        size=20,
                                                        color=ft.colors.BLACK,
                                                        weight=ft.FontWeight.BOLD,
                                                    )
                                                ),
                                            ]
                                        ),
                                        ft.Column(
                                            expand=True,
                                            controls=[
                                                ft.Row(
                                                    alignment=ft.MainAxisAlignment.CENTER,
                                                    height=45,
                                                    controls=[
                                                        ft.Container(
                                                            margin=ft.margin.only(left=20),
                                                            
                                                            expand=True,
                                                            alignment=ft.alignment.center,
                                                            content=ft.Text(
                                                                "Editar Datos",
                                                                size=25,
                                                                color=ft.colors.LIGHT_BLUE_900,
                                                                weight=ft.FontWeight.BOLD,
                                                            )
                                                        )
                                                    ]
                                                    
                                                ),
                                                ft.Row(
                                                    expand=True,
                                                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                                    controls=[
                                                        ft.Container(
                                                            margin=ft.margin.only(left=20),
                                                            content=ft.Column(
                                                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                                                controls=[
                                                                    new_user,
                                                                    new_email,
                                                                    new_password,
                                                                    
                                                                ]
                                                            )
                                                        ),
                                                        ft.Column(
                                                            alignment=ft.MainAxisAlignment.END,
                                                            controls=[
                                                                ft.Container(
                                                                    bgcolor=ft.colors.LIGHT_BLUE_900,
                                                                    padding=ft.padding.all(12),
                                                                    margin=ft.margin.only(bottom=20),
                                                                    ink=True,
                                                                    on_click=lambda e: open_change(new_user.value,new_email.value,new_password.value),
                                                                    content=ft.Text(
                                                                        "Confirmar",
                                                                        color=ft.colors.WHITE,
                                                                        weight=ft.FontWeight.BOLD,
                                                                    )
                                                                )
                                                            ]
                                                        )
                                                    ]
                                                )
                                            ]
                                        )
                                    ]
                                ),
                                ft.VerticalDivider(
                                    1,
                                    color=ft.colors.LIGHT_BLUE_900),
                                ft.Column(
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    expand=1,
                                    controls=[
                                        ft.Row(
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            height=45,
                                            controls=[
                                                ft.Container(
                                                    margin=ft.margin.only(right=20),
                                                    expand=True,
                                                    alignment=ft.alignment.center,
                                                    content=ft.Text(
                                                        "Todos los Usuarios",
                                                        size=25,
                                                        color=ft.colors.RED,
                                                        weight=ft.FontWeight.BOLD,
                                                    )
                                                )
                                            ]
                                        ),
                                        ft.Column(
                                            expand=4,
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                            controls=[
                                                ft.Container(
                                                    border=ft.border.all(2,color=ft.colors.RED),
                                                    margin=ft.margin.symmetric(20,50),
                                                    expand=True,
                                                    width=370,
                                                    content=list_admins,
                                                )
                                                
                                            ]
                                        ),
                                        ft.Row(
                                            expand=1,
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            controls=[
                                                ft.Container(
                                                    padding=ft.padding.all(10),
                                                    margin=ft.margin.only(right=10),
                                                    ink=True,
                                                    on_click=open_add_admin,
                                                    bgcolor=ft.colors.RED,
                                                    content=ft.Text("Añadir un Nuevo Administrador",size=20,color=ft.colors.WHITE,weight=ft.FontWeight.BOLD),
                                                )
                                            ]
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                )
            )
        ]
    )
    container=ft.Container(
        expand=True,
        padding=ft.padding.only(10,10,10,15),
        content=panel
    )
    
    
    return container