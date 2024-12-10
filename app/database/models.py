import sqlite3 as sql
from .admin import Admin
import os


# Obtener la ruta absoluta del directorio actual
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
db_path = os.path.join(base_dir, 'tabernaculo.db').replace("\\","/")

class MoldelAdmin():
    @classmethod
    def login(self,admin):
        """
        Esta funcion recibe como argumente un objeto tipo Admin y comprueba si existe
        
        Retorna un objeto tipo Admin si existe el Email y None si no hay respuesta de la base de datos
        """
        try:
            print(db_path)
            print(db_path)
            conn=sql.connect(db_path)
            cursor=conn.cursor()
            instruccion = """SELECT * FROM Admins WHERE Email='{}'""".format(admin.email)
            cursor.execute(instruccion)
            result=cursor.fetchone()
            conn.commit()
            conn.close()
            if result != None:
                admin=Admin(result[0],result[1],(Admin.check_password(result[2],admin.password)),result[3])
                return admin
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def get_admin_by_id(self, admin_id):
        """
        Retorna un objeto Admin dado su ID.
        """
        try:
            conn = sql.connect(db_path)
            cursor = conn.cursor()
            instruccion = """SELECT * FROM Admins WHERE Id = ?"""
            cursor.execute(instruccion, (admin_id,))
            result = cursor.fetchone()
            conn.commit()
            conn.close()
            
            return Admin(result[0], result[1], result[2], result[3])  # Asumiendo que el constructor de Admin toma estos parámetros
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def create_admin(self, admin):
        """
        Crea un nuevo administrador en la base de datos.
        """
        try:
            conn = sql.connect(db_path)
            cursor = conn.cursor()
            instruccion = """INSERT INTO Admins (Email, Password, Name) VALUES (?, ?, ?)"""
            data = (admin.email,admin.password,admin.name)  # Asegúrate de encriptar la contraseña antes de guardarla
            cursor.execute(instruccion, data)
            conn.commit()
            conn.close()
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def edit_admin(self, admin):
        """
        Edita la información de un administrador existente en la base de datos.
        """
        try:
            print(admin.password)
            conn = sql.connect(db_path)
            cursor = conn.cursor()
            instruccion = f"""UPDATE Admins SET Email = '{admin.email}', Password = '{admin.password}', Name = '{admin.name}' WHERE Id = {admin.id}"""
            cursor.execute(instruccion)
            conn.commit()
            conn.close()
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def delete_admin(cls, admin_id):
        """
        Elimina un administrador de la base de datos utilizando su ID.
        """
        try:
            conn = sql.connect(db_path)
            cursor = conn.cursor()
            instruccion = """DELETE FROM Admins WHERE Id = ?"""
            cursor.execute(instruccion, (admin_id,))
            conn.commit()
            conn.close()
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def get_all_admins(self,id_admin):
        """
        Retorna una lista de todos los administradores.
        """
        try:
            conn = sql.connect(db_path)
            cursor = conn.cursor()
            instruccion = """SELECT * FROM Admins WHERE Id != ?"""
            cursor.execute(instruccion,(id_admin,))
            result = cursor.fetchall()
            conn.commit()
            conn.close()
            return [Admin(row[0], row[1], row[2], row[3]) for row in result]
        except Exception as ex:
            raise Exception(ex)

