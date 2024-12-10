import flet as ft
from database.models import ModelService, ModelMember, ModelAsistence
from database.service import Service
from components.general_table import text_create
from components.event_table import input_date
import datetime
import time
def asist_panel(page,icon):
    #dialogs
    def close_dlg(e):
        page.dialog.open=False
        page.update()
    
    def del_service(id_service):
        ModelService.delete_service(id_service)
        ModelAsistence.delete_persons_from_service(id_service)
        page.dialog.open=False
        iter=ModelService.show_services()
        update_table(iter)
        page.update()
    
    def list_members_asist(service):
        
        table_members=ft.DataTable(
            divider_thickness=0,
            horizontal_lines=ft.BorderSide(0,color=ft.colors.WHITE),
            expand=1,
            heading_row_color=ft.colors.LIGHT_BLUE_900,
            heading_text_style=ft.TextStyle(color=ft.colors.WHITE, weight=ft.FontWeight.BOLD),
            data_text_style=ft.TextStyle(weight=ft.FontWeight.BOLD),
            columns=[
                ft.DataColumn(ft.Text("N°"), heading_row_alignment=ft.MainAxisAlignment.START),
                ft.DataColumn(ft.Text("Cédula"),heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("Nombre y Apellido"), numeric=True, heading_row_alignment=ft.MainAxisAlignment.CENTER),
            ],
        )
        
        list_members=ModelAsistence.get_attendees_by_service_id(service.id_service)
        list_members_sorted = sorted(list_members, key=lambda member: int(member[0]))
        
        for i,member_feature in enumerate(list_members_sorted):
            row_color = ft.colors.BLUE_GREY_100 if (i+1) % 2 == 0 else None
            table_members.rows.append(ft.DataRow(
                color=row_color,
                cells=[
                    ft.DataCell(
                        ft.Container(
                            alignment=ft.alignment.center_left,
                            content=ft.Text(
                                f"{i+1}",
                                text_align=ft.TextAlign.START,
                                color=ft.colors.BLACK,
                            )
                        )
                    ),
                    ft.DataCell(
                        ft.Container(
                        alignment=ft.alignment.center,
                        content=ft.Text(
                                f"{int(member_feature[0])}",
                                text_align=ft.TextAlign.CENTER,
                                color=ft.colors.BLACK,
                            )
                        ),
                    ),
                    ft.DataCell(
                        ft.Container(
                            alignment=ft.alignment.center,
                            content=ft.Text(
                                f"{member_feature[1]}",
                                color=ft.colors.BLACK,
                                text_align=ft.TextAlign.CENTER,
                                width=550,
                            )
                        ),
                    ),
                ],
            ),
        )
        
        dialog=ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Asistencia del dia {datetime.datetime.strptime(service.date,'%Y-%m-%d %H:%M:%S').date().strftime('%d/%m/%Y')}",
                color=ft.colors.LIGHT_BLUE_900,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
            ),
            bgcolor=ft.colors.WHITE,
            shadow_color=ft.colors.BLACK,
            shape=ft.RoundedRectangleBorder(radius=0),
            content=ft.Container(
                height=800,
                expand=True,
                border=ft.border.all(2,color=ft.colors.LIGHT_BLUE_900),
                content=ft.Column(
                    scroll='ALWAYS',
                    controls=[
                        ft.Row(
                            expand=True,
                            controls=[
                                table_members
                            ]
                        )
                    ]
                )
            ),
            actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            actions=[
                ft.ElevatedButton(
                    "Eliminar del Registro", 
                    on_click=lambda e: del_service(service.id_service), 
                    bgcolor=ft.colors.RED,
                    color=ft.colors.WHITE,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=0))
                ),
                ft.ElevatedButton(
                    "Cerrar", 
                    on_click=close_dlg, 
                    bgcolor=ft.colors.LIGHT_BLUE_900,
                    color=ft.colors.WHITE,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=0))
                )
            ]
        )
        return dialog
    
    def open_info(e):
        service=e.control.data
        dialog=list_members_asist(service)
        page.dialog=dialog
        page.dialog.open=True
        page.update()
    
    def create_service(e):
        service_name=text_create(" Tema del Servicio","",ft.icons.FILTER_FRAMES,55,None)
        
        d_date=input_date("Día",2,60)
        d_date.height=74
        d_date.value=datetime.datetime.now().day
        m_date=input_date("Mes",2,60)
        m_date.height=74
        m_date.value=datetime.datetime.now().month
        y_date=input_date("AÑo",4,100)
        y_date.height=74
        y_date.value=datetime.datetime.now().year
        
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
        
        def date_verify(d,m,y):
            try:
                date=datetime.datetime.strptime(f"{d.value} {m.value} {y.value}",'%d %m %Y')
                return date
            except ValueError as ve:
                return None
        
        table_members=ft.DataTable(
            divider_thickness=0,
            horizontal_lines=ft.BorderSide(0,color=ft.colors.WHITE),
            expand=1,
            heading_row_color=ft.colors.LIGHT_BLUE_900,
            heading_text_style=ft.TextStyle(color=ft.colors.WHITE, weight=ft.FontWeight.BOLD),
            data_text_style=ft.TextStyle(weight=ft.FontWeight.BOLD),
            columns=[
                ft.DataColumn(ft.Text("N°"), heading_row_alignment=ft.MainAxisAlignment.START),
                ft.DataColumn(ft.Text("Cédula"),heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("Nombre y Apellido"), numeric=True, heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("Asistencia"),heading_row_alignment=ft.MainAxisAlignment.END),
            ],
        )
        
        member_asist=[]
        
        def get_index(e):
            if e.control.value==True:
                member_asist.append(e.control.data)
                print(member_asist)
            else:
                member_asist.remove(e.control.data)
                print(member_asist)
        
        list_members=ModelMember.dashboard()
        list_members_sorted = sorted(list_members, key=lambda member: int(member[0]))
        
        for i,member_feature in enumerate(list_members_sorted):
            row_color = ft.colors.BLUE_GREY_100 if (i+1) % 2 == 0 else None
            table_members.rows.append(ft.DataRow(
                color=row_color,
                cells=[
                    ft.DataCell(
                        ft.Container(
                            alignment=ft.alignment.center_left,
                            content=ft.Text(
                                f"{i+1}",
                                text_align=ft.TextAlign.START,
                                color=ft.colors.BLACK,
                            )
                        )
                    ),
                    ft.DataCell(
                        ft.Container(
                        alignment=ft.alignment.center,
                        content=ft.Text(
                                f"{int(member_feature[0])}",
                                text_align=ft.TextAlign.CENTER,
                                color=ft.colors.BLACK,
                            )
                        ),
                    ),
                    ft.DataCell(
                        ft.Container(
                            alignment=ft.alignment.center,
                            content=ft.Text(
                                f"{member_feature[1]}",
                                color=ft.colors.BLACK,
                                text_align=ft.TextAlign.CENTER,
                                width=550,
                            )
                        ),
                    ),
                    ft.DataCell(
                        ft.Container(
                            alignment=ft.alignment.center_right,
                            margin=ft.margin.only(right=10),
                            content=ft.Checkbox(
                                check_color=ft.colors.LIGHT_BLUE_900,
                                on_change=get_index,
                                data=member_feature[-1],
                                fill_color={
                                    ft.ControlState.DEFAULT: ft.colors.WHITE,
                                    ft.ControlState.SELECTED: ft.colors.LIGHT_BLUE_300}
                            )
                        )
                    ),
                ],
            ),
        )
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Nueva Asistencia de Servico Dominical",
                color=ft.colors.LIGHT_BLUE_900,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
            ),
            bgcolor=ft.colors.WHITE,
            shadow_color=ft.colors.BLACK,
            shape=ft.RoundedRectangleBorder(radius=0),
            content=ft.Column(
                width=1000,
                expand=True,
                controls=[
                    ft.Column(
                        expand=1,
                        controls=[
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                controls=[
                                    service_name,
                                    error_date,
                                    no_complete,
                                    ft.Row(
                                        width=300,
                                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                        spacing=20,
                                        controls=[
                                            d_date,
                                            m_date,
                                            y_date,
                                        ]
                                    )
                                ]
                            )
                        ]
                    ),
                    ft.Container(
                        expand=4,
                        border=ft.border.all(2,color=ft.colors.LIGHT_BLUE_900),
                        content=ft.Column(
                            scroll='ALWAYS',
                            controls=[
                                ft.Row(
                                    expand=True,
                                    controls=[
                                        table_members
                                        
                                    ]
                                )
                            ]
                        )
                    )
                ]
            ),
            actions_alignment=ft.MainAxisAlignment.END,
            actions=[
                ft.ElevatedButton(
                    "Registrar",
                    on_click=lambda e : save_create(error_date,no_complete,Service(None,service_name.value,date_verify(d_date,m_date,y_date),len(member_asist)),member_asist),
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
        
        page.dialog=dialog
        page.dialog.open=True
        page.update()
        
        return dialog
    
    def save_create(error_date,no_complete,service,asist):
        if service.service_theme:
            if service.date != None:
                id_service=ModelService.create_service(service)
                for person in asist:
                    ModelAsistence.add_person(id_service,person)
                page.dialog.open=False
                ModelService.maintain_last_32_services()
                iter=ModelService.show_services()
                update_table(iter)
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
    #icono de registar un nuevo servicio
    icon.on_click= create_service
    #tabla de servicios
    
    #datatable y botones de paginas de tabla
    page_size = 8
    current_page = 0
    table=ft.DataTable(
        column_spacing=0,
        divider_thickness=0,
        horizontal_lines=ft.BorderSide(1,color=ft.colors.WHITE),
        expand=1,
        heading_row_color=ft.colors.ORANGE_ACCENT_700,
        heading_text_style=ft.TextStyle(color=ft.colors.WHITE, weight=ft.FontWeight.BOLD),
        data_text_style=ft.TextStyle(weight=ft.FontWeight.BOLD),
        columns=[
            ft.DataColumn(ft.Text("N°"), heading_row_alignment=ft.MainAxisAlignment.START),
            ft.DataColumn(ft.Text("Tema del Servicio"),heading_row_alignment=ft.MainAxisAlignment.CENTER),
            ft.DataColumn(ft.Text("Cantidad de Asistencias"), numeric=True, heading_row_alignment=ft.MainAxisAlignment.CENTER),
            ft.DataColumn(ft.Text("Fecha"),heading_row_alignment=ft.MainAxisAlignment.END),
        ],
    )
    
    def show_current_page():
        actual_page.value=f"{current_page + 1}"
        page.update()
    
    def next_page(e):
        nonlocal current_page
        if (current_page + 1) * page_size < len(ModelService.show_services()):
            current_page += 1
            update_table(ModelService.show_services())
            show_current_page()
    
    def prev_page(e):
        nonlocal current_page
        if current_page > 0:
            current_page -= 1
            update_table(ModelService.show_services())
            show_current_page()
    
    actual_page=ft.Text(
        "1",
        color=ft.colors.ORANGE_ACCENT_700,
        weight=ft.FontWeight.BOLD
    )
    
    #panel que incluye todo
    panel=ft.Column(
        spacing=20,
        controls=[
            ft.Row(
                expand=1,
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                controls=[
                    table
                ]
            ),
            ft.Row(
                alignment=ft.MainAxisAlignment.END,
                controls=[
                    ft.Row(
                        spacing=20,
                        controls=[
                            ft.Card(
                                color=ft.colors.WHITE,
                                scale=1.5,
                                elevation=5,
                                shape=ft.RoundedRectangleBorder(0),
                                rotate=3.14159265,
                                content=ft.Container(
                                    on_click=prev_page,
                                    content=ft.Icon(name=ft.icons.PLAY_ARROW_SHARP,color=ft.colors.ORANGE_ACCENT_700,),
                                )
                            ),
                            ft.Card(
                                shape=ft.RoundedRectangleBorder(0),
                                elevation=5,
                                color=ft.colors.WHITE,
                                scale=1.5,
                                content=ft.Container(
                                    alignment=ft.alignment.center,
                                    width=25,
                                    height=25,
                                    content=actual_page
                                    
                                    )
                            ),
                            ft.Card(
                                shape=ft.RoundedRectangleBorder(0),
                                color=ft.colors.WHITE,
                                elevation=5,
                                scale=1.5,
                                content=ft.Container(
                                    on_click=next_page,
                                    content=ft.Icon(name=ft.icons.PLAY_ARROW_SHARP,color=ft.colors.ORANGE_ACCENT_700,)
                                )
                            ),
                        ]
                    )
                ]
            )
        ]
    )
    
    contenedor= ft.Container(
        padding=ft.padding.only(10,10,15,10),
        content=panel
    )
    
    
    # funsion que actualiza la tabla
    def update_table(iter):
        #logica para las paginas de la tabla
        nonlocal current_page
        list_services_sorted = sorted(iter,key=lambda service: service[-2], reverse=True)
        start_index = current_page * page_size
        end_index = start_index + page_size
        page_services = list_services_sorted[start_index:end_index]
        table.rows.clear()
        #iteracion de las data row
        for i, service_feature in enumerate(page_services):
            service = Service(service_feature[0], service_feature[1], service_feature[2], service_feature[3])
            row_color = ft.colors.DEEP_ORANGE_50 if (i + 1) % 2 == 0 else None
            row_number = start_index + i + 1
            table.rows.append(ft.DataRow(
                color=row_color,
                on_long_press=open_info,
                data=service,
                cells=[
                    ft.DataCell(
                        ft.Container(
                            alignment=ft.alignment.center_left,
                            content=ft.Text(
                                f"{row_number}",
                                text_align=ft.TextAlign.START,
                                color=ft.colors.BLACK,
                            )
                        )
                    ),
                    ft.DataCell(
                        ft.Container(
                        alignment=ft.alignment.center,
                        content=ft.Text(
                                f"{service.service_theme}.",
                                text_align=ft.TextAlign.CENTER,
                                color=ft.colors.BLACK,
                                width=550,
                            )
                        ),
                    ),
                    ft.DataCell(
                        ft.Container(
                            alignment=ft.alignment.center,
                            content=ft.Text(
                                f"{int(service.num_asist)}",
                                color=ft.colors.BLACK,
                                text_align=ft.TextAlign.CENTER
                            )
                        ),
                    ),
                    ft.DataCell(
                        ft.Container(
                            alignment=ft.alignment.center_right,
                            content=ft.Text(
                                f"{datetime.datetime.strptime(service.date,'%Y-%m-%d %H:%M:%S').date().strftime('%d/%m/%Y')}",
                                color=ft.colors.BLACK,
                                text_align=ft.TextAlign.END
                            )
                        )
                    ),
                ],
            ))
        page.update()
    
    
    #ejecucion de la tabla por primera vez
    list_services = ModelService.show_services()
    list_services_sorted = sorted(list_services,key=lambda service: service[-2], reverse=True)
    start_index = current_page * page_size
    end_index = start_index + page_size
    page_services = list_services_sorted[start_index:end_index]
    
    for i,service_feature in enumerate(page_services):
        service=Service(service_feature[0],service_feature[1],service_feature[2],service_feature[3])
        row_color = ft.colors.DEEP_ORANGE_50 if (i+1) % 2 == 0 else None
        row_number = start_index + i + 1
        table.rows.append(ft.DataRow(
            on_long_press=open_info,
            data=service,
            color=row_color,
            cells=[
                ft.DataCell(
                    ft.Container(
                        alignment=ft.alignment.center_left,
                        content=ft.Text(
                            f"{row_number}",
                            text_align=ft.TextAlign.START,
                            color=ft.colors.BLACK,
                        )
                    )
                ),
                ft.DataCell(
                    ft.Container(
                    alignment=ft.alignment.center,
                    content=ft.Text(
                            f"{service.service_theme}.",
                            text_align=ft.TextAlign.CENTER,
                            color=ft.colors.BLACK,
                            width=550,
                        )
                    ),
                ),
                ft.DataCell(
                    ft.Container(
                        alignment=ft.alignment.center,
                        content=ft.Text(
                            f"{int(service.num_asist)}",
                            color=ft.colors.BLACK,
                            text_align=ft.TextAlign.CENTER
                        )
                    ),
                ),
                ft.DataCell(
                    ft.Container(
                        alignment=ft.alignment.center_right,
                        content=ft.Text(
                            f"{datetime.datetime.strptime(service.date,'%Y-%m-%d %H:%M:%S').date().strftime('%d/%m/%Y')}",
                            color=ft.colors.BLACK,
                            text_align=ft.TextAlign.END
                        )
                    )
                ),
            ],
        ),
    )
    
    page.update()
    
    
    return contenedor