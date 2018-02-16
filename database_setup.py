import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine #(create_engine) used for configuration at the end of the file
from sqlalchemy.ext.declarative import declarative_base # to use in configuration and class code
from sqlalchemy.orm import relationship # to create foreign key relationships (used when write up mapper)

# making instance to declarative_base class
# declarative_base will let SQLAlchemy know that classes are special that correspond to tables in database
Base = declarative_base()

class Restaurant(Base): # Class
	__tablename__ = 'restaurant' # Table

	# Mapper
	name = Column(String(80),nullable=False)
	id = Column(Integer,primary_key=True)

	def __str__(self):
		return self.name
	@property
	def serialize(self):
		return {
			'name':self.name,
			'id':self.id,
		}

class MenuItem(Base): # Class
	__tablename__ = 'menu_item' # Table

	# Mapper
	name = Column(String(80),nullable=False)
	id = Column(Integer ,primary_key=True)
	course = Column(String(250))
	description = Column(String(250))
	restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
	restaurant = relationship(Restaurant)
	price = Column(String(250))
	def __str__(self):
		return self.name

	@property	#property for JSON
	def serialize(self):
		return {
		'name' : self.name,
		'description' : self.description,
		'id' : self.id,
		'price' : self.price,
		'course' : self.course,
		'restaurant' : self.restaurant.name,
		}
############### The end of file ##################

# making instance to create_engine class and point to dabase we will use
engine = create_engine('sqlite:///restaurantmenus.db')

# which goes into the database and adds the classes soon create new tables on database.
Base.metadata.create_all(engine)