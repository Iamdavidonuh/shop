from app import db, login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


association_table = db.Table('association', db.Model.metadata,
	db.Column('product',db.Integer, db.ForeignKey('product.id')),
	db.Column('order',db.Integer, db.ForeignKey('order.id'))
	)

'''
	models holds database tables
'''


class User(UserMixin, db.Model):

	__tablename__="user"

	id = db.Column(db.Integer, primary_key=True)
	firstname = db.Column(db.String(24), index=True)
	lastname = db.Column(db.String(24), index=True)
	email = db.Column(db.String(50), index=True, unique=True)
	password_hash = db.Column(db.String)
	phonenumber = db.Column(db.String(18), index=True, unique=True)
	is_admin = db.Column(db.Boolean, default = False)
	#user and order relationship is a one to many 
	order = db.relationship('Order', backref='my_orders')
	#user and kart is one to one relationship
	kart = db.relationship('Kart', uselist=False, backref='user_kart')
	#one to many relationships with Shipping info
	shipping_info = db.relationship('ShippingInfo', backref='role',lazy='dynamic')
	
	def set_password(self, password):
		self.password_hash = generate_password_hash(password)
	
	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return '<User {}>'.format(self.email)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))





class ShippingInfo(db.Model):
	__tablename__ = "shipping info"
	id = db.Column(db.Integer, primary_key=True)
	address1 = db.Column(db.String(200), index=True)
	address2 = db.Column(db.String(200), index=True)
	postcode = db.Column(db.String(12), index=True)
	city = db.Column(db.String(24), index=True)
	state = db.Column(db.String(24), index=True)
	country = db.Column(db.String(24), index=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


	def __repr__(self):
		return '<ShippingInfo {}>'.format(self.address1)




class Categories(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	category_name  = db.Column(db.String(20), index = True) 
	#one to many relationship btwn categories and products
	product = db.relationship('Products', backref='products_categories')

	def __repr__(self):
		return '<Categories {}>'.format(self.category_name)
	
class Products(db.Model):
	__tablename__ = 'product'
	id = db.Column(db.Integer, primary_key=True)
	product_name = db.Column(db.String(100), index=True)
	product_price = db.Column(db.Integer, index=True)
	product_image = db.Column(db.String(120),index=True)
	product_description = db.Column(db.String(200), index=True)
	product_stock = db.Column(db.Integer, index = True)
	#foreign key to categories
	categories_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
	#foreign key to kart
	kart_id = db.Column(db.Integer, db.ForeignKey('kart.id'))
	#one to many relationship btwn products and productsvariations
	variation = db.relationship('ProductVariations', backref='product_variation')
	'''
		foreign key for product.id
		test this weda its one order several products or several orders, serveral products
		using many to many for now	
		#many many rel with order
	'''
	order = db.relationship("Order", secondary = association_table)

	def __repr__(self):
		return '<Products {}>'.format(self.product_name)



''' product variation table for Products (one to many relationship)'''
class ProductVariations(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	product_size = db.Column(db.String(5), index = True)
	product_color = db.Column(db.String(10), index=True)
	products_id = db.Column(db.Integer, db.ForeignKey('product.id'))

	def __repr__(self):
		return '<Variations for {} -- {}>'.format(self.products_id.product_name, self.product_size)



class Kart(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	product_name = db.Column(db.String, index =True)
	#one cart many products (relationship)
	product_kart = db.relationship('Products', backref='products_kart')
	#foreign key for productid
	
	#foreign key for userid indicating a one to one rel with user
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	#user and kart is one to one relationship
	user = db.relationship('User', uselist=False, backref='user')
	def __repr__(self):
		return '<Cart {}>'.format(self.product_name)




class Order(db.Model):
	__tablename__ = 'order'
	id = db.Column(db.Integer, primary_key=True)
	quantity = db.Column(db.Integer, index = True)
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	'''

		foreign key for product.id
		test this weda its one order several products or several orders, serveral products
		using many to many for now	

		products_order = db.relationship("Order", backref="products")
		

	'''
	#foreign key for userid
	#
	#user and order relationship is a one to many(foreign key
	# linking the user class and the order class)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<Order {}>'.format(self.timestamp)