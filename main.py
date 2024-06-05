from fastapi import FastAPI, HTTPException, status
from typing import Union, List
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

class Contenido(BaseModel): 
    id : str
    nombre : str
    descripcion : str

class Materia(BaseModel): 
    id : str
    nombre : str
    nivel : str
    unidad_credito : float
    precio : float
    descripcion : str
    contenidos : List[Contenido]

class Estudiante(BaseModel): 
    cedula : str
    nombres : str
    apellidos : str
    nacimiento : datetime
    telefono : str
    direccion : str
    color_favorito : Union[str, None] = None
    record_academico : List[Materia]

estudiantes : List[Estudiante] = []
contenidos : List[Contenido] = []
materias : List[Materia] = []

@app.get('/contenidos')
async def listar_contenidos(): 
    return contenidos

@app.post('/contenido')
async def crear_contenido(contenido : Contenido): 
    for esto in contenidos: 
        if esto.id == contenido.id: 
            return HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="La id no se puede repetir"
            )
    contenidos.append(contenido)
    return contenido

@app.get('/materias')
async def listar_materias(): 
    return materias

@app.post('/materia')
async def crear_materia(materia : Materia): 
    for esto in materias: 
        if esto.id == materia.id: 
            return HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="La id no se puede repetir"
            )
    materias.append(materia)
    return materia

@app.post('/estudiante')
async def crear(estudiante : Estudiante): 
    for esto in estudiantes: 
        if esto.cedula == estudiante.cedula: 
            return HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="La cédula no se puede repetir"
            )
    estudiantes.append(estudiante)
    return estudiante

@app.get('/estudiantes')
async def listar(): 
    return estudiantes

@app.get('/estudiante/{cedula}')
async def buscar(cedula : str): 
    for esto in estudiantes: 
        if esto.cedula == cedula: 
            return esto
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, 
        detail="No se pudo encontrar un estudiante con tal cédula"
    )

@app.get('/estudiante_record_academico/{cedula}')
async def mostrar_record_academico(cedula : str): 
    for esto in estudiantes: 
        if esto.cedula == cedula: 
            return esto.record_academico
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, 
        detail="No se pudo encontrar un estudiante con tal cédula"
    )

@app.put('/estudiante/{cedula}')
async def modificar(cedula : str, estudiante : Estudiante): 
    if cedula != estudiante.cedula: 
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="La cédula del parámetro es diferente a la cédula del estudiante"
        )
    for i in range(len(estudiantes)): 
        if estudiantes[i].cedula == estudiante.cedula: 
            estudiantes[i] = estudiante
            return estudiantes[i]
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, 
        detail="No se pudo encontrar un estudiante con tal cédula"
    )

@app.delete('/estudiante/{cedula}')
async def eliminar(cedula : str): 
    for i in range(len(estudiantes)): 
        if estudiantes[i].cedula == cedula: 
            estudiante = estudiantes[i]
            estudiantes.remove(estudiante)
            return estudiante
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, 
        detail="No se pudo encontrar un estudiante con tal cédula"
    )