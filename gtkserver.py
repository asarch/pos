#!/usr/bin/python

# dialog1 - Configuracion del servidor

class Server:
	def __init__(self, glade):
		self.glade = glade
		self.window = glade.get_widget('dialog1')
		self.tipo_servidor = glade.get_widget('combobox1')
		self.archivo_sqlite3 = glade.get_widget('filechooserbutton1')
		self.servidor = glade.get_widget('entry1')
		self.puerto = glade.get_widget('entry2')
		self.database = glade.get_widget('entry3')
		self.usuario = glade.get_widget('entry4')
		self.password = glade.get_widget('entry5')
		self.mostrar_password = glade.get_widget('checkbutton1')
		self.limpiar = glade.get_widget('button3')
		self.ok = glade.get_widget('button2')
		self.cancelar = glade.get_widget('button1')
		self.window.set_title('Configuracion del Servidor')

	def show(self):
		self.window.show_all()