class ModelMember():
    @classmethod
    def dashboard(self):
        """
        retorna una lista con todos los datos de los miembros
        """
        try:
            conn=sql.connect(db_path)
            cursor=conn.cursor()
            instruccion = """SELECT * FROM Members"""
            cursor.execute(instruccion)
            result=cursor.fetchall()
            conn.commit()
            conn.close()
            return result
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def edit_member(self,member):
        try:
            conn=sql.connect(db_path)
            cursor=conn.cursor()
            instruccion =  """
                UPDATE Members SET 
                    DNI_member = ?,
                    Full_name = ?,
                    Age = ?,
                    Phone = ?,
                    Occupation = ?,
                    Occupation_place = ?,
                    Knowledge = ?,
                    Vehicle = ?,
                    Responsabilities = ?,
                    Civil_status = ?,
                    Childrens = ?,
                    Nationality = ?,
                    Herarchy = ?,
                    Situation = ?
                WHERE Id_member = ?
            """
            data = (
            member.DNI,
            member.full_name,
            member.age,
            member.phone,
            member.occupation,
            member.occupation_place,
            member.knowledge,
            member.vehicle,
            member.responsabilities,
            member.civil_status,
            member.childrens,
            member.nationality,
            member.hierarchy,
            member.situation,
            member.id_member)
            cursor.execute(instruccion,data)
            conn.commit()
            conn.close()
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def delete_member(self,id):
        try:
            conn=sql.connect(db_path)
            cursor=conn.cursor()
            instruccion = f"""DELETE FROM Members Where Id_member = {id} """
            cursor.execute(instruccion)
            conn.commit()
            conn.close()
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def create_member(self,member):
        try:
            conn=sql.connect(db_path)
            cursor=conn.cursor()
            instruccion = f"""INSERT INTO Members (
            DNI_member,
            Full_name,
            Age,
            Phone,
            Occupation,
            Occupation_place,
            Knowledge,
            Vehicle,
            Responsabilities,
            Civil_status,
            Childrens,
            Nationality,
            Herarchy,
            Situation
            ) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            data = (
            member.DNI,
            member.full_name,
            member.age,
            member.phone,
            member.occupation,
            member.occupation_place,
            member.knowledge,
            member.vehicle,
            member.responsabilities,
            member.civil_status,
            member.childrens,
            member.nationality,
            member.hierarchy,
            member.situation,
            )
            cursor.execute(instruccion,data)
            conn.commit()
            conn.close()
        except Exception as ex:
            raise Exception(ex)

class ModelEvent():
    @classmethod
    def events(self):
        """
        Retorna una lista con todos los datos de los Eventos
        """
        try:
            conn=sql.connect(db_path)
            cursor=conn.cursor()
            instruccion = """SELECT * FROM Events"""
            cursor.execute(instruccion)
            result=cursor.fetchall()
            conn.commit()
            conn.close()
            return result
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def create_event(self,event):
        """
        Retorna una lista con todos los datos de los Eventos
        """
        try:
            conn=sql.connect(db_path)
            cursor=conn.cursor()
            instruccion = """INSERT INTO Events (
                Id_event,
                Name_event,
                Kind_of_event,
                Leader,
                Matirials,
                Start_time,
                End_time,
                Info
                ) VALUES (?,?,?,?,?,?,?,?)"""
            data = (
                event.id_event,
                event.name_event,
                event.kind_event,
                event.leader,
                event.matirials,
                event.start_time,
                event.end_time,
                event.info
            )
            cursor.execute(instruccion,data)
            result=cursor.fetchall()
            conn.commit()
            conn.close()
            return result
        except Exception as ex:
            raise Exception(ex)
    
    
    @classmethod
    def edit_event(self, event):
        """
        Modifica todos los datos de un evento en la base de datos.
        """
        try:
            conn = sql.connect(db_path)
            cursor = conn.cursor()
            instruccion = """
                UPDATE Events SET
                    Name_event = ?,
                    kind_of_event = ?,
                    Leader = ?,
                    Matirials = ?,
                    Start_time = ?,
                    End_time = ?,
                    Info = ?
                WHERE Id_event = ?
            """
            
            data = (
                event.name_event,
                event.kind_event,
                event.leader,
                event.matirials,
                event.start_time,
                event.end_time,
                event.info,
                event.id_event  # Usamos el id_event para identificar qué evento modificar
            )
            
            cursor.execute(instruccion, data)
            conn.commit()
            conn.close()
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def delete_event(self, id_event):
        """
        Elimina un evento de la base de datos utilizando su id_event.
        """
        try:
            conn = sql.connect(db_path)
            cursor = conn.cursor()
            instruccion = f"DELETE FROM Events WHERE id_event = ?"
            cursor.execute(instruccion, (id_event,))
            conn.commit()
            conn.close()
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def persons_event(self,id_event):
        """
        Retorna una lista con todos los nombres de miembros de un evento
        """
        try:
            conn=sql.connect(db_path)
            cursor=conn.cursor()
            instruccion = f"""SELECT m.Full_name, m.Id_member FROM Members_in_events i
                JOIN Members m ON i.Id_member = m.Id_member
                JOIN Events e ON i.Id_event = e.Id_event WHERE e.Id_event = {id_event}
                """
            cursor.execute(instruccion)
            result=cursor.fetchall()
            conn.commit()
            conn.close()
            return result
        except Exception as ex:
            raise Exception(ex)

class ModelInvited():
    
    
    @classmethod
    def actual_event(self):
        """
        Inserta un miembro a un evento
        """
        try:
            conn=sql.connect(db_path)
            cursor=conn.cursor()
            instruccion = f"""SELECT Id_event FROM Events ORDER BY Id_event DESC LIMIT 1
                """
            cursor.execute(instruccion)
            result=cursor.fetchone()
            conn.commit()
            conn.close()
            return result[0]
        except Exception as ex:
            raise Exception(ex)
        
    
    @classmethod
    def add_person(self,id_event,id_person):
        """
        Inserta un miembro a un evento
        """
        try:
            conn=sql.connect(db_path)
            cursor=conn.cursor()
            instruccion = f"""INSERT INTO Members_in_events (Id_member, Id_event) VALUES ({id_person},{id_event})
                """
            cursor.execute(instruccion)
            conn.commit()
            conn.close()
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def delete_persons_from_event(self,id_event):
        """
        Elimina un miembro de un evento en la base de datos utilizando su id_member y id_event.
        """
        try:
            conn = sql.connect(db_path)
            cursor = conn.cursor()
            instruccion = """DELETE FROM Members_in_events WHERE Id_event = ?"""
            cursor.execute(instruccion, (id_event,))
            conn.commit()
            conn.close()
        except Exception as ex:
            raise Exception(ex)

class ModelService():
    @classmethod
    def show_services(self):
        """
        Muestra los servicios de la base de datos
        """
        try:
            conn=sql.connect(db_path)
            cursor=conn.cursor()
            instruccion = """SELECT * FROM Services"""
            cursor.execute(instruccion)
            result=cursor.fetchall()
            conn.commit()
            conn.close()
            return result
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def create_service(self,service):
        """
        Crea un servicio pasandole un objeto tipo servicio
        """
        try:
            conn = sql.connect(db_path)
            cursor = conn.cursor()
            instruccion = """INSERT INTO Services (Service_theme, Num_asist, Date) VALUES (?, ?, ?)"""
            data = (service.service_theme, service.num_asist, service.date)
            cursor.execute(instruccion, data)
            id_service=cursor.lastrowid
            conn.commit()
            conn.close()
            return id_service
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def delete_service(self, id_service):
        """
        Elimina un servicio de la base de datos utilizando su id_service.
        """
        try:
            conn = sql.connect(db_path)
            cursor = conn.cursor()
            instruccion = """DELETE FROM Services WHERE Id_service = ?"""
            cursor.execute(instruccion, (id_service,))
            conn.commit()
            conn.close()
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def maintain_last_32_services(self):
        """
        Elimina servicios de manera que siempre se mantengan los últimos 32 registrados,
        y también elimina las asistencias asociadas a esos servicios.
        """
        try:
            conn = sql.connect(db_path)
            cursor = conn.cursor()
            # Contar el número total de servicios
            cursor.execute("SELECT COUNT(*) FROM Services")
            total_services = cursor.fetchone()[0]
            # Si hay más de 32 servicios, eliminar los más antiguos
            if total_services > 32:
                services_to_delete = total_services - 32
                
                # Obtener los IDs de los servicios a eliminar
                cursor.execute(""" 
                    SELECT Id_service FROM Services 
                    ORDER BY Date,Id_service ASC
                    LIMIT ?
                """, (services_to_delete,))
                
                services_ids = cursor.fetchall()
                
                # Eliminar las asistencias asociadas a esos servicios
                if services_ids:
                    ids = [service[0] for service in services_ids]  # Extraer los IDs de la lista de tuplas
                    cursor.execute(""" 
                        DELETE FROM Asists 
                        WHERE Id_service IN ({})
                    """.format(','.join('?' * len(ids))), ids)
                
                # Eliminar los servicios más antiguos
                cursor.execute(""" 
                    DELETE FROM Services 
                    WHERE Id_service IN ({})
                """.format(','.join('?' * len(ids))), ids)
                print(ids)
                
                conn.commit()
            conn.close()
        except Exception as ex:
            raise Exception(ex)

class ModelAsistence():
    
    @classmethod
    def get_attendees_by_service_id(self, id_service):
        """
        Retorna el DNI y el nombre completo de las personas que asistieron a un servicio
        dado el ID del servicio.
        """
        try:
            conn = sql.connect(db_path)
            cursor = conn.cursor()
            instruccion = """
                SELECT m.DNI_member, m.Full_name 
                FROM Asists a
                JOIN Members m ON a.Id_member = m.Id_member
                WHERE a.Id_service = ?
            """
            cursor.execute(instruccion, (id_service,))
            result = cursor.fetchall()
            conn.commit()
            conn.close()
            return result
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def add_person(self,id_service,id_member):
        """
        Inserta un miembro a un servicio
        """
        try:
            conn=sql.connect(db_path)
            cursor=conn.cursor()
            instruccion = f"""INSERT INTO Asists (Id_member, Id_service) VALUES ({id_member},{id_service})
                """
            cursor.execute(instruccion)
            conn.commit()
            conn.close()
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def delete_persons_from_service(self,id_service):
        """
        Elimina un miembro de un evento en la base de datos utilizando su id_member y id_event.
        """
        try:
            conn = sql.connect(db_path)
            cursor = conn.cursor()
            instruccion = """DELETE FROM Asists WHERE Id_service = ?"""
            cursor.execute(instruccion, (id_service,))
            conn.commit()
            conn.close()
        except Exception as ex:
            raise Exception(ex)




