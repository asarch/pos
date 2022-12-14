#!/usr/bin/python

# dialog3 - Creacion de las categorias

# GTK+
import gtk
import gtk.glade
import pygtk

# Base de dato del dialogo
from databases import categoria

class GtkCategory:
	def __init__(self, glade):
		# Objetos GTK+
		self.glade = glade
		self.window = glade.get_widget('dialog3')
		self.nombre = glade.get_widget('entry11')
		self.lista_categorias = glade.get_widget('treeview2')
		self.guardar = glade.get_widget('button9')
		self.nuevo = glade.get_widget('button5')
		self.eliminar = glade.get_widget('button31')
		self.cerrar = glade.get_widget('button11')
		self.window.set_title('Categorias')

		# Lista de categorias
		self.model = gtk.ListStore(str)
		self.lista_categorias.set_model(self.model)
		self.renderer = gtk.CellRendererText()
		self.column = gtk.TreeViewColumn("Nombre", self.renderer, text = 0)
		self.lista_categorias.append_column(self.column)

		# Configuraciones iniciales
		self.registro = ''
		self.guardar.set_sensitive(False)
		self.nuevo.set_sensitive(False)
		self.eliminar.set_sensitive(False)
		self.actualizar_lista()

		# Las funciones de llamada de respuesta
		self.nombre.connect('changed', self.cambio_texto)
		self.lista_categorias.connect('cursor-changed', self.cambio_lista)
		self.eliminar.connect('clicked', self.eliminar_registro)
		self.guardar.connect('clicked', self.guardar_registro)
		self.cerrar.connect('clicked', self.cerrar_ventana)

	def show(self):
		self.window.show_all()

	def actualizar_lista(self):
		self.model.clear()

		for entry in categoria.select():
			self.model.append([entry.nombre])

	def cambio_texto(self, object):
		self.guardar.set_sensitive(self.nombre.get_text_length())
		self.nuevo.set_sensitive(self.nombre.get_text_length())

	def cambio_lista(self, object):
		selection = object.get_selection()
		model, treeiter = selection.get_selected()

		if treeiter != None:
			self.registro_seleccionado = model[treeiter][0]
			self.eliminar.set_sensitive(True)

	def eliminar_registro(self, object):
		eliminar_categoria = categoria.select(categoria.q.nombre == self.registro_seleccionado)
		categoria.delete(eliminar_categoria[0].id)
		self.actualizar_lista()

	def guardar_registro(self, object):
		nueva_categoria = categoria(nombre = self.nombre.get_text())
		self.nombre.set_text('')
		self.actualizar_lista()

	def cerrar_ventana(self, object):
		self.window.hide()
