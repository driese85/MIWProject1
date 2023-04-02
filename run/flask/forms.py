from flask_wtf import FlaskForm
from wtforms import DecimalRangeField
from wtforms.validators import NumberRange
from wtforms.validators import InputRequired

# Class to create Flask form to retrieve parameters for making lifespan predictions
class getLifespanForm(FlaskForm):
    genetic = DecimalRangeField('genetic', validators=[InputRequired(), NumberRange(60, 110)])
    length = DecimalRangeField('length', validators=[InputRequired(), NumberRange(150, 215)])
    mass = DecimalRangeField('mass', validators=[InputRequired(), NumberRange(50, 165)])
    exercise = DecimalRangeField('exercise', validators=[InputRequired(), NumberRange(0, 8)])
    smoking = DecimalRangeField('smoking', validators=[InputRequired(), NumberRange(0, 25)])
    alcohol = DecimalRangeField('alcohol', validators=[InputRequired(), NumberRange(0, 10)])
    sugar = DecimalRangeField('sugar', validators=[InputRequired(), NumberRange(0, 15)])