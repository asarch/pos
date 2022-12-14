#!/usr/bin/python

# dialog4 - Alta de los productos

import gtk
import gtk.glade
import pygtk

from databases import marca
from databases import categoria
from databases import producto

class GtkProduct:
	def __init__(self, glade):
		self.glade = glade
		self.window = glade.get_widget('dialog4')
		self.nombre = glade.get_widget('entry12')
		self.precio = glade.get_widget('entry13')
		self.lista_marcas = glade.get_widget('combobox3')
		self.lista_categorias = glade.get_widget('combobox4')
		self.imagen = glade.get_widget('filechooserbutton2')
		self.nuevo = glade.get_widget('button13')
		self.guardar = glade.get_widget('button12')
		self.eliminar = glade.get_widget('button14')
		self.ok = glade.get_widget('button15')
		self.lista_productos = glade.get_widget('treeview3')
		self.window.set_title('Productos')

		# Marcas disponibles
		self.lista_marcas_modelo = gtk.ListStore(str)
		self.lista_marcas.set_model(self.lista_marcas_modelo)
		self.lista_marcas_renderer = gtk.CellRendererText()
		self.lista_marcas.pack_start(self.lista_marcas_renderer)

		for entry in marca.select():
			self.lista_marcas_modelo.append([entry.nombre])

		self.lista_marcas.set_active(0)

		# Categorias disponibles
		self.lista_categorias_modelo = gtk.ListStore(str)
		self.lista_categorias.set_model(self.lista_categorias_modelo)
		self.lista_categorias_renderer = gtk.CellRendererText()
		self.lista_categorias.pack_start(self.lista_categorias_renderer)

		for entry in categoria.select():
			self.lista_categorias_modelo.append([entry.nombre])

		self.lista_categorias.set_active(0)

		# Lista de productos
		self.lista_productos_modelo = gtk.ListStore(str, str, str, str)
		self.lista_productos.set_model(self.lista_productos_modelo)
		self.lista_productos_renderer = gtk.CellRendererText()

		self.column_nombre = gtk.TreeViewColumn("Nombre", self.lista_productos_renderer, text = 0)
		self.column_marca = gtk.TreeViewColumn("Marca", self.lista_productos_renderer, text = 1)
		self.column_precio = gtk.TreeViewColumn("Precio", self.lista_productos_renderer, text = 2)
		self.column_categoria = gtk.TreeViewColumn("Categoria", self.lista_productos_renderer, text = 3)

		self.lista_productos.append_column(self.column_nombre)
		self.lista_productos.append_column(self.column_marca)
		self.lista_productos.append_column(self.column_precio)
		self.lista_productos.append_column(self.column_categoria)

		# Configuraciones iniciales
		self.imagen.set_sensitive(False)
		self.actualizar_lista()

		# Funciones de llamada de respuesta
		self.guardar.connect('clicked', self.guardar_registro)
		self.nuevo.connect('clicked', self.nuevo_registro)
		self.lista_productos.connect('cursor-changed', self.cambio_lista)
		self.eliminar.connect('clicked', self.eliminar_registro)
		self.ok.connect('clicked', self.ocultar_ventana)

	def show(self):
		self.window.show_all()
	
	def guardar_registro(self, object):
		marca_producto = marca.select(marca.q.nombre == self.lista_marcas.get_active_text())
		categoria_producto = categoria.select(categoria.q.nombre == self.lista_categorias.get_active_text())

		print int(self.precio.get_text())

		nuevo_producto = producto(
			nombre = self.nombre.get_text(),
			marca = marca_producto[0].id,
			precio = int(self.precio.get_text()),
			descripcion = "PYTHON",
			categoria = categoria_producto[0].id
		)

		self.actualizar_lista()
		self.nombre.set_text('')
		self.lista_marcas.set_active(0)
		self.precio.set_text('')
		self.lista_categorias.set_active(0)

	def actualizar_lista(self):
		self.lista_productos_modelo.clear()

		for entry in producto.select():
			self.lista_productos_modelo.append([
				entry.nombre,
				entry.marca.nombre,
				entry.precio,
				entry.categoria.nombre
			])

	def nuevo_registro(self, object):
		self.nombre.set_text('')
		self.precio.set_text('')
		self.lista_marcas.set_active(0)
		self.lista_categorias.set_active(0)

	def cambio_lista(self, object):
		selection = object.get_selection()
		model, treeiter = selection.get_selected()

		if treeiter != None:
			self.registro_seleccionado = model[treeiter][0]

	def eliminar_registro(self, object):
		eliminar_registro = producto.select(producto.q.nombre == self.registro_seleccionado)
		producto.delete(eliminar_registro[0].id)
		self.actualizar_lista()
		print >> sys.stderr, self.registro_seleccionado

	def ocultar_ventana(self, object):
		self.window.hide()
