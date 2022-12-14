#!/usr/bin/python

# dialog8 - Administracion de los roles

# Modulos de GTK+
import gtk
import gtk.glade
import pygtk

# Objeto relacionado al dialogo de configuracion
from databases import rol

class GtkRol:
	def __init__(self, glade):
		# Preparamos los widgets del dialogo
		self.glade = glade
		self.window = glade.get_widget('dialog8')
		self.nombre = glade.get_widget('entry17')
		self.roles = glade.get_widget('treeview5')

		self.guardar = glade.get_widget('button10')
		self.nuevo = glade.get_widget('button32')
		self.eliminar = glade.get_widget('button33')
		self.close = glade.get_widget('button34')

		# Conectamos las funciones de llamada de respuesta
		self.close.connect('clicked', self.cerrar_ventana)
		self.nombre.connect('changed', self.cuadro_texto)
		self.nuevo.connect('clicked', self.boton_nuevo)
		self.guardar.connect('clicked', self.boton_guardar)
		self.roles.connect('cursor-changed', self.cambio_lista_roles)
		self.eliminar.connect('clicked', self.eliminar_registro)

		# Preparamos la lista de los roles de la base de datos
		self.model = gtk.ListStore(str)
		self.roles.set_model(self.model)
		self.renderer = gtk.CellRendererText()
		self.column = gtk.TreeViewColumn("Roles", self.renderer, text=0)
		self.roles.append_column(self.column)

		# Otras configuraciones iniciales
		self.rol_seleccionado = ''
		self.window.set_title('Administrar Roles')
		self.guardar.set_sensitive(False)
		self.nuevo.set_sensitive(False)
		self.eliminar.set_sensitive(False)
		self.update_list()

	def update_list(self):
		self.model.clear()

		for entry in rol.select():
			self.model.append([entry.nombre])

	def show(self):
		self.window.show_all()

	def cuadro_texto(self, object):
		self.guardar.set_sensitive(self.nombre.get_text_length())
		self.nuevo.set_sensitive(self.nombre.get_text_length())

	def boton_nuevo(self, object):
		self.nombre.set_text('')

	def boton_guardar(self, selection):
		nuevo_rol = rol(nombre = self.nombre.get_text())

		self.nombre.set_text('')
		self.guardar.set_sensitive(False)
		self.nuevo.set_sensitive(False)
		self.update_list()

	def cambio_lista_roles(self, object):
		selection = object.get_selection()
		model, treeiter = selection.get_selected()

		if treeiter != None:
			self.rol_seleccionado = model[treeiter][0]
			self.eliminar.set_sensitive(True)

	def eliminar_registro(self, object):
		eliminar_rol = rol.select(rol.q.nombre == self.rol_seleccionado)
		rol.delete(eliminar_rol[0].id)
		self.update_list()

	def cerrar_ventana(self, object):
		self.window.hide()
