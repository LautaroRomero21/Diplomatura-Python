"""
::PATRON OBSERVER:: Utilizacion de un sujeto que sera observado por un observer que realizara una accion al detectar un cambio de estado en el sujeto
"""


class Sujeto:
    """
    :Descripcion:
         Es el objeto que tendra su lista de observadores a los cuales debera notificar en caso de un cambio en el.

    :Atributos:
        :observadores (list): lista de sus observadores.
    """

    observadores = []

    def agregar(self, observador):
        self.observadores.append(observador)

    def quitar(self, observador):
        self.observadores.remove(observador)

    def notificar(self):
        for observador in self.observadores:
            observador.update()


class Observador:
    """
    :Descripcion:
         Es el objeto que tendra que observa al sujeto y realiza sus acciones correspondientes en base a un cambio en su sujeto.
    """

    def update(self):
        raise NotImplementedError("Delegación de actualización")


class ObservadorRegistroEnBase(Observador):
    """
    :Descripcion:
        Observador determinado que, al haber un registro en la base de datos que observa, hace que la ventana actualice su treeview.
    """

    def __init__(self, obj_observado, ventana):
        self.obj_observado = obj_observado
        self.ventana_asociada = ventana

        self.obj_observado.agregar(self)

    def update(self):
        self.ventana_asociada.actualizar_tree()
