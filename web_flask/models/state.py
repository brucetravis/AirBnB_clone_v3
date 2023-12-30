#!/usr/bin/python3
"""
State class
"""
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv
import models


class State(BaseModel, Base):
    """State class"""
    __tablename__ = "states"

    name = Column(String(128), nullable=False)

    if getenv("HBNB_TYPE_STORAGE") == 'db':
        cities = relationship("City", backref="state", cascade="all, delete-orphan")

    else:
        @property
        def cities(self):
            """Getter attribute cities that returns the list of City instances
            with state_id equals to the current State.id"""
            all_cities = models.storage.all(City)
            state_cities = [city for city in all_cities.values() if city.state_id == self.id]
            return state_cities
