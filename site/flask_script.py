from flask import Flask, render_template, redirect, url_for, flash
from sklearn.externals import joblib

app = Flask(__name__)
app.secret_key = 'some_secret'

template_path = 'index.html'


@app.route("/")
@app.route('/index')
def index():
    return render_template(template_path)


@app.route("/accupancy", methods=['GET', 'POST'])
def move_forward():
    # oom = joblib.load('model_occ_measure_trainingroom.pkl')
    # day = 13
    # day_of_week = 5
    # hour = 0
    # minute = 0
    # co2 = 422
    # temperature = 20
    # humidity = 46
    # outputFrom_model = model.predict(pd.DataFrame([[day, day_of_week, hour, minute, co2, temperature, humidity]],
    #                                               columns=['day', 'day_of_week', 'hour', 'minute', 'co2', 'temperature',
    #                                                        'humidity']))

    print('sdafsd')
    return render_template('sososos.html', message=1)


if __name__ == "__main__":
    app.run()
