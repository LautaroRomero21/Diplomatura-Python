from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
import re

id = 0
boton_aceptar = None

#########################################################################################
#####################################  FUNCIONES  #######################################
#########################################################################################


def crear_base():
    global con
    con = sqlite3.connect("baseTPFinal.db")


def crear_tabla():
    global cursor
    cursor = con.cursor()
    sql = "CREATE TABLE IF NOT EXISTS ventas(id INTEGER PRIMARY KEY AUTOINCREMENT, fecha text, producto text, cantidad INTEGER, precio real, precio_total real)"
    cursor.execute(sql)
    con.commit()


def actualizar_tabla():
    global id
    cursor.execute("SELECT * FROM ventas")
    ventas = cursor.fetchall()
    if ventas:
        for filas in ventas:
            tree.insert(
                "",
                "end",
                text=str(filas[0]),
                values=(filas[1], filas[2], filas[3], filas[4], filas[5]),
            )
        id = filas[0]
    else:
        id = 0


def registrar():
    global id
    id += 1
    # Verificar si la tabla está vacía
    cursor.execute("SELECT COUNT(*) FROM ventas")
    cant_productos = cursor.fetchone()[0]
    # Si la tabla está vacía, reiniciar el contador de ID
    if cant_productos == 0:
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='ventas'")
        con.commit()
        id = 1

    var_fecha = (
        str(var_fecha_dia.get())
        + "/"
        + str(var_fecha_mes.get())
        + "/"
        + str(var_fecha_anio.get())
    )

    precio_total = round((var_precio.get() * var_cantidad.get()), 2)

    if re.match(r"^[0-9a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", var_producto.get()):
        tree.insert(
            "",
            "end",
            text=str(id),
            values=(
                var_fecha,
                var_producto.get(),
                var_cantidad.get(),
                var_precio.get(),
                precio_total,  # Agrega el precio total a la nueva columna
            ),
        )

        data = (
            var_fecha,
            var_producto.get(),
            var_cantidad.get(),
            var_precio.get(),
            precio_total,
        )
        sql = "INSERT INTO ventas (fecha, producto, cantidad, precio, precio_total) VALUES(?, ?, ?, ?, ?)"
        cursor.execute(sql, data)
        con.commit()

        var_fecha_dia.set(0)
        var_fecha_mes.set(0)
        var_fecha_anio.set(0)
        var_producto.set("")
        var_cantidad.set(0)
        var_precio.set(0.0)
        messagebox.showinfo("Éxito", "Venta registrada con éxito")
    else:
        messagebox.showerror("Error", "El producto no es válido.")


def aceptar_modificacion(id_modificar):
    nueva_fecha = (
        str(var_fecha_dia.get())
        + "/"
        + str(var_fecha_mes.get())
        + "/"
        + str(var_fecha_anio.get())
    )
    nuevo_precio_total = round((var_precio.get() * var_cantidad.get()), 2)

    for item in tree.get_children():
        posible_id = tree.item(item, "text")
        if int(posible_id) == id_modificar:
            tree.item(
                item,
                values=(
                    nueva_fecha,
                    var_producto.get(),
                    var_cantidad.get(),
                    var_precio.get(),
                    nuevo_precio_total,
                ),
            )
    data = (
        nueva_fecha,
        var_producto.get(),
        var_cantidad.get(),
        var_precio.get(),
        nuevo_precio_total,
        id_modificar,
    )
    sql = "UPDATE ventas SET fecha=?,producto=?,cantidad=?,precio=?,precio_total=? WHERE id=?;"
    cursor.execute(sql, data)
    con.commit()
    var_fecha_dia.set(0)
    var_fecha_mes.set(0)
    var_fecha_anio.set(0)
    var_producto.set("")
    var_cantidad.set(0)
    var_precio.set(0.0)
    messagebox.showinfo("Éxito", "Venta modificada con éxito")
    boton_aceptar.destroy()


def modificar():
    global entry_id_modificar
    global boton_ok
    global etiqueta_id_modificar
    global boton_aceptar

    if boton_aceptar:
        boton_aceptar.destroy()
    entry_id_modificar = Entry(app, width=12)
    entry_id_modificar.place(x=341, y=287)
    boton_ok = Button(
        app, text="✔", bg="#7EFF71", font="Helvetica 8 bold", command=obtener_datos
    )
    boton_ok.place(x=362, y=310, relwidth=0.05, relheight=0.04)
    etiqueta_id_modificar = Label(
        app, text="ID a modificar :", bg="#8B8B8B", fg="white"
    )
    etiqueta_id_modificar.place(x=338, y=267)


