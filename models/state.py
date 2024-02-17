#!/usr/bin/python3
"""Module handling the State class"""
from models.base_model import BaseModel


class State(BaseModel):
    """
    State class inheriting from the BaseModel

    Attributes:
        name (str): The name of the state.
    """

    name = ""

    def __init__(self, *args, **kwargs):
        """Initializes State"""
        super().__init__(*args, **kwargs)
