from flask_wtf import FlaskForm
from wtforms import RadioField
from wtforms.validators import DataRequired

class ProductVariations(FlaskForm):
    sizes = RadioField('Sizes',validators=[DataRequired(message="select a product size")],
    choices=[('Small','S'),('Medium','M'),('Large','L'),('Extra Large','XL')])


