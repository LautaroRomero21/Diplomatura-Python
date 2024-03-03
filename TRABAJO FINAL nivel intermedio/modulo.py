"""
:Importaciones:
- `peewee`: Se utiliza para interactuar con la base de datos SQLite.
- `os`: Interactua con el sistema operativo y gestiona rutas de archivos.
- `datetime`: Trabaja con el formato de fecha.

Se define y conecta a una base de datos SQLite llamada 'baseTPFinal.db', y se establecen las rutas de directorio y archivo de registro de errores.
"""

from peewee import (
    PeeweeException,
    fn,
    SqliteDatabase,
    Model,
    IntegerField,
    DoubleField,
    DateField,
    CharField,
    DoesNotExist,
)
import os
from datetime import datetime

db = SqliteDatabase("baseTPFinal.db")

BASE_DIR = os.path.dirname((os.path.abspath(__file__)))
LOG_PATH = os.path.join(BASE_DIR, "log.txt")


class RegistroLogError(Exception):
    """
    :Descripcion:
        Clase personalizada para manejar excepciones y registrar errores en un archivo log.txt.

    :Atributos:
        :linea (int): Número de línea donde se produjo el error.
        :archivo (str): Nombre del archivo donde se produjo el error.
        :fecha (datetime): Fecha y hora en que se produjo el error.
    """

    def __init__(self, linea, archivo, fecha):
        self.linea = linea
        self.archivo = archivo
        self.fecha = fecha

    def registrar_error(self):
        """
        :Metodo: Registra un error en el archivo log.txt.
        """
        with open(LOG_PATH, "a") as log_file:
            print(
                "Se ha dado un error en el archivo:",
                self.archivo,
                "linea:",
                self.linea,
                "fecha:",
                self.fecha,
                file=log_file,
            )


class Venta(Model):
    """
    :Descripcion:
        Clase que define el modelo de la tabla 'Venta' en la base de datos.
    """

    id = IntegerField(unique=True)
    "Identificador único de la venta"
    fecha = DateField()
    "Fecha de la venta"
    producto = CharField()
    "Nombre del producto vendido"
    cantidad = IntegerField()
    "Cantidad de productos vendidos"
    precio = DoubleField()
    "Precio unitario del producto"
    precio_total = DoubleField()
    "Precio total de la venta"

    class Meta:
        database = db


class Base:
    """
    :Descripcion:
        Clase que maneja las distintas acciones que se realizan con una base de datos.
    """

    def __init__(self):
        try:
            db.connect()
            db.create_tables([Venta])
        except PeeweeException:
            print("Error al conectarse a la base de datos")

    def registrar(self, fecha, producto, cantidad, precio, precio_total):
        """
        :Metodo: Registra una nueva venta en la base de datos.
        """
        try:
            Venta.create(
                id=self.mayor_id() + 1,
                fecha=fecha,
                producto=producto,
                cantidad=cantidad,
                precio=precio,
                precio_total=precio_total,
            )
        except PeeweeException as error:
            self.registrar_error(error)
            print("Error al registrar la venta en la Base de Datos")

    def modificar(
        self,
        id_a_modificar,
        nueva_fecha,
        nuevo_producto,
        nueva_cantidad,
        nuevo_precio,
        nuevo_precio_total,
    ):
        """
        :Metodo: Modifica una venta ya existente en la base.
        """
        try:
            venta_modificada = Venta.update(
                fecha=nueva_fecha,
                producto=nuevo_producto,
                cantidad=nueva_cantidad,
                precio=nuevo_precio,
                precio_total=nuevo_precio_total,
            ).where(Venta.id == id_a_modificar)
            venta_modificada.execute()
        except PeeweeException as error:
            self.registrar_error(error)
            print("Error al modificar la venta en la Base de Datos")

    def consultar_total_vendido(self, fecha_inicial, fecha_final):
        """
        :Metodo: Consulta el dinero total vendido entre dos fechas.
        """
        try:
            total_vendido = (
                Venta.select(fn.Sum(Venta.precio_total))
                .where((Venta.fecha >= fecha_inicial) & (Venta.fecha <= fecha_final))
                .scalar()
                or 0
            )
            return total_vendido
        except PeeweeException as error:
            self.registrar_error(error)
            print("Error al consultar el total vendido en la Base de Datos")
            return None

    def eliminar(self, id_a_eliminar):
        """
        :Metodo: Elimina una venta de la base de datos.
        """
        try:
            venta_a_eliminar = Venta.get(Venta.id == id_a_eliminar)
            venta_a_eliminar.delete_instance()
        except PeeweeException as error:
            self.registrar_error(error)
            print("Error al eliminar la venta de la Base de Datos")

    def mayor_id(self):
        """
        :Metodo: Obtiene el ultiom ID ingresado en la base de datos.
        """
        try:
            max_id = Venta.select(fn.Max(Venta.id)).scalar() or 0
            return max_id
        except PeeweeException as error:
            self.registrar_error(error)
            print("Error al obtener el mayor ID de venta de la Base de Datos")
            return None

    def obtener_datos_venta(self, id):
        """
        :Metodo: Obtiene los datos de una venta por su ID.
        """
        try:
            return Venta.get(Venta.id == id)
        except DoesNotExist as error:
            self.registrar_error(error)
            print("No existe la venta con el id indicado")

    def registrar_error(self, exception):
        """
        :Metodo: Registra un error en el archivo de log.
        """
        error = RegistroLogError(
            exception.__traceback__.tb_lineno,
            os.path.basename(exception.__traceback__.tb_frame.f_code.co_filename),
            datetime.now(),
        )
        error.registrar_error()
