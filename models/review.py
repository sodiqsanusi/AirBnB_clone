#!/usr/bin/python3
"""Module handling the Review class"""
from models.base_model import BaseModel


class Review(BaseModel):
    """
    Review class inheriting from the BaseModel

     Attributes:
        place_id (str): The Place id
        user_id (str): The User id
        text (str): The text of the review
    """

    place_id = ""
    user_id = ""
    text = ""

    def __init__(self, *args, **kwargs):
        """Initializes Review"""
        super().__init__(*args, **kwargs)
