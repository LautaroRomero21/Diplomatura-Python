"""
Desde aqui se debe ejecutar el codigo del trabajo

:Importaciones:
- :`vista`: Contiene la interfaz grafica de la app.
- :`modulo`: Encapsula la logica de la base de datos y operaciones relacionadas con las ventas.
- :`Tk`: Crea de la ventana principal de la app.

El controlador crea una instancia de la app, inicializa la base de datos y crea la ventana principal utilizando la interfaz grafica y la base de datos.
"""

import vista
import modulo
from tkinter import Tk

if __name__ == "__main__":
    app = Tk()
    base = modulo.Base()
    aplicacion = vista.Ventana(app, base)
    app.mainloop()
