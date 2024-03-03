"""
:Importaciones:
- `validador_campos(ValidadorVenta)`: Se instancia para validar los campos de una venta.
- `Tkinter`: Realiza el trabajo para la interfaz gráfica.
- `Venta(modulo)`: Se utiliza para actualizar el treeview con la base de datos.
- `datetme`: Trabaja con el formato de fecha.

Se realizaron distintas clases hijas de algunas de tkinter para acortar codigo y pasar directamente la posicion del objeto al instanciarlo, sin necesidad de escribir 2 lineas de codigo.
"""

from validador_campos import ValidadorVenta
from tkinter import (
    Frame,
    Label,
    Button,
    Entry,
    ttk,
    X,
    messagebox,
    IntVar,
    DoubleVar,
    StringVar,
    _tkinter,
)
from modulo import Venta
from datetime import date


class Marco(Frame):
    """
    :Descripcion: Crea un marco dentro de la aplicacion.
    """

    def __init__(self, ventana, color_fondo=None, place_info=None):
        super().__init__(ventana, bg=color_fondo)
        self.place(**place_info)


class Etiqueta(Label):
    """
    :Descripcion: Crea una etiqueta dentro de la aplicacion.
    """

    def __init__(
        self,
        ventana,
        texto,
        fuente,
        color_fondo,
        color_letra=None,
        place_info=None,
        pack_info=None,
    ):
        super().__init__(
            ventana, text=texto, font=fuente, bg=color_fondo, fg=color_letra
        )
        if place_info:
            self.place(**place_info)
        elif pack_info:
            self.pack(**pack_info)


class Boton(Button):
    """
    :Descripcion: Crea un boton junto con su funcion dentro de la aplicacion.
    """

    def __init__(
        self,
        ventana,
        texto,
        color_fondo,
        fuente,
        color_letra=None,
        place_info=None,
        funcion_info=None,
    ):
        super().__init__(
            ventana,
            text=texto,
            bg=color_fondo,
            font=fuente,
            fg=color_letra,
            command=funcion_info,
        )
        self.place(**place_info)


class Entrada(Entry):
    """
    :Descripcion: Crea una entrada de texto dentro de la aplicacion.
    """

    def __init__(self, ventana, variable, ancho, place_info):
        super().__init__(ventana, textvariable=variable, width=ancho)
        self.place(**place_info)


