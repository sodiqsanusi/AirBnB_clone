#!/usr/bin/python3
"""Regarding Amenities"""
from models.base_model import BaseModel


class Amenity(BaseModel):
    """
    Class handling the amenities

    Attributes:
        name (str): The name of the amenity.
    """

    name = ""

    def __init__(self, *args, **kwargs):
        """Initializes amenity"""
        super().__init__(*args, **kwargs)
