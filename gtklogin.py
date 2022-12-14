#!/usr/bin/python

# dialog6 - Dialogo de acceso

# GTK+
import gtk
import gtk.glade
import pygtk

from databases import usuario

import sys

class GtkLogin:
	def __init__(self, glade):
		# Inicializacion de las variables miembro
		self.glade = glade
		self.window = self.glade.get_widget('dialog6')
		self.nickname = self.glade.get_widget('entry15')
		self.password = self.glade.get_widget('entry16')
		self.clear = self.glade.get_widget('button20')
		self.ok = self.glade.get_widget('button21')
		self.usuario_id = -1

		# Llamadas de respuesta
		self.clear.connect('clicked', self.borrar_texto)
		self.nickname.connect('changed', self.cambio_texto)
		self.password.connect('changed', self.cambio_texto)
		self.ok.connect('clicked', self.cerrar_dialogo)

		# Otras inicializaciones
		self.clear.set_sensitive(False)
		self.ok.set_sensitive(False)
		self.window.set_title("Iniciar Sesion")

	def borrar_texto(self, object):
		self.nickname.set_text('')
		self.password.set_text('')

	def show(self):
		self.window.show_all()
		return self.usuario_id

	def hide(self, object):
		self.window.hide()

	def check_user(self):
		print "Checando"

	def cambio_texto(self, object):
		self.clear.set_sensitive(self.nickname.get_text_length() or self.password.get_text_length())
		self.ok.set_sensitive(self.nickname.get_text_length() or self.password.get_text_length())
	
	def cerrar_dialogo(self, object):
		# Buscamos al usuario por el apodo
		apodo = usuario.select(usuario.q.apodo == self.nickname.get_text()).count()

		# Si no lo encontramos
		if not apodo:
			msg = gtk.MessageDialog(
				None,
				gtk.DIALOG_DESTROY_WITH_PARENT,
				gtk.MESSAGE_ERROR,
				gtk.BUTTONS_OK,
				"No existe el usuario '%s'" % self.nickname.get_text()
			)
			msg.run()
			msg.destroy()
			return

		# Ahora obtenemos el password del usuario
		pwd = usuario.select(usuario.q.apodo == self.nickname.get_text())

		# Si no son iguales
		if pwd[0].password != self.password.get_text():
			msg = gtk.MessageDialog(
				None,
				gtk.DIALOG_DESTROY_WITH_PARENT,
				gtk.MESSAGE_ERROR,
				gtk.BUTTONS_OK,
				"Password incorrecto"
			)
			msg.run()
			msg.destroy()
			return

		self.usuario_id = pwd[0].id
		self.nickname.set_text('')
		self.password.set_text('')
		self.window.hide()

	def get_usuario_id(self):
		return self.usuario_id
