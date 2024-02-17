#!/usr/bin/python3
"""Class focusing on the city attributes"""
from models.base_model import BaseModel


class City(BaseModel):
    """
    City class inheriting from the BaseModel

    Attributes:
        state_id (str): The state id
        name (str): The name of the city
    """

    state_id = ""
    name = ""

    def __init__(self, *args, **kwargs):
        """Initializes City"""
        super().__init__(*args, **kwargs)
