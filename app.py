from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_URL = "https://api.edamam.com/api/food-database/v2/parser"
APP_ID = "TU_APP_ID"
APP_KEY = "TU_APP_KEY"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        food = request.form.get('food')
        if not food:
            return render_template('index.html', error="Por favor ingresa un alimento.")
        params = {
            "ingr": food,
            "app_id": APP_ID,
            "app_key": APP_KEY
        }
        resp = requests.get(API_URL, params=params)
        if resp.status_code != 200:
            return render_template('index.html', error="Error al consultar la API.")
        data = resp.json()
        hints = data.get("hints", [])
        if not hints:
            return render_template('index.html', error="No se encontraron datos para ese alimento.")
        first = hints[0]
        food_label = first["food"]["label"]
        nutrients = first["food"]["nutrients"]
        return render_template('result.html', food=food_label, nutrients=nutrients)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
hsdjsdjgfdjfgh