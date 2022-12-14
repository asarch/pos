#!/usr/bin/env python

import gtk
import gtk.glade
import pygtk

from gtkrol import GtkRol
from gtklogin import GtkLogin
from gtkcategory import GtkCategory
from gtkbrand import GtkBrand
from gtkmanagement import GtkManagement
from gtkuser import GtkUser
from gtkproduct import GtkProduct
from gtkinventory import GtkInventory
from gtkwindow import GtkWindow

# Objeto principal del esquema de Glade
glade = gtk.glade.XML('pos.glade')

login = GtkWindow(glade)
login.show()

gtk.main()

#from databases import marca
#print marca.select(marca.q.id == 2)[0]

#from databases import rol
#from databases import usuario

#jaime = usuario.select(usuario.q.apodo == 'jaime')
#print jaime
#for roles in jaime:
#	print roles.nombre
#glade = gtk.glade.XML('pos.glade')
#dialog = GtkWindow(glade)
#dialog.show()

# Cada ventana es responsable de una sola accion

#gtk.main()
