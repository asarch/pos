#!/usr/bin/python

#  TODO:
#
#    - 16/Mar/2014
#
#        Es necesario reorganizar la ventana principal para realizar las ventas.
#        Cuando un usuario se logge, lo primero que mostrara seran las ventas (compras)
#        ya realizadas por ese usuario.
# 

import gtk
import gtk.glade
import pygtk

from gtklogin import GtkLogin
from gtkmanagement import GtkManagement

from databases import marca
from databases import categoria
from databases import producto
from databases import inventario

import sys

class GtkWindow:
	def __init__(self, glade):
		# Configuracion de los widgets GTK+
		self.glade = glade
		self.window = glade.get_widget('window1')
		self.lista_productos = glade.get_widget('treeview7')
		self.carrito = glade.get_widget('treeview8')
		self.usuario = glade.get_widget('label45')
		self.fecha_compra = glade.get_widget('label46')
		self.hora_compra = glade.get_widget('label47')
		self.total = glade.get_widget('label49')
		self.agregar = glade.get_widget('button35')
		self.quitar = glade.get_widget('button36')
		self.aplicar = glade.get_widget('button37')
		self.toolbar = glade.get_widget('toolbar1')
		self.login = glade.get_widget('imagemenuitem6')
		self.logout = glade.get_widget('imagemenuitem7')

		# Lista de productos
		self.lista_productos_modelo = gtk.ListStore(str, str, str, str, str)
		self.lista_productos.set_model(self.lista_productos_modelo)
		self.lista_productos_renderer = gtk.CellRendererText()

		self.column_nombre = gtk.TreeViewColumn("Nombre", self.lista_productos_renderer, text = 0)
		self.column_marca = gtk.TreeViewColumn("Marca", self.lista_productos_renderer, text = 1)
		self.column_precio = gtk.TreeViewColumn("Precio unitario", self.lista_productos_renderer, text = 2)
		self.column_categoria = gtk.TreeViewColumn("Categoria", self.lista_productos_renderer, text = 3)
		self.column_cantidad = gtk.TreeViewColumn("Disponible", self.lista_productos_renderer, text = 4)

		self.lista_productos.append_column(self.column_nombre)
		self.lista_productos.append_column(self.column_marca)
		self.lista_productos.append_column(self.column_precio)
		self.lista_productos.append_column(self.column_categoria)
		self.lista_productos.append_column(self.column_cantidad)

		# Carrito
		self.carrito_modelo = gtk.ListStore(str, str, str)
		self.carrito.set_model(self.carrito_modelo)
		self.carrito_renderer = gtk.CellRendererText()

		self.column_item = gtk.TreeViewColumn("#", self.carrito_renderer, text = 0)
		self.column_producto = gtk.TreeViewColumn("Producto", self.carrito_renderer, text = 1)
		self.column_precio_unitario = gtk.TreeViewColumn("Precio unitario", self.carrito_renderer, text = 2)
		self.column_items = gtk.TreeViewColumn("Cantidad", self.carrito_renderer, text = 3)
		self.column_subtotal = gtk.TreeViewColumn("SubTotal", self.carrito_renderer, text = 4)

		self.carrito.append_column(self.column_item)
		self.carrito.append_column(self.column_producto)
		self.carrito.append_column(self.column_precio_unitario)
		self.carrito.append_column(self.column_items)
		self.carrito.append_column(self.column_subtotal)

		# Funciones de llamada de respuesta
		self.lista_productos.connect('cursor-changed', self.cambio_lista_productos)
		self.agregar.connect('clicked', self.agregar_producto)
		self.login.connect('activate', self.iniciar_sesion)
		self.logout.connect('activate', self.cerrar_sesion)

		# Configuraciones iniciales
		self.window.set_title('POS - Punto de Venta - 1.0')
		self.window.set_default_size(640, 480)
		self.actualizar_productos()

		# ToolBar
		self.icon_configurar = gtk.Image()
		self.icon_configurar.set_from_stock(gtk.STOCK_PREFERENCES, gtk.ICON_SIZE_SMALL_TOOLBAR)
		self.toolbar_configurar = self.toolbar.append_item(
			"Cofigurar",
			"Configurar aplicacion",
			"Private",
			self.icon_configurar,
			self.configuraciones
		)

		self.icon_salir = gtk.Image()
		self.icon_salir.set_from_stock(gtk.STOCK_QUIT, gtk.ICON_SIZE_SMALL_TOOLBAR)
		self.toolbar_salir = self.toolbar.append_item(
			"Salir",
			"Termina el programa",
			"Private",
			self.icon_salir,
			gtk.main_quit
		)

		self.toolbar.set_style(gtk.TOOLBAR_BOTH)

		#now = datetime.datetime.now()
		# Necesitamos el id de un usuario
		#self.venta_actual = venta(
		#		total = 0,
		#		fecha = "%d-%d-%d" % (now.day, now.month, now.year),
		#		time = "%d:%d:%d" % (now.hour, now.minute, now.second),
		#		usuario = usuario_id
		#		)

		# Usuario actual
		#self.usuario_id = -1
		#self.lista_productos.set_sensitive(False)
		#self.carrito.set_sensitive(False)
		#self.icon_configurar.set_sensitive(False)
		#self.agregar.set_sensitive(False)
		#self.quitar.set_sensitive(False)
		#self.aplicar.set_sensitive(False)

	def show(self):
		self.window.show_all()

	def actualizar_productos(self):
		self.lista_productos_modelo.clear()

		for entry in producto.select():
			hay_producto = inventario.select(inventario.q.id == entry.id).count()

			if hay_producto:
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

	def cambio_lista_productos(self, object):
		selection = object.get_selection()
		model, treeiter = selection.get_selected()

		if treeiter != None:
			self.producto_seleccionado = model[treeiter][0]

		#print >> sys.stderr, self.producto_seleccionado

	def agregar_producto(self, object):
		print "Hello, world!"

	def configuraciones(self, object):
		a = GtkManagement(self.glade)
		a.show()
		#print "Hello, world!"

	def iniciar_sesion(self, object):
		login = GtkLogin(self.glade)
		login.show()
		print "Ya llegamos aqui: ", login.get_usuario_id()

	def cerrar_sesion(self, object):
		print "Hello, world!"
