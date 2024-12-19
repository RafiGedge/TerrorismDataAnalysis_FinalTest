from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database.models.base import Base


class Country(Base):
    __tablename__ = 'countries'  # noqa

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True, unique=True)

    events = relationship("Event", back_populates="countries")

# from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
# from sqlalchemy.ext.declarative import declarative_base
#
# Base = declarative_base()
#
#
# # טבלה ראשית
# class Parent(Base):
#     __tablename__ = 'parents'
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#
#
# # טבלה עם מפתח זר שמפנה ל-Parent
# class Child(Base):
#     __tablename__ = 'children'
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     parent_id = Column(Integer, ForeignKey('parents.id'))  # מפתח זר
#
#     # אופציונלי: יצירת קשר ORM עם הטבלה Parent
#     parent = relationship("Parent", back_populates="children")
#
#
# # הגדרה הפוכה של הקשר בטבלה Parent
# Parent.children = relationship("Child", back_populates="parent")
#
# # יצירת חיבור לדטאבייס
# engine = create_engine('postgresql://user:password@localhost/mydatabase')
#
# # יצירת הטבלאות בדטאבייס
# Base.metadata.create_all(engine)
#
#
# from sqlalchemy.orm import sessionmaker
#
# # יצירת Session
# Session = sessionmaker(bind=engine)
# session = Session()
#
# # יצירת אובייקט Parent
# new_parent = Parent(name="John Doe")
# session.add(new_parent)
# session.commit()
#
# # יצירת Child שמפנה ל-Parent
# new_child = Child(name="Jane Doe", parent_id=new_parent.id)
# session.add(new_child)
# session.commit()
#
# # שליפת הילדים של ההורה
# parent = session.query(Parent).filter_by(name="John Doe").first()
# print(parent.children)  # מציג את כל הילדים
