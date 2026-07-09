from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    name: Mapped[str] = mapped_column(String(80), nullable=False)

    favorite_planets: Mapped[list["FavoritePlanet"]] = relationship("FavoritePlanet")
    favorite_characters: Mapped[list["FavoriteCharacter"]] = relationship("FavoriteCharacter")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            # do not serialize the password, its a security breach
        }
    
class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    population: Mapped[int] = mapped_column(nullable=True)
    climate: Mapped[str] = mapped_column(String(80), nullable=True)
    diameter: Mapped[int] = mapped_column(nullable=True)

    favorite_planets: Mapped[list["FavoritePlanet"]] = relationship("FavoritePlanet")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "climate": self.climate,
            "diameter": self.diameter,
        }

class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    age: Mapped[int] = mapped_column(nullable=True)
    height: Mapped[float] = mapped_column(Float, nullable=True)
    weight: Mapped[int] = mapped_column(nullable=True)
    sex: Mapped[str] = mapped_column(String(80), nullable=False)

    favorite_characters: Mapped[list["FavoriteCharacter"]] = relationship("FavoriteCharacter")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "height": self.height,
            "weight": self.weight,
            "sex": self.sex,
        }

class FavoritePlanet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"))
    
    user: Mapped["User"] = relationship('User')
    planet: Mapped["Planet"] = relationship('Planet')

class FavoriteCharacter(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    character_id: Mapped[int] = mapped_column(ForeignKey("character.id"))

    user: Mapped["User"] = relationship('User')
    character: Mapped["Character"] = relationship('Character')
