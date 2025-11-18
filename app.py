from flask import Flask, render_template, request
import requests

app = Flask(__name__)

app.secret_key = 'tu clave'
API_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"
API_KEY = "ZbbRfULye2wWXsAx49Q9ZwhmsDWqAztO7MfBi4Hu"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        food = request.form.get('food')
        if not food:
            return render_template('index.html', error="Por favor ingresa un alimento.")

        params = {
            "query": food,
            "api_key": API_KEY
        }

        resp = requests.get(API_URL, params=params)

        if resp.status_code != 200:
            return render_template('index.html', error="Error al consultar la API.")

        data = resp.json()
        foods = data.get("foods", [])

        if not foods:
            return render_template('index.html', error="No se encontraron datos para ese alimento.")

        first = foods[0]
        food_label = first.get("description", "Sin nombre")

        nutrients = {n["nutrientName"]: n["value"] for n in first.get("foodNutrients", [])}

        return render_template('resultados.html', food=food_label, nutrients=nutrients)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