def obtener_datos():
    global boton_aceptar
    id_modificar = int(entry_id_modificar.get())
    cursor.execute("SELECT * FROM ventas WHERE id=?", (id_modificar,))
    compra_existente = cursor.fetchone()

    if compra_existente:
        match = re.match(r"(\d+)/(\d+)/(\d+)", compra_existente[1])
        if match:
            dia, mes, anio = match.groups()
            var_fecha_dia.set(int(dia))
            var_fecha_mes.set(int(mes))
            var_fecha_anio.set(int(anio))
        var_producto.set(compra_existente[2])
        var_cantidad.set(compra_existente[3])
        var_precio.set(compra_existente[4])
        boton_aceptar = Button(
            app,
            text="Aceptar",
            bg="#7EFF71",
            font="Helvetica 8 bold",
            command=lambda: aceptar_modificacion(id_modificar),
        )
        boton_aceptar.place(x=340, y=280, relwidth=0.1, relheight=0.07)
    else:
        messagebox.showerror("Error", "Compra no encontrada")
    entry_id_modificar.destroy()
    boton_ok.destroy()
    etiqueta_id_modificar.destroy()


def consultar():
    total_vendido = 0
    fecha_inicial = (
        var_anio_inicial.get() * 10000
        + var_mes_inicial.get() * 100
        + var_dia_inicial.get()
    )
    fecha_final = (
        var_anio_final.get() * 10000 + var_mes_final.get() * 100 + var_dia_final.get()
    )

    cursor.execute("SELECT * FROM ventas")
    ventas = cursor.fetchall()
    if ventas:
        for filas in ventas:
            dia, mes, anio = filas[1].split("/")
            fecha_consultada = int(anio) * 10000 + int(mes) * 100 + int(dia)
            if fecha_inicial <= fecha_consultada <= fecha_final:
                total_vendido += filas[5]

    etiqueta_resultado = Label(
        app,
        bg="#F9E192",
        fg="blue",
        font="Helvetica 15",
    )
    etiqueta_resultado.place(x=535, y=250, relwidth=0.15, relheight=0.07)
    etiqueta_resultado["text"] = total_vendido


def eliminar():
    if tree.focus():
        id_a_eliminar = tree.item(tree.focus(), "text")
        confirmar = messagebox.askyesno(
            "Confirmacion",
            "¿Estás seguro de que quieres eliminar la compra seleccionada?",
        )
        if confirmar:
            data = (id_a_eliminar,)
            sql = "DELETE from ventas where id = ?;"
            cursor.execute(sql, data)
            con.commit()
            tree.delete(tree.focus())
            messagebox.showinfo("Éxito", "Venta eliminada con éxito")


def salir():
    eleccion = messagebox.askyesno(
        "Confirmacion", "¿Estás seguro de que quieres salir?"
    )
    if eleccion:
        app.destroy()


#########################################################################################
#####################################  VISUAL  ##########################################
#########################################################################################

app = Tk()
app.geometry("760x540")
app.title("TRABAJO FINAL")
app.configure(bg="#8B8B8B")

var_fecha_dia = IntVar()
var_fecha_mes = IntVar()
var_fecha_anio = IntVar()
var_producto = StringVar()
var_cantidad = IntVar()
var_precio = DoubleVar()
var_dia_inicial = IntVar()
var_mes_inicial = IntVar()
var_anio_inicial = IntVar()
var_dia_final = IntVar()
var_mes_final = IntVar()
var_anio_final = IntVar()

frame = Frame(app, bg="#F9E192")
frame.place(x=10, y=50, relwidth=0.42, relheight=0.52)
frame = Frame(app, bg="#F9E192")
frame.place(x=430, y=50, relwidth=0.42, relheight=0.52)
frame = Frame(app, bg="#F9E192")
frame.place(x=430, y=50, relwidth=0.42, relheight=0.52)

