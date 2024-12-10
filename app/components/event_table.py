import flet as ft
from database.models import ModelEvent, ModelMember, ModelInvited
from database.events import Event
from components.general_table import text_create, text_edit
import datetime
import time

class input_date(ft.TextField):
    def __init__(self,label,length,width):
        super().__init__()
        self.label=label
        self.width=width
        self.label_style=ft.TextStyle(color=ft.colors.ORANGE_ACCENT_700,weight=ft.FontWeight.BOLD)
        self.color=ft.colors.LIGHT_BLUE_900
        self.border_color=ft.colors.LIGHT_BLUE_900
        self.max_length=length
        self.helper_style=ft.TextStyle(color=ft.colors.LIGHT_BLUE_900)
        self.input_filter=ft.NumbersOnlyInputFilter()
        self.height=60
        self.content_padding=ft.padding.only(bottom=5,left=6,right=8)
        self.text_align=ft.TextAlign.RIGHT


class input_date_invertido(input_date):
    def __init__(self, label, length, width):
        super().__init__(label, length, width)
        # Cambiar los colores a los inversos
        self.label_style = ft.TextStyle(color=ft.colors.LIGHT_BLUE_900, weight=ft.FontWeight.BOLD)  # Cambiado a azul
        self.color = ft.colors.ORANGE_ACCENT_700 # Cambiado a naranja
        self.border_color = ft.colors.ORANGE_ACCENT_700  # Cambiado a naranja
        self.helper_style = ft.TextStyle(color=ft.colors.ORANGE_ACCENT_700)  # Cambiado a naranja

