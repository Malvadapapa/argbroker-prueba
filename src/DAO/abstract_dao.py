import abc

class AbstractDAO(abc.ABC):
    @abc.abstractmethod
    def crear(self, objeto):
        pass

    @abc.abstractmethod
    def obtener(self, id):
        pass

    @abc.abstractmethod
    def actualizar(self, objeto):
        pass

    @abc.abstractmethod
    def eliminar(self, id):
        pass