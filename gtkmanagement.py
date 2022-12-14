#!/usr/bin/python

import gtk
import gtk.glade
import pygtk

# dialog7 - Administracion del sistema

from gtkuser import GtkUser
from gtkrol import GtkRol
from gtkbrand import GtkBrand
from gtkcategory import GtkCategory
from gtkuser import GtkUser
from gtkinventory import GtkInventory
from gtkproduct import GtkProduct

from databases import *

class GtkManagement:
	def __init__(self, glade):
		self.glade = glade
		self.window = glade.get_widget('dialog7')
		self.usuarios = glade.get_widget('button22')
		self.productos = glade.get_widget('button23')
		self.categorias = glade.get_widget('button24')
		self.marcas = glade.get_widget('button25')
		self.roles = glade.get_widget('button26')
		self.inventario = glade.get_widget('button27')
		self.quit = glade.get_widget('button30')

		# Configuraciones iniciales
		self.window.set_title('Administrar Sistema')

		# Funciones de llamadas de respuesta
		self.usuarios.connect('clicked', self.configurar_usuario)
		self.categorias.connect('clicked', self.configurar_categoria)
		self.marcas.connect('clicked', self.configurar_marcas)
		self.roles.connect('clicked', self.configurar_roles)
		self.quit.connect('clicked', gtk.main_quit)
		self.inventario.connect('clicked', self.configurar_inventario)
		self.productos.connect('clicked', self.configurar_productos)

	def show(self):
		self.window.show_all()

	def configurar_categoria(self, object):
		dlg = GtkCategory(self.glade)
		dlg.show()

	def configurar_marcas(self, object):
		dlg = GtkBrand(self.glade)
		dlg.show()

	def configurar_roles(self, object):
		dlg = GtkRol(self.glade)
		dlg.show()

	def configurar_usuario(self, object):
		dlg = GtkUser(self.glade)
		dlg.show()

	def configurar_inventario(self, object):
		dlg = GtkInventory(self.glade)
		dlg.show()

	def configurar_productos(self, object):
		dlg = GtkProduct(self.glade)
		dlg.show()
		#dlg.destroy()
