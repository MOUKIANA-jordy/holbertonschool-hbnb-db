"""
  Now is easy to implement the database repository. The DBRepository
  should implement the Repository (Storage) interface and the methods defined
  in the abstract class Storage.

  The methods to implement are:
    - get_all
    - get
    - save
    - update
    - delete
    - reload (which can be empty)
"""

from src.models.base import Base
from src.persistence.repository import Repository
from sqlalchemy.org import SQLAlchemyError

class DBRepository(Repository):
    """Database repository implementation"""

    def __init__(self):
        """Initialize the repository with SQLAlchemy's session"""
        self.session = db.session

    def get_all(self, model_name: str) -> list:
        """Retrieve all records of a given model"""

        model_class = globals()[model_name]
        try:
            return self.session.query(model_class).all()
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error retrieving all {model_name}: {e}")
            return []

    def get(self, model_name: str, obj_id: str) -> Base | None:
        """Retrieve a record by its ID"""
        model_class = globals()[model_name]
        try:
            return self.session.query(model_class).get(obj_id)
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error retrieving {model_name} with id {obj_id}: {e}")
            return None

    def save(self, obj: Base) -> None:
        """Save a new record"""
        try:
            self.session.add(obj)
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error saving {obj}: {e}")
    def update(self, obj: Base) -> Base | None:
        """Update an existing record"""
        try:
            existing_obj = self.session.query(type(obj)).get(obj.id)
            if existing_obj:
                self.session.merge(obj)
                self.session.commit()
                return obj
            else:
                print(f"No record found to update: {obj}")
                return None
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error updating {obj}: {e}")
            return None

    def delete(self, obj: Base) -> bool:
        """Delete a record"""
        try:
            self.session.delete(obj)
            self.session.commit()
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error deleting {obj}: {e}")
            return False

    def reload(self) -> None:
        """Reload can be used to refresh the session, can be a no-op"""
        self.session.flush()
