import json
import time
from flask import Response
from flask_jwt_extended import create_access_token
from datetime import timedelta
import datetime

from unittest import TestCase
from unittest.mock import Mock, patch
import uuid 
import random

from application import application

class testBlackList(TestCase):

    def setUp(self):
        self.client=application.test_client()
        self.tokenfijo="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4MDYyMzQwNCwianRpIjoiZmVjYTI5NTAtY2I1My00ZWVkLWFiN2ItZjM5ZTMwMDg2NzkxIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjgwNjIzNDA0fQ.aF924YU7GlLR_u6YuFZeZgul2o75ltDYrNkIC6e4a4Q"
        self.userId=2
        self.offerId=1
        self.postId=1
        access_token_expires = timedelta(minutes=120)
        self.token=create_access_token(identity=self.userId, expires_delta=access_token_expires)
        access_token_expires = timedelta(seconds=3)
        self.tokenexpired=create_access_token(identity=self.userId, expires_delta=access_token_expires)
        #self.token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY3NTczMTY3MywianRpIjoiOGU1OWJjZmQtNTJlYi00YzQ1LWI1NDUtZTU3MGYxMDBiNTQ0IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MiwibmJmIjoxNjc1NzMxNjczLCJleHAiOjE2NzU3Mzg4NzN9.iPaNwx0Sp2TcPOyv5p12e7RyPAUDih3lrLxV0mVN43Q"
        #self.tokenexpired="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY3NTY4NDg3NiwianRpIjoiZjdkYzNlN2QtMzFhNy00NWZhLTg3NjItNzIwZDQ0NTUyMWZjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MiwibmJmIjoxNjc1Njg0ODc2LCJleHAiOjE2NzU2ODY2NzZ9.fPQFhAK_4k16NqpMGcT2eV-q-PQRUKHrLMiQY-xzDYM"


    def test_ping(self):
        endpoint_ping='/empresas/ping'
        solicitud_ping=self.client.get(endpoint_ping)
        respuesta_ping=json.loads(solicitud_ping.get_data())
        msg=respuesta_ping["Mensaje"]
        self.assertEqual(solicitud_ping.status_code, 200)
        self.assertIn("Pong", msg)

    def test_crea_empresa(self):
        headers={
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.tokenfijo)
        }

        endpoint_empresa='/empresas'

        unico=str(uuid.uuid1())
        nombre_empresa="Nombre Empresa"+unico
        correo=nombre_empresa+'@correo.com'
        usuario=random.randint(10000, 100000000)
        nueva_empresa={
            "nombre":nombre_empresa,
            "tipo":"Comercio",
            "correo":correo,
            "celular":"3042384590",
            "contacto":"Lep Corp14",
            "pais":"Colombia",
            "ciudad":"Valledupar",
            "direccion":"Calle 7 # 11 - 10",
            "id_usuario":usuario,
            "is_active":True,
            "estado":"ACTIVO"
        }

        solicitud_crear=self.client.post(endpoint_empresa, 
                                                data=json.dumps(nueva_empresa), 
                                                headers=headers)
        respuesta_crear=json.loads(solicitud_crear.get_data())
        print(respuesta_crear['Empresa']['correo'])
        #jj=respuesta_crear['Seleccion'][0]
        self.assertEqual(respuesta_crear['Empresa']['correo'], correo)
        self.assertEqual(solicitud_crear.status_code, 201)

    def test_consulta_empresa(self):
        headers={
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.tokenfijo)
        }

        endpoint_empresa='/empresas'

        unico=str(uuid.uuid1())
        nombre_empresa="Nombre Empresa"+unico
        correo=nombre_empresa+'@correo.com'
        usuario=random.randint(10000, 100000000)
        nueva_empresa={
            "nombre":nombre_empresa,
            "tipo":"Comercio",
            "correo":correo,
            "celular":"3042384590",
            "contacto":"Lep Corp14",
            "pais":"Colombia",
            "ciudad":"Valledupar",
            "direccion":"Calle 7 # 11 - 10",
            "id_usuario":usuario,
            "is_active":True,
            "estado":"ACTIVO"
        }

        solicitud_crear=self.client.post(endpoint_empresa, 
                                                data=json.dumps(nueva_empresa), 
                                                headers=headers)
        respuesta_crear=json.loads(solicitud_crear.get_data())
        num_emp=respuesta_crear['Empresa']['id']

        endpoint_consulta_empresa='/empresa/'+str(num_emp)
        solicitud_consulta=self.client.get(endpoint_consulta_empresa)
        respuesta_consulta=json.loads(solicitud_consulta.get_data())
        self.assertEqual(respuesta_consulta['id'], num_emp)
        self.assertEqual(respuesta_consulta['id_usuario'], usuario)
        self.assertEqual(solicitud_consulta.status_code, 200)        

    def test_crea_proyecto(self):
        headers={
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.tokenfijo)
        }

        endpoint_empresa='/empresas'

        unico=str(uuid.uuid1())
        nombre_empresa="Nombre Empresa"+unico
        correo=nombre_empresa+'@correo.com'
        usuario=random.randint(10000, 100000000)
        nueva_empresa={
            "nombre":nombre_empresa,
            "tipo":"Comercio",
            "correo":correo,
            "celular":"3042384590",
            "contacto":"Lep Corp14",
            "pais":"Colombia",
            "ciudad":"Valledupar",
            "direccion":"Calle 7 # 11 - 10",
            "id_usuario":usuario,
            "is_active":True,
            "estado":"ACTIVO"
        }

        solicitud_crear=self.client.post(endpoint_empresa, 
                                                data=json.dumps(nueva_empresa), 
                                                headers=headers)
        respuesta_crear=json.loads(solicitud_crear.get_data())
        num_emp=respuesta_crear['Empresa']['id']

        nuevo_proyecto={
            "nombre":"Nombre Proyecto de Prueba",
            "descripcion":"Descripcion del Proyecto de Prueba"
        }

        endpoint_crea_proyecto='/empresas/'+str(num_emp)+'/proyectos'
        solicitud_crea_proyecto=self.client.post(endpoint_crea_proyecto,
                                                 data=json.dumps(nuevo_proyecto), 
                                                 headers=headers)
        respuesta_crea_proyecto=json.loads(solicitud_crea_proyecto.get_data())
        self.assertEqual(respuesta_crea_proyecto['Proyecto nuevo: ']['nombre'], "Nombre Proyecto de Prueba")
        self.assertEqual(respuesta_crea_proyecto['Proyecto nuevo: ']['id_emp'], num_emp)
        self.assertEqual(solicitud_crea_proyecto.status_code, 200)        

    def test_crea_perfiles(self):
        headers={
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.tokenfijo)
        }

        endpoint_empresa='/empresas'

        unico=str(uuid.uuid1())
        nombre_empresa="Nombre Empresa"+unico
        correo=nombre_empresa+'@correo.com'
        usuario=random.randint(10000, 100000000)
        nueva_empresa={
            "nombre":nombre_empresa,
            "tipo":"Comercio",
            "correo":correo,
            "celular":"3042384590",
            "contacto":"Lep Corp14",
            "pais":"Colombia",
            "ciudad":"Valledupar",
            "direccion":"Calle 7 # 11 - 10",
            "id_usuario":usuario,
            "is_active":True,
            "estado":"ACTIVO"
        }

        solicitud_crear=self.client.post(endpoint_empresa, 
                                                data=json.dumps(nueva_empresa), 
                                                headers=headers)
        respuesta_crear=json.loads(solicitud_crear.get_data())
        num_emp=respuesta_crear['Empresa']['id']

        nuevo_proyecto={
            "nombre":"Nombre Proyecto de Prueba",
            "descripcion":"Descripcion del Proyecto de Prueba"
        }

        endpoint_crea_proyecto='/empresas/'+str(num_emp)+'/proyectos'
        solicitud_crea_proyecto=self.client.post(endpoint_crea_proyecto,
                                                 data=json.dumps(nuevo_proyecto), 
                                                 headers=headers)
        respuesta_crea_proyecto=json.loads(solicitud_crea_proyecto.get_data())
        num_proy=respuesta_crea_proyecto['Proyecto nuevo: ']['id']

        endpoint_perfiles='/empresas/proyectos/'+str(num_proy)+'/perfiles'
        nuevo_perfil={
                "nombre":"Nombre Perfil de prueba",
                "lstHabils":[1,5,10]
        }
        solicitud_crear_perfil=self.client.post(endpoint_perfiles, 
                                                data=json.dumps(nuevo_perfil), 
                                                headers=headers)
        respuesta_crear_perfil=json.loads(solicitud_crear_perfil.get_data())

        self.assertEqual(respuesta_crear_perfil['Perfil nuevo: ']['id_proy'], num_proy)
        self.assertEqual(respuesta_crear_perfil['Perfil nuevo: ']['id_cand'], 0)
        self.assertEqual(solicitud_crear_perfil.status_code, 200)        