class Ventana:
    """
    :Descripcion: Clase que define la ventana principal de la aplicacion y modifica su vista segun lo requerido.

    :__init__: Se realiza la colocacion de cada parte visual dentro de la aplicacion junto con sus funciones.
    """

    #################################################################################
    ############################### PARTE VISUAL ####################################
    #################################################################################

    def __init__(self, app, base_conectada) -> None:
        self.ventana = app
        self.base = base_conectada
        self.ventana.geometry("760x540")
        self.ventana.title("TRABAJO FINAL")
        self.ventana.configure(bg="#8B8B8B")
        self.var_fecha_dia = IntVar()
        self.var_fecha_mes = IntVar()
        self.var_fecha_anio = IntVar()
        self.var_producto = StringVar()
        self.var_cantidad = IntVar()
        self.var_precio = DoubleVar()
        self.var_dia_inicial = IntVar()
        self.var_mes_inicial = IntVar()
        self.var_anio_inicial = IntVar()
        self.var_dia_final = IntVar()
        self.var_mes_final = IntVar()
        self.var_anio_final = IntVar()

        self.marco1 = Marco(
            self.ventana,
            color_fondo="#F9E192",
            place_info={"x": 10, "y": 50, "relwidth": 0.42, "relheight": 0.52},
        )
        self.marco2 = Marco(
            self.ventana,
            color_fondo="#F9E192",
            place_info={"x": 430, "y": 50, "relwidth": 0.42, "relheight": 0.52},
        )

        self.etiqueta_ventas = Etiqueta(
            self.ventana,
            texto="VENTAS FERRETERIA",
            fuente="Helvetica 15 bold",
            color_fondo="#F9E192",
            pack_info={"fill": X},
        )
        self.etiqueta_fecha = Etiqueta(
            self.ventana,
            texto="Fecha",
            fuente="Helvetica 10 bold",
            color_fondo="#F9E192",
            color_letra="black",
            place_info={"x": 43, "y": 110},
        )
        self.etiqueta_producto = Etiqueta(
            self.ventana,
            texto="Producto",
            fuente="Helvetica 10 bold",
            color_fondo="#F9E192",
            color_letra="black",
            place_info={"x": 36, "y": 160},
        )
        self.etiqueta_cantidad = Etiqueta(
            self.ventana,
            texto="Cantidad",
            fuente="Helvetica 10 bold",
            color_fondo="#F9E192",
            color_letra="black",
            place_info={"x": 37, "y": 210},
        )
        self.etiqueta_precio = Etiqueta(
            self.ventana,
            texto="Precio c/u",
            fuente="Helvetica 10 bold",
            color_fondo="#F9E192",
            color_letra="black",
            place_info={"x": 34, "y": 260},
        )
        self.etiqueta_consultar = Etiqueta(
            self.ventana,
            texto="Consulta",
            fuente="Helvetica 15 bold",
            color_fondo="#F9E192",
            place_info={"x": 536, "y": 60, "relwidth": 0.15, "relheight": 0.07},
        )
        self.etiqueta_carga = Etiqueta(
            self.ventana,
            texto="Carga de Ventas",
            fuente="Helvetica 15 bold",
            color_fondo="#F9E192",
            place_info={"x": 75, "y": 60, "relwidth": 0.25, "relheight": 0.07},
        )
        self.etiqueta_fecha_inicial = Etiqueta(
            self.ventana,
            texto="Fecha Inicial",
            fuente="Helvetica 10 bold",
            color_fondo="#F9E192",
            place_info={"x": 435, "y": 100, "relwidth": 0.15, "relheight": 0.07},
        )
        self.etiqueta_fecha_final = Etiqueta(
            self.ventana,
            texto="Fecha Final",
            fuente="Helvetica 10 bold",
            color_fondo="#F9E192",
            place_info={"x": 435, "y": 160, "relwidth": 0.15, "relheight": 0.07},
        )
        self.etiqueta_resultado_consulta = Etiqueta(
            self.ventana,
            texto="Facturacion total:",
            fuente="Helvetica 12 bold",
            color_fondo="#F9E192",
            place_info={"x": 480, "y": 215, "relwidth": 0.3, "relheight": 0.07},
        )

        self.boton_registrar = Boton(
            self.ventana,
            texto="Registrar",
            color_fondo="#2EFF19",
            fuente="Helvetica 8 bold",
            funcion_info=self.registrar_venta,
            place_info={"x": 340, "y": 50, "relwidth": 0.1, "relheight": 0.07},
        )
        self.boton_modificar = Boton(
            self.ventana,
            texto="Modificar",
            color_fondo="#7EFF71",
            fuente="Helvetica 8 bold",
            funcion_info=self.iniciar_modificacion,
            place_info={"x": 340, "y": 90, "relwidth": 0.1, "relheight": 0.07},
        )
        self.boton_eliminar = Boton(
            self.ventana,
            texto="Eliminar",
            color_fondo="#FF4343",
            fuente="Helvetica 8 bold",
            funcion_info=self.eliminar_venta,
            place_info={"x": 340, "y": 170, "relwidth": 0.1, "relheight": 0.07},
        )
        self.boton_consultar = Boton(
            self.ventana,
            texto="Consultar",
            color_fondo="#4691FF",
            fuente="Helvetica 8 bold",
            funcion_info=self.mostrar_consulta,
            place_info={"x": 340, "y": 130, "relwidth": 0.1, "relheight": 0.07},
        )
        self.boton_salir = Boton(
            self.ventana,
            texto="Salir",
            color_fondo="#FD8F79",
            fuente="Helvetica 8 bold",
            funcion_info=self.salir,
            place_info={"x": 340, "y": 210, "relwidth": 0.1, "relheight": 0.07},
        )

        self.entry_fecha_dia = Entrada(
            self.ventana,
            variable=self.var_fecha_dia,
            ancho=8,
            place_info={"x": 120, "y": 112},
        )
        self.entry_fecha_mes = Entrada(
            self.ventana,
            variable=self.var_fecha_mes,
            ancho=8,
            place_info={"x": 180, "y": 112},
        )
        self.entry_fecha_anio = Entrada(
            self.ventana,
            variable=self.var_fecha_anio,
            ancho=8,
            place_info={"x": 240, "y": 112},
        )
        self.entry_producto = Entrada(
            self.ventana,
            variable=self.var_producto,
            ancho=28,
            place_info={"x": 120, "y": 162},
        )
        self.entry_cantidad = Entrada(
            self.ventana,
            variable=self.var_cantidad,
            ancho=28,
            place_info={"x": 120, "y": 212},
        )
        self.entry_precio = Entrada(
            self.ventana,
            variable=self.var_precio,
            ancho=28,
            place_info={"x": 120, "y": 262},
        )
        self.entry_dia_inicial = Entrada(
            self.ventana,
            variable=self.var_dia_inicial,
            ancho=8,
            place_info={"x": 550, "y": 110},
        )
        self.entry_mes_inicial = Entrada(
            self.ventana,
            variable=self.var_mes_inicial,
            ancho=8,
            place_info={"x": 610, "y": 110},
        )
        self.entry_anio_inicial = Entrada(
            self.ventana,
            variable=self.var_anio_inicial,
            ancho=8,
            place_info={"x": 670, "y": 110},
        )
        self.entry_dia_final = Entrada(
            self.ventana,
            variable=self.var_dia_final,
            ancho=8,
            place_info={"x": 550, "y": 170},
        )
        self.entry_mes_final = Entrada(
            self.ventana,
            variable=self.var_mes_final,
            ancho=8,
            place_info={"x": 610, "y": 170},
        )
        self.entry_anio_final = Entrada(
            self.ventana,
            variable=self.var_anio_final,
            ancho=8,
            place_info={"x": 670, "y": 170},
        )

        self.tree = ttk.Treeview(self.ventana)
        self.tree["columns"] = (
            "col1",
            "col2",
            "col3",
            "col4",
            "col5",
        )
        self.tree.column("#0", width=5, minwidth=25, anchor="w")
        self.tree.column("col1", width=5, minwidth=50, anchor="e")
        self.tree.column("col2", width=120, minwidth=80, anchor="w")
        self.tree.column("col3", width=5, minwidth=80, anchor="e")
        self.tree.column("col4", width=5, minwidth=80, anchor="e")
        self.tree.column("col5", width=5, minwidth=80, anchor="e")

        self.tree.heading("#0", text="ID")
        self.tree.heading("col1", text="Fecha")
        self.tree.heading("col2", text="Producto")
        self.tree.heading("col3", text="Cantidad")
        self.tree.heading("col4", text="Precio c/u")
        self.tree.heading("col5", text="Precio Total")

        self.tree.place(x=0, y=350, relwidth=1, relheight=1)

        self.actualizar_tree()

    #################################################################################
    ############################### METODOS DEL VIEW ################################
    #################################################################################

    def actualizar_tree(self):
        """
        :Metodo: Actualiza la vista del treeview con los datos de la base relacionada.
        """
        ventas = self.tree.get_children()
        for venta in ventas:
            self.tree.delete(venta)
        for venta in Venta.select():
            self.tree.insert(
                "",
                0,
                text=(venta.id),
                values=(
                    venta.fecha,
                    venta.producto,
                    venta.cantidad,
                    venta.precio,
                    venta.precio_total,
                ),
            )

    def registrar_venta(self):
        """
        :Metodo: Hace que la base de datos registre una venta en caso de cumplir con las validacion de campos.
        """
        precio_total = round((self.var_precio.get() * self.var_cantidad.get()), 2)
        try:
            var_fecha = date(
                self.var_fecha_anio.get(),
                self.var_fecha_mes.get(),
                self.var_fecha_dia.get(),
            )
            validador = ValidadorVenta(
                var_fecha,
                self.var_producto.get(),
                self.var_cantidad.get(),
                self.var_precio.get(),
            )
            if validador.campos_validos():
                self.base.registrar(
                    var_fecha,
                    self.var_producto.get(),
                    self.var_cantidad.get(),
                    self.var_precio.get(),
                    precio_total,
                )
                self.actualizar_tree()
                messagebox.showinfo("Éxito", "Venta registrada con éxito")
            else:
                messagebox.showerror("Error", "Campos no validos.")

        except (_tkinter.TclError, ValueError):
            messagebox.showerror("Error", "Campos no validos.")

    def eliminar_venta(self):
        """
        :Metodo: Hace que la base de datos elimine la venta seleccionada en el treeview y actualiza la vista.
        """
        if self.tree.focus():
            confirmar = messagebox.askyesno(
                "Confirmacion",
                "¿Estás seguro de que quieres eliminar la compra seleccionada?",
            )
            if confirmar:
                id_a_eliminar = self.tree.item(self.tree.focus(), "text")
                self.base.eliminar(id_a_eliminar)
                self.actualizar_tree()
                messagebox.showinfo("Éxito", "Venta eliminada con éxito")

    def iniciar_modificacion(self):
        """
        :Metodo: Inicia el proceso de modificacion de una venta seleccionada en el treeview.
        """
        if self.tree.focus():
            id_venta = self.tree.item(self.tree.focus())["text"]
            self.cargar_datos(id_venta)

    def cargar_datos(self, id):
        """
        :Metodo: Carga los datos de una venta seleccionada en el treeview en los campos de entrada.
        """
        venta = self.base.obtener_datos_venta(id)

        self.var_fecha_dia.set(venta.fecha.day)
        self.var_fecha_mes.set(venta.fecha.month)
        self.var_fecha_anio.set(venta.fecha.year)
        self.var_producto.set(venta.producto)
        self.var_cantidad.set(venta.cantidad)
        self.var_precio.set(venta.precio)

        self.boton_aceptar = Boton(
            self.ventana,
            texto="Aceptar",
            color_fondo="#7EFF71",
            fuente="Helvetica 8 bold",
            funcion_info=lambda: self.finalizar_modificacion(id),
            place_info={"x": 340, "y": 280, "relwidth": 0.1, "relheight": 0.07},
        )

    def finalizar_modificacion(self, id):
        """
        :Metodo: Finaliza el proceso de modificación de una venta y actualiza la vista.
        """
        try:
            var_fecha = date(
                self.var_fecha_anio.get(),
                self.var_fecha_mes.get(),
                self.var_fecha_dia.get(),
            )
            validador = ValidadorVenta(
                var_fecha,
                self.var_producto.get(),
                self.var_cantidad.get(),
                self.var_precio.get(),
            )
            if validador.campos_validos():
                self.boton_aceptar.destroy()
                self.base.modificar(
                    id,
                    var_fecha,
                    self.var_producto.get(),
                    self.var_cantidad.get(),
                    self.var_precio.get(),
                    round((self.var_precio.get() * self.var_cantidad.get()), 2),
                )
                self.actualizar_tree()
                self.reiniciar_valores()
            else:
                messagebox.showerror("Error", "Campos no validos.")
        except ValueError:
            messagebox.showerror("Error", "Campos no validos.")

    def mostrar_consulta(self):
        """
        :Metodo: Muestra la consulta hecha a la base de datos por el total vendido entre dos fechas.
        """
        try:
            self.fecha_inicial = date(
                self.var_anio_inicial.get(),
                self.var_mes_inicial.get(),
                self.var_dia_inicial.get(),
            )

            self.fecha_final = date(
                self.var_anio_final.get(),
                self.var_mes_final.get(),
                self.var_dia_final.get(),
            )

            total_vendido = self.base.consultar_total_vendido(
                self.fecha_inicial, self.fecha_final
            )
            Etiqueta(
                self.ventana,
                texto=total_vendido,
                fuente="Helvetica 10 bold",
                color_fondo="#F9E192",
                color_letra="blue",
                place_info={"x": 535, "y": 250, "relwidth": 0.15, "relheight": 0.07},
            )
        except ValueError:
            messagebox.showinfo("Error", "Fecha invalida")

    def reiniciar_valores(self):
        """
        :Metodo: Reinicia los valores de los campos de entrada a sus valores default.
        """
        self.var_fecha_dia.set(0)
        self.var_fecha_mes.set(0)
        self.var_fecha_anio.set(0)
        self.var_producto.set("")
        self.var_cantidad.set(0)
        self.var_precio.set(0.0)

    def salir(self):
        """
        :Metodo: Cierra la aplicación en caso de confirmarse por el usuario.
        """
        if messagebox.askyesno("Confirmacion", "¿Estás seguro de que quieres salir?"):
            self.ventana.destroy()
