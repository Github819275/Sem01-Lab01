"""Abstract base class for all storage implementations."""

import json
from abc import ABC
from pathlib import Path
from typing import ClassVar, Generic, TypeVar, cast

from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)

class BaseStorage(ABC, Generic[T]):
    """Abstract base class for all storage implementations."""
    
    dto_class: ClassVar[type[T]]  # pyrefly: ignore[invalid-annotation] 
    # generic ClassVar with TypeVar is valid runtime pattern
    id_field: str = "id"  # Default ID field name
    
    def __init__(self, file_path: Path) -> None:
        """Initialize the storage with the given file path."""
        self.file_path = file_path
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self._save_to_file([])

    def _load_from_file(self) -> list[dict]:
        try:
            with open(self.file_path, encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save_to_file(self, data: list[dict]) -> None:
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    # --- Generic CRUD operations ---

    def get_by_id(self, entity_id: str) -> T | None:  
        """Retrieve an entity by its ID."""
        for item in self._load_from_file():
            model = self.dto_class.model_validate(item)
            if getattr(model, self.id_field) == entity_id:
                return model  # pyrefly: ignore[bad-return] — dto_class.model_validate() returns T subtype
        return None

    def get_all(self) -> list[T]:
        """Retrieve all entities."""
        return [self.dto_class.model_validate(item) 
        for item in self._load_from_file()]  # pyrefly: ignore[bad-return] 
        # dto_class.model_validate() returns list of T subtype

    def add(self, entity: T) -> T:
        """Add a new entity."""
        data = self._load_from_file()
        if any(getattr(self.dto_class.model_validate(item), self.id_field) == getattr(entity, self.id_field)
               for item in data):
            raise ValueError(f"Entity with {self.id_field} '{getattr(entity, self.id_field)}' already exists.")
        data.append(entity.model_dump())
        self._save_to_file(data)
        return entity

    def update(self, entity: T) -> T:  
        """Update an existing entity."""
        data = self._load_from_file()
        for i, item in enumerate(data):
            model = self.dto_class.model_validate(item)
            if getattr(model, self.id_field) == getattr(entity, self.id_field):
                data[i] = entity.model_dump()
                self._save_to_file(data)
                return entity  # pyrefly: ignore[bad-return]
                # returning same entity instance of type T
        raise ValueError(f"Entity with {self.id_field} {getattr(entity, self.id_field)} not found.")

    def delete(self, entity_id: str) -> bool:
        """Delete an entity by its ID."""
        data = self._load_from_file()
        new_data = [
            item for item in data
            if getattr(self.dto_class.model_validate(item), self.id_field) != entity_id
        ]
        if len(data) == len(new_data):
            return False
        self._save_to_file(new_data)
        return True
