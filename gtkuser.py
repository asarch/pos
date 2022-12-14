#!/usr/bin/python

# dialog2 - Creacion de los usuarios

import gtk
import gtk.glade
import pygtk

from databases import rol
from databases import usuario

class GtkUser:
	def __init__(self, glade):
		# Objetos GTK+
		self.glade = glade
		self.window = glade.get_widget('dialog2')
		self.apodo = glade.get_widget('entry6')
		self.nombre = glade.get_widget('entry7')
		self.apellido_paterno = glade.get_widget('entry8')
		self.apellido_materno = glade.get_widget('entry9')
		self.password = glade.get_widget('entry10')
		self.lista_roles = glade.get_widget('combobox2')
		self.lista_usuarios = glade.get_widget('treeview1')
		self.nuevo = glade.get_widget('button6')
		self.guardar = glade.get_widget('button7')
		self.eliminar = glade.get_widget('button8')
		self.cerrar = glade.get_widget('button4')
		self.window.set_title('Administrar Usuarios')

		# Lista de usuarios
		self.lista_usuarios_modelo = gtk.ListStore(str, str, str, str, str)
		self.lista_usuarios.set_model(self.lista_usuarios_modelo)
		self.lista_usuarios_renderer = gtk.CellRendererText()

		self.column_apodo = gtk.TreeViewColumn("Apodo", self.lista_usuarios_renderer, text = 0)
		self.column_nombre = gtk.TreeViewColumn("Nombre", self.lista_usuarios_renderer, text = 1)
		self.column_apellido_paterno = gtk.TreeViewColumn("Apellido paterno", self.lista_usuarios_renderer, text = 2)
		self.column_apellido_materno = gtk.TreeViewColumn("Apellido materno", self.lista_usuarios_renderer, text = 3)
		self.column_rol = gtk.TreeViewColumn("Tipo de usuario", self.lista_usuarios_renderer, text = 4)

		self.lista_usuarios.append_column(self.column_apodo)
		self.lista_usuarios.append_column(self.column_nombre)
		self.lista_usuarios.append_column(self.column_apellido_paterno)
		self.lista_usuarios.append_column(self.column_apellido_materno)
		self.lista_usuarios.append_column(self.column_rol)

		# Lista de roles
		self.lista_roles_modelo = gtk.ListStore(str)
		self.lista_roles.set_model(self.lista_roles_modelo)
		self.lista_roles_renderer = gtk.CellRendererText()
		self.lista_roles.pack_start(self.lista_roles_renderer) 

		# Funciones de llamada de respuesta
		self.cerrar.connect('clicked', self.ocultar_ventana)
		self.guardar.connect('clicked', self.guardar_registro)
		self.eliminar.connect('clicked', self.eliminar_registro)
		self.lista_usuarios.connect('cursor-changed', self.cambio_lista)
		self.nuevo.connect('clicked', self.nuevo_registro)

		# Configuraciones iniciales
		for entry in rol.select():
			self.lista_roles_modelo.append([entry.nombre])

		self.lista_roles.set_active(0)
		self.actualizar_lista()
		self.eliminar.set_sensitive(False)

	def show(self):
		self.window.show_all()

	def cambio_texto(self, object):
		self.guardar.set_sensitive(self.nombre.get_text_length())

	def guardar_registro(self, object):
		rol_usuario = rol.select(rol.q.nombre == self.lista_roles.get_active_text())

		nuevo_usuario = usuario(
			apodo = self.apodo.get_text(),
			nombre = self.nombre.get_text(),
			apellido_paterno = self.apellido_paterno.get_text(),
			apellido_materno = self.apellido_materno.get_text(),
			rol = rol_usuario[0].id,
			password = self.password.get_text()
		)

		self.nuevo_registro()

	def actualizar_lista(self):
		self.lista_usuarios_modelo.clear()

		for entry in usuario.select():
			self.lista_usuarios_modelo.append([
				entry.apodo,
				entry.nombre,
				entry.apellido_paterno,
				entry.apellido_materno,
				entry.rol.nombre,
			])

	def cambio_lista(self, object):
		selection = object.get_selection()
		model, treeiter = selection.get_selected()

		if treeiter != None:
			self.usuario_seleccionado = model[treeiter][0]
			self.eliminar.set_sensitive(True)

	def eliminar_registro(self, object):
		eliminar_usuario = usuario.select(usuario.q.apodo == self.usuario_seleccionado)
		usuario.delete(eliminar_usuario[0].id)
		self.actualizar_lista()

	def nuevo_registro(self):
		self.apodo.set_text('')
		self.nombre.set_text('')
		self.apellido_paterno.set_text('')
		self.apellido_materno.set_text('')
		self.password.set_text('')
		self.lista_roles.set_active(0)
		self.actualizar_lista()

	def ocultar_ventana(self, object):
		self.window.hide()
