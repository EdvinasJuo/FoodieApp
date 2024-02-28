from django.shortcuts import render
import requests
import json
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def home(request):
    if request.method == 'POST':
        query = request.POST['query']
        api_url = 'https://api.api-ninjas.com/v1/nutrition?query='
        api_request = requests.get(api_url + query, headers={'X-Api-Key': 'MarmH/S8YZHOx2B+Fu01pw==SQCUSi3nuyIQZtLZ'})

        try:
            api = json.loads(api_request.content)  # uzloadinamas json su content

            calories_to_burn = api[0].get('calories', 0)
            # vidutinis zmogaus svoris (kg)
            user_weight_kg = 80

            # skaiciuojamas jogging time
            jogging_rate = 7.0
            jogging_time = round(calories_to_burn / (jogging_rate * user_weight_kg) * 60, 2)

            # skaiciuojamas yoga time
            yoga_rate = 3.0
            yoga_time = round(calories_to_burn / (yoga_rate * user_weight_kg) * 60, 2)

            # skaiciuojamas gym time
            gym_rate = 	7.0
            gym_workout_time = round(calories_to_burn / (gym_rate * user_weight_kg) * 60, 2)

            #skaiciuojamas swimming time
            swimming_rate = 8.3
            swimming_time = round(calories_to_burn / (swimming_rate * user_weight_kg) * 60, 2)

            nutritional_values = {
                'Carbohydrates': api[0].get('carbohydrates_total_g', 0),
                'Cholesterol': api[0].get('cholesterol_mg', 0),
                'Saturated Fat': api[0].get('fat_saturated_g', 0),
                'Total Fat': api[0].get('fat_total_g', 0),
                'Fiber Content': api[0].get('fiber_g', 0),
                'Potassium': api[0].get('potassium_mg', 0),
                'Protein': api[0].get('protein_g', 0),
                'Sodium': api[0].get('sodium_mg', 0),
                'Sugar': api[0].get('sugar_g', 0),
            }

            # Plotting the bar chart design
            plt.figure(figsize=(12, 8))
            bars = plt.bar(nutritional_values.keys(), nutritional_values.values(),
                           color=['#ffba08', '#f48c06', '#d00000', 'purple', 'orange', 'brown', 'pink', 'gray', 'cyan'])

            # Adding data labels
            for bar in bars:
                yvalue = bar.get_height()
                plt.text(bar.get_x() + bar.get_width() / 2, yvalue, round(yvalue, 2), ha='center', va='bottom')

            # titles and labes
            plt.title('Nutritional Values for ' + api[0].get('name', 'Food'))
            plt.xlabel('Nutritional Values')
            plt.ylabel('Amount (g)')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()

            # saving the chart as a bytesIO object
            chart_buffer = BytesIO()
            plt.savefig(chart_buffer, format='png')
            chart_buffer.seek(0)
            plt.close()

            # converting the chart to base64 encoded string
            chart_base64 = base64.b64encode(chart_buffer.read()).decode('utf-8')

            context = {
                'api': api,
                'jogging_time': jogging_time,
                'yoga_time': yoga_time,
                'gym_workout_time':gym_workout_time,
                'swimming_time': swimming_time,
                'chart_base64': chart_base64
            }

        except Exception as e:
            api = "There was an error..."
            print(e)

            # nustatomos default reiksmes
            jogging_time = 0
            power_yoga_time = 0
            gym_workout_time = 0
            swimming_time = 0

            context = {
                'api': api,
                'jogging_time': jogging_time,
                'power_yoga_time': power_yoga_time,
                'gym_workout_time': gym_workout_time,
                'swimming_time': swimming_time,
            }

        return render(request, 'home.html', context=context)
    else:
        return render(request, 'home.html', {'query': 'Enter a valid query'})