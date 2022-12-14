#!/usr/bin/python

# dialog5 - Administracion de las marcas

# Modulos de GTK+
import gtk
import gtk.glade
import pygtk

from databases import marca

class GtkBrand:
	def __init__(self, glade):
		# Widgets de GTK+
		self.glade = glade
		self.window = glade.get_widget('dialog5')
		self.nombre = glade.get_widget('entry14')
		self.nuevo = glade.get_widget('button17')
		self.guardar = glade.get_widget('button16')
		self.eliminar = glade.get_widget('button18')
		self.lista_marcas = glade.get_widget('treeview4')
		self.cerrar = glade.get_widget('button19')
		self.window.set_title('Administrar Marcas')

		# Lista de marcas
		self.model = gtk.ListStore(str)
		self.lista_marcas.set_model(self.model)
		self.renderer = gtk.CellRendererText()
		self.column = gtk.TreeViewColumn("Nombre", self.renderer, text = 0)
		self.lista_marcas.append_column(self.column)

		# Configuraciones iniciales
		self.actualizar_lista()
		self.guardar.set_sensitive(False)
		self.nuevo.set_sensitive(False)
		self.eliminar.set_sensitive(False)

		# Funciones de llamada de respuesta
		self.nombre.connect('changed', self.cambio_texto)
		self.lista_marcas.connect('cursor-changed', self.cambio_lista)
		self.guardar.connect('clicked', self.guardar_registro)
		self.eliminar.connect('clicked', self.eliminar_registro)
		self.nuevo.connect('clicked', self.nuevo_registro)
		self.cerrar.connect('clicked', self.cerrar_ventana)

	def show(self):
		self.window.show_all()

	def actualizar_lista(self):
		self.model.clear()

		for entry in marca.select():
			self.model.append([entry.nombre])

	def cambio_texto(self, object):
		self.nuevo.set_sensitive(self.nombre.get_text_length())
		self.guardar.set_sensitive(self.nombre.get_text_length())

	def cambio_lista(self, object):
		selection = object.get_selection()
		model, treeiter = selection.get_selected()

		if treeiter != None:
			self.marca_seleccionada = model[treeiter][0]
			self.eliminar.set_sensitive(True)

	def guardar_registro(self, object):
		nueva_marca = marca(nombre = self.nombre.get_text())
		self.actualizar_lista()
		self.nombre.set_text('')

	def eliminar_registro(self, object):
		eliminar_marca = marca.select(marca.q.nombre == self.marca_seleccionada)
		marca.delete(eliminar_marca[0].id)
		self.actualizar_lista()

	def nuevo_registro(self, object):
		self.nombre.set_text('')

	def cerrar_ventana(self, object):
		self.window.hide()
