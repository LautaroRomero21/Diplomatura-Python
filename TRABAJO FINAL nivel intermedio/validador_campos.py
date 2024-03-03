"""
:Importaciones:
- `re`: Realiza validaciones utilizando expresiones regulares.
- `datetime`: Trabaja con el formato de fecha.
"""

import re
from datetime import datetime


class ValidadorVenta:
    """
    :Descripcion: Clase que puede verificar un campo determinado de una venta pasada al inicializarla.
    """

    def __init__(self, fecha, nombre_producto, cantidad, precio):
        self.fecha = fecha
        self.nombre_producto = nombre_producto
        self.cantidad = cantidad
        self.precio = precio

    def campos_validos(self):
        """
        :Metodo: Verifica que todos los demas metodos se cumplan.

        :Returns:
            bool: True si todos los campos son validos, False en caso contrario.
        """
        return (
            self.validar_producto()
            and self.validar_fecha()
            and self.validar_cantidad()
            and self.validar_precio()
        )

    def validar_producto(self):
        """
        :Metodo: Valida el nombre del producto.

        :Returns:
            bool: True si el nombre del producto es alfanumerico, False en caso contrario.
        """
        return bool(
            re.match(r"^[0-9a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", str(self.nombre_producto))
        )

    def validar_fecha(self):
        """
        :Metodo: Valida el campo de la fecha.

        :Returns:
            bool: True si la fecha es menor o igual a la actual, False en caso contrario.
        """
        try:
            return self.fecha <= datetime.now().date()
        except ValueError:
            return False

    def validar_cantidad(self):
        """
        :Metodo: Valida el campo de la cantidad.

        :Returns:
            bool: True si la cantidad es un numero natural, False en caso contrario.
        """
        return bool(re.match("^[1-9][0-9]*$", str(self.cantidad)))

    def validar_precio(self):
        """
        :Metodo: Valida el campo del precio.

        :Returns:
            bool: True si el precio es un numero real positivo, False en caso contrario.
        """
        return bool(re.match("^[0-9]+(\.[0-9]+)?$", str(self.precio)))
