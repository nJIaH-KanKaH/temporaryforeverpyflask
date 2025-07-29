from flask import Flask, request, jsonify
import json
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
    
def load_costs():
    with open('costs.json', 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route('/options', methods=['GET'])
def get_options():
    return jsonify(load_costs())

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    num_people = data.get('num_people', 1)
    selected = data.get('selected', {})
    costs = load_costs()
    total = 0

    # Add base cost per person
    base_cost = costs.get('base_cost', 0)
    total += base_cost * num_people

    # Build lookup tables for excursions and food by day
    excursions_by_day = {}
    food_by_day = {}
    for day in costs.get('days', []):
        # Excursions: map day_id -> {exc_id: exc_obj}
        if day.get('excursions'):
            excursions_by_day[day['id']] = {exc['id']: exc for exc in day['excursions']}
        # Food: map day_id -> {food_name: food_obj}
        if day.get('food'):
            food_by_day[day['id']] = {f['name']: f for f in day['food']}

    # Add selected excursions (only those not included), checking by day and id
    for day_id, exc_ids in selected.get('excursions', {}).items():
        for exc_id in exc_ids:
            exc = excursions_by_day.get(day_id, {}).get(exc_id)
            if exc and not exc.get('included', False):
                total += exc['cost_eur'] * num_people

    # Add selected food
    for day_id, food_names in selected.get('food', {}).items():
        for food_name in food_names:
            food_obj = food_by_day.get(day_id, {}).get(food_name)
            if food_obj:
                total += food_obj['cost_eur'] * num_people

    return jsonify({'total_cost_eur': total})

if __name__ == '__main__':
    app.run(debug=True, port=5051)