def event_panel(page,search,icon):
    
    
    #Variables de edit dialog
    event_name = text_edit(" Nombre del Evento","",ft.icons.PERM_IDENTITY,30,ft.TextOnlyInputFilter())
    event_type= text_edit(" Tipo de Evento","",ft.icons.PERM_IDENTITY,12,None )
    materials =text_edit(" Materiales","",ft.icons.PERM_IDENTITY,200,None)
    responsibilities= text_edit(" Responsables","",ft.icons.PERM_IDENTITY,200,None)
    description = text_edit(" Descripción","",ft.icons.PERM_IDENTITY,400,None)
    materials.multiline=True
    description.multiline=True
    responsibilities.multiline=True
    description.height=149
    responsibilities.height=149
    materials.height=149
    description.content_padding=ft.padding.only(bottom=10,top=3)
    responsibilities.content_padding=ft.padding.only(bottom=10,top=3)
    materials.content_padding=ft.padding.only(bottom=10,top=3)
    
    s_date_day = input_date_invertido("Día",2,60)
    s_date_month = input_date_invertido("Mes",2,60)
    s_date_year =  input_date_invertido("Año",4,100)
    
    e_date_day = input_date_invertido("Día",2,60)
    e_date_month = input_date_invertido("Mes",2,60)
    e_date_year =  input_date_invertido("Año",4,100)
    
    #Dialogs
    def edit_dialog(e, event_to_edit):
        event_name.value=event_to_edit.name_event
        event_type.value=event_to_edit.kind_event
        materials.value=event_to_edit.matirials
        responsibilities.value=event_to_edit.leader
        description.value=event_to_edit.info
        s_date_day.value=event_to_edit.start_time.split("/")[0]
        s_date_month.value=event_to_edit.start_time.split("/")[1]
        s_date_year.value=event_to_edit.start_time.split("/")[2]
        e_date_day.value=event_to_edit.end_time.split("/")[0]
        e_date_month.value=event_to_edit.end_time.split("/")[1]
        e_date_year.value=event_to_edit.end_time.split("/")[2]
        
        def date_verify(d,m,y):
            try:
                date=datetime.datetime.strptime(f"{d.value} {m.value} {y.value}",'%d %m %Y')
                return date.strftime("%d/%m/%Y")
            except ValueError as ve:
                return None
            
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
        
        error_date= ft.Container(
            visible=False,
            width=300,
            alignment=ft.alignment.center,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(
                        "INTRODUZCA UNA FECHA VALIDA",
                        color=ft.colors.YELLOW_ACCENT_700,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Divider(
                        height=9,
                        thickness=3,
                        color = ft.colors.YELLOW_ACCENT_700,
                    )
                ]
            )
        )
        
        members_to_add=ft.Column(
            spacing=10,
            height=400,
            width=250,
            scroll=ft.ScrollMode.ALWAYS,
            
        )
        
        members_added=[]
        
        def get_index(e):
            if e.control.value==True:
                members_added.append(e.control.data)
            else:
                members_added.remove(e.control.data)
        
        total_members=ModelMember.dashboard()
        members_to_edit=ModelEvent.persons_event(event_to_edit.id_event)
        id_member = [sublist[1] for sublist in members_to_edit]
        
        def check_member(someone,actual_member):
            if someone in actual_member:
                members_added.append(someone)
                return True
            else:
                False
        
        for member in total_members:
            check_add= ft.Checkbox(
                label="Añadir",
                value=check_member(member[-1],id_member),
                label_position=ft.LabelPosition.LEFT,
                label_style=ft.TextStyle(color=ft.colors.GREY_300),
                check_color=ft.colors.WHITE,
                on_change=get_index,
                data=member[-1],
                fill_color={
                    ft.ControlState.DEFAULT: ft.colors.WHITE,
                    ft.ControlState.SELECTED: ft.colors.ORANGE_ACCENT_700}
            )
            people=ft.Container(
                expand=True,
                padding=ft.padding.only(left=10,top=5,bottom=10),
                border=ft.border.only(bottom=ft.BorderSide(1,color=ft.colors.BLUE_GREY_400)),
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    controls=[
                        ft.Text(
                            f"{member[1]}",
                            color=ft.colors.ORANGE_ACCENT_700,
                            weight=ft.FontWeight.BOLD,
                            size=14,
                            width=150,
                        ),
                        check_add
                    ]
                )
            )
            
            members_to_add.controls.append(people)
        
        dialog=ft.AlertDialog(
            modal=True,
            title=ft.Text("Editar Evento", color=ft.colors.ORANGE_ACCENT_700, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
            bgcolor=ft.colors.WHITE,
            shadow_color=ft.colors.BLACK,
            shape=ft.RoundedRectangleBorder(radius=0),
            content=ft.Container(
                height=500,
                width=800,
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                    controls=[      
                        ft.Column(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            spacing=5,
                            width=250,
                            controls=[
                                event_name,
                                event_type,
                                ft.Text(
                                    "Fecha de Inicio del Evento",
                                    height=20,
                                    size=18,
                                    color=ft.colors.LIGHT_BLUE_900,
                                    weight=ft.FontWeight.BOLD
                                ),
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    controls=[
                                        s_date_day,
                                        s_date_month,
                                        s_date_year,
                                    ]
                                ),
                                ft.Text(
                                    "Fecha de Cierre del Evento",
                                    size=18,
                                    color=ft.colors.ORANGE_ACCENT_700,
                                    weight=ft.FontWeight.BOLD
                                ),
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    controls=[
                                        e_date_day,
                                        e_date_month,
                                        e_date_year,
                                    ]
                                ),
                                error_date
                            ]
                        ),
                        ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                no_complete,
                                ft.Container(
                                    border=ft.border.all(2,color=ft.colors.ORANGE_ACCENT_700),
                                    content=ft.Column(
                                        controls=[
                                            ft.Container(
                                                margin=ft.margin.all(0),
                                                expand=True,
                                                bgcolor=ft.colors.ORANGE_ACCENT_700,
                                                border=ft.border.all(2,color=ft.colors.ORANGE_ACCENT_700),
                                                content=ft.Row(
                                                    alignment=ft.MainAxisAlignment.CENTER,
                                                    height=60,
                                                    width=250,
                                                    controls=[
                                                        ft.Text(
                                                            "AÑADIR PARTICIPANTES",
                                                            weight=ft.FontWeight.BOLD,
                                                            color=ft.colors.WHITE
                                                        )
                                                    ]
                                                )
                                            ),
                                            members_to_add
                                        ]
                                    )
                                ),      
                            ]
                        ),
                        ft.Column(
                            alignment=ft.MainAxisAlignment.START,
                            spacing=16,
                            width=250,
                            controls=[
                                responsibilities,
                                materials,
                                description,
                            ]
                        ),
                        
                    ]
                )
            ),
            actions=[
                ft.ElevatedButton(
                    "Aceptar",
                    on_click=lambda e :set_event(no_complete,error_date,members_added,Event(event_to_edit.id_event,event_name.value,event_type.value,responsibilities.value,materials.value,date_verify(s_date_day,s_date_month,s_date_year),date_verify(e_date_day,e_date_month,e_date_year),description.value)),
                    bgcolor=ft.colors.LIGHT_BLUE_900,
                    color=ft.colors.WHITE,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=0)),
                ),
                ft.ElevatedButton(
                    "Cancelar", 
                    on_click=close_dlg, 
                    bgcolor=ft.colors.RED,
                    color=ft.colors.WHITE,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=0))
                )
            ],
        )
        return dialog
    
    def open_edit(e):
        event_to_edit=e.control.data
        dialog=edit_dialog(e,event_to_edit)
        page.dialog=dialog
        page.dialog.open=True
        page.update()
    
    def open_create(e):
        event_name_field = text_create(" Nombre del Evento","",ft.icons.PERM_IDENTITY,30,None)
        event_type_field = text_create(" Tipo de Evento","",ft.icons.PERM_IDENTITY,12,None )
        materials_field =text_create(" Materiales","",ft.icons.PERM_IDENTITY,200,None)
        responsibilities_field = text_create(" Responsables","",ft.icons.PERM_IDENTITY,200,None)
        description_field = text_create(" Descripción","",ft.icons.PERM_IDENTITY,400,None)
        materials_field.multiline=True
        description_field.multiline=True
        responsibilities_field.multiline=True
        description_field.height=149
        responsibilities_field.height=149
        materials_field.height=149
        description_field.content_padding=ft.padding.only(bottom=10,top=3)
        responsibilities_field.content_padding=ft.padding.only(bottom=10,top=3)
        materials_field.content_padding=ft.padding.only(bottom=10,top=3)
        
        s_date_day = input_date("Día",2,60)
        s_date_month = input_date("Mes",2,60)
        s_date_year =  input_date("Año",4,100)
        
        e_date_day = input_date("Día",2,60)
        e_date_month = input_date("Mes",2,60)
        e_date_year =  input_date("Año",4,100)
        
        def date_verify(d,m,y):
            try:
                date=datetime.datetime.strptime(f"{d.value} {m.value} {y.value}",'%d %m %Y')
                return date.strftime("%d/%m/%Y")
            except ValueError as ve:
                return None
        
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
        
        error_date= ft.Container(
            visible=False,
            width=300,
            alignment=ft.alignment.center,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(
                        "INTRODUZCA UNA FECHA VALIDA",
                        color=ft.colors.YELLOW_ACCENT_700,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Divider(
                        height=9,
                        thickness=3,
                        color = ft.colors.YELLOW_ACCENT_700,
                    )
                ]
            )
        )
        
        members_to_add=ft.Column(
            spacing=10,
            height=400,
            width=250,
            scroll=ft.ScrollMode.ALWAYS,
            
        )
        members_added=[]
        
        members=ModelMember.dashboard()
        
        def get_index(e):
            if e.control.value==True:
                members_added.append(e.control.data)
                print(members_added)
            else:
                members_added.remove(e.control.data)
                print(members_added)
        
        for member in members:
            check_add= ft.Checkbox(
                label="Añadir",
                label_position=ft.LabelPosition.LEFT,
                label_style=ft.TextStyle(color=ft.colors.BLUE_GREY_400),
                check_color=ft.colors.LIGHT_BLUE_900,
                on_change=get_index,
                data=member[-1],
                fill_color={
                    ft.ControlState.DEFAULT: ft.colors.WHITE,
                    ft.ControlState.SELECTED: ft.colors.LIGHT_BLUE_300}
            )
            people=ft.Container(
                expand=True,
                padding=ft.padding.only(left=10,top=5,bottom=10),
                border=ft.border.only(bottom=ft.BorderSide(1,color=ft.colors.BLUE_GREY_400)),
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    controls=[
                        ft.Text(
                            f"{member[1]}",
                            color=ft.colors.LIGHT_BLUE_900,
                            weight=ft.FontWeight.BOLD,
                            size=14,
                            width=150,
                        ),
                        check_add
                    ]
                )
            )
            
            members_to_add.controls.append(people)
        
        create_dialog= ft.AlertDialog(
        modal=True,
        title=ft.Text("Registrar Nuevo Evento", color=ft.colors.LIGHT_BLUE_900, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
        bgcolor=ft.colors.WHITE,
        shadow_color=ft.colors.BLACK,
        shape=ft.RoundedRectangleBorder(radius=0),
        content=ft.Container(
            height=500,
            width=800,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                controls=[      
                    ft.Column(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        spacing=5,
                        width=250,
                        controls=[
                            event_name_field,
                            event_type_field,
                            ft.Text(
                                "Fecha de Inicio del Evento",
                                height=20,
                                size=18,
                                color=ft.colors.LIGHT_BLUE_900,
                                weight=ft.FontWeight.BOLD
                            ),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    s_date_day,
                                    s_date_month,
                                    s_date_year,
                                ]
                            ),
                            ft.Text(
                                "Fecha de Cierre del Evento",
                                size=18,
                                color=ft.colors.ORANGE_ACCENT_700,
                                weight=ft.FontWeight.BOLD
                            ),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    e_date_day,
                                    e_date_month,
                                    e_date_year,
                                ]
                            ),
                            error_date
                        ]
                    ),
                    ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            no_complete,
                            ft.Container(
                                border=ft.border.all(2,color=ft.colors.LIGHT_BLUE_900),
                                content=ft.Column(
                                    controls=[
                                        ft.Container(
                                            margin=ft.margin.all(0),
                                            expand=True,
                                            bgcolor=ft.colors.LIGHT_BLUE_900,
                                            border=ft.border.all(2,color=ft.colors.LIGHT_BLUE_900),
                                            content=ft.Row(
                                                alignment=ft.MainAxisAlignment.CENTER,
                                                height=60,
                                                width=250,
                                                controls=[
                                                    ft.Text(
                                                        "AÑADIR PARTICIPANTES",
                                                        weight=ft.FontWeight.BOLD,
                                                        color=ft.colors.WHITE
                                                    )
                                                ]
                                            )
                                        ),
                                        members_to_add
                                    ]
                                )
                            ),      
                        ]
                    ),
                    ft.Column(
                        alignment=ft.MainAxisAlignment.START,
                        spacing=16,
                        width=250,
                        controls=[
                            responsibilities_field,
                            materials_field,
                            description_field,
                        ]
                    ),
                    
                ]
            )
        ),
        actions=[
            ft.ElevatedButton(
                "Registrar",
                on_click=lambda e :register(no_complete,error_date,members_added,Event(None,event_name_field.value,event_type_field.value,responsibilities_field.value,materials_field.value,date_verify(s_date_day,s_date_month,s_date_year),date_verify(e_date_day,e_date_month,e_date_year),description_field.value)),
                bgcolor=ft.colors.LIGHT_BLUE_900,
                color=ft.colors.WHITE,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=0)),
            ),
            ft.ElevatedButton(
                "Cancelar", 
                on_click=close_dlg, 
                bgcolor=ft.colors.RED,
                color=ft.colors.WHITE,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=0))
            )
        ],
        )
        
        page.dialog = create_dialog
        page.dialog.open = True
        page.update()
    
    def set_event(no_complete,error_date,members_added,event):
        if event.name_event and event.kind_event and event.leader and event.matirials and event.info:
            if (event.start_time and event.end_time)!= None:
                ModelEvent.edit_event(event)
                ModelInvited.delete_persons_from_event(event.id_event)
                for id_member in members_added:
                    ModelInvited.add_person(event.id_event,id_member)
                page.dialog.open=False
                iter=ModelEvent.events()
                show_panel(iter)
                page.update()
            else:
                error_date.visible=True
                error_date.update()
                time.sleep(1.5)
                error_date.visible= False
                error_date.update()
        else:
            no_complete.visible=True
            no_complete.update()
            time.sleep(1.5)
            no_complete.visible= False
            no_complete.update()
    
    def register(no_complete,error_date,members_added,event):
        if event.name_event and event.kind_event and event.leader and event.matirials and event.info:
            if (event.start_time and event.end_time)!= None:
                ModelEvent.create_event(event)
                if len(members_added)>0:
                    id_event=ModelInvited.actual_event()
                    for id_member in members_added:
                        ModelInvited.add_person(id_event,id_member)
                page.dialog.open=False
                iter=ModelEvent.events()
                show_panel(iter)
                page.update()
            else:
                error_date.visible=True
                error_date.update()
                time.sleep(1.5)
                error_date.visible= False
                error_date.update()
        else:
            no_complete.visible=True
            no_complete.update()
            time.sleep(1.5)
            no_complete.visible= False
            no_complete.update()
    
    def delete_event(id):
        ModelInvited.delete_persons_from_event(id)
        ModelEvent.delete_event(id)
        page.dialog.open=False
        iter=ModelEvent.events()
        show_panel(iter)
        page.update()
    
    def delete_dialog(e,id):
        delete_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Advertencia",
                color=ft.colors.RED,
                weight=ft.FontWeight.BOLD
            ),
            
            bgcolor=ft.colors.WHITE,
            shadow_color=ft.colors.BLACK,
            shape=ft.RoundedRectangleBorder(radius=0),
            content=ft.Container(
                content=ft.Text(
                    value="Al aceptar se borraran todos los datos de este evento",
                    color=ft.colors.BLACK,
                    text_align=ft.TextAlign.JUSTIFY
                ),
            ),
            actions=[
                ft.ElevatedButton("Aceptar", on_click=lambda e: delete_event(id), bgcolor=ft.colors.RED,color=ft.colors.WHITE,style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=0))),
                ft.ElevatedButton("Cancelar", on_click=close_dlg, bgcolor=ft.colors.LIGHT_BLUE_900,color=ft.colors.WHITE,style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=0)))
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        return delete_dialog
    
    def info_dialog(e,info):
        dialog = ft.AlertDialog(
            title=ft.Text(f"Informacion del Evento",
                color=ft.colors.YELLOW_ACCENT_700,
                weight=ft.FontWeight.BOLD
            ),
            bgcolor=ft.colors.WHITE,
            shadow_color=ft.colors.BLACK,
            shape=ft.RoundedRectangleBorder(radius=0),
            content=ft.Container(
                content=ft.Text(
                    width=800,
                    value=info,
                    color=ft.colors.BLACK,
                    text_align=ft.TextAlign.JUSTIFY
                ),
            ),
            actions_alignment=ft.MainAxisAlignment.END,
        )
        return dialog
    
    def leader_dialog(e,leader):
        dialog = ft.AlertDialog(
            title=ft.Text(f"Responsables",
                color=ft.colors.ORANGE_ACCENT_700,
                weight=ft.FontWeight.BOLD
            ),
            bgcolor=ft.colors.WHITE,
            shadow_color=ft.colors.BLACK,
            shape=ft.RoundedRectangleBorder(radius=0),
            content=ft.Container(
                content=ft.Text(
                    value=leader,
                    color=ft.colors.BLACK,
                    text_align=ft.TextAlign.JUSTIFY
                ),
            ),
            actions_alignment=ft.MainAxisAlignment.END,
        )
        return dialog
    
    def open_responsabilities(e):
        leader=e.control.data
        dialog=leader_dialog(e,leader)
        page.dialog=dialog
        page.dialog.open=True
        page.update()
    
    def open_info(e):
        leader=e.control.data
        dialog=info_dialog(e,leader)
        page.dialog=dialog
        page.dialog.open=True
        page.update()
    
    def open_delete(e):
        id=e.control.data
        dialog=delete_dialog(e,id)
        page.dialog=dialog
        page.dialog.open=True
        page.update()
        
    def close_dlg(e):
        page.dialog.open=False
        page.update()
    #Icono para añadir eventos
    icon.on_click=open_create
    
    events=ModelEvent.events()
    
    event_list=ft.Row(
        alignment=ft.MainAxisAlignment.START,
        wrap=True,
        expand=True,
        controls=[]
    )
    
    columna=ft.Column(
        expand=True,
        scroll="auto",
        controls=[
            ft.Container(
                padding=ft.padding.only(10,10,15,10),
                content=event_list
            )
        ]
    )
    def show_panel(iter):
        event_list.controls.clear()
        
        for features in iter:
            event=Event(features[0],features[1],features[2],features[3],features[4],features[5],features[6],features[7])
            
            members_in_event=ft.Column(
                spacing=10,
                height=170,
                width=200,
                scroll=ft.ScrollMode.ALWAYS,
            )
            list_people=ModelEvent.persons_event(event.id_event)
            
            for member in list_people:
                people=ft.Container(
                    padding=ft.padding.only(left=15,bottom=5),
                    border=ft.border.only(bottom=ft.BorderSide(1,color="grey")),
                    content=ft.Row(
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    
                        controls=[
                            ft.Text(
                                f"{member[0]}",
                                color=ft.colors.LIGHT_BLUE_900,
                                weight=ft.FontWeight.BOLD,
                                size=14,
                                width=160
                            )
                        ]
                    )
                )
                
                members_in_event.controls.append(people)
                
            crd=ft.Card(
                shape=ft.RoundedRectangleBorder(radius=0),
                width=400,
                height=350,
                elevation=20,
                content=ft.Container(
                    bgcolor=ft.colors.WHITE,
                    border=None,
                    content=ft.Column(
                        controls=[
                            ft.Container(
                                bgcolor=ft.colors.LIGHT_BLUE_900,
                                content=ft.Row(
                                    height=60,
                                    controls=[
                                        ft.ListTile(
                                            width=400,
                                            title=ft.Text(
                                                value=event.name_event,
                                                weight=ft.FontWeight(ft.FontWeight.BOLD),
                                                color=ft.colors.WHITE
                                            ),
                                            icon_color=ft.colors.WHITE,
                                            trailing=ft.PopupMenuButton(
                                                icon=ft.icons.MORE_VERT,
                                                items=[
                                                    ft.PopupMenuItem(
                                                        on_click=open_info,
                                                        data=event.info,
                                                        content=ft.Row(
                                                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                                            controls=[
                                                                ft.Text(
                                                                    "Informacion",
                                                                    color=ft.colors.YELLOW_ACCENT_700,
                                                                ),
                                                                ft.Icon(
                                                                    name=ft.icons.INFO,
                                                                    color=ft.colors.YELLOW_ACCENT_700
                                                                )
                                                            ]
                                                        )
                                                    ),
                                                    ft.PopupMenuItem(
                                                        data=event,
                                                        on_click=open_edit,
                                                        content=ft.Row(
                                                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                                            controls=[
                                                                ft.Text(
                                                                    "Editar",
                                                                    color=ft.colors.LIGHT_BLUE_900,
                                                                ),
                                                                ft.Icon(
                                                                    name=ft.icons.EDIT,
                                                                    color=ft.colors.LIGHT_BLUE_900
                                                                )
                                                            ]
                                                        )
                                                    ),
                                                    ft.PopupMenuItem(
                                                        data=event.id_event,
                                                        on_click=open_delete,
                                                        content=ft.Row(
                                                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                                            controls=[
                                                                ft.Text(
                                                                    "Eliminar Evento",
                                                                    color=ft.colors.RED,
                                                                ),
                                                                ft.Icon(
                                                                    name=ft.icons.DELETE,
                                                                    color=ft.colors.RED
                                                                )
                                                            ]
                                                        )
                                                    ),
                                                ],
                                                shape=ft.RoundedRectangleBorder(radius=0),
                                                bgcolor=ft.colors.WHITE,
                                            ),
                                        ),
                                    ]
                                )
                            ),
                            ft.Row(
                                expand=True,
                                controls=[
                                    ft.Column(
                                        expand=1,
                                        spacing=1,
                                        controls=[
                                            ft.Column(
                                                controls=[
                                                    ft.Container(
                                                        margin=ft.margin.only(left=10),
                                                        padding=ft.padding.all(0),
                                                        content=ft.Text(
                                                            f"Tipo de Evento:\n{event.kind_event}",
                                                            color=ft.colors.BLACK,
                                                            weight=ft.FontWeight.BOLD,
                                                            text_align=ft.TextAlign.START,
                                                            size=13
                                                        )
                                                    ),
                                                    
                                                    ft.Container(
                                                        margin=ft.margin.only(left=10),
                                                        padding=ft.padding.all(3),
                                                        bgcolor=ft.colors.ORANGE_ACCENT_700,
                                                        width=167,
                                                        ink=True,
                                                        border=ft.border.all(1,color=ft.colors.YELLOW_ACCENT_700),
                                                        on_click=open_responsabilities,
                                                        data=event.leader,
                                                        content=ft.Text(
                                                            f"Responsables",
                                                            color=ft.colors.WHITE,
                                                            weight=ft.FontWeight.BOLD,
                                                            text_align=ft.TextAlign.CENTER,
                                                            size=13
                                                        )
                                                    ),
                                                    
                                                ]
                                            ),
                                            ft.Column(
                                                controls=[
                                                    ft.Container(
                                                        padding=ft.padding.only(left=10),
                                                        content=ft.Text(
                                                            f"Materiales:",
                                                            color=ft.colors.LIGHT_BLUE_900,
                                                            weight=ft.FontWeight.BOLD,
                                                            text_align=ft.TextAlign.START,
                                                        )
                                                    ),
                                                    ft.Container(
                                                        padding=ft.padding.symmetric(5),
                                                        margin=ft.margin.only(left=10,bottom=10),
                                                        border=ft.border.all(2,color=ft.colors.LIGHT_BLUE_900),
                                                        height= 155,
                                                        width=167,
                                                        content=ft.Column(
                                                            scroll=ft.ScrollMode.ALWAYS,
                                                            controls=[
                                                                ft.Container(
                                                                    padding=ft.padding.only(left=10,right=10,bottom=5),
                                                                    content=ft.Text(
                                                                        f"{event.matirials}",
                                                                        color=ft.colors.BLACK,
                                                                        text_align=ft.TextAlign.JUSTIFY,
                                                                        size=10,
                                                                        weight=ft.FontWeight.BOLD
                                                                    )
                                                                )
                                                            ]
                                                        )
                                                    ),
                                                ]
                                            )
                                        ]
                                    ),
                                    ft.Column(
                                        expand=1,
                                        controls=[
                                            ft.Column(
                                                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                                expand=True,
                                                controls=[
                                                    ft.Text(
                                                        f"Fecha de Inicio: {event.start_time}",
                                                        color=ft.colors.LIGHT_BLUE_900,
                                                        weight=ft.FontWeight.BOLD,
                                                        size=13
                                                    ),
                                                    ft.Text(
                                                        f"Fecha de Cierre: {event.end_time}",
                                                        color=ft.colors.ORANGE_ACCENT_700,
                                                        weight=ft.FontWeight.BOLD,
                                                        size=13
                                                    )
                                                ]
                                            ),
                                            ft.Text(
                                                "Participantes:",
                                                color=ft.colors.BLACK,
                                                weight=ft.FontWeight.BOLD,
                                                text_align=ft.TextAlign.CENTER
                                            ),
                                            ft.Container(
                                                padding=ft.padding.only(top=5),
                                                margin=ft.margin.only(bottom=10,right=10),
                                                border=ft.border.all(2,color=ft.colors.ORANGE_ACCENT_700),
                                                content=members_in_event
                                            )
                                        ]
                                    )
                                ]
                            ),
                        ]
                    )
                )
            )
            event_list.controls.append(crd)
        
    for features in events:
        
        event=Event(features[0],features[1],features[2],features[3],features[4],features[5],features[6],features[7])
        
        members_in_event=ft.Column(
            spacing=10,
            height=170,
            width=200,
            scroll=ft.ScrollMode.ALWAYS,
        )
        list_people=ModelEvent.persons_event(event.id_event)
        
        for member in list_people:
            people=ft.Container(
                padding=ft.padding.only(left=15,bottom=5),
                border=ft.border.only(bottom=ft.BorderSide(1,color="grey")),
                content=ft.Row(
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    
                    controls=[
                        ft.Text(
                            f"{member[0]}",
                            color=ft.colors.LIGHT_BLUE_900,
                            weight=ft.FontWeight.BOLD,
                            size=14,
                            width=160
                        )
                    ]
                )
            )
            
            members_in_event.controls.append(people)
            
        crd=ft.Card(
            shape=ft.RoundedRectangleBorder(radius=0),
            width=400,
            height=350,
            elevation=20,
            content=ft.Container(
                bgcolor=ft.colors.WHITE,
                border=None,
                content=ft.Column(
                    controls=[
                        ft.Container(
                            bgcolor=ft.colors.LIGHT_BLUE_900,
                            content=ft.Row(
                                height=60,
                                controls=[
                                    ft.ListTile(
                                        width=400,
                                        title=ft.Text(
                                            value=event.name_event,
                                            weight=ft.FontWeight(ft.FontWeight.BOLD),
                                            color=ft.colors.WHITE
                                        ),
                                        icon_color=ft.colors.WHITE,
                                        trailing=ft.PopupMenuButton(
                                            icon=ft.icons.MORE_VERT,
                                            items=[
                                                ft.PopupMenuItem(
                                                    on_click=open_info,
                                                    data=event.info,
                                                    content=ft.Row(
                                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                                        controls=[
                                                            ft.Text(
                                                                "Informacion",
                                                                color=ft.colors.YELLOW_ACCENT_700,
                                                            ),
                                                            ft.Icon(
                                                                name=ft.icons.INFO,
                                                                color=ft.colors.YELLOW_ACCENT_700
                                                            )
                                                        ]
                                                    )
                                                ),
                                                ft.PopupMenuItem(
                                                    data=event,
                                                    on_click=open_edit,
                                                    content=ft.Row(
                                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                                        controls=[
                                                            ft.Text(
                                                                "Editar",
                                                                color=ft.colors.LIGHT_BLUE_900,
                                                            ),
                                                            ft.Icon(
                                                                name=ft.icons.EDIT,
                                                                color=ft.colors.LIGHT_BLUE_900
                                                            )
                                                        ]
                                                    )
                                                ),
                                                ft.PopupMenuItem(
                                                    data=event.id_event,
                                                    on_click=open_delete,
                                                    content=ft.Row(
                                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                                        controls=[
                                                            ft.Text(
                                                                "Eliminar Evento",
                                                                color=ft.colors.RED,
                                                            ),
                                                            ft.Icon(
                                                                name=ft.icons.DELETE,
                                                                color=ft.colors.RED
                                                            )
                                                        ]
                                                    )
                                                ),
                                            ],
                                            shape=ft.RoundedRectangleBorder(radius=0),
                                            bgcolor=ft.colors.WHITE,
                                        ),
                                    ),
                                ]
                            )
                        ),
                        ft.Row(
                            expand=True,
                            controls=[
                                ft.Column(
                                    expand=1,
                                    spacing=1,
                                    controls=[
                                        ft.Column(
                                            controls=[
                                                ft.Container(
                                                    margin=ft.margin.only(left=10),
                                                    padding=ft.padding.all(0),
                                                    content=ft.Text(
                                                        f"Tipo de Evento:\n{event.kind_event}",
                                                        color=ft.colors.BLACK,
                                                        weight=ft.FontWeight.BOLD,
                                                        text_align=ft.TextAlign.START,
                                                        size=13
                                                    )
                                                ),
                                                ft.Container(
                                                    margin=ft.margin.only(left=10),
                                                    padding=ft.padding.all(3),
                                                    bgcolor=ft.colors.ORANGE_ACCENT_700,
                                                    width=167,
                                                    ink=True,
                                                    border=ft.border.all(1,color=ft.colors.YELLOW_ACCENT_700),
                                                    on_click=open_responsabilities,
                                                    data=event.leader,
                                                    content=ft.Text(
                                                        f"Responsables",
                                                        color=ft.colors.WHITE,
                                                        weight=ft.FontWeight.BOLD,
                                                        text_align=ft.TextAlign.CENTER,
                                                        size=13
                                                    )
                                                ),
                                                
                                            ]
                                        ),
                                        ft.Column(
                                            controls=[
                                                ft.Container(
                                                    padding=ft.padding.only(left=10),
                                                    content=ft.Text(
                                                        f"Materiales:",
                                                        color=ft.colors.LIGHT_BLUE_900,
                                                        weight=ft.FontWeight.BOLD,
                                                        text_align=ft.TextAlign.START,
                                                    )
                                                ),
                                                ft.Container(
                                                    padding=ft.padding.symmetric(5),
                                                    margin=ft.margin.only(left=10,bottom=10),
                                                    border=ft.border.all(2,color=ft.colors.LIGHT_BLUE_900),
                                                    height= 155,
                                                    width=167,
                                                    content=ft.Column(
                                                        scroll=ft.ScrollMode.ALWAYS,
                                                        controls=[
                                                            ft.Container(
                                                                padding=ft.padding.only(left=10,right=10,bottom=5),
                                                                content=ft.Text(
                                                                    f"{event.matirials}",
                                                                    color=ft.colors.BLACK,
                                                                    text_align=ft.TextAlign.JUSTIFY,
                                                                    size=10,
                                                                    weight=ft.FontWeight.BOLD
                                                                )
                                                            )
                                                        ]
                                                    )
                                                ),
                                            ]
                                        )
                                    ]
                                ),
                                ft.Column(
                                    expand=1,
                                    controls=[
                                        ft.Column(
                                            alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                            expand=True,
                                            controls=[
                                                ft.Text(
                                                    f"Fecha de Inicio: {event.start_time}",
                                                    color=ft.colors.LIGHT_BLUE_900,
                                                    weight=ft.FontWeight.BOLD,
                                                    size=13
                                                ),
                                                ft.Text(
                                                    f"Fecha de Cierre: {event.end_time}",
                                                    color=ft.colors.ORANGE_ACCENT_700,
                                                    weight=ft.FontWeight.BOLD,
                                                    size=13
                                                )
                                            ]
                                        ),
                                        ft.Text(
                                            "Participantes:",
                                            color=ft.colors.BLACK,
                                            weight=ft.FontWeight.BOLD,
                                            text_align=ft.TextAlign.CENTER
                                        ),
                                        ft.Container(
                                            padding=ft.padding.only(top=5),
                                            margin=ft.margin.only(bottom=10,right=10),
                                            border=ft.border.all(2,color=ft.colors.ORANGE_ACCENT_700),
                                            content=members_in_event
                                        )
                                    ]
                                )
                            ]
                        ),
                    ]
                )
            )
        )
        event_list.controls.append(crd)
        page.update()
    
    #Search
    def search_event(e):
        inp=search.value
        list_search=list(filter(lambda x:inp.lower() in x[1].lower() , events))
        if inp !="":
            if len(list_search) > 0:
                event_list.controls.clear()
                show_panel(list_search)
            else:
                show_panel([])
        elif inp == "" :
            event_list.controls.clear()
            events_reset=ModelEvent.events()
            show_panel(events_reset)
        time.sleep(0.2)
        page.update()
    
    search.on_change = search_event
    
    return columna