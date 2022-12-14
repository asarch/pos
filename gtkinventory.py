#!/usr/bin/python

import gtk
import gtk.glade
import pygtk

from databases import marca
from databases import categoria
from databases import producto
from databases import inventario

import sys

class GtkInventory:
	def __init__(self, glade):
		self.glade = glade
		self.window = glade.get_widget('dialog9')
		self.cantidad = glade.get_widget('entry18')
		self.lista_productos = glade.get_widget('treeview6')
		self.guardar = glade.get_widget('button29')
		self.ok = glade.get_widget('button28')
		self.window.set_title("Inventario")

		# Lista productos
		self.lista_productos_modelo = gtk.ListStore(str, str, str, str, str)
		self.lista_productos.set_model(self.lista_productos_modelo)
		self.lista_productos_renderer = gtk.CellRendererText()

		self.column_nombre = gtk.TreeViewColumn("Nombre", self.lista_productos_renderer, text = 0)
		self.column_marca = gtk.TreeViewColumn("Marca", self.lista_productos_renderer, text = 1)
		self.column_precio = gtk.TreeViewColumn("Precio", self.lista_productos_renderer, text = 2)
		self.column_categoria = gtk.TreeViewColumn("Categoria", self.lista_productos_renderer, text = 3)
		self.column_cantidad = gtk.TreeViewColumn("Disponible", self.lista_productos_renderer, text = 4)

		self.lista_productos.append_column(self.column_nombre)
		self.lista_productos.append_column(self.column_marca)
		self.lista_productos.append_column(self.column_precio)
		self.lista_productos.append_column(self.column_categoria)
		self.lista_productos.append_column(self.column_cantidad)

		self.actualizar_lista()

		# Funciones de llamada de respuesta
		self.lista_productos.connect('cursor-changed', self.cambio_lista)
		self.cantidad.connect('changed', self.cambio_cantidad)
		self.guardar.connect('clicked', self.guardar_registro)
		self.ok.connect('clicked', self.ocultar_ventana)

	def show(self):
		self.window.show_all()

	def actualizar_lista(self):
		self.lista_productos_modelo.clear()
		
		# Recorremos la tabla de los productos
		for entry in producto.select():
			# Buscamos el id del producto en la tabla de inventario
			hay_producto = inventario.select(inventario.q.id == entry.id).count()
			
			# Si encontramos alguno
			if hay_producto:
				# Obtenemos cuantos hay
				disponible = inventario.select(inventario.q.id == entry.id)[0].cantidad
			else:
				disponible = 0

			self.lista_productos_modelo.append([
				entry.nombre,
				entry.marca.nombre,
				entry.precio,
				entry.categoria.nombre,
				disponible
			])

	def cambio_lista(self, object):
		selection = object.get_selection()
		model, treeiter = selection.get_selected()

		if treeiter != None:
			# Obtenemos el nombre del producto seleccionado
			self.producto_seleccionado = model[treeiter][0]

			# Buscamos su id en la tabla de productos
			producto_id = producto.select(producto.q.nombre == self.producto_seleccionado)

			# Vemos si ese producto tiene existencia
			hay_producto = inventario.select(inventario.q.id == producto_id[0].id).count()

			# Si tiene, cuantos hay
			if hay_producto:
				disponible = inventario.select(inventario.q.id == producto_id[0].id)[0].cantidad
			else:
				disponible = 0

			self.cantidad.set_text('%d' % disponible)

	def cambio_cantidad(self, object):
		self.guardar.set_sensitive(self.cantidad.get_text_length())

	def guardar_registro(self, object):
		# Obtenemos el id del producto seleccionado
		prod_id = producto.select(producto.q.nombre == self.producto_seleccionado)

		# Obtenemos su cantidad en la tabla de inventarios
		hay_producto = inventario.select(inventario.q.id == prod_id[0].id).count()

		# Si se encuentra
		if hay_producto:
			disponible = inventario.select(inventario.q.id == prod_id[0].id)

			# Actualizamos la cantidad disponible
			disponible[0].cantidad = int(self.cantidad.get_text())
		else:
			nueva_cantidad = inventario(producto = prod_id[0].id, cantidad = int(self.cantidad.get_text()))

		self.actualizar_lista()

	def ocultar_ventana(self, object):
		self.window.hide()
