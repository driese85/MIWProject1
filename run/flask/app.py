from flask import Flask, render_template, redirect, url_for, session, request, jsonify
from forms import getLifespanForm
import pickle
import numpy as np
import pandas as pd
from icecream import ic

# init Flask app
app = Flask(__name__)
# Secret key for use with CSRF token
# TODO: put key in environment variable
app.config['SECRET_KEY'] = 'ebc72148568923ee1fdd713b4a247f4c97548a11a409fbfc'

# load the model from disk
filename = 'data/finalized_model.pkl'
model = pickle.load(open(filename, 'rb'))

# route to index page with form to enter parameters for prediction
@app.route('/', methods=['GET', 'POST'])
def index():
    # create instance of getLifespanForm class
    form = getLifespanForm()
    # if form validates succesfully, save parameters in session variable to access in subsequent requests
    if form.validate_on_submit():
        session['params'] = {
                                'genetic': float(form.genetic.data),
                                'length': float(form.length.data),
                                'mass': float(form.mass.data),
                                'exercise': float(form.exercise.data),
                                'smoking': float(form.smoking.data),
                                'alcohol': float(form.alcohol.data),
                                'sugar': float(form.sugar.data)
                                }
        # create session key to save parameters for new predictions
        session['new_params'] = session.get('params')
        return redirect(url_for('predict'))
    return render_template('index.html', form=form)

# route to predict page to make the predicition and show the output
@app.route('/predict')
def predict():
    # save new params to params variable
    params = session.get('new_params')
    # create a copy to pass to model later on
    params_copied = params.copy()
    # calculate BMI and save to params and params_copied
    params_copied['bmi'] = params_copied['mass'] / (params_copied['length']/100)**2
    params['bmi'] = params_copied['bmi']
    # create power transforms to use in model
    params_copied['mass_square'] = params_copied['mass']**2
    params_copied['bmi_square'] = params_copied['bmi']**2
    params_copied['exercise_sqrt'] = np.power(params_copied['exercise'], 1/2)
    # remove mass since it can't be passed to the model
    params_copied.pop('mass')
    ic(params_copied)
    # create DataFrame out of dictionary
    params_df = pd.DataFrame(params_copied, index=[0])
    # Reorder columns to match order with trained model
    params_df = params_df.reindex(columns=['genetic', 'length', 'bmi', 'exercise', 'smoking', 'alcohol', 'sugar', 'mass_square', 'bmi_square', 'exercise_sqrt'])
    ic(params_df)
    # make prediction
    prediction = model.predict(params_df)
    ic(f"Prediction output: {prediction}")
    return render_template('predict.html', params=params, prediction=prediction)

# ajax route to use in combination with JS AJAX requests
@app.route('/ajax_prediction', methods = ['POST'])
def ajax_request():
    # save new params to session params
    session_params = session.get('new_params')
    ic(session_params)
    # retrieve param name and value to use for creating a new prediction
    ajax_param_name = request.form['parameter_name']
    ajax_param_value = request.form['parameter_value']
    # update parameter
    params_copied = session_params.copy()
    params_copied[ajax_param_name] = float(ajax_param_value)
    session_params[ajax_param_name] = float(ajax_param_value)
    # save parameter in session
    session['new_params'] = session_params
    # calculate BMI
    params_copied['bmi'] = params_copied['mass'] / (params_copied['length']/100)**2
    session_params['bmi'] = params_copied['bmi']
    # calculate power transforms
    params_copied['mass_square'] = params_copied['mass']**2
    session_params['mass_square'] = params_copied['mass_square']
    params_copied['bmi_square'] = params_copied['bmi']**2
    session_params['bmi square'] = params_copied['bmi_square']
    params_copied['exercise_sqrt'] = np.power(params_copied['exercise'], 1/2)
    # remove mass
    params_copied.pop('mass')
    ic(params_copied)
    ic(session_params)
    # create DataFrame
    params_df = pd.DataFrame(params_copied, index=[0])
    # reorder columns to match order of trained model
    params_df = params_df.reindex(columns=['genetic', 'length', 'bmi', 'exercise', 'smoking', 'alcohol', 'sugar', 'mass_square', 'bmi_square', 'exercise_sqrt'])
    ic(params_df)
    # make prediction
    prediction = model.predict(params_df)
    # get values of old and new param
    new_param = session['new_params'].get(ajax_param_name)
    old_param = session['params'].get(ajax_param_name)
    # return values as JSON to ajax request
    return jsonify(prediction=round(prediction[0], 1), new_param=new_param, old_param=old_param)

if __name__ == "__main__":
    app.run()