from flask_restful import Api
from flask_jwt_extended import JWTManager
from faker import Faker
import random
import os
from flask_cors import CORS
import time
from sqlalchemy import DateTime, Date
from sqlalchemy.sql import func
from datetime import date
from datetime import datetime

from flask import Flask
import os
def create_app(config_name, settings_module='config.ProductionConfig'):
    app=Flask(__name__)
    app.config.from_object(settings_module)
    return app

settings_module = os.getenv('APP_SETTINGS_MODULE','config.ProductionConfig')
application = create_app('default', settings_module)
app_context=application.app_context()
app_context.push()



import enum
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from sqlalchemy import DateTime, Date
from sqlalchemy.sql import func

db = SQLAlchemy()

class Estado(enum.Enum):
    ACTIVO = 1
    INACTIVO = 2

class Nivel_Estudios(enum.Enum):
    PREGRADO = 1
    ESPECIALIZACION = 2
    MAESTRIA = 3
    DOCTORADO = 4
    DIPLOMADOS = 5
    CURSOS = 6

class Calificacion(enum.Enum):
    EXCELENTE = 1
    BUENA = 2
    REGULAR = 3
    MALA = 4

class Entrevistas(db.Model):
    __tablename__ = 'entrevistas'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_cand = db.Column(db.Integer, nullable=False)
    idPerfilProy = db.Column(db.Integer, nullable=False)
    cuando = db.Column(db.DateTime(timezone=True), nullable=True, default=func.now())  #datetime.datetime.utcnow
    contacto = db.Column(db.Unicode(120), nullable=False, default='MISSING')
    calificacion = db.Column(db.Enum(Calificacion), nullable=True)  
    valoracion = db.Column(db.Integer, nullable=True)
    anotaciones = db.Column(db.Unicode(2000), nullable=True,)

    def __init__(self, *args, **kw):
        super(Entrevistas, self).__init__(*args, **kw)

    def get_id(self):
        return self.id

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return Entrevistas.query.get(id)

    @staticmethod
    def get_count():
        return Entrevistas.query.count()
    
    @staticmethod
    def get_by_idUser(idCand):
        return Entrevistas.query.filter_by(id_cand=idCand).all()
    
    @staticmethod
    def get_by_idPerfilProy(idPerfilProy):
        return Entrevistas.query.filter_by(idPerfilProy=idPerfilProy).all()

    @staticmethod
    def getAll():
        return Entrevistas.query.all()
    
class CalifADiccionario(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        else:
            return value.name #{'llave':value.name, 'valor':value.value} #{value.name}  #{'llave':value.name, 'valor':value.value}
         
class EntrevistasSchema(SQLAlchemyAutoSchema):
    calificacion=CalifADiccionario(attribute=('calificacion'))
    class Meta:
        model = Entrevistas
        include_relationships = True
        load_instance = True

entrevistas_schema = EntrevistasSchema()


class EvalMensual(db.Model):
    __tablename__ = 'evalmensual'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_cand = db.Column(db.Integer, nullable=False)
    idPerfilProy = db.Column(db.Integer, nullable=False)
    anno = db.Column(db.Integer, nullable=False)
    strmes = db.Column(db.Unicode(15), nullable=False)
    mes = db.Column(db.Integer, nullable=False)
    calificacion = db.Column(db.Enum(Calificacion), nullable=False, default=Calificacion.REGULAR)  
    valoracion = db.Column(db.Integer, nullable=True, default=0)
    nota = db.Column(db.Unicode(2000), nullable=False, default='MISSING')

    def __init__(self, *args, **kw):
        super(EvalMensual, self).__init__(*args, **kw)

    def get_id(self):
        return self.id

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return EvalMensual.query.get(id)

    @staticmethod
    def get_count():
        return EvalMensual.query.count()
    
    @staticmethod
    def getAll():
        return EvalMensual.query.all()
    
    @staticmethod
    def get_by_idUser(idCand):
        return EvalMensual.query.filter_by(id_cand=idCand).all()
    
    @staticmethod
    def get_by_idPerfilProy(idPerfilProy2):
        return EvalMensual.query.filter_by(idPerfilProy=idPerfilProy2
                                        ).order_by(EvalMensual.anno.desc(), EvalMensual.mes.desc()
                                        ).all()

class EvalMensualSchema(SQLAlchemyAutoSchema):
    calificacion=CalifADiccionario(attribute=('calificacion'))
    class Meta:
        model = EvalMensual
        include_relationships = True
        load_instance = True

evalmensual_schema = EvalMensualSchema()


class Empresa(db.Model):
    __tablename__ = 'empresas'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.Unicode(128), nullable=False, default='MISSING', unique=True)
    tipo = db.Column(db.Unicode(128), nullable=False, default='MISSING')
    correo = db.Column(db.Unicode(128), nullable=False, unique=True)
    celular = db.Column(db.Unicode(128), nullable=True)
    contacto = db.Column(db.Unicode(128), default='MISSING')
    pais = db.Column(db.Unicode(128))
    ciudad = db.Column(db.Unicode(128))
    direccion = db.Column(db.Unicode(128))
    id_usuario = db.Column(db.Integer, nullable=False, default=0, unique=True)
    is_active = db.Column(db.Boolean, default=True)
    estado = db.Column(db.Enum(Estado), nullable=False, default=Estado.ACTIVO)  

    def __init__(self, *args, **kw):
        super(Empresa, self).__init__(*args, **kw)

    def get_id(self):
        return self.id

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return Empresa.query.get(id)

    @staticmethod
    def get_by_email(email):
        return Empresa.query.filter_by(email=email).first()

    @staticmethod
    def get_count():
        return Empresa.query.count()
    
    @staticmethod
    def get_by_idUser(idUser):
        return Empresa.query.filter_by(id_usuario=idUser).first()
    
    @staticmethod
    def getAll():
        return Empresa.query.all()

