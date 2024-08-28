from django.shortcuts import render,redirect
import json
import os
from pathlib import Path
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from nutrional_json.settings import BASE_DIR



from django.core.paginator import Paginator

def food_view(request):
    # Construct the full file path within the static directory
    json_file_path = os.path.join('static', 'data.json')

    # Ensure the file exists before attempting to read it
    if not os.path.exists(json_file_path):
        raise FileNotFoundError(f"File not found: {json_file_path}")

    # Read the JSON file
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Create a Paginator object with your data
    # Get the current page number from the request
    # Pass the paginated data to the template
    return render(request, 'list_food.html', {'data': data})

def success_page(request):
    return render(request, 'success.html')



def food_add_view(request):

    message = ''
    if request.method == 'POST':
        form_data = {
            'name': request.POST.get('name'),
            'measure': request.POST.get('measure'),
            'grams': request.POST.get('grams'),
            'calories': request.POST.get('calories'),
            'protein': request.POST.get('protein'),
            'fat': request.POST.get('fat'),
            'saturated_fat': request.POST.get('saturated_fat'),
            'fiber': request.POST.get('fiber'),
            'carbohydrates': request.POST.get('carbohydrates'),
            'category': request.POST.get('category'),
            # Add other fields here based on your form
        }
        
        json_file_path = os.path.join('static', 'data.json')

        if os.path.exists(json_file_path):
            with open(json_file_path, 'r') as f:
                        data = json.load(f)
        else:
                    data = []

          # Check if item already exists
        existing_names = {item['name'] for item in data}
        if form_data['name'] in existing_names:
            print('Sorry, this item already exists.')
            message = f"{form_data['name']} already exists."
        else:
            print('congrats for uploading')
            
            with open(json_file_path, 'w') as f:
                json.dump(data, f, indent=4)
            
            return redirect('food_view')
        
    # If request method is GET, render the form page
    return render(request, 'add_food.html',{'message':message})





def food_delete_view(request):
    message = ''
    if request.method == 'POST':
        form_data = {
            'name': request.POST.get('name'),

        }
        
        json_file_path = os.path.join('static', 'data.json')

        if os.path.exists(json_file_path):
            with open(json_file_path, 'r') as f:
                data = json.load(f)
        else:
            data = []

        existing_names = {item['name'] for item in data}
        if form_data['name'] not in existing_names:
            print('Sorry, this item does not exist.')
            message = f"{form_data['name']} does not exist."
        else:
            print('Congrats on deleting.')

            data = [item for item in data if item['name'] != form_data['name']]

            with open(json_file_path, 'w') as f:
                json.dump(data, f, indent=4)

            return redirect('food_view')

    return render(request, 'delete_food.html', {'message': message})


def bmiCalculator_views(request):
    message = ''
    if request.method == 'POST':
        
        the_weight    = int(request.POST.get('weight'))
        the_height    = int(request.POST.get('height'))
        
        the_BMI = the_weight / (the_height/100)**2

        if the_BMI <= 18.15:
            message = f'weight your BMI:{the_BMI}'
        elif the_BMI <= 24.9:
            message = f'healthy your BMI:{the_BMI}'
        elif the_BMI <= 29.9:
             message = f'weight your BMI:{the_BMI}'
        else:
             message = f'Go diet and Gym your BMI:{the_BMI}'

    return render(request,'calculate_ibm.html',{'message':message})