from sqlalchemy import Boolean, Column, Integer, String

from database import Base

class ColorPallete(Base):
    __tablename__ = "color_pallete"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    color1 = Column(String)
    color2 = Column(String)
    color3 = Column(String)
    color4 = Column(String)
    color5 = Column(String)