etiqueta_ventas = Label(
    app, text="VENTAS FERRETERIA", font="Helvetica 15 bold", bg="#F9E192"
)
etiqueta_ventas.pack(fill=X)
etiqueta_fecha = Label(
    app, text="Fecha", font="Helvetica 10 bold", bg="#F9E192", fg="black"
)
etiqueta_fecha.place(x=43, y=110)
etiqueta_producto = Label(
    app, text="Producto", font="Helvetica 10 bold", bg="#F9E192", fg="black"
)
etiqueta_producto.place(x=36, y=160)
etiqueta_cantidad = Label(
    app, text="Cantidad", font="Helvetica 10 bold", bg="#F9E192", fg="black"
)
etiqueta_cantidad.place(x=37, y=210)
etiqueta_precio = Label(
    app, text="Precio c/u", font="Helvetica 10 bold", bg="#F9E192", fg="black"
)
etiqueta_precio.place(x=34, y=260)
etiqueta_consultar = Label(app, text="Consulta", font="Helvetica 15 bold", bg="#F9E192")
etiqueta_consultar.place(x=536, y=60, relwidth=0.15, relheight=0.07)
etiqueta_fecha_inicial = Label(
    app, text="Fecha Inicial", font="Helvetica 10 bold", bg="#F9E192"
)
etiqueta_carga = Label(
    app, text="Carga de Ventas", font="Helvetica 15 bold", bg="#F9E192"
)
etiqueta_carga.place(x=75, y=60, relwidth=0.25, relheight=0.07)
etiqueta_fecha_inicial.place(x=435, y=100, relwidth=0.15, relheight=0.07)
etiqueta_fecha_final = Label(
    app, text="Fecha Final", font="Helvetica 10 bold", bg="#F9E192"
)
etiqueta_fecha_final.place(x=435, y=160, relwidth=0.15, relheight=0.07)
etiqueta_resultado_consulta = Label(
    app,
    text="Facturacion total:",
    font="Helvetica 12 bold",
    bg="#F9E192",
)
etiqueta_resultado_consulta.place(x=480, y=215, relwidth=0.3, relheight=0.07)

boton_registrar = Button(
    app, text="Registrar", bg="#2EFF19", font="Helvetica 8 bold", command=registrar
)
boton_registrar.place(x=340, y=50, relwidth=0.1, relheight=0.07)
boton_modificar = Button(
    app, text="Modificar", bg="#7EFF71", font="Helvetica 8 bold", command=modificar
)
boton_modificar.place(x=340, y=90, relwidth=0.1, relheight=0.07)
boton_eliminar = Button(
    app, text="Eliminar", bg="#FF4343", font="Helvetica 8 bold", command=eliminar
)
boton_eliminar.place(x=340, y=170, relwidth=0.1, relheight=0.07)
boton_consultar = Button(
    app, text="Consultar", bg="#4691FF", font="Helvetica 8 bold", command=consultar
)
boton_consultar.place(x=340, y=130, relwidth=0.1, relheight=0.07)
boton_salir = Button(
    app, text="Salir", bg="#FD8F79", font="Helvetica 8 bold", command=salir
)
boton_salir.place(x=340, y=210, relwidth=0.1, relheight=0.07)


entry_fecha_dia = Entry(app, textvariable=var_fecha_dia, width=8)
entry_fecha_dia.place(x=120, y=112)
entry_fecha_mes = Entry(app, textvariable=var_fecha_mes, width=8)
entry_fecha_mes.place(x=180, y=112)
entry_fecha_anio = Entry(app, textvariable=var_fecha_anio, width=8)
entry_fecha_anio.place(x=240, y=112)
entry_producto = Entry(app, textvariable=var_producto, width=28)
entry_producto.place(x=120, y=162)
entry_cantidad = Entry(app, textvariable=var_cantidad, width=28)
entry_cantidad.place(x=120, y=212)
entry_precio = Entry(app, textvariable=var_precio, width=28)
entry_precio.place(x=120, y=262)
entry_dia_inicial = Entry(app, textvariable=var_dia_inicial, width=8)
entry_dia_inicial.place(x=550, y=110)
entry_mes_inicial = Entry(app, textvariable=var_mes_inicial, width=8)
entry_mes_inicial.place(x=610, y=110)
entry_anio_inicial = Entry(app, textvariable=var_anio_inicial, width=8)
entry_anio_inicial.place(x=670, y=110)
entry_dia_final = Entry(app, textvariable=var_dia_final, width=8)
entry_dia_final.place(x=550, y=170)
entry_mes_final = Entry(app, textvariable=var_mes_final, width=8)
entry_mes_final.place(x=610, y=170)
entry_anio_final = Entry(app, textvariable=var_anio_final, width=8)
entry_anio_final.place(x=670, y=170)

tree = ttk.Treeview(app)
tree["columns"] = (
    "col1",
    "col2",
    "col3",
    "col4",
    "col5",
)
tree.column("#0", width=5, minwidth=25, anchor=W)
tree.column("col1", width=5, minwidth=50, anchor=E)
tree.column("col2", width=120, minwidth=80, anchor=W)
tree.column("col3", width=5, minwidth=80, anchor=E)
tree.column("col4", width=5, minwidth=80, anchor=E)
tree.column("col5", width=5, minwidth=80, anchor=E)

tree.heading("#0", text="ID")
tree.heading("col1", text="Fecha")
tree.heading("col2", text="Producto")
tree.heading("col3", text="Cantidad")
tree.heading("col4", text="Precio c/u")
tree.heading("col5", text="Precio Total")

tree.place(x=0, y=350, relwidth=1, relheight=1)

crear_base()
crear_tabla()
actualizar_tabla()

app.mainloop()