class EnumADiccionario(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        else:
            return value.name #{'llave':value.name, 'valor':value.value} #{value.name}  #{'llave':value.name, 'valor':value.value}
    
class EmpresaSchema(SQLAlchemyAutoSchema):
    estado=EnumADiccionario(attribute=('estado'))
    class Meta:
        model = Empresa
        include_relationships = True
        load_instance = True

empresa_schema = EmpresaSchema()

#fecharecogida = datetime.strptime('10/11/2016', "%d/%m/%Y"),
class Proyecto(db.Model):
    __tablename__ = 'proyectos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_emp = db.Column(db.Integer, nullable=False)
    nombre = db.Column(db.Unicode(128), nullable=False, default='MISSING')
    fecha_inicio = db.Column(Date(), nullable=True, default=func.now())
    descripcion = db.Column(db.Unicode(255), nullable=False, default='MISSING')


    def __init__(self, *args, **kw):
        super(Proyecto, self).__init__(*args, **kw)

    def get_id(self):
        return self.id

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return Proyecto.query.get(id)

    @staticmethod
    def get_count():
        return Proyecto.query.count()

    @staticmethod
    def get_by_empresa(id_emp):
        return Proyecto.query.filter(Proyecto.id_emp==id_emp).all()
    
    @staticmethod
    def getAll():
        return Proyecto.query.all()

 
class ProyectoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Proyecto
        include_relationships = True
        load_instance = True

proyecto_schema = ProyectoSchema()


class PerfilesProyecto(db.Model):
    __tablename__ = 'perfiles_proyectos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.Unicode(128), nullable=False, default='MISSING')
    id_proy = db.Column(db.Integer, nullable=False)
    id_perfil = db.Column(db.Integer, nullable=False)
    id_cand = db.Column(db.Integer, nullable=False, default=0)
    fecha_asig = db.Column(Date(), nullable=True)

    def __init__(self, *args, **kw):
        super(PerfilesProyecto, self).__init__(*args, **kw)

    def get_id(self):
        return self.id

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return PerfilesProyecto.query.get(id)

    @staticmethod
    def get_count():
        return PerfilesProyecto.query.count()
    
    @staticmethod
    def get_by_idProy(idProy):
        return PerfilesProyecto.query.filter_by(id_proy=idProy).all()
    
    @staticmethod
    def getAll():
        return PerfilesProyecto.query.all()
    
    @staticmethod
    def get_count_assign():
        return PerfilesProyecto.query.filter(PerfilesProyecto.id_cand!=0).count()

    
class PerfilesProyectoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = PerfilesProyecto
        include_relationships = True
        load_instance = True

perfiles_proyecto_schema = PerfilesProyectoSchema()


class EmpleadoEmpresa(db.Model):
    __tablename__ = 'empleado_empresa'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_emp = db.Column(db.Integer, nullable=False)
    nombre = db.Column(db.Unicode(128), nullable=False, default='MISSING')
    id_perfil = db.Column(db.Integer, nullable=True)


    def __init__(self, *args, **kw):
        super(EmpleadoEmpresa, self).__init__(*args, **kw)

    def get_id(self):
        return self.id

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return EmpleadoEmpresa.query.get(id)

 
class EmpleadoEmpresaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = EmpleadoEmpresa
        include_relationships = True
        load_instance = True

empleado_empresa_schema = EmpleadoEmpresaSchema()


class Encargado(db.Model):
    __tablename__ = 'encargado'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_proy = db.Column(db.Integer, nullable=False)
    id_empleado = db.Column(db.Integer, nullable=False)
    rol = db.Column(db.Unicode(128), nullable=False, default='MISSING')


    def __init__(self, *args, **kw):
        super(Encargado, self).__init__(*args, **kw)

    def get_id(self):
        return self.id

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return Encargado.query.get(id)

 
class EncargadoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Encargado
        include_relationships = True
        load_instance = True

encargado_schema = EncargadoSchema()

db.init_app(application)
db.create_all()


CORS(application)



from datetime import datetime
from datetime import timedelta
import pytz
from dateutil import parser
import math
import random
import uuid
from flask import request, current_app
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc, asc

import os
import requests
import json
from faker import Faker

from flask_jwt_extended import get_jwt_identity, jwt_required, create_access_token, verify_jwt_in_request
from flask_jwt_extended import get_jwt
from flask_jwt_extended.exceptions import NoAuthorizationError
from functools import wraps
from jwt import InvalidSignatureError, ExpiredSignatureError, InvalidTokenError

empresa_schema = EmpresaSchema()
proyecto_schema = ProyectoSchema()
perfilesproyecto_schema = PerfilesProyectoSchema()

access_token_expires = timedelta(minutes=120)

def authorization_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            print("Authorization Required")
            try:
                verify_jwt_in_request()  
                try:
                    req_headers = request.headers  #{"Authorization": f"Bearer {lst[1]}"}
                    roles= {"roles":["EMPRESA","EMPLEADO_ABC"]}
                    r = requests.post(f"{current_app.config['HOST_PORT_AUTH']}/auth/me", headers=req_headers, json=roles)
                    if r.json().get("authorization") is None:
                        return {"Error:": "Autorizacion Negada por Autoridad. "}, 401
                    else:
                        lstTokens=request.path.split(sep='/')    
                        lstTokens[len(lstTokens)-1]
                        user_url=lstTokens[len(lstTokens)-1]
                        if r.json().get("id")==int(user_url):
                            return fn(*args, **kwargs)       
                        else:
                            return {"Error:": "Inconsistencia en la peticion"}, 401
                except Exception as inst:
                    print(type(inst))    # the exception instance
                    print(inst)
                    return {"Error:": "Usuario Desautorizado. No se pudo verificar con Autoridad."}, 401
            except ExpiredSignatureError:
                return {"Error:": "Token Expired"}, 401
            except InvalidSignatureError:
                return {"Error:": "Signature verification failed"}, 401
            except NoAuthorizationError:
                return {"Error:": "Missing JWT"}, 401
            except Exception as inst:
                print("excepcion")
                print(type(inst))    # the exception instance
                print(inst)
                return {"Error:": "Usuario desautorizado. Error General."}, 401
        return decorator
    return wrapper

def empresa_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            try:
                verify_jwt_in_request()  
                claims = get_jwt()  #claims = get_jwt_claims()
                try:
                    print(claims)
                    if claims['MyUserType'] != 'EMPRESA':
                        return {"Error:": "Usuario Desautorizado"}, 401
                    else:
                        return fn(*args, **kwargs)                
                except Exception as inst:
                   return {"Error:": "Usuario Desautorizado"}, 401
            except ExpiredSignatureError:
                return {"Error:": "Token Expired"}, 401
            except InvalidSignatureError:
                return {"Error:": "Signature verification failed"}, 401
            except NoAuthorizationError:
                return {"Error:": "Missing JWT"}, 401
            except Exception as inst:
                print("excepcion")
                print(type(inst))    # the exception instance
                print(inst)
                return {"Error:": "Usuario Desautorizado"}, 401
        return decorator
    return wrapper

class VistaEmpresaUsuario(Resource):
    @authorization_required()
    def get(self, id_usuario):
        print("Consulta Empresa Usuario")
        try:
            empresa = Empresa.get_by_idUser(id_usuario)
        except Exception as inst:
            print("excepcion")
            print(type(inst))    # the exception instance
            print(inst)
            return {"Error:": "Error en el Servidor"}, 500
        return empresa_schema.dump(empresa), 200

class VistaEntrevistasPuesto(Resource):  #'/empresas/proyectos/perfiles/entrevistas/<int:id_proyperfil>
    def get(self, id_proyperfil):
        print("Lista Entrevistas de un Puesto")
        objPerfilProy=PerfilesProyecto.get_by_id(id_proyperfil)
        id_perfil=objPerfilProy.id_perfil
        id_proy=objPerfilProy.id_proy
        lstEntrevistas=db.session.query(Empresa.nombre.label('nom_empresa'), 
                        Proyecto.nombre.label('nom_proyecto'),
                        PerfilesProyecto.nombre.label('nom_perfil'),
                        Entrevistas.id,
                        Entrevistas.id_cand,
                        Entrevistas.contacto,
                        Entrevistas.cuando,
                        Entrevistas.calificacion,
                        Entrevistas.valoracion,
                        Entrevistas.anotaciones,
                        ).filter(PerfilesProyecto.id_perfil==id_perfil
                        ).filter(PerfilesProyecto.id_proy==id_proy
                        ).filter(Entrevistas.idPerfilProy==PerfilesProyecto.id
                        ).filter(PerfilesProyecto.id_proy==Proyecto.id
                        ).filter(Proyecto.id_emp==Empresa.id
                        ).order_by(Empresa.nombre.asc(), Proyecto.nombre.asc(), PerfilesProyecto.nombre.asc()
                        ).all()
        
        for e in lstEntrevistas:
            print(e)
        data = []
        i=0
        for e in lstEntrevistas:
            i=i+1
            ev_data = {
                'Num': i,
                'nom_empresa': e.nom_empresa,
                'nom_proyecto': e.nom_proyecto,
                'nom_perfil': e.nom_perfil,
                'id': e.id,
                'id_cand': e.id_cand,
                'cuando': e.cuando.isoformat() if e.cuando else '',
                'contacto': e.contacto,
                'calificacion': e.calificacion.name if e.calificacion else '',
                'valoracion': e.valoracion,
                'anotaciones': e.anotaciones,
                'candidato': ''
            }
            data.append(ev_data)
        return {'Entrevistas': data, 'totalCount': i}, 200
        
class VistaEntrevistasPuestoOriginal(Resource):  #'/empresas/proyectos/perfiles/entrevistas/<int:id_proyperfil>
    def get(self, id_proyperfil):
        print("Lista Entrevistas de un Puesto")
        lstEntrevistas=db.session.query(Empresa.nombre.label('nom_empresa'), 
                        Proyecto.nombre.label('nom_proyecto'),
                        PerfilesProyecto.nombre.label('nom_perfil'),
                        Entrevistas.id,
                        Entrevistas.id_cand,
                        Entrevistas.contacto,
                        Entrevistas.cuando,
                        Entrevistas.calificacion,
                        Entrevistas.valoracion,
                        Entrevistas.anotaciones,
                        ).filter(Entrevistas.idPerfilProy==id_proyperfil
                        ).filter(Entrevistas.idPerfilProy==PerfilesProyecto.id
                        ).filter(PerfilesProyecto.id_proy==Proyecto.id
                        ).filter(Proyecto.id_emp==Empresa.id
                        ).order_by(Empresa.nombre.asc(), Proyecto.nombre.asc(), PerfilesProyecto.nombre.asc()
                        ).all()
        for e in lstEntrevistas:
            print(e)
        data = []
        i=0
        for e in lstEntrevistas:
            i=i+1
            ev_data = {
                'Num': i,
                'nom_empresa': e.nom_empresa,
                'nom_proyecto': e.nom_proyecto,
                'nom_perfil': e.nom_perfil,
                'id': e.id,
                'id_cand': e.id_cand,
                'cuando': e.cuando.isoformat() if e.cuando else '',
                'contacto': e.contacto,
                'calificacion': e.calificacion.name if e.calificacion else '',
                'valoracion': e.valoracion,
                'anotaciones': e.anotaciones,
                'candidato': ''
            }
            data.append(ev_data)
        return {'Entrevistas': data, 'totalCount': i}, 200

class VistaEntrevistasResultado(Resource): #'/entrevistas/<int:id_entrevista>'
    def post(self, id_entrevista):
        print("Guardar Resultados de una entrevista")
        print(id_entrevista)
        print("json: ")
        print(request.json)
        try:
            entrevista=Entrevistas.query.filter(Entrevistas.id==id_entrevista).first()
            if entrevista is None:
               return {"mensaje": "Entrevista no se pudo actualizar: el id de la entrevista no existe."}, 400
            entrevista.anotaciones=request.json.get("anotaciones")
            if entrevista.anotaciones=='':
               return {"mensaje": "Entrevista no se pudo actualizar: las anotaciones no fueron suministradas."}, 400
            entrevista.calificacion=Calificacion[request.json.get("calificacion")] #Calificacion[request.get_json()['valuation']]
            db.session.add(entrevista)
            db.session.commit()
            return entrevistas_schema.dump(entrevista), 200    #OJO CON ESTE CAMBIO
        except Exception as inst:
            db.session.rollback()
            print(type(inst))    # the exception instance
            #print(inst)
            print("Entrevista no se pudo actualizar.")
            return {"Mensaje: ":"Error: Entrevista no se pudo actualizar."+str(type(inst))}, 500

    def get(self, id_entrevista):
        print("Obtener Resultados de una entrevista")
        print(id_entrevista)
        e=db.session.query(Empresa.nombre.label('nom_empresa'), 
                        Proyecto.nombre.label('nom_proyecto'),
                        PerfilesProyecto.nombre.label('nom_perfil'),
                        PerfilesProyecto.id_perfil,
                        PerfilesProyecto.id.label('id_perfilproy'),
                        Entrevistas.id,
                        Entrevistas.id_cand,
                        Entrevistas.contacto,
                        Entrevistas.cuando,
                        Entrevistas.calificacion,
                        Entrevistas.valoracion,
                        Entrevistas.anotaciones,
                        ).filter(Entrevistas.id==id_entrevista
                        ).filter(Entrevistas.idPerfilProy==PerfilesProyecto.id
                        ).filter(PerfilesProyecto.id_proy==Proyecto.id
                        ).filter(Proyecto.id_emp==Empresa.id
                        ).first()
        print("Despues Consulta")
        if e is None:
            print("e is None")
        else:
            print("e is Not None")
        ev_data = {
            'nom_empresa': e.nom_empresa,
            'nom_proyecto': e.nom_proyecto,
            'nom_perfil': e.nom_perfil,
            'id_perfil': e.id_perfil,
            'id_perfilproy': e.id_perfilproy,
            'id': e.id,
            'id_cand': e.id_cand,
            'cuando': e.cuando.isoformat() if e.cuando else '',
            'calificacion': e.calificacion.name if e.calificacion else '',
            'valoracion': e.valoracion,
            'anotaciones': e.anotaciones,
            'candidato': '',
            'contacto': e.contacto
        }
        print("ev_data")
        print(ev_data)
        return {"Entrevista": ev_data}, 200
    
class VistaEntrevistasCandidatos(Resource):
    def post(self, id_cand):
        print("Obteniendo Las Entrevistas de los Candidatos")
        print("id_cand")
        print(id_cand)
        print("json: ")
        print(request.json)
        max=request.json.get("max", 50)
        num_pag=request.json.get("num_pag", 1)
        order=request.json.get("order", "ASC")
        empresa=request.json.get("empresa", "Solidaria")
        proyecto=request.json.get("proyecto", "Solidaria")
        perfil=request.json.get("perfil", "Solidaria")
        contacto=request.json.get("contacto", "")
        candidato=request.json.get("candidato", "Solidaria")
        inicio=request.json.get("inicio", "")
        fin=request.json.get("fin", "")

        if inicio==None or inicio=='':
            fecha_inicio = datetime.strptime('1970-01-01 00:00:00',"%Y-%m-%d %H:%M:%S")
        if fin==None or fin=='':
            fecha_fin = datetime.strptime('3000-01-01 00:00:00',"%Y-%m-%d %H:%M:%S")
        if inicio!=None and fin!=None and inicio!='' and fin!='':
            fecha_inicio = parser.parse(inicio)
            fecha_fin = parser.parse(fin)
            fecha_fin=fecha_fin+timedelta(hours=23)
            fecha_fin=fecha_fin+timedelta(minutes=59)

        numEntrevistas=db.session.query(Entrevistas.id, 
                                        Entrevistas.id_cand,
                                        Entrevistas.idPerfilProy,
                                        Entrevistas.cuando,
                                        Entrevistas.contacto,
                                        Entrevistas.calificacion,
                                        Entrevistas.anotaciones,
                                        Entrevistas.valoracion,
                                        PerfilesProyecto.id_perfil,
                                        Empresa.nombre.label('nom_empresa'), 
                                        Proyecto.nombre.label('nom_proyecto'),
                                        PerfilesProyecto.nombre.label('nom_perfil'),
                        ).filter(Entrevistas.idPerfilProy==PerfilesProyecto.id
                        ).filter(PerfilesProyecto.id_proy==Proyecto.id
                        ).filter(Proyecto.id_emp==Empresa.id
                        ).filter(Entrevistas.id_cand==id_cand
                        ).filter(Empresa.nombre.ilike(f'%{empresa}%')
                        ).filter(Proyecto.nombre.ilike(f'%{proyecto}%')
                        ).filter(PerfilesProyecto.nombre.ilike(f'%{perfil}%')
                        ).filter(Entrevistas.contacto.ilike(f'%{contacto}%') 
                        ).filter(Entrevistas.cuando>=fecha_inicio 
                        ).filter(Entrevistas.cuando<=fecha_fin
                        ).count()
        
        lstEntrevistas=db.session.query(Entrevistas.id, 
                                        Entrevistas.id_cand,
                                        Entrevistas.idPerfilProy,
                                        Entrevistas.cuando,
                                        Entrevistas.contacto,
                                        Entrevistas.calificacion,
                                        Entrevistas.anotaciones,
                                        Entrevistas.valoracion,
                                        PerfilesProyecto.id_perfil,
                                        Empresa.nombre.label('nom_empresa'), 
                                        Proyecto.nombre.label('nom_proyecto'),
                                        PerfilesProyecto.nombre.label('nom_perfil'),
                        ).filter(Entrevistas.idPerfilProy==PerfilesProyecto.id
                        ).filter(PerfilesProyecto.id_proy==Proyecto.id
                        ).filter(Proyecto.id_emp==Empresa.id
                        ).filter(Entrevistas.id_cand==id_cand
                        ).filter(Empresa.nombre.ilike(f'%{empresa}%')
                        ).filter(Proyecto.nombre.ilike(f'%{proyecto}%')
                        ).filter(PerfilesProyecto.nombre.ilike(f'%{perfil}%')
                        ).filter(Entrevistas.contacto.ilike(f'%{contacto}%') 
                        ).filter(Entrevistas.cuando>=fecha_inicio 
                        ).filter(Entrevistas.cuando<=fecha_fin
                        ).order_by(Empresa.nombre.asc(), Proyecto.nombre.asc(), PerfilesProyecto.nombre.asc()
                        ).paginate(page=num_pag, per_page=max, error_out=False)
            
        print("Lista de Entrevistas")
        for p in lstEntrevistas:
            print(p.nom_empresa, p.nom_proyecto, p.nom_perfil, p.id, p.id_perfil, p.id_cand )
        data = []
        i=0
        for p in lstEntrevistas:
            i=i+1
            ev_data = {
                'Num':(num_pag-1)*max + i,
                'cuando': p.cuando.isoformat() if p.cuando else '',
                'calificacion': p.calificacion.name if p.calificacion else '',
                'anotaciones': p.anotaciones,
                'nom_empresa': p.nom_empresa,
                'nom_proyecto': p.nom_proyecto,
                'nom_perfil': p.nom_perfil,
                'contacto': p.contacto,
                'id': p.id,
                'idPerfilProy': p.idPerfilProy,
                'id_perfil': p.id_perfil,
                'id_cand': p.id_cand,
                'candidato': '',
                'valoracion': p.valoracion
            }
            data.append(ev_data)
        return {'Entrevistas': data, 'totalCount': numEntrevistas}, 200

    def get(self, id_cand):
        print("GET: Obteniendo Las Entrevistas de los Candidatos")
        print("id_cand")
        print(id_cand)
        print("json: ")
        print(request.json)
        max=request.json.get("max", 50)
        num_pag=request.json.get("num_pag", 1)
        order=request.json.get("order", "ASC")
        empresa=request.json.get("empresa", "Solidaria")
        proyecto=request.json.get("proyecto", "Solidaria")
        perfil=request.json.get("perfil", "Solidaria")
        contacto=request.json.get("contacto", "")
        candidato=request.json.get("candidato", "Solidaria")
        inicio=request.json.get("inicio", "")
        fin=request.json.get("fin", "")

        if inicio==None or inicio=='':
            fecha_inicio = datetime.strptime('1970-01-01 00:00:00',"%Y-%m-%d %H:%M:%S")
        if fin==None or fin=='':
            fecha_fin = datetime.strptime('3000-01-01 00:00:00',"%Y-%m-%d %H:%M:%S")
        if inicio!=None and fin!=None and inicio!='' and fin!='':
            fecha_inicio = parser.parse(inicio)
            fecha_fin = parser.parse(fin)
            fecha_fin=fecha_fin+timedelta(hours=23)
            fecha_fin=fecha_fin+timedelta(minutes=59)

        numEntrevistas=db.session.query(Entrevistas.id, 
                                        Entrevistas.id_cand,
                                        Entrevistas.idPerfilProy,
                                        Entrevistas.cuando,
                                        Entrevistas.contacto,
                                        Entrevistas.calificacion,
                                        Entrevistas.anotaciones,
                                        Entrevistas.valoracion,
                                        PerfilesProyecto.id_perfil,
                                        Empresa.nombre.label('nom_empresa'), 
                                        Proyecto.nombre.label('nom_proyecto'),
                                        PerfilesProyecto.nombre.label('nom_perfil'),
                        ).filter(Entrevistas.idPerfilProy==PerfilesProyecto.id
                        ).filter(PerfilesProyecto.id_proy==Proyecto.id
                        ).filter(Proyecto.id_emp==Empresa.id
                        ).filter(Entrevistas.id_cand==id_cand
                        ).filter(Empresa.nombre.ilike(f'%{empresa}%')
                        ).filter(Proyecto.nombre.ilike(f'%{proyecto}%')
                        ).filter(PerfilesProyecto.nombre.ilike(f'%{perfil}%')
                        ).filter(Entrevistas.contacto.ilike(f'%{contacto}%') 
                        ).filter(Entrevistas.cuando>=fecha_inicio 
                        ).filter(Entrevistas.cuando<=fecha_fin
                        ).count()
        
        lstEntrevistas=db.session.query(Entrevistas.id, 
                                        Entrevistas.id_cand,
                                        Entrevistas.idPerfilProy,
                                        Entrevistas.cuando,
                                        Entrevistas.contacto,
                                        Entrevistas.calificacion,
                                        Entrevistas.anotaciones,
                                        Entrevistas.valoracion,
                                        PerfilesProyecto.id_perfil,
                                        Empresa.nombre.label('nom_empresa'), 
                                        Proyecto.nombre.label('nom_proyecto'),
                                        PerfilesProyecto.nombre.label('nom_perfil'),
                        ).filter(Entrevistas.idPerfilProy==PerfilesProyecto.id
                        ).filter(PerfilesProyecto.id_proy==Proyecto.id
                        ).filter(Proyecto.id_emp==Empresa.id
                        ).filter(Entrevistas.id_cand==id_cand
                        ).filter(Empresa.nombre.ilike(f'%{empresa}%')
                        ).filter(Proyecto.nombre.ilike(f'%{proyecto}%')
                        ).filter(PerfilesProyecto.nombre.ilike(f'%{perfil}%')
                        ).filter(Entrevistas.contacto.ilike(f'%{contacto}%') 
                        ).filter(Entrevistas.cuando>=fecha_inicio 
                        ).filter(Entrevistas.cuando<=fecha_fin
                        ).order_by(Empresa.nombre.asc(), Proyecto.nombre.asc(), PerfilesProyecto.nombre.asc()
                        ).paginate(page=num_pag, per_page=max, error_out=False)
            
        print("Lista de Entrevistas")
        for p in lstEntrevistas:
            print(p.nom_empresa, p.nom_proyecto, p.nom_perfil, p.id, p.id_perfil, p.id_cand )
        data = []
        i=0
        for p in lstEntrevistas:
            i=i+1
            ev_data = {
                'Num':(num_pag-1)*max + i,
                'cuando': p.cuando.isoformat() if p.cuando else '',
                'calificacion': p.calificacion.name if p.calificacion else '',
                'anotaciones': p.anotaciones,
                'nom_empresa': p.nom_empresa,
                'nom_proyecto': p.nom_proyecto,
                'nom_perfil': p.nom_perfil,
                'contacto': p.contacto,
                'id': p.id,
                'idPerfilProy': p.idPerfilProy,
                'id_perfil': p.id_perfil,
                'id_cand': p.id_cand,
                'candidato': '',
                'valoracion': p.valoracion
            }
            data.append(ev_data)
        return {'Entrevistas': data, 'totalCount': numEntrevistas}, 200
    
class VistaEntrevistasEmpresas(Resource):
    def post(self, id_empresa):
        print("Obteniendo Las Entrevistas de una Empresa")
        print("id_empresa")
        print(id_empresa)
        print("json: ")
        print(request.json)
        max=request.json.get("max", 50)
        num_pag=request.json.get("num_pag", 1)
        order=request.json.get("order", "ASC")
        empresa=request.json.get("empresa", "")
        proyecto=request.json.get("proyecto", "")
        perfil=request.json.get("perfil", "")
        contacto=request.json.get("contacto", "")
        candidato=request.json.get("candidato", "")
        inicio=request.json.get("inicio", "")
        fin=request.json.get("fin", "")
        print("Inicio")
        print(inicio)
        print("Fin")
        print(fin)
        #fecha_inicio=datetime.strptime(inicio,"%Y-%m-%dT%H:%M:%SZ")
        #fecha_fin=datetime.strptime(fin,"%Y-%m-%dT%H:%M:%SZ")
        #fecha_inicio=datetime.now()
        #fecha_fin=datetime.now()+ timedelta(days=10)
        #fecha_inicio = parser.parse(inicio)
        #fecha_fin = parser.parse(fin)
        if inicio==None or inicio=='':
            fecha_inicio = datetime.strptime('1970-01-01 00:00:00',"%Y-%m-%d %H:%M:%S")
        if fin==None or fin=='':
            fecha_fin = datetime.strptime('3000-01-01 00:00:00',"%Y-%m-%d %H:%M:%S")
        if inicio!=None and fin!=None and inicio!='' and fin!='':
            fecha_inicio = parser.parse(inicio)
            fecha_fin = parser.parse(fin)
            fecha_fin=fecha_fin+timedelta(hours=23)
            fecha_fin=fecha_fin+timedelta(minutes=59)

        print("fecha_inicio")
        print(fecha_inicio)
        print("fecha_fin")
        print(fecha_fin)

        lstNumCand=request.json.get("lstNumCand", [0])
        print("lstNumCand")
        print(lstNumCand)
        #time.sleep(1)
        if lstNumCand==[-1]:
            print("Sin busqueda de candidatos")
            numEntrevistas=db.session.query(Entrevistas.id, 
                                            Entrevistas.id_cand,
                                            Entrevistas.idPerfilProy,
                                            Entrevistas.cuando,
                                            Entrevistas.contacto,
                                            Entrevistas.calificacion,
                                            Entrevistas.anotaciones,
                                            Entrevistas.valoracion,
                                            PerfilesProyecto.id_perfil,
                                            Empresa.nombre.label('nom_empresa'), 
                                            Proyecto.nombre.label('nom_proyecto'),
                                            PerfilesProyecto.nombre.label('nom_perfil'),
                            ).filter(Entrevistas.idPerfilProy==PerfilesProyecto.id
                            ).filter(PerfilesProyecto.id_proy==Proyecto.id
                            ).filter(Proyecto.id_emp==Empresa.id
                            ).filter(Empresa.id==id_empresa
                            ).filter(Empresa.nombre.ilike(f'%{empresa}%')
                            ).filter(Proyecto.nombre.ilike(f'%{proyecto}%')
                            ).filter(PerfilesProyecto.nombre.ilike(f'%{perfil}%')
                            ).filter(Entrevistas.contacto.ilike(f'%{contacto}%') 
                            ).filter(Entrevistas.cuando>=fecha_inicio 
                            ).filter(Entrevistas.cuando<=fecha_fin
                            ).count()
            lstEntrevistas=db.session.query(Entrevistas.id, 
                                            Entrevistas.id_cand,
                                            Entrevistas.idPerfilProy,
                                            Entrevistas.cuando,
                                            Entrevistas.contacto,
                                            Entrevistas.calificacion,
                                            Entrevistas.anotaciones,
                                            Entrevistas.valoracion,
                                            PerfilesProyecto.id_perfil,
                                            Empresa.nombre.label('nom_empresa'), 
                                            Proyecto.nombre.label('nom_proyecto'),
                                            PerfilesProyecto.nombre.label('nom_perfil'),
                            ).filter(Entrevistas.idPerfilProy==PerfilesProyecto.id
                            ).filter(PerfilesProyecto.id_proy==Proyecto.id
                            ).filter(Proyecto.id_emp==Empresa.id
                            ).filter(Empresa.id==id_empresa
                            ).filter(Empresa.nombre.ilike(f'%{empresa}%')
                            ).filter(Proyecto.nombre.ilike(f'%{proyecto}%')
                            ).filter(PerfilesProyecto.nombre.ilike(f'%{perfil}%')
                            ).filter(Entrevistas.contacto.ilike(f'%{contacto}%') 
                            ).filter(Entrevistas.cuando>=fecha_inicio 
                            ).filter(Entrevistas.cuando<=fecha_fin
                            ).order_by(Empresa.nombre.asc(), Proyecto.nombre.asc(), PerfilesProyecto.nombre.asc()
                            ).paginate(page=num_pag, per_page=max, error_out=False)
        else:
            print("Con busqueda de candidatos")
            numEntrevistas=db.session.query(Entrevistas.id, 
                                            Entrevistas.id_cand,
                                            Entrevistas.idPerfilProy,
                                            Entrevistas.cuando,
                                            Entrevistas.contacto,
                                            Entrevistas.calificacion,
                                            Entrevistas.anotaciones,
                                            Entrevistas.valoracion,
                                            PerfilesProyecto.id_perfil,
                                            Empresa.nombre.label('nom_empresa'), 
                                            Proyecto.nombre.label('nom_proyecto'),
                                            PerfilesProyecto.nombre.label('nom_perfil'),
                            ).filter(Entrevistas.idPerfilProy==PerfilesProyecto.id
                            ).filter(PerfilesProyecto.id_proy==Proyecto.id
                            ).filter(Proyecto.id_emp==Empresa.id
                            ).filter(Empresa.id==id_empresa
                            ).filter(Empresa.nombre.ilike(f'%{empresa}%')
                            ).filter(Proyecto.nombre.ilike(f'%{proyecto}%')
                            ).filter(PerfilesProyecto.nombre.ilike(f'%{perfil}%')
                            ).filter(Entrevistas.contacto.ilike(f'%{contacto}%') 
                            ).filter(Entrevistas.id_cand.in_(lstNumCand)
                            ).filter(Entrevistas.cuando>=fecha_inicio 
                            ).filter(Entrevistas.cuando<=fecha_fin
                            ).count()
            lstEntrevistas=db.session.query(Entrevistas.id, 
                                            Entrevistas.id_cand,
                                            Entrevistas.idPerfilProy,
                                            Entrevistas.cuando,
                                            Entrevistas.contacto,
                                            Entrevistas.calificacion,
                                            Entrevistas.anotaciones,
                                            Entrevistas.valoracion,
                                            PerfilesProyecto.id_perfil,
                                            Empresa.nombre.label('nom_empresa'), 
                                            Proyecto.nombre.label('nom_proyecto'),
                                            PerfilesProyecto.nombre.label('nom_perfil'),
                            ).filter(Entrevistas.idPerfilProy==PerfilesProyecto.id
                            ).filter(PerfilesProyecto.id_proy==Proyecto.id
                            ).filter(Proyecto.id_emp==Empresa.id
                            ).filter(Empresa.id==id_empresa
                            ).filter(Empresa.nombre.ilike(f'%{empresa}%')
                            ).filter(Proyecto.nombre.ilike(f'%{proyecto}%')
                            ).filter(PerfilesProyecto.nombre.ilike(f'%{perfil}%')
                            ).filter(Entrevistas.contacto.ilike(f'%{contacto}%') 
                            ).filter(Entrevistas.id_cand.in_(lstNumCand)
                            ).filter(Entrevistas.cuando>=fecha_inicio 
                            ).filter(Entrevistas.cuando<=fecha_fin
                            ).order_by(Empresa.nombre.asc(), Proyecto.nombre.asc(), PerfilesProyecto.nombre.asc()
                            ).paginate(page=num_pag, per_page=max, error_out=False)
        print("Lista de Entrevistas")
        for p in lstEntrevistas:
            print(p.nom_empresa, p.nom_proyecto, p.nom_perfil, p.id, p.id_perfil, p.id_cand )
        data = []
        i=0
        for p in lstEntrevistas:
            i=i+1
            ev_data = {
                'Num':(num_pag-1)*max + i,
                'cuando': p.cuando.isoformat() if p.cuando else '',
                'calificacion': p.calificacion.name if p.calificacion else '',
                'anotaciones': p.anotaciones,
                'nom_empresa': p.nom_empresa,
                'nom_proyecto': p.nom_proyecto,
                'nom_perfil': p.nom_perfil,
                'contacto': p.contacto,
                'id': p.id,
                'idPerfilProy': p.idPerfilProy,
                'id_perfil': p.id_perfil,
                'id_cand': p.id_cand,
                'candidato': '',
                'valoracion': p.valoracion
            }
            data.append(ev_data)
        return {'Entrevistas': data, 'totalCount': numEntrevistas}, 200

class VistaLasEntrevistas(Resource):
    def post(self):
        print("Obteniendo Todas Las Entrevistas")
        print("json: ")
        print(request.json)
        max=request.json.get("max", 50)
        num_pag=request.json.get("num_pag", 1)
        order=request.json.get("order", "ASC")
        empresa=request.json.get("empresa", "Solidaria")
        proyecto=request.json.get("proyecto", "Solidaria")
        perfil=request.json.get("perfil", "Solidaria")
        contacto=request.json.get("contacto", "")
        candidato=request.json.get("candidato", "Solidaria")
        inicio=request.json.get("inicio", "")
        fin=request.json.get("fin", "")
        print("Inicio")
        print(inicio)
        print("Fin")
        print(fin)
        #fecha_inicio=datetime.strptime(inicio,"%Y-%m-%dT%H:%M:%SZ")
        #fecha_fin=datetime.strptime(fin,"%Y-%m-%dT%H:%M:%SZ")
        #fecha_inicio=datetime.now()
        #fecha_fin=datetime.now()+ timedelta(days=10)
        #fecha_inicio = parser.parse(inicio)
        #fecha_fin = parser.parse(fin)
        if inicio==None or inicio=='':
            fecha_inicio = datetime.strptime('1970-01-01 00:00:00',"%Y-%m-%d %H:%M:%S")
        if fin==None or fin=='':
            fecha_fin = datetime.strptime('3000-01-01 00:00:00',"%Y-%m-%d %H:%M:%S")
        if inicio!=None and fin!=None and inicio!='' and fin!='':
            fecha_inicio = parser.parse(inicio)
            fecha_fin = parser.parse(fin)
            fecha_fin=fecha_fin+timedelta(hours=23)
            fecha_fin=fecha_fin+timedelta(minutes=59)
        print("fecha_inicio")
        print(fecha_inicio)
        print("fecha_fin")
        print(fecha_fin)

        lstNumCand=request.json.get("lstNumCand", [0])
        print("lstNumCand")
        print(lstNumCand)
        #time.sleep(1)
        if lstNumCand==[-1]:
            print("Sin busqueda de candidatos")
            numEntrevistas=db.session.query(Entrevistas.id, 
                                            Entrevistas.id_cand,
                                            Entrevistas.idPerfilProy,
                                            Entrevistas.cuando,
                                            Entrevistas.contacto,
                                            Entrevistas.calificacion,
                                            Entrevistas.anotaciones,
                                            Entrevistas.valoracion,
                                            PerfilesProyecto.id_perfil,
                                            Empresa.nombre.label('nom_empresa'), 
                                            Proyecto.nombre.label('nom_proyecto'),
                                            PerfilesProyecto.nombre.label('nom_perfil'),
                            ).filter(Entrevistas.idPerfilProy==PerfilesProyecto.id
                            ).filter(PerfilesProyecto.id_proy==Proyecto.id
                            ).filter(Proyecto.id_emp==Empresa.id
                            ).filter(Empresa.nombre.ilike(f'%{empresa}%')
                            ).filter(Proyecto.nombre.ilike(f'%{proyecto}%')
                            ).filter(PerfilesProyecto.nombre.ilike(f'%{perfil}%')
                            ).filter(Entrevistas.contacto.ilike(f'%{contacto}%') 
                            ).filter(Entrevistas.cuando>=fecha_inicio 
                            ).filter(Entrevistas.cuando<=fecha_fin
                            ).count()
            lstEntrevistas=db.session.query(Entrevistas.id, 
                                            Entrevistas.id_cand,
                                            Entrevistas.idPerfilProy,
                                            Entrevistas.cuando,
                                            Entrevistas.contacto,
                                            Entrevistas.calificacion,
                                            Entrevistas.anotaciones,
                                            Entrevistas.valoracion,
                                            PerfilesProyecto.id_perfil,
                                            Empresa.nombre.label('nom_empresa'), 
                                            Proyecto.nombre.label('nom_proyecto'),
                                            PerfilesProyecto.nombre.label('nom_perfil'),
                            ).filter(Entrevistas.idPerfilProy==PerfilesProyecto.id
                            ).filter(PerfilesProyecto.id_proy==Proyecto.id
                            ).filter(Proyecto.id_emp==Empresa.id
                            ).filter(Empresa.nombre.ilike(f'%{empresa}%')
                            ).filter(Proyecto.nombre.ilike(f'%{proyecto}%')
                            ).filter(PerfilesProyecto.nombre.ilike(f'%{perfil}%')
                            ).filter(Entrevistas.contacto.ilike(f'%{contacto}%') 
                            ).filter(Entrevistas.cuando>=fecha_inicio 
                            ).filter(Entrevistas.cuando<=fecha_fin
                            ).order_by(Empresa.nombre.asc(), Proyecto.nombre.asc(), PerfilesProyecto.nombre.asc()
                            ).paginate(page=num_pag, per_page=max, error_out=False)
        else:
            print("Con busqueda de candidatos")
            numEntrevistas=db.session.query(Entrevistas.id, 
                                            Entrevistas.id_cand,
                                            Entrevistas.idPerfilProy,
                                            Entrevistas.cuando,
                                            Entrevistas.contacto,
                                            Entrevistas.calificacion,
                                            Entrevistas.anotaciones,
                                            Entrevistas.valoracion,
                                            PerfilesProyecto.id_perfil,
                                            Empresa.nombre.label('nom_empresa'), 
                                            Proyecto.nombre.label('nom_proyecto'),
                                            PerfilesProyecto.nombre.label('nom_perfil'),
                            ).filter(Entrevistas.idPerfilProy==PerfilesProyecto.id
                            ).filter(PerfilesProyecto.id_proy==Proyecto.id
                            ).filter(Proyecto.id_emp==Empresa.id
                            ).filter(Empresa.nombre.ilike(f'%{empresa}%')
                            ).filter(Proyecto.nombre.ilike(f'%{proyecto}%')
                            ).filter(PerfilesProyecto.nombre.ilike(f'%{perfil}%')
                            ).filter(Entrevistas.contacto.ilike(f'%{contacto}%') 
                            ).filter(Entrevistas.id_cand.in_(lstNumCand)
                            ).filter(Entrevistas.cuando>=fecha_inicio 
                            ).filter(Entrevistas.cuando<=fecha_fin
                            ).count()
            lstEntrevistas=db.session.query(Entrevistas.id, 
                                            Entrevistas.id_cand,
                                            Entrevistas.idPerfilProy,
                                            Entrevistas.cuando,
                                            Entrevistas.contacto,
                                            Entrevistas.calificacion,
                                            Entrevistas.anotaciones,
                                            Entrevistas.valoracion,
                                            PerfilesProyecto.id_perfil,
                                            Empresa.nombre.label('nom_empresa'), 
                                            Proyecto.nombre.label('nom_proyecto'),
                                            PerfilesProyecto.nombre.label('nom_perfil'),
                            ).filter(Entrevistas.idPerfilProy==PerfilesProyecto.id
                            ).filter(PerfilesProyecto.id_proy==Proyecto.id
                            ).filter(Proyecto.id_emp==Empresa.id
                            ).filter(Empresa.nombre.ilike(f'%{empresa}%')
                            ).filter(Proyecto.nombre.ilike(f'%{proyecto}%')
                            ).filter(PerfilesProyecto.nombre.ilike(f'%{perfil}%')
                            ).filter(Entrevistas.contacto.ilike(f'%{contacto}%') 
                            ).filter(Entrevistas.id_cand.in_(lstNumCand)
                            ).filter(Entrevistas.cuando>=fecha_inicio 
                            ).filter(Entrevistas.cuando<=fecha_fin
                            ).order_by(Empresa.nombre.asc(), Proyecto.nombre.asc(), PerfilesProyecto.nombre.asc()
                            ).paginate(page=num_pag, per_page=max, error_out=False)
        print("Lista de Entrevistas")
        for p in lstEntrevistas:
            print(p.nom_empresa, p.nom_proyecto, p.nom_perfil, p.id, p.id_perfil, p.id_cand )
        data = []
        i=0
        for p in lstEntrevistas:
            i=i+1
            ev_data = {
                'Num':(num_pag-1)*max + i,
                'cuando': p.cuando.isoformat() if p.cuando else '',
                'calificacion': p.calificacion.name if p.calificacion else '',
                'anotaciones': p.anotaciones,
                'nom_empresa': p.nom_empresa,
                'nom_proyecto': p.nom_proyecto,
                'nom_perfil': p.nom_perfil,
                'contacto': p.contacto,
                'id': p.id,
                'idPerfilProy': p.idPerfilProy,
                'id_perfil': p.id_perfil,
                'id_cand': p.id_cand,
                'candidato': '',
                'valoracion': p.valoracion
            }
            data.append(ev_data)
        return {'Entrevistas': data, 'totalCount': numEntrevistas}, 200

class VistaEntrevistas(Resource):
    def post(self):
        print("Creando Entrevista")
        print(request.json)
        try:
            zona=request.json.get("zona")
            hora=request.json.get("hora")
            fecha=request.json.get("fecha")
            id_cand=request.json.get("id_cand")
            contacto=request.json.get("contacto")
            perfilProyId=request.json.get("perfilProyId")

            objPerfilProy=PerfilesProyecto.get_by_id(perfilProyId)
            id_proy=objPerfilProy.id_proy
            id_perfil=objPerfilProy.id_perfil
            
            numEntrevistas=db.session.query(Entrevistas.id).filter(Entrevistas.idPerfilProy==PerfilesProyecto.id
                                           ).filter(Entrevistas.id_cand==id_cand
                                           ).filter(PerfilesProyecto.id_proy==id_proy
                                           ).filter(PerfilesProyecto.id_perfil==id_perfil).count()
            if numEntrevistas!=0:
               return {"mensaje": "Entrevista no se pudo crear: el candidato YA tiene entrevista para este mismo Perfil."}, 400
             
            nE=Entrevistas()
            nE.idPerfilProy=perfilProyId
            nE.cuando=datetime.strptime(fecha+' '+hora+' '+zona[3:],
                              "%Y-%m-%d %H:%M %z")  #print(request.json.get("fecha")+' '+request.json.get("hora")+' '+zona[3:])
            print("Local")            
            print(nE.cuando)
            nE.cuando=nE.cuando.astimezone(pytz.UTC)
            print("UTC")            
            print(nE.cuando)
            nE.id_cand=id_cand
            nE.contacto=contacto

            entrevista= Entrevistas.query.filter(Entrevistas.idPerfilProy==nE.idPerfilProy
                                        ).filter(Entrevistas.cuando==nE.cuando
                                        ).first()
            print("Despues del query")
            if entrevista is not None:
               return {"mensaje": "Entrevista no se pudo crear: la fecha y hora suministrada ya esta ocupada para este puesto."}, 400
            print("Despues del condicional")
            
            if nE.id_cand==0:
                return {"mensaje": "Entrevista no se pudo crear: No selecciono candidato a Entrevistar."}, 400
            print("Antes de grabar")
            db.session.add(nE)
            db.session.commit()
            return evalmensual_schema.dump(nE), 201
        except Exception as inst:
            db.session.rollback()
            print(type(inst))    # the exception instance
            print(inst)
            print("Entrevista no se pudo crear.")
            return {"Mensaje: ":"Error: Entrevista no se pudo crear."+str(type(inst))}, 500

    def get(self):
        print("Obteniendo Todas Las Entrevistas")
        print("json: ")
        print(request.json)
        max=request.json.get("max", 50)
        num_pag=request.json.get("num_pag", 1)
        order=request.json.get("order", "ASC")
        empresa=request.json.get("empresa", "Solidaria")
        proyecto=request.json.get("proyecto", "Solidaria")
        perfil=request.json.get("perfil", "Solidaria")
        candidato=request.json.get("candidato", "Solidaria")
        lstNumCand=request.json.get("lstNumCand", [0])
        print("lstNumCand")
        print(lstNumCand)
        #time.sleep(1)
        if lstNumCand==[-1]:
            numPuestos=db.session.query(Empresa.nombre.label('nom_empresa'), 
                                    Proyecto.nombre.label('nom_proyecto'),
                                    PerfilesProyecto.nombre.label('nom_perfil'),
                                    PerfilesProyecto.id,
                                    PerfilesProyecto.id_perfil,
                                    PerfilesProyecto.id_cand
                                    ).filter(Empresa.id==Proyecto.id_emp
                                    ).filter(Proyecto.id==PerfilesProyecto.id_proy
                                    ).filter(Empresa.nombre.ilike(f'%{empresa}%')
                                    ).filter(Proyecto.nombre.ilike(f'%{proyecto}%')
                                    ).filter(PerfilesProyecto.nombre.ilike(f'%{perfil}%')
                                    ).count()
            lstPuestos=db.session.query(Empresa.nombre.label('nom_empresa'), 
                                    Proyecto.nombre.label('nom_proyecto'),
                                    PerfilesProyecto.nombre.label('nom_perfil'),
                                    PerfilesProyecto.id,
                                    PerfilesProyecto.id_perfil,
                                    PerfilesProyecto.id_cand
                                    ).filter(Empresa.id==Proyecto.id_emp
                                    ).filter(Proyecto.id==PerfilesProyecto.id_proy
                                    ).filter(Empresa.nombre.ilike(f'%{empresa}%')
                                    ).filter(Proyecto.nombre.ilike(f'%{proyecto}%')
                                    ).filter(PerfilesProyecto.nombre.ilike(f'%{perfil}%')
                                    ).order_by(Empresa.nombre.asc(), Proyecto.nombre.asc(), PerfilesProyecto.nombre.asc()
                                    ).paginate(page=num_pag, per_page=max, error_out=False)
        else:
            numPuestos=db.session.query(Empresa.nombre.label('nom_empresa'), 
                                    Proyecto.nombre.label('nom_proyecto'),
                                    PerfilesProyecto.nombre.label('nom_perfil'),
                                    PerfilesProyecto.id,
                                    PerfilesProyecto.id_perfil,
                                    PerfilesProyecto.id_cand
                                    ).filter(Empresa.id==Proyecto.id_emp
                                    ).filter(Proyecto.id==PerfilesProyecto.id_proy
                                    ).filter(Empresa.nombre.ilike(f'%{empresa}%')
                                    ).filter(Proyecto.nombre.ilike(f'%{proyecto}%')
                                    ).filter(PerfilesProyecto.nombre.ilike(f'%{perfil}%')
                                    ).filter(PerfilesProyecto.id_cand.in_(lstNumCand)
                                    ).count()
            lstPuestos=db.session.query(Empresa.nombre.label('nom_empresa'), 
                                    Proyecto.nombre.label('nom_proyecto'),
                                    PerfilesProyecto.nombre.label('nom_perfil'),
                                    PerfilesProyecto.id,
                                    PerfilesProyecto.id_perfil,
                                    PerfilesProyecto.id_cand
                                    ).filter(Empresa.id==Proyecto.id_emp
                                    ).filter(Proyecto.id==PerfilesProyecto.id_proy
                                    ).filter(Empresa.nombre.ilike(f'%{empresa}%')
                                    ).filter(Proyecto.nombre.ilike(f'%{proyecto}%')
                                    ).filter(PerfilesProyecto.nombre.ilike(f'%{perfil}%')
                                    ).filter(PerfilesProyecto.id_cand.in_(lstNumCand)                                             
                                    ).order_by(Empresa.nombre.asc(), Proyecto.nombre.asc(), PerfilesProyecto.nombre.asc()
                                    ).paginate(page=num_pag, per_page=max, error_out=False)
        for p in lstPuestos:
            print(p.nom_empresa, p.nom_proyecto, p.nom_perfil, p.id, p.id_perfil, p.id_cand )
        data = []
        i=0
        for p in lstPuestos:
            i=i+1
            puesto_data = {
                'Num':(num_pag-1)*max + i,
                'nom_empresa': p.nom_empresa,
                'nom_proyecto': p.nom_proyecto,
                'nom_perfil': p.nom_perfil,
                'id': p.id,
                'id_perfil': p.id_perfil,
                'id_cand': p.id_cand,
                'candidato': ''
            }
            data.append(puesto_data)
        return {'Puestos': data, 'totalCount': numPuestos}, 200

class VistaEntrevistasOriginal(Resource):
    def post(self):
        print("Creando Entrevista")
        print(request.json)
        try:
            zona=request.json.get("zona")
            print("Uno")
            nE=Entrevistas()
            print("Dos")
            nE.idPerfilProy=request.json.get("perfilProyId")
            print("Tres")
            print(request.json.get("fecha")+' '+request.json.get("hora")+' '+zona[3:])
            nE.cuando=datetime.strptime(request.json.get("fecha")+' '+request.json.get("hora")+' '+zona[3:],
                              "%Y-%m-%d %H:%M %z")
            print("cuando")
            print(nE.cuando)
            print(type(nE.cuando))
            #request.json.get("fecha")+'T'+request.json.get("hora")
            # nE.cuando=request.json.get("cuando")
            entrevista= Entrevistas.query.filter(Entrevistas.idPerfilProy==nE.idPerfilProy
                                        ).filter(Entrevistas.cuando==nE.cuando
                                        ).first()
            print("Despues del query")
            if entrevista is not None:
               return {"mensaje": "Entrevista no se pudo crear: la fecha y hora suministrada ya esta ocupada para este puesto."}, 400
            print("Despues del condicional")
            nE.id_cand=request.json.get("id_cand")
            nE.contacto=request.json.get("contacto")
            if nE.id_cand==0:
                return {"mensaje": "Entrevista no se pudo crear: No selecciono candidato a Entrevistar."}, 400
            print("Antes de grabar")
            db.session.add(nE)
            db.session.commit()
            return evalmensual_schema.dump(nE), 201
        except Exception as inst:
            db.session.rollback()
            print(type(inst))    # the exception instance
            print(inst)
            print("Entrevista no se pudo crear.")
            return {"Mensaje: ":"Error: Entrevista no se pudo crear."+str(type(inst))}, 500

    def get(self):
        print("Obteniendo Todas Las Entrevistas")
        print("json: ")
        print(request.json)
        max=request.json.get("max", 50)
        num_pag=request.json.get("num_pag", 1)
        order=request.json.get("order", "ASC")
        empresa=request.json.get("empresa", "Solidaria")
        proyecto=request.json.get("proyecto", "Solidaria")
        perfil=request.json.get("perfil", "Solidaria")
        candidato=request.json.get("candidato", "Solidaria")
        lstNumCand=request.json.get("lstNumCand", [0])
        print("lstNumCand")
        print(lstNumCand)
        #time.sleep(1)
        if lstNumCand==[-1]:
            numPuestos=db.session.query(Empresa.nombre.label('nom_empresa'), 
                                    Proyecto.nombre.label('nom_proyecto'),
                                    PerfilesProyecto.nombre.label('nom_perfil'),
                                    PerfilesProyecto.id,
                                    PerfilesProyecto.id_perfil,
                                    PerfilesProyecto.id_cand
                                    ).filter(Empresa.id==Proyecto.id_emp
                                    ).filter(Proyecto.id==PerfilesProyecto.id_proy
                                    ).filter(Empresa.nombre.ilike(f'%{empresa}%')
                                    ).filter(Proyecto.nombre.ilike(f'%{proyecto}%')
                                    ).filter(PerfilesProyecto.nombre.ilike(f'%{perfil}%')
                                    ).count()
            lstPuestos=db.session.query(Empresa.nombre.label('nom_empresa'), 
                                    Proyecto.nombre.label('nom_proyecto'),
                                    PerfilesProyecto.nombre.label('nom_perfil'),
                                    PerfilesProyecto.id,
                                    PerfilesProyecto.id_perfil,
                                    PerfilesProyecto.id_cand
                                    ).filter(Empresa.id==Proyecto.id_emp
                                    ).filter(Proyecto.id==PerfilesProyecto.id_proy
                                    ).filter(Empresa.nombre.ilike(f'%{empresa}%')
                                    ).filter(Proyecto.nombre.ilike(f'%{proyecto}%')
                                    ).filter(PerfilesProyecto.nombre.ilike(f'%{perfil}%')
                                    ).order_by(Empresa.nombre.asc(), Proyecto.nombre.asc(), PerfilesProyecto.nombre.asc()
                                    ).paginate(page=num_pag, per_page=max, error_out=False)
        else:
            numPuestos=db.session.query(Empresa.nombre.label('nom_empresa'), 
                                    Proyecto.nombre.label('nom_proyecto'),
                                    PerfilesProyecto.nombre.label('nom_perfil'),
                                    PerfilesProyecto.id,
                                    PerfilesProyecto.id_perfil,
                                    PerfilesProyecto.id_cand
                                    ).filter(Empresa.id==Proyecto.id_emp
                                    ).filter(Proyecto.id==PerfilesProyecto.id_proy
                                    ).filter(Empresa.nombre.ilike(f'%{empresa}%')
                                    ).filter(Proyecto.nombre.ilike(f'%{proyecto}%')
                                    ).filter(PerfilesProyecto.nombre.ilike(f'%{perfil}%')
                                    ).filter(PerfilesProyecto.id_cand.in_(lstNumCand)
                                    ).count()
            lstPuestos=db.session.query(Empresa.nombre.label('nom_empresa'), 
                                    Proyecto.nombre.label('nom_proyecto'),
                                    PerfilesProyecto.nombre.label('nom_perfil'),
                                    PerfilesProyecto.id,
                                    PerfilesProyecto.id_perfil,
                                    PerfilesProyecto.id_cand
                                    ).filter(Empresa.id==Proyecto.id_emp
                                    ).filter(Proyecto.id==PerfilesProyecto.id_proy
                                    ).filter(Empresa.nombre.ilike(f'%{empresa}%')
                                    ).filter(Proyecto.nombre.ilike(f'%{proyecto}%')
                                    ).filter(PerfilesProyecto.nombre.ilike(f'%{perfil}%')
                                    ).filter(PerfilesProyecto.id_cand.in_(lstNumCand)                                             
                                    ).order_by(Empresa.nombre.asc(), Proyecto.nombre.asc(), PerfilesProyecto.nombre.asc()
                                    ).paginate(page=num_pag, per_page=max, error_out=False)
        for p in lstPuestos:
            print(p.nom_empresa, p.nom_proyecto, p.nom_perfil, p.id, p.id_perfil, p.id_cand )
        data = []
        i=0
        for p in lstPuestos:
            i=i+1
            puesto_data = {
                'Num':(num_pag-1)*max + i,
                'nom_empresa': p.nom_empresa,
                'nom_proyecto': p.nom_proyecto,
                'nom_perfil': p.nom_perfil,
                'id': p.id,
                'id_perfil': p.id_perfil,
                'id_cand': p.id_cand,
                'candidato': ''
            }
            data.append(puesto_data)
        return {'Puestos': data, 'totalCount': numPuestos}, 200

class VistaEvaluaciones(Resource):
    def post(self):
        print("Creando Evaluacion")
        print(request.json)
        try:
            mesesIngles=["January","February","March","April","May","June","July","August","September","October","November","December"];
            mesesSpanish=["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"];
            nEval=EvalMensual()
            nEval.idPerfilProy=request.json.get("idPerfilProy")
            nEval.anno=request.json.get("year")
            nEval.mes=request.json.get("month")
            evaluacion = EvalMensual.query.filter(EvalMensual.idPerfilProy==nEval.idPerfilProy
                                         ).filter(EvalMensual.anno==nEval.anno
                                         ).filter(EvalMensual.mes==nEval.mes
                                         ).first()
            if evaluacion is not None:
               return {"mensaje": "Evaluacion no se pudo crear: El periodo suministrado ya esta evaluado."}, 400
            nEval.strmes=mesesSpanish[nEval.mes]
            nEval.id_cand=request.json.get("id_cand")
            if nEval.id_cand==0:
                return {"mensaje": "Evaluacion no se pudo crear: No selecciono empleado a Evaluar."}, 400
            nEval.calificacion=Calificacion[request.get_json()['valuation']]
            nEval.valoracion=0
            nEval.nota=request.json.get("note")
            if nEval.nota=='':
               return {"mensaje": "Evaluacion no se pudo crear: No se suministro un comentario en la valoracion."}, 400
            db.session.add(nEval)
            db.session.commit()
            return evalmensual_schema.dump(nEval), 201
        except Exception as inst:
            db.session.rollback()
            print(type(inst))    # the exception instance
            print(inst)
            print("Evaluacion no se pudo crear.")
            return {"Mensaje: ":"Error: Evaluacion no se pudo crear."+str(type(inst))}, 500
        
class VistaEmpresas(Resource):
    def post(self):
        print("Creando Empresa")
        try:
            ne=Empresa()
            ne.nombre=request.json.get("nombre")
            empresa = Empresa.query.filter(Empresa.nombre == ne.nombre).first()
            if empresa is not None:
               return {"mensaje": "Empresa no se pudo crear: El nombre suministrado ya existe."}, 400
            ne.correo=request.json.get("correo")
            empresa = Empresa.query.filter(Empresa.correo == ne.correo).first()
            if empresa is not None:
               return {"mensaje": "Empresa no se pudo crear: El correo suministrado ya existe."}, 400
            ne.tipo=request.json.get("tipo")
            ne.pais=request.json.get("pais")
            ne.ciudad=request.json.get("ciudad")
            ne.direccion=request.json.get("direccion")
            ne.contacto=request.json.get("contacto")
            ne.celular=request.json.get("celular")
            ne.estado=Estado[request.get_json()['estado']]
            ne.is_active=request.json.get("is_active")
            ne.id_usuario=request.json.get("id_usuario")
            empresa = Empresa.query.filter(Empresa.id_usuario == ne.id_usuario).first()
            if empresa is not None:
               return {"mensaje": "Empresa no se pudo crear: El id_usuario suministrado ya existe."}, 400
            db.session.add(ne)
            db.session.commit()
            return {"Empresa":empresa_schema.dump(ne)}, 201
        except Exception as inst:
            db.session.rollback()
            print(type(inst))    # the exception instance
            #print(inst)
            print("Empresa no se pudo crear.")
            return {"Mensaje: ":"Error: Empresa no se pudo crear."+str(type(inst))}, 500
    
    def get(self):
        print("Listar Empresas")
        #user_jwt=int(get_jwt_identity())  
        #max=request.json.get("max", 50)
        #if request.get_json()['order']=="ASC":
        #   return  [tarea_schema.dump(tar) for tar in Tarea.query.filter(Tarea.id_usr==user_jwt).order_by(Tarea.fecha.asc()).paginate(page=1, per_page=max, error_out=False)] 
        #else:
        #   return  [tarea_schema.dump(tar) for tar in Tarea.query.filter(Tarea.id_usr==user_jwt).order_by(Tarea.fecha.desc()).paginate(page=1, per_page=max, error_out=False)]  
        return {"Empresa": "Empresa1"}, 200

class VistaEmpresa(Resource):
    def get(self, id_empresa):
        print("Consultar Empresa")
        try:
            empresa = Empresa.query.get_or_404(id_empresa)
            return empresa_schema.dump(empresa), 200
        except Exception as inst:
            print(type(inst))    # the exception instance
            #print(inst)
            print("No se pudo obtener la informacion de la Empresa.")
            return {"Mensaje: ":"Error: No se pudo obtener la informacion de la Empresa."}, 500

class VistaEmpresaDetalle(Resource):
    def get(self, id_empresa):
        print("Consultar Detalle Empresa")
        try:
            empresa = Empresa.query.get_or_404(id_empresa)
            empresaJSON = empresa_schema.dump(empresa)
        except Exception as inst:
            print(type(inst))    # the exception instance
            #print(inst)
            print("No se pudo obtener la informacion de la Empresa.")
            return {"Mensaje: ":"Error: No se pudo obtener la informacion de la Empresa."}, 50
        
        try:
            proyectosJSON=[proyecto_schema.dump(p) for p in Proyecto.get_by_empresa(id_empresa)]
            empresaJSON["proyectos"]=proyectosJSON
            return empresaJSON, 200
        except Exception as inst:
            print(type(inst))    # the exception instance
            #print(inst)
            print("No se pudo obtener la informacion de los proyectos.")
            return empresaJSON, 200

class VistaEmpresaDetalleUsuario(Resource):
    def get(self, id_usuario):
        print("Consultar Detalle Empresa de un Usuario")
        try:
            empresa = Empresa.get_by_idUser(id_usuario)
            empresaJSON = empresa_schema.dump(empresa)
        except Exception as inst:
            print(type(inst))    # the exception instance
            #print(inst)
            print("No se pudo obtener la informacion de la Empresa.")
            return {"Mensaje: ":"Error: No se pudo obtener la informacion de la Empresa."}, 50
        
        try:
            proyectosJSON=[proyecto_schema.dump(p) for p in Proyecto.get_by_empresa(empresa.id)]
            empresaJSON["proyectos"]=proyectosJSON
            return empresaJSON, 200
        except Exception as inst:
            print(type(inst))    # the exception instance
            #print(inst)
            print("No se pudo obtener la informacion de los proyectos.")
            return empresaJSON, 200

class VistaProyectos(Resource):
    def post(self, id_emp):
        print("Crear Proyecto")
        emp=Empresa.get_by_id(id_emp)
        if emp is not None:
            try:
                np=Proyecto()
                np.nombre=request.json.get("nombre")
                np.id_emp=id_emp
                proyecto = Proyecto.query.filter(Proyecto.nombre == np.nombre).filter(Proyecto.id_emp == np.id_emp ).first()
                if proyecto is not None:
                   return {"mensaje": "proyecto no se pudo crear: El nombre suministrado ya existe para esta empresa."}, 400
                np.descripcion=request.json.get("descripcion")
                strFecha=request.json.get("fecha_inicio", None)
                if strFecha is None:
                    np.fecha_inicio=func.now() #datetime.now()  campofecha.isoformat()
                else:
                    dateFecha=datetime.strptime(strFecha, '%Y-%m-%d')
                    if dateFecha < datetime.now():
                       np.fecha_inicio=datetime.now()
                    else:
                       np.fecha_inicio=dateFecha
                db.session.add(np)
                db.session.commit()
                return {"Proyecto nuevo: ":proyecto_schema.dump(np)}, 200
            except Exception as inst:
                db.session.rollback()
                print(type(inst))    # the exception instance
                print(inst)
                print("Proyecto no se pudo crear.")
                return {"Mensaje: ":"Error: Proyecto no se pudo crear."}, 500
        else:
            return {"Mensaje: ":"Error: Proyecto no se pudo crear. La empresa no existe."}, 400

    def get(self, id_emp):
        print("Consultar Proyectos de una Empresa")
        try:
            return  [proyecto_schema.dump(p) for p in Proyecto.get_by_empresa(id_emp)], 200
        except Exception as inst:
            db.session.rollback()
            print(type(inst))    # the exception instance
            #print(inst)
            print("No se pudo obtener la informacion de los Proyectos.")
            return {"Mensaje: ":"Error: No se pudo obtener la informacion de los Proyectos."}, 500

class VistaProyectoDetalle(Resource):
    def get(self, id_proy):
        print("Consultar Un Proyecto")
        try:
            proy=Proyecto.get_by_id(id_proy)
            print("despues")
            if proy is not None:
                proyJSON=proyecto_schema.dump(proy)
                empresa=Empresa.get_by_id(proy.id_emp)
                proyJSON["empresa"]=empresa.nombre
                lstPerfJSON=[perfiles_proyecto_schema.dump(perf) for perf in PerfilesProyecto.get_by_idProy(id_proy)]
                proyJSON["perfiles"]=lstPerfJSON               
                return proyJSON, 200
            else:
                return {"Mensaje: ":"Error: Proyecto No existe."}, 500    
        except Exception as inst:
            #db.session.rollback()
            print(type(inst))    # the exception instance
            #print(inst)
            print("No se pudo obtener la informacion de los Proyectos.")
            return {"Mensaje: ":"Error: No se pudo obtener la informacion de los Proyectos."}, 500

class VistaProyecto(Resource):
    def get(self, id_proy):
        print("Consultar Proyecto")
        try:
            proyecto = Proyecto.query.get_or_404(id_proy)
            return proyecto_schema.dump(proyecto)
        except Exception as inst:
            db.session.rollback()
            print(type(inst))    # the exception instance
            #print(inst)
            print("No se pudo obtener la informacion del Proyecto.")
            return {"Mensaje: ":"Error: No se pudo obtener la informacion del Proyecto."}, 500

class VistaPerfilesStr(Resource):
    def post(self, id_proy):
        print("Crear perfil de Proyecto con Str")
        proy=Proyecto.get_by_id(id_proy)
        if proy is not None:
            print(proy)
            print(proy.nombre)
            print(proy.id)
            try:
                print(request.get_json())
                nombre=request.json.get("nombre")
                strHabils=request.json.get("lstHabils")
                print(nombre)
                print(strHabils)
                lstHabils=[]
                for n in strHabils.split(","):
                    lstHabils.append(int(n))
                
                headers={}
                body={"nombre":nombre, "lstHabils":lstHabils}
                print(request.json.get("lstHabils"))
                
                response = send_post_request(f"{current_app.config['HOST_PORT_PERFILES']}/perfil/crear", headers=headers, body=body)
                print(response) 
                if response.get("id_perfil")!=0:

                    npp=PerfilesProyecto()
                    npp.nombre=nombre ##request.json.get("nombre")
                    npp.id_cand=0
                    npp.id_proy=proy.id
                    npp.id_perfil=response.get("id_perfil")
                    print(npp.nombre)
                    print(npp.id_proy)
                    perfProy = PerfilesProyecto.query.filter(PerfilesProyecto.nombre == npp.nombre).filter(PerfilesProyecto.id_proy==npp.id_proy).first()
                    if perfProy is not None:
                       print(perfProy.nombre)
                       print(perfProy.id_proy)
                       return {"mensaje": "perfil no se pudo crear: El nombre de perfil suministrado ya existe para este proyecto."}, 400
                    print("Despues de busqueda")
                    db.session.add(npp)
                    db.session.commit()
                    return {"Perfil nuevo: ":perfilesproyecto_schema.dump(npp)}, 200
                else:
                    return {"Mensaje: ":"Error: Perfil no se pudo crear. Error en modulo Perfil."}, 500    
            except Exception as inst:
                db.session.rollback()
                print(type(inst))    # the exception instance
                #print(inst)
                print("Perfil no se pudo crear.")
                return {"Mensaje: ":"Error: Perfil no se pudo crear. Error general. "}, 500
        else:
            return {"Mensaje: ":"Error: Perfil no se pudo crear. El proyecto no existe."}, 400

class VistaPerfiles(Resource):
    def post(self, id_proy):
        print("Crear perfil de Proyecto")
        proy=Proyecto.get_by_id(id_proy)
        if proy is not None:
            try:
                headers={}
                body=request.get_json()
                print(request.json.get("lstHabils"))
                response = send_post_request(f"{current_app.config['HOST_PORT_PERFILES']}/perfil/crear", headers=headers, body=body)
                print(response) 
                if response.get("id_perfil")!=0:
                    npp=PerfilesProyecto()
                    npp.nombre=request.json.get("nombre")
                    npp.id_cand=0
                    npp.id_proy=proy.id
                    npp.id_perfil=response.get("id_perfil")
                    perfProy = PerfilesProyecto.query.filter(PerfilesProyecto.nombre == npp.nombre).filter(PerfilesProyecto.id_proy == npp.id_proy ).first()
                    if perfProy is not None:
                       return {"mensaje": "perfil no se pudo crear: El nombre de perfil suministrado ya existe para este proyecto."}, 400
                    db.session.add(npp)
                    db.session.commit()
                    return {"Perfil nuevo: ":perfilesproyecto_schema.dump(npp)}, 200
                else:
                    return {"Mensaje: ":"Error: Perfil no se pudo crear. Error en modulo Perfil."}, 500    
            except Exception as inst:
                db.session.rollback()
                print(type(inst))    # the exception instance
                #print(inst)
                print("Perfil no se pudo crear.")
                return {"Mensaje: ":"Error: Perfil no se pudo crear. Error general. "}, 500
        else:
            return {"Mensaje: ":"Error: Perfil no se pudo crear. El proyecto no existe."}, 400

class VistaEmpresaPuestosOfrecidosNoAsignados(Resource):
    def post(self, id_empresa):
        print("Obtener Puestos Ofrecidos por una empresa NO Asignados")
        print(id_empresa)
        max=request.json.get("max", 50)
        num_pag=request.json.get("num_pag", 1)
        order=request.json.get("order", "ASC")
        proyecto=request.json.get("proyecto", "Solidaria")
        perfil=request.json.get("perfil", "Solidaria")
        candidato=request.json.get("candidato", "Solidaria")
        lstNumCand=request.json.get("lstNumCand", [0])
        print("json: ")
        print(request.json)
        print("lstNumCand")
        print(lstNumCand)
        #time.sleep(1)
        #if request.get_json()['order']=="ASC":
               
        numPuestos=db.session.query(Proyecto.nombre.label('nom_proyecto'),
                                Proyecto.fecha_inicio,
                                PerfilesProyecto.nombre.label('nom_perfil'),
                                PerfilesProyecto.id,
                                PerfilesProyecto.id_perfil,
                                PerfilesProyecto.id_cand,
                                PerfilesProyecto.fecha_asig,
                                ).filter(Proyecto.id_emp==id_empresa
                                ).filter(PerfilesProyecto.id_cand==0
                                ).filter(Proyecto.id==PerfilesProyecto.id_proy
                                ).filter(Proyecto.nombre.ilike(f'%{proyecto}%')
                                ).filter(PerfilesProyecto.nombre.ilike(f'%{perfil}%')
                                ).count()
        lstPuestos=db.session.query(Proyecto.nombre.label('nom_proyecto'),
                                Proyecto.fecha_inicio,
                                PerfilesProyecto.nombre.label('nom_perfil'),
                                PerfilesProyecto.id,
                                PerfilesProyecto.id_perfil,
                                PerfilesProyecto.id_cand,
                                PerfilesProyecto.fecha_asig,
                                ).filter(Proyecto.id_emp==id_empresa
                                ).filter(PerfilesProyecto.id_cand==0
                                ).filter(Proyecto.id==PerfilesProyecto.id_proy
                                ).filter(Proyecto.nombre.ilike(f'%{proyecto}%')
                                ).filter(PerfilesProyecto.nombre.ilike(f'%{perfil}%')
                                ).order_by(Proyecto.nombre.asc(), PerfilesProyecto.nombre.asc()
                                ).paginate(page=num_pag, per_page=max, error_out=False)
        
        for p in lstPuestos:
            print(p.nom_proyecto, p.nom_perfil, p.id, p.id_perfil, p.id_cand, p.fecha_inicio, p.fecha_asig)
        data = []
        i=0
        for p in lstPuestos:
            i=i+1
            puesto_data = {
                'Num':(num_pag-1)*max + i,
                'nom_empresa': '',
                'nom_proyecto': p.nom_proyecto,
                'nom_perfil': p.nom_perfil,
                'id': p.id,
                'id_perfil': p.id_perfil,
                'id_cand': p.id_cand,
                'candidato': '',
                'fecha_inicio': p.fecha_inicio.isoformat() if p.fecha_inicio else '',
                'fecha_asig': p.fecha_asig.isoformat() if p.fecha_asig else ''
            }
            data.append(puesto_data)
        return {'Puestos': data, 'totalCount': numPuestos}, 200


class VistaEmpresaPuestosOfrecidosAsignados(Resource):
    def post(self, id_empresa):
        print("Obtener Puestos Ofrecidos por una empresa Asignados")
        print(id_empresa)
        max=request.json.get("max", 50)
        num_pag=request.json.get("num_pag", 1)
        order=request.json.get("order", "ASC")
        proyecto=request.json.get("proyecto", "Solidaria")
        perfil=request.json.get("perfil", "Solidaria")
        candidato=request.json.get("candidato", "Solidaria")
        lstNumCand=request.json.get("lstNumCand", [0])
        print("json: ")
        print(request.json)
        print("lstNumCand")
        print(lstNumCand)
        #time.sleep(1)
        #if request.get_json()['order']=="ASC":
        if lstNumCand==[-1]:
            numPuestos=db.session.query(Proyecto.nombre.label('nom_proyecto'),
                                    Proyecto.fecha_inicio,
                                    PerfilesProyecto.nombre.label('nom_perfil'),
                                    PerfilesProyecto.id,
                                    PerfilesProyecto.id_perfil,
                                    PerfilesProyecto.id_cand,
                                    PerfilesProyecto.fecha_asig,
                                    ).filter(Proyecto.id_emp==id_empresa
                                    ).filter(PerfilesProyecto.id_cand!=0
                                    ).filter(Proyecto.id==PerfilesProyecto.id_proy
                                    ).filter(Proyecto.nombre.ilike(f'%{proyecto}%')
                                    ).filter(PerfilesProyecto.nombre.ilike(f'%{perfil}%')
                                    ).count()
            lstPuestos=db.session.query(Proyecto.nombre.label('nom_proyecto'),
                                    Proyecto.fecha_inicio,
                                    PerfilesProyecto.nombre.label('nom_perfil'),
                                    PerfilesProyecto.id,
                                    PerfilesProyecto.id_perfil,
                                    PerfilesProyecto.id_cand,
                                    PerfilesProyecto.fecha_asig,
                                    ).filter(Proyecto.id_emp==id_empresa
                                    ).filter(PerfilesProyecto.id_cand!=0
                                    ).filter(Proyecto.id==PerfilesProyecto.id_proy
                                    ).filter(Proyecto.nombre.ilike(f'%{proyecto}%')
                                    ).filter(PerfilesProyecto.nombre.ilike(f'%{perfil}%')
                                    ).order_by(Proyecto.nombre.asc(), PerfilesProyecto.nombre.asc()
                                    ).paginate(page=num_pag, per_page=max, error_out=False)
        else:
            numPuestos=db.session.query(Proyecto.nombre.label('nom_proyecto'),
                                    Proyecto.fecha_inicio,
                                    PerfilesProyecto.nombre.label('nom_perfil'),
                                    PerfilesProyecto.id,
                                    PerfilesProyecto.id_perfil,
                                    PerfilesProyecto.id_cand,
                                    PerfilesProyecto.fecha_asig,
                                    ).filter(Proyecto.id_emp==id_empresa
                                    ).filter(PerfilesProyecto.id_cand!=0
                                    ).filter(Proyecto.id==PerfilesProyecto.id_proy
                                    ).filter(Proyecto.nombre.ilike(f'%{proyecto}%')
                                    ).filter(PerfilesProyecto.nombre.ilike(f'%{perfil}%')
                                    ).filter(PerfilesProyecto.id_cand.in_(lstNumCand)
                                    ).count()
            lstPuestos=db.session.query(Proyecto.nombre.label('nom_proyecto'),
                                    Proyecto.fecha_inicio,
                                    PerfilesProyecto.nombre.label('nom_perfil'),
                                    PerfilesProyecto.id,
                                    PerfilesProyecto.id_perfil,
                                    PerfilesProyecto.id_cand,
                                    PerfilesProyecto.fecha_asig,
                                    ).filter(Proyecto.id_emp==id_empresa
                                    ).filter(PerfilesProyecto.id_cand!=0
                                    ).filter(Proyecto.id==PerfilesProyecto.id_proy
                                    ).filter(Proyecto.nombre.ilike(f'%{proyecto}%')
                                    ).filter(PerfilesProyecto.nombre.ilike(f'%{perfil}%')
                                    ).filter(PerfilesProyecto.id_cand.in_(lstNumCand)                                             
                                    ).order_by(Proyecto.nombre.asc(), PerfilesProyecto.nombre.asc()
                                    ).paginate(page=num_pag, per_page=max, error_out=False)
        for p in lstPuestos:
            print(p.nom_proyecto, p.nom_perfil, p.id, p.id_perfil, p.id_cand, p.fecha_inicio, p.fecha_asig)
        data = []
        i=0
        for p in lstPuestos:
            i=i+1
            puesto_data = {
                'Num':(num_pag-1)*max + i,
                'nom_empresa': '',
                'nom_proyecto': p.nom_proyecto,
                'nom_perfil': p.nom_perfil,
                'id': p.id,
                'id_perfil': p.id_perfil,
                'id_cand': p.id_cand,
                'candidato': '',
                'fecha_inicio': p.fecha_inicio.isoformat() if p.fecha_inicio else '',
                'fecha_asig': p.fecha_asig.isoformat() if p.fecha_asig else ''
            }
            data.append(puesto_data)
        return {'Puestos': data, 'totalCount': numPuestos}, 200


class VistaEmpresaPuestosOfrecidos(Resource):
    def post(self, id_empresa):
        print("Obtener Puestos Ofrecidos por una empresa")
        print(id_empresa)
        max=request.json.get("max", 50)
        num_pag=request.json.get("num_pag", 1)
        order=request.json.get("order", "ASC")
        proyecto=request.json.get("proyecto", "Solidaria")
        perfil=request.json.get("perfil", "Solidaria")
        candidato=request.json.get("candidato", "Solidaria")
        lstNumCand=request.json.get("lstNumCand", [0])
        print("json: ")
        print(request.json)
        print("lstNumCand")
        print(lstNumCand)
        #time.sleep(1)
        #if request.get_json()['order']=="ASC":
        if lstNumCand==[-1]:
            numPuestos=db.session.query(Proyecto.nombre.label('nom_proyecto'),
                                    Proyecto.fecha_inicio,
                                    PerfilesProyecto.nombre.label('nom_perfil'),
                                    PerfilesProyecto.id,
                                    PerfilesProyecto.id_perfil,
                                    PerfilesProyecto.id_cand,
                                    PerfilesProyecto.fecha_asig,
                                    ).filter(Proyecto.id_emp==id_empresa
                                    ).filter(Proyecto.id==PerfilesProyecto.id_proy
                                    ).filter(Proyecto.nombre.ilike(f'%{proyecto}%')
                                    ).filter(PerfilesProyecto.nombre.ilike(f'%{perfil}%')
                                    ).count()
            lstPuestos=db.session.query(Proyecto.nombre.label('nom_proyecto'),
                                    Proyecto.fecha_inicio,
                                    PerfilesProyecto.nombre.label('nom_perfil'),
                                    PerfilesProyecto.id,
                                    PerfilesProyecto.id_perfil,
                                    PerfilesProyecto.id_cand,
                                    PerfilesProyecto.fecha_asig,
                                    ).filter(Proyecto.id_emp==id_empresa
                                    ).filter(Proyecto.id==PerfilesProyecto.id_proy
                                    ).filter(Proyecto.nombre.ilike(f'%{proyecto}%')
                                    ).filter(PerfilesProyecto.nombre.ilike(f'%{perfil}%')
                                    ).order_by(Proyecto.nombre.asc(), PerfilesProyecto.nombre.asc()
                                    ).paginate(page=num_pag, per_page=max, error_out=False)
        else:
            numPuestos=db.session.query(Proyecto.nombre.label('nom_proyecto'),
                                    Proyecto.fecha_inicio,
                                    PerfilesProyecto.nombre.label('nom_perfil'),
                                    PerfilesProyecto.id,
                                    PerfilesProyecto.id_perfil,
                                    PerfilesProyecto.id_cand,
                                    PerfilesProyecto.fecha_asig,
                                    ).filter(Proyecto.id_emp==id_empresa
                                    ).filter(Proyecto.id==PerfilesProyecto.id_proy
                                    ).filter(Proyecto.nombre.ilike(f'%{proyecto}%')
                                    ).filter(PerfilesProyecto.nombre.ilike(f'%{perfil}%')
                                    ).filter(PerfilesProyecto.id_cand.in_(lstNumCand)
                                    ).count()
            lstPuestos=db.session.query(Proyecto.nombre.label('nom_proyecto'),
                                    Proyecto.fecha_inicio,
                                    PerfilesProyecto.nombre.label('nom_perfil'),
                                    PerfilesProyecto.id,
                                    PerfilesProyecto.id_perfil,
                                    PerfilesProyecto.id_cand,
                                    PerfilesProyecto.fecha_asig,
                                    ).filter(Proyecto.id_emp==id_empresa
                                    ).filter(Proyecto.id==PerfilesProyecto.id_proy
                                    ).filter(Proyecto.nombre.ilike(f'%{proyecto}%')
                                    ).filter(PerfilesProyecto.nombre.ilike(f'%{perfil}%')
                                    ).filter(PerfilesProyecto.id_cand.in_(lstNumCand)                                             
                                    ).order_by(Proyecto.nombre.asc(), PerfilesProyecto.nombre.asc()
                                    ).paginate(page=num_pag, per_page=max, error_out=False)
        for p in lstPuestos:
            print(p.nom_proyecto, p.nom_perfil, p.id, p.id_perfil, p.id_cand, p.fecha_inicio, p.fecha_asig)
        data = []
        i=0
        for p in lstPuestos:
            i=i+1
            puesto_data = {
                'Num':(num_pag-1)*max + i,
                'nom_empresa': '',
                'nom_proyecto': p.nom_proyecto,
                'nom_perfil': p.nom_perfil,
                'id': p.id,
                'id_perfil': p.id_perfil,
                'id_cand': p.id_cand,
                'candidato': '',
                'fecha_inicio': p.fecha_inicio.isoformat() if p.fecha_inicio else '',
                'fecha_asig': p.fecha_asig.isoformat() if p.fecha_asig else ''
            }
            data.append(puesto_data)
        return {'Puestos': data, 'totalCount': numPuestos}, 200


def get(self, id_usuario):
        print("Consulta Empresa Usuario")
        try:
            empresa = Empresa.get_by_idUser(id_usuario)
        except Exception as inst:
            print("excepcion")
            print(type(inst))    # the exception instance
            print(inst)
            return {"Error:": "Error en el Servidor"}, 500
        return empresa_schema.dump(empresa), 200


class VistaEvalsPuesto(Resource):
    def get(self, id_proyperfil):
        print("Obtener Evaluaciones de un Puesto")
        print("id_proyperfil")
        print(id_proyperfil)
        try:
            lstEvals=EvalMensual.get_by_idPerfilProy(id_proyperfil)
        except Exception as inst:
            db.session.rollback()
            print(type(inst))    # the exception instance
            print(inst)
            print("No se pudo obtener las Evaluaciones del Puesto.")
            return {"Mensaje: ":"Error: No se pudo obtener las Evaluaciones del Puesto."+str(type(inst))}, 500
        return  {"lstEvals":[evalmensual_schema.dump(e) for e in lstEvals]}, 200

class VistaPuestosOfrecidosNoAsignados(Resource):
    def post(self):
        print("Obtener Puestos Ofrecidos No Asignados")
        max=request.json.get("max", 50)
        num_pag=request.json.get("num_pag", 1)
        order=request.json.get("order", "ASC")
        empresa=request.json.get("empresa", "")
        proyecto=request.json.get("proyecto", "")
        perfil=request.json.get("perfil", "")
        candidato=request.json.get("candidato", "")
        lstNumCand=request.json.get("lstNumCand", [0])
        print("json: ")
        print(request.json)
        print("lstNumCand")
        print(lstNumCand)
        #time.sleep(1)
        #if request.get_json()['order']=="ASC":

        numPuestos=db.session.query(Empresa.nombre.label('nom_empresa'), 
                                Proyecto.fecha_inicio,
                                Proyecto.nombre.label('nom_proyecto'),
                                PerfilesProyecto.nombre.label('nom_perfil'),
                                PerfilesProyecto.id,
                                PerfilesProyecto.id_perfil,
                                PerfilesProyecto.id_cand,
                                PerfilesProyecto.fecha_asig
                                ).filter(Empresa.id==Proyecto.id_emp
                                ).filter(Proyecto.id==PerfilesProyecto.id_proy
                                ).filter(PerfilesProyecto.id_cand==0
                                ).filter(Empresa.nombre.ilike(f'%{empresa}%')
                                ).filter(Proyecto.nombre.ilike(f'%{proyecto}%')
                                ).filter(PerfilesProyecto.nombre.ilike(f'%{perfil}%')                                             
                                ).count()
        print("Num_Puestos")
        print(numPuestos)
        lstPuestos=db.session.query(Empresa.nombre.label('nom_empresa'), 
                                Proyecto.fecha_inicio,
                                Proyecto.nombre.label('nom_proyecto'),
                                PerfilesProyecto.nombre.label('nom_perfil'),
                                PerfilesProyecto.id,
                                PerfilesProyecto.id_perfil,
                                PerfilesProyecto.id_cand,
                                PerfilesProyecto.fecha_asig
                                ).filter(Empresa.id==Proyecto.id_emp
                                ).filter(Proyecto.id==PerfilesProyecto.id_proy
                                ).filter(PerfilesProyecto.id_cand==0
                                ).filter(Empresa.nombre.ilike(f'%{empresa}%')
                                ).filter(Proyecto.nombre.ilike(f'%{proyecto}%')
                                ).filter(PerfilesProyecto.nombre.ilike(f'%{perfil}%')
                                ).order_by(Empresa.nombre.asc(), Proyecto.nombre.asc(), PerfilesProyecto.nombre.asc()
                                ).paginate(page=num_pag, per_page=max, error_out=False)
        for p in lstPuestos:
            print(p.nom_empresa, p.nom_proyecto, p.nom_perfil, p.id, p.id_perfil, p.id_cand )
        data = []
        i=0
        for p in lstPuestos:
            i=i+1
            puesto_data = {
                'Num':(num_pag-1)*max + i,
                'nom_empresa': p.nom_empresa,
                'nom_proyecto': p.nom_proyecto,
                'nom_perfil': p.nom_perfil,
                'id': p.id,
                'id_perfil': p.id_perfil,
                'id_cand': p.id_cand,
                'candidato': '',
                'fecha_inicio': p.fecha_inicio.isoformat() if p.fecha_inicio else '',
                'fecha_asig': p.fecha_asig.isoformat() if p.fecha_asig else ''
            }
            data.append(puesto_data)
        return {'Puestos': data, 'totalCount': numPuestos}, 200

class VistaPuestosOfrecidosAsignados(Resource):
    def post(self):
        print("Obtener Puestos Ofrecidos Asignados")
        max=request.json.get("max", 50)
        num_pag=request.json.get("num_pag", 1)
        order=request.json.get("order", "ASC")
        empresa=request.json.get("empresa", "")
        proyecto=request.json.get("proyecto", "")
        perfil=request.json.get("perfil", "")
        candidato=request.json.get("candidato", "")
        lstNumCand=request.json.get("lstNumCand", [0])
        print("json: ")
        print(request.json)
        print("lstNumCand")
        print(lstNumCand)
        #time.sleep(1)
        #if request.get_json()['order']=="ASC":
        if lstNumCand==[-1]:
            numPuestos=db.session.query(Empresa.nombre.label('nom_empresa'), 
                                    Proyecto.fecha_inicio,
                                    Proyecto.nombre.label('nom_proyecto'),
                                    PerfilesProyecto.nombre.label('nom_perfil'),
                                    PerfilesProyecto.id,
                                    PerfilesProyecto.id_perfil,
                                    PerfilesProyecto.id_cand,
                                    PerfilesProyecto.fecha_asig
                                    ).filter(Empresa.id==Proyecto.id_emp
                                    ).filter(Proyecto.id==PerfilesProyecto.id_proy
                                    ).filter(PerfilesProyecto.id_cand!=0
                                    ).filter(Empresa.nombre.ilike(f'%{empresa}%')
                                    ).filter(Proyecto.nombre.ilike(f'%{proyecto}%')
                                    ).filter(PerfilesProyecto.nombre.ilike(f'%{perfil}%')                                             
                                    ).count()
            print("Num_Puestos")
            print(numPuestos)
            lstPuestos=db.session.query(Empresa.nombre.label('nom_empresa'), 
                                    Proyecto.fecha_inicio,
                                    Proyecto.nombre.label('nom_proyecto'),
                                    PerfilesProyecto.nombre.label('nom_perfil'),
                                    PerfilesProyecto.id,
                                    PerfilesProyecto.id_perfil,
                                    PerfilesProyecto.id_cand,
                                    PerfilesProyecto.fecha_asig
                                    ).filter(Empresa.id==Proyecto.id_emp
                                    ).filter(Proyecto.id==PerfilesProyecto.id_proy
                                    ).filter(PerfilesProyecto.id_cand!=0
                                    ).filter(Empresa.nombre.ilike(f'%{empresa}%')
                                    ).filter(Proyecto.nombre.ilike(f'%{proyecto}%')
                                    ).filter(PerfilesProyecto.nombre.ilike(f'%{perfil}%')
                                    ).order_by(Empresa.nombre.asc(), Proyecto.nombre.asc(), PerfilesProyecto.nombre.asc()
                                    ).paginate(page=num_pag, per_page=max, error_out=False)
        else:
            numPuestos=db.session.query(Empresa.nombre.label('nom_empresa'), 
                                    Proyecto.fecha_inicio,
                                    Proyecto.nombre.label('nom_proyecto'),
                                    PerfilesProyecto.nombre.label('nom_perfil'),
                                    PerfilesProyecto.id,
                                    PerfilesProyecto.id_perfil,
                                    PerfilesProyecto.id_cand,
                                    PerfilesProyecto.fecha_asig
                                    ).filter(Empresa.id==Proyecto.id_emp
                                    ).filter(Proyecto.id==PerfilesProyecto.id_proy
                                    ).filter(PerfilesProyecto.id_cand!=0
                                    ).filter(Empresa.nombre.ilike(f'%{empresa}%')
                                    ).filter(Proyecto.nombre.ilike(f'%{proyecto}%')
                                    ).filter(PerfilesProyecto.nombre.ilike(f'%{perfil}%')
                                    ).filter(PerfilesProyecto.id_cand.in_(lstNumCand)
                                    ).count()
            lstPuestos=db.session.query(Empresa.nombre.label('nom_empresa'), 
                                    Proyecto.fecha_inicio,
                                    Proyecto.nombre.label('nom_proyecto'),
                                    PerfilesProyecto.nombre.label('nom_perfil'),
                                    PerfilesProyecto.id,
                                    PerfilesProyecto.id_perfil,
                                    PerfilesProyecto.id_cand,
                                    PerfilesProyecto.fecha_asig
                                    ).filter(Empresa.id==Proyecto.id_emp
                                    ).filter(Proyecto.id==PerfilesProyecto.id_proy
                                    ).filter(PerfilesProyecto.id_cand!=0
                                    ).filter(Empresa.nombre.ilike(f'%{empresa}%')
                                    ).filter(Proyecto.nombre.ilike(f'%{proyecto}%')
                                    ).filter(PerfilesProyecto.nombre.ilike(f'%{perfil}%')
                                    ).filter(PerfilesProyecto.id_cand.in_(lstNumCand)                                             
                                    ).order_by(Empresa.nombre.asc(), Proyecto.nombre.asc(), PerfilesProyecto.nombre.asc()
                                    ).paginate(page=num_pag, per_page=max, error_out=False)
        for p in lstPuestos:
            print(p.nom_empresa, p.nom_proyecto, p.nom_perfil, p.id, p.id_perfil, p.id_cand )
        data = []
        i=0
        for p in lstPuestos:
            i=i+1
            puesto_data = {
                'Num':(num_pag-1)*max + i,
                'nom_empresa': p.nom_empresa,
                'nom_proyecto': p.nom_proyecto,
                'nom_perfil': p.nom_perfil,
                'id': p.id,
                'id_perfil': p.id_perfil,
                'id_cand': p.id_cand,
                'candidato': '',
                'fecha_inicio': p.fecha_inicio.isoformat() if p.fecha_inicio else '',
                'fecha_asig': p.fecha_asig.isoformat() if p.fecha_asig else ''
            }
            data.append(puesto_data)
        return {'Puestos': data, 'totalCount': numPuestos}, 200


class VistaPuestosOfrecidos(Resource):
    def post(self):
        print("Obtener Puestos Ofrecidos")
        max=request.json.get("max", 50)
        num_pag=request.json.get("num_pag", 1)
        order=request.json.get("order", "ASC")
        empresa=request.json.get("empresa", "")
        proyecto=request.json.get("proyecto", "")
        perfil=request.json.get("perfil", "")
        candidato=request.json.get("candidato", "")
        lstNumCand=request.json.get("lstNumCand", [0])
        print("json: ")
        print(request.json)
        print("lstNumCand")
        print(lstNumCand)
        #time.sleep(1)
        #if request.get_json()['order']=="ASC":
        if lstNumCand==[-1]:
            numPuestos=db.session.query(Empresa.nombre.label('nom_empresa'), 
                                    Proyecto.nombre.label('nom_proyecto'),
                                    PerfilesProyecto.nombre.label('nom_perfil'),
                                    PerfilesProyecto.id,
                                    PerfilesProyecto.id_perfil,
                                    PerfilesProyecto.id_cand
                                    ).filter(Empresa.id==Proyecto.id_emp
                                    ).filter(Proyecto.id==PerfilesProyecto.id_proy
                                    ).filter(Empresa.nombre.ilike(f'%{empresa}%')
                                    ).filter(Proyecto.nombre.ilike(f'%{proyecto}%')
                                    ).filter(PerfilesProyecto.nombre.ilike(f'%{perfil}%')                                             
                                    ).count()
            print("Num_Puestos")
            print(numPuestos)
            lstPuestos=db.session.query(Empresa.nombre.label('nom_empresa'), 
                                    Proyecto.nombre.label('nom_proyecto'),
                                    PerfilesProyecto.nombre.label('nom_perfil'),
                                    PerfilesProyecto.id,
                                    PerfilesProyecto.id_perfil,
                                    PerfilesProyecto.id_cand
                                    ).filter(Empresa.id==Proyecto.id_emp
                                    ).filter(Proyecto.id==PerfilesProyecto.id_proy
                                    ).filter(Empresa.nombre.ilike(f'%{empresa}%')
                                    ).filter(Proyecto.nombre.ilike(f'%{proyecto}%')
                                    ).filter(PerfilesProyecto.nombre.ilike(f'%{perfil}%')
                                    ).order_by(Empresa.nombre.asc(), Proyecto.nombre.asc(), PerfilesProyecto.nombre.asc()
                                    ).paginate(page=num_pag, per_page=max, error_out=False)
        else:
            numPuestos=db.session.query(Empresa.nombre.label('nom_empresa'), 
                                    Proyecto.nombre.label('nom_proyecto'),
                                    PerfilesProyecto.nombre.label('nom_perfil'),
                                    PerfilesProyecto.id,
                                    PerfilesProyecto.id_perfil,
                                    PerfilesProyecto.id_cand
                                    ).filter(Empresa.id==Proyecto.id_emp
                                    ).filter(Proyecto.id==PerfilesProyecto.id_proy
                                    ).filter(Empresa.nombre.ilike(f'%{empresa}%')
                                    ).filter(Proyecto.nombre.ilike(f'%{proyecto}%')
                                    ).filter(PerfilesProyecto.nombre.ilike(f'%{perfil}%')
                                    ).filter(PerfilesProyecto.id_cand.in_(lstNumCand)
                                    ).count()
            lstPuestos=db.session.query(Empresa.nombre.label('nom_empresa'), 
                                    Proyecto.nombre.label('nom_proyecto'),
                                    PerfilesProyecto.nombre.label('nom_perfil'),
                                    PerfilesProyecto.id,
                                    PerfilesProyecto.id_perfil,
                                    PerfilesProyecto.id_cand
                                    ).filter(Empresa.id==Proyecto.id_emp
                                    ).filter(Proyecto.id==PerfilesProyecto.id_proy
                                    ).filter(Empresa.nombre.ilike(f'%{empresa}%')
                                    ).filter(Proyecto.nombre.ilike(f'%{proyecto}%')
                                    ).filter(PerfilesProyecto.nombre.ilike(f'%{perfil}%')
                                    ).filter(PerfilesProyecto.id_cand.in_(lstNumCand)                                             
                                    ).order_by(Empresa.nombre.asc(), Proyecto.nombre.asc(), PerfilesProyecto.nombre.asc()
                                    ).paginate(page=num_pag, per_page=max, error_out=False)
        for p in lstPuestos:
            print(p.nom_empresa, p.nom_proyecto, p.nom_perfil, p.id, p.id_perfil, p.id_cand )
        data = []
        i=0
        for p in lstPuestos:
            i=i+1
            puesto_data = {
                'Num':(num_pag-1)*max + i,
                'nom_empresa': p.nom_empresa,
                'nom_proyecto': p.nom_proyecto,
                'nom_perfil': p.nom_perfil,
                'id': p.id,
                'id_perfil': p.id_perfil,
                'id_cand': p.id_cand,
                'candidato': ''
            }
            data.append(puesto_data)
        return {'Puestos': data, 'totalCount': numPuestos}, 200
    
    #lstHabils=db.session.query(Perfil.id, (HabilPerfil.id).label('num_habilperfil'), HabilPerfil.calificacion, HabilPerfil.valoracion, (Habilidad.id).label('num_habil'), Habilidad.nombre, Habilidad.tipo
    #       ).filter(Perfil.id==HabilPerfil.id_perfil
    #       ).filter(HabilPerfil.id_habil==Habilidad.id
    #       ).filter(Perfil.id==id_perfil).all()
    #len(data)
    #long_lista=len(lstHabils)
    #conteo=(func.count(HabilPerfil.id_perfil)).label('conteo')
    #lstCumplenHabils = db.session.query(HabilPerfil.id_perfil, HabilPerfil.id_habil, HabilPerfil.valoracion).filter(HabilPerfil.id_perfil.in_(db.session.query(HabilPerfil.id_perfil).filter(HabilPerfil.id_habil.in_(lstHabils)).group_by(HabilPerfil.id_perfil).having(conteo==long_lista)))

    #queryLongCorrecta=db.session.query(HabilPerfil.id_perfil, conteo).group_by(HabilPerfil.id_perfil).having(conteo==long_lista).all()   

class VistaAsignaCandidato(Resource):
    def post(self, id_proyperfil):
        print("Asignacion Candidato PerfilProyecto")
        try:
            print(request.json)
            id_cand=request.json.get("id_cand", None)
            fecha_inicio=request.json.get("fecha_inicio", None)
            if fecha_inicio:
                dateFecha_Inicio=datetime.strptime(fecha_inicio, '%Y-%m-%d')
                if id_cand is not None:
                    pp = PerfilesProyecto.query.filter(PerfilesProyecto.id == id_proyperfil).first()
                    if pp is not None:
                        pp.id_cand=id_cand
                        if dateFecha_Inicio > datetime.now():
                            pp.fecha_asig=dateFecha_Inicio
                        else:
                            pp.fecha_asig=datetime.now()  
                        db.session.add(pp)
                        db.session.commit()
                        return {"perfilProyecto":perfiles_proyecto_schema.dump(pp)}, 200  ## OJO ERROR
                    else:
                        print("1")
                        return {"mensaje": "PerfilProyecto no se pudo actualizar: El perfil suministrado NO existe."}, 400 
                else:
                    print("2")
                    return {"mensaje": "PerfilProyecto no se pudo actualizar: falta el parametro candidato."}, 400
            else:
                print("3")
                return {"mensaje": "PerfilProyecto no se pudo actualizar: falta el parametro fecha Inicio."}, 400
        except Exception as inst:
            db.session.rollback()
            print(type(inst))    # the exception instance
            print(inst)
            print("PerfilProyecto no se pudo actualizar.")
            return {"Mensaje: ":"Error: PerfilProyecto no se pudo actualizar."+str(type(inst))}, 500

class VistaPerfilProyectoDet(Resource):
    def get(self, id_proyperfil):
        print("Get PerfilProyecto Detallado")
        print(id_proyperfil)
        p=db.session.query(Empresa.nombre.label('nom_empresa'), 
                           Empresa.contacto.label('contacto_empresa'),
                                Proyecto.nombre.label('nom_proyecto'),
                                Proyecto.fecha_inicio,
                                PerfilesProyecto.nombre.label('nom_perfil'),
                                PerfilesProyecto.id,
                                PerfilesProyecto.id_perfil,
                                PerfilesProyecto.id_cand,
                                PerfilesProyecto.fecha_asig,
                                ).filter(Empresa.id==Proyecto.id_emp
                                ).filter(Proyecto.id==PerfilesProyecto.id_proy
                                ).filter(PerfilesProyecto.id==id_proyperfil).first()
        print(p.nom_empresa, p.nom_proyecto, p.nom_perfil, p.id, p.id_perfil, p.id_cand )
        perfil = {
            'nom_empresa': p.nom_empresa,
            'contacto_empresa': p.contacto_empresa,
            'nom_proyecto': p.nom_proyecto,
            'fecha_inicio': p.fecha_inicio.isoformat(),
            'nom_perfil': p.nom_perfil,
            'id': p.id,
            'id_perfil': p.id_perfil,
            'id_cand': p.id_cand,
            'candidato': '',
            'fecha_asig': p.fecha_asig.isoformat() if p.fecha_asig else ''
        }
        return {'Perfil': perfil}, 200
    
class VistaPing(Resource):
    def get(self):
        print("pong")
        return {"Mensaje":"Pong"}, 200

def send_post_request(url, headers, body):
    try:
        response = requests.post(url, json=body, headers=headers, timeout=5000)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as inst:
        print(type(inst))
        #print(inst)
        return -1

api = Api(application)                        
api.add_resource(VistaEntrevistasCandidatos, '/entrevistasCandidato/<int:id_cand>')
api.add_resource(VistaEntrevistasEmpresas, '/entrevistasEmpresa/<int:id_empresa>')
api.add_resource(VistaLasEntrevistas, '/entrevistasPortal')
api.add_resource(VistaEntrevistas, '/empresas/proyectos/perfiles/entrevistas')
api.add_resource(VistaEntrevistasPuesto, '/empresas/proyectos/perfiles/entrevistas/<int:id_proyperfil>')
api.add_resource(VistaEntrevistasResultado, '/entrevistas/<int:id_entrevista>')

api.add_resource(VistaEvaluaciones, '/empresas/proyectos/perfiles/evaluaciones')
api.add_resource(VistaEvalsPuesto, '/empresas/proyectos/perfiles/evaluaciones/<int:id_proyperfil>')
api.add_resource(VistaAsignaCandidato, '/empresas/proyectos/perfiles/asignacion/<int:id_proyperfil>')
api.add_resource(VistaPerfilProyectoDet, '/empresas/proyectos/perfiles/<int:id_proyperfil>')
api.add_resource(VistaPuestosOfrecidosNoAsignados, '/empresas/puestosNoAsig')
api.add_resource(VistaPuestosOfrecidosAsignados, '/empresas/puestosAsig')
api.add_resource(VistaPuestosOfrecidos, '/empresas/puestos')
api.add_resource(VistaEmpresaPuestosOfrecidos, '/empresas/<int:id_empresa>/puestos')
api.add_resource(VistaEmpresaPuestosOfrecidosNoAsignados, '/empresas/<int:id_empresa>/puestosNoAsig')
api.add_resource(VistaEmpresaPuestosOfrecidosAsignados, '/empresas/<int:id_empresa>/puestosAsig')
api.add_resource(VistaProyectoDetalle, '/empresas/proyectos/<int:id_proy>/detallePerfiles')
api.add_resource(VistaPerfilesStr, '/empresas/proyectos/<int:id_proy>/perfilesStr')
api.add_resource(VistaPerfiles, '/empresas/proyectos/<int:id_proy>/perfiles')
api.add_resource(VistaProyecto, '/empresas/proyecto/<int:id_proy>')
api.add_resource(VistaProyectos, '/empresas/<int:id_emp>/proyectos')
api.add_resource(VistaEmpresaUsuario, '/miempresa/<int:id_usuario>')
api.add_resource(VistaEmpresas, '/empresas')
api.add_resource(VistaEmpresa, '/empresa/<int:id_empresa>')
api.add_resource(VistaEmpresaDetalle, '/empresaDetalle/<int:id_empresa>')
api.add_resource(VistaEmpresaDetalleUsuario, '/empresaUsuarioDetalle/<int:id_usuario>')
api.add_resource(VistaPing, '/empresas/ping')

jwt = JWTManager(application)

faker=Faker()
if Empresa.get_count()==0:
    print("Creando Empresas.")
    regT=0  #nombre,tipo,correo,celular,contacto,pais,ciudad,direccion,id_usuario
    with open("./empresas.txt") as archivo:
        for linea in archivo:
            try:
                campos=linea.split(sep='|')
                cn=Empresa()
                cn.nombre=campos[9]
                cn.nombre=cn.nombre[0:-1]
                cn.tipo=campos[1]
                cn.correo=campos[2]
                cn.celular=campos[3]
                cn.contacto=campos[4]
                cn.pais=campos[5]
                cn.ciudad=campos[6]
                cn.direccion=campos[7]
                cn.estado=Estado.ACTIVO
                db.session.add(cn)
                db.session.commit()
                cn.id_usuario=cn.id+33000
                db.session.add(cn)
                db.session.commit()
                regT=regT+1
            except Exception as inst:
                db.session.rollback()
                print(type(inst))    # the exception instance
                print(inst)
                print("Empresa no se pudo crear.")

if Proyecto.get_count()==0:
    print("Creando Proyectos.")
    regT=0  #nombre|fecha_inicio|id_emp|descripcion
    with open("./proyectos25.txt") as archivo:
        for linea in archivo:
            try:
                campos=linea.split(sep='|')
                cn=Proyecto()
                cn.nombre=campos[0]+"("+campos[4][0:-1]+")"
                cn.fecha_inicio=datetime.strptime(campos[1], '%Y-%m-%d')
                cn.id_emp=int(campos[2])
                cn.descripcion=campos[3]
                db.session.add(cn)
                db.session.commit()
                regT=regT+1
                print("=====================")
                print(cn.nombre)
                print(regT)
            except Exception as inst:
                db.session.rollback()
                print(type(inst))    # the exception instance
                print(inst)
                print("Proyecto no se pudo crear.")

if PerfilesProyecto.get_count()==0:
    print("Creando PerfilesProyectos.")
    regT=0  #nombre,id_proy,id_perfil
    with open("./perfilesproyectos20.txt") as archivo:
        for linea in archivo:
            try:
                campos=linea.split(sep='|')
                cn=PerfilesProyecto()
                cn.nombre=campos[0]
                cn.id_proy=int(campos[1])
                cn.id_perfil=int(campos[2])
                db.session.add(cn)
                db.session.commit()
                regT=regT+1
                print("=====================")
                print(cn.nombre)
                print(regT)
            except Exception as inst:
                db.session.rollback()
                print(type(inst))    # the exception instance
                print(inst)
                print("PerfilProyecto no se pudo crear.")

if Entrevistas.get_count()==0:
    print("Creando Entrevistas.")
    regT=0  #id_cand, idPerfilProy, cuando, contacto, calificacion, valoracion, anotaciones
    with open("./entrevistas.txt") as archivo:
        for linea in archivo:
            try:
                campos=linea.split(sep='|')
                cn=Entrevistas()
                cn.id_cand=int(campos[0])
                cn.idPerfilProy=int(campos[1])
                cn.cuando=datetime.strptime(campos[2][0:-6], '%Y-%m-%dT%H:%M:%S')
                cn.contacto=campos[3]
                cn.valoracion=0
                if campos[4]!="None":
                    cn.calificacion=Calificacion[campos[4]]
                    cn.anotaciones=faker.text(400)
                else:
                    cn.calificacion=None
                    cn.anotaciones=None
                db.session.add(cn)
                db.session.commit()
                regT=regT+1
                print("=====================")
                print(cn.idPerfilProy)
                print(regT)
            except Exception as inst:
                db.session.rollback()
                print(type(inst))    # the exception instance
                print(inst)
                print("Entrevista no se pudo crear.")

if PerfilesProyecto.get_count_assign()==0:
    print("Asignando Candidatos.")
    regT=0  #idPerfilProy, id_cand
    with open("./asignacion.txt") as archivo:
        for linea in archivo:
            try:
                campos=linea.split(sep='|')
                cn=PerfilesProyecto.get_by_id(int(campos[0]))
                cn.id_cand=int(campos[1])
                cn.fecha_asig=date.today()
                db.session.add(cn)
                db.session.commit()
                regT=regT+1
                print("=====================")
                print(cn.id)
                print(regT)
            except Exception as inst:
                db.session.rollback()
                print(type(inst))    # the exception instance
                print(inst)
                print("Asignacion no se pudo hacer.")

if EvalMensual.get_count()==0:
    print("Creando Evaluaciones Mensuales.")
    mesesSpanish=["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"];
    regT=0  #id_cand, idPerfilProy, anno, mes, calificacion, valoracion   // strmes, nota
    with open("./evaluaciones.txt") as archivo:
        for linea in archivo:
            try:
                campos=linea.split(sep='|')
                cn=EvalMensual()
                cn.id_cand=int(campos[0])
                cn.idPerfilProy=int(campos[1])
                cn.anno=int(campos[2])
                cn.mes=int(campos[3])-1
                cn.strmes=mesesSpanish[cn.mes]
                cn.calificacion=Calificacion[campos[4]]
                cn.valoracion=0
                cn.nota=faker.text(300)
                db.session.add(cn)
                db.session.commit()
                regT=regT+1
                print("=====================")
                print(cn.id)
                print(regT)
            except Exception as inst:
                db.session.rollback()
                print(type(inst))    # the exception instance
                print(inst)
                print("Evaluacion no se pudo crear.")

if False:
    host=f"{application.config['HOST_PORT_GATEWAY']}"
    headers={} #headers = {"Authorization": f"Bearer {os.environ.get('TRUE_NATIVE_TOKEN')}"}
    with open("./evaluaciones.txt", "xt+") as archivo:
        #id_cand, idPerfilProy, anno, mes, calificacion, valoracion   // strmes, nota
        for i in range(10000):          
            p=PerfilesProyecto.get_by_id(i+1)
            j=Proyecto.get_by_id(p.id_proy)
            lstEvals=EvalMensual.get_by_idPerfilProy(p.id)
            if len(lstEvals)==0:
                FechaInicio=p.fecha_asig
                if j.fecha_inicio>FechaInicio:
                    FechaInicio=j.fecha_inicio
                #print("Fecha_inicio: ", FechaInicio)
                #print("Fecha_asig: ", p.fecha_asig)
                #print("Fecha_proy: ", j.fecha_inicio)
                mes_ini=FechaInicio.month
                anno_ini=FechaInicio.year
                if p.id_cand!=0:
                    num_evals=random.randint(1, 3)
                    for k in range(num_evals):
                        #print("anno: ", anno_ini)
                        #print("mes: ", mes_ini)
                        linea=str(p.id_cand)+"|"+str(p.id)+"|"+str(anno_ini)+"|"+str(mes_ini)+"|"+Calificacion(random.randint(1,4)).name+"|"+"0"+"\n"                        
                        print(linea)
                        archivo.write(linea)
                        mes_ini=mes_ini+1
                        if mes_ini==13:
                            mes_ini=1
                            anno_ini=anno_ini+1
        archivo.close()    

if False:
    host=f"{application.config['HOST_PORT_GATEWAY']}"
    headers={} #headers = {"Authorization": f"Bearer {os.environ.get('TRUE_NATIVE_TOKEN')}"}
    with open("./entrevistas.txt", "xt+") as archivo:
        #id_cand, idPerfilProy, cuando, contacto, calificacion, valoracion, anotaciones
        for i in range(20000):          
            p=PerfilesProyecto.get_by_id(i+1)
            if p.id_perfil!=0:
                url=host+'/cumplenPerfil/'+str(p.id_perfil)
                response = requests.get(url=url, headers=headers, timeout=5000)
                #print("==================")
                #print(response.json())
                #print("==================")
                #print(response.json().get("Respuesta").get("Seleccion"))
                lstCandCumplen=response.json().get("Respuesta").get("Seleccion")
                conteo=0
                for c in lstCandCumplen:
                    conteo=conteo+1
                    if conteo<=3:
                        calificacion=""
                        calif=random.randint(0, 4)
                        if calif==0:
                            calificacion="None"
                        else:    
                            calificacion=Calificacion(calif).name
                        fechayhora=faker.date_between(start_date= "+1d" ,end_date= "+30d" )
                        cuandoStr=fechayhora.strftime('%Y-%m-%d')
                        hora=str(random.randint(8, 21)).zfill(2)
                        min=str(random.randint(0,2)*20).zfill(2)
                        cuandoStr=cuandoStr+"T"+hora+":"+min+":00-05:00" #":00-05:00"
                        #print(cuandoStr)
                        linea=str(c["id_cand"])+"|"+str(p.id)+"|"+cuandoStr+"|"+faker.name()+"|"+calificacion+"|"+"0"+"\n"                        
                        print(linea)
                        archivo.write(linea)
            else:
                print("Warning: existe al menos un id_perfil igual a cero. En: ", p.id)
        archivo.close()    


if False:
    host=f"{application.config['HOST_PORT_GATEWAY']}"
    headers={} #headers = {"Authorization": f"Bearer {os.environ.get('TRUE_NATIVE_TOKEN')}"}
    with open("./asignacion.txt", "xt+") as archivo:
        #idPerfilProy, id_cand
        for i in range(10000):          
            p=PerfilesProyecto.get_by_id(i+1)
            if p.id_perfil!=0:
                url=host+'/cumplenPerfil/'+str(p.id_perfil)
                response = requests.get(url=url, headers=headers, timeout=5000)
                lstCandCumplen=response.json().get("Respuesta").get("Seleccion")
                eleccion=random.randint(1,4)
                conteo=0
                for c in lstCandCumplen:
                    conteo=conteo+1
                    if conteo==eleccion:
                        linea=str(p.id)+"|"+str(c["id_cand"])+"\n"                        
                        print(linea)
                        archivo.write(linea)
            else:
                print("Warning: existe al menos un id_perfil igual a cero. En: ", p.id)
        archivo.close()    

