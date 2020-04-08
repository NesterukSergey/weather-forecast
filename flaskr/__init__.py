import os
from flask import Flask, render_template, jsonify, request
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

from weather.forecast import *
from weather.recommendation import *


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    SECRET_KEY = os.urandom(32)
    app.config['SECRET_KEY'] = SECRET_KEY

    class CityForm(FlaskForm):
        city = StringField('city', validators=[DataRequired()])

    @app.route('/', methods=['POST', 'GET'])
    @app.route('/weather-forecast')
    def main():
        form = CityForm()
        return render_template('base.html', form=form)

    @app.route('/forecast', methods=['POST'])
    def forecast():
        city = request.form['city']
        df = get_daily_forecast(city)

        if df['status'] == 'ok':
            recom = get_recom(df)
            return jsonify({
                'text': city,
                'forecast': df,
                'recom': recom,
                'status': df['status']
            })

        return jsonify({
            'text': city,
            'status': df['status']
        })

    return app
