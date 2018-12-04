from datetime import datetime

from app import db

association_table = db.Table('association', db.Model.metadata,
	db.Column('product',db.Integer, db.ForeignKey('product.id')),
	db.Column('order',db.Integer, db.ForeignKey('order.id'))
	)

'''
	models holds database tables
'''

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	firstname = db.Column(db.String(24), index=True, unique=True)
	lastname = db.Column(db.String(24), index=True, unique=True)
	email = db.Column(db.String(50), index=True, unique=True)
	password = db.Column(db.String(128))
	phonenumber = db.Colunm(db.String(18), index=True, unique=True)
	address1 = db.Column(db.String(200), index=True, unique=True)
	address2 = db.Column(db.String(200), index=True, unique=True)
	postcode = db.Column(db.Integer(12), index=True)
	city = db.Column(db.String(24), index=True)
	state = db.Column(db.String(24), index=True)
	country = db.Column(db.String(24), index=True)
	#user and order relationship is a one to many 
	order = db.relationship('Order', backref='my_orders')
	#user and kart is one to one relationship
	kart = db.relationship('Kart', uselist=False, backref='user_kart')

	def __repr__(self):
		return '<User {}'.format(self.email)




class Categories(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	category_name  = db.Column(db.String(20), index = True, unique=True) 
	#one to many relationship btwn categories and products
	product = db.relationship('Products', backref='products_categories')

	def __repr__(self):
		return '<Categories {}'.format(self.category_name)
	


class Products(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	product_name = db.Column(db.String(100), index=True, unique=True)
	product_price = db.Column(db.Numeric(7), index=True)
	product_image = db.Column(db.String(120),index=True, unique=True)
	product_stock = db.Column(Integer(3), index = True)
	#foreign key to categories
	categories_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
	#foreign key to kart
	kart_id = db.Column(db.Integer, db.ForeignKey('kart.id'))
	
	#many many rel with order
	order = db.relationship("Order", secondary = association_table)

	def __repr__(self):
		return '<Products {}'.format(self.product_name)



class Kart(db.Model):
	id = db.Column(db.Integer, primary_key=True)

	#one cart many products (relationship)
	product_kart = db.relationship('Products', backref='products_kart')
	#foreign key for productid

	#foreign key for userid
	#indicating a one to one rel with user
	user_id = db.Column(db.Integer, ForeignKey('user.id'))
	user = db.relationship('User', uselist=False, backref='user')




class Order(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	
	'''

		foreign key for product.id
		test this weda its one order several products or several orders, serveral products
		using many to many for now	
	'''
	products_order = db.relationship("Order", primary_key=True)


	#foreign key for userid
	#
	#user and order relationship is a one to many(foreign key
	# linking the user class and the order class)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<Order {}'.format(self.timestamp)