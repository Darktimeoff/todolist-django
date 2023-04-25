
from django.db.models.manager import BaseManager
from typing import TypeVar, Generic, Type

T = TypeVar('T')

class Dao(Generic[T]):
    query: BaseManager[T]

    def __init__(self, model: Type[T], ordering=None):
        self.query = model.objects.all()
        if ordering:
            self.query = self.query.order_by(ordering)
        

    def get_all(self) -> BaseManager[T]:
        return self.query.all()
    
    def get_by_id(self, id: int) -> T:
        """raise DoesNotExist exception if not found"""
        return self.query.get(pk=id)
    
    def create(self, data: dict) -> T:
        return self.query.create(**data)