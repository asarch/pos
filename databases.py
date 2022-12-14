#!/usr/bin/python

from sqlobject import *
from sqlobject.sqlite import builder

# Conexion principal con la base de datos de la aplicacion
conn = builder()('pos.db')

class rol(SQLObject):
	_connection = conn
	nombre = StringCol()
	usuarios = MultipleJoin('usuario')

class usuario(SQLObject):
	_connection = conn
	apodo = StringCol()
	nombre = StringCol()
	apellido_paterno = StringCol()
	apellido_materno = StringCol()
	rol = ForeignKey('rol')
	password = StringCol()

class marca(SQLObject):
	_connection = conn
	nombre = StringCol()
	productos = MultipleJoin('producto')

class categoria(SQLObject):
	_connection = conn
	nombre = StringCol()
	productos = MultipleJoin('producto')

class venta(SQLObject):
	_connection = conn
	total = CurrencyCol()
	fecha = DateCol()
	hora = TimeCol()
	usuario = ForeignKey('usuario')
	producto_venta = MultipleJoin('producto_venta')

class producto(SQLObject):
	_connection = conn
	nombre = StringCol()
	marca = ForeignKey('marca')
	precio = IntCol()
	descripcion = BLOBCol()
	categoria = ForeignKey('categoria')
	inventario = MultipleJoin('inventario')
	producto_venta = MultipleJoin('producto_venta')

class inventario(SQLObject):
	_connection = conn
	producto = ForeignKey('producto')
	cantidad = IntCol()
	
class producto_venta(SQLObject):
	_connection = conn
	producto = ForeignKey('producto')
	venta = ForeignKey('venta')
