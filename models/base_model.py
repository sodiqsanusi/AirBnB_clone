#!/usr/bin/python3
"""Defines the BaseModel class"""
import models
from uuid import uuid4
from datetime import datetime


class BaseModel:
    """Represents the BaseModel"""

    DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"

    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel.

        Args:
            *args (any): Unused.
            **kwargs (dict): Key pairs of attributes.
        """
        self.id = str(uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()
        self.load_from_kwargs(kwargs)

    def load_from_kwargs(self, kwargs):
        """Load attributes from keyword arguments."""
        if kwargs:
            for key, value in kwargs.items():
                if key in ("created_at", "updated_at"):
                    setattr(self,
                            key,
                            datetime.strptime(value, self.DATE_FORMAT))
                else:
                    setattr(self, key, value)
        else:
            models.storage.new(self)

    def save(self):
        """Update updated_at with the current datetime and save."""
        self.updated_at = datetime.today()
        models.storage.save()

    def to_dict(self):
        """Return the dictionary of the BaseModel instance.

        Includes the key/value pair __class__ representing
        the class name of the object.
        """
        return {
            **self.__dict__,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "__class__": self.__class__.__name__,
        }

    def __str__(self):
        """Return the print/str representation of the BaseModel instance."""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"
