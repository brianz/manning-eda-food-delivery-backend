import abc

from ..domain import model


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def create_menu_item(self, menu_item: model.MenuItem):
        raise NotImplementedError

    # @abc.abstractmethod
    # def get(self, reference) -> models.Batch:
    #     raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session):
        self.session = session

    def create_menu_item(self, menu_item: model.MenuItem):
        return super().create_menu_item(menu_item)


# class SqlAlchemyMenuRepository(AbstractRepository):

#     def (self, batch):
#         self.session.add(batch)

# def get(self, reference):
#     return self.session.query(models.Menu).filter_by(reference=reference).one()

# def list(self):
#     return self.session.query(models.Menu).all()
