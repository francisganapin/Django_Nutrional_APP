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

        #check if item is already exist
        existing_names = {item['name'] for item in data}
        if form_data['name'] in existing_names:
            print('sorry this item already exist')
            message = f'{form_data['name']} is already exist'
        else:
            print('congrats for uploading')
            
            with open(json_file_path, 'w') as f:
                json.dump(data, f, indent=4)
            
            return redirect('food_view')
        
    # If request method is GET, render the form page
    return render(request, 'add_food.html',{'message':message})


def food_remove_view(request):
    json_file_path = os.path.join('static', 'data.json')

    if request.method == 'POST':
        try:
            item_name = request.POST.get('item_name')

            if not item_name:
                return HttpResponseBadRequest('Item name not provided')

            # Read data from data.json
            with open(json_file_path, 'r') as f:
                data = json.load(f)
            
            # Find the item to delete based on item_name
            updated_data = [item for item in data if item.get('name') != item_name]

            # Check if item_name was found and deleted
            if len(updated_data) == len(data):
                # Item was not found and not deleted
                return JsonResponse({'message': f'Item "{item_name}" not found in the list.'})

            # Write updated data back to data.json
            with open(json_file_path, 'w') as f:
                json.dump(updated_data, f, indent=4)

            # Return success message
            return JsonResponse({'message': f'Item "{item_name}" deleted successfully'})

        except Exception as e:
            return HttpResponseBadRequest(f'Error deleting item: {str(e)}')

    else:
        # If not a POST request, handle the search and filter form
        try:
            # Check if data.json file exists
            if not os.path.exists(json_file_path):
                raise FileNotFoundError('Data file not found')

            # Read data from data.json
            with open(json_file_path, 'r') as f:
                data = json.load(f)

            # Handle search and filter functionality
            search_input = request.GET.get('search')
            category_input = request.GET.get('category')

            if search_input:
                # Perform search based on search_input (example: filter data based on search criteria)
                data = [item for item in data if search_input.lower() in item['name'].lower()]

            # Render the HTML template with the filtered data
            return render(request, 'index3.html', {'data': data, 'search_input': search_input, 'category_input': category_input})

        except FileNotFoundError:
            return HttpResponseBadRequest('Data file not found')
        except json.JSONDecodeError as e:
            return HttpResponseBadRequest(f'Error decoding JSON: {str(e)}')
        except Exception as e:
            return HttpResponseBadRequest(f'Error: {str(e)}')

     



def food_delete_view(request):

    message = ''
    if request.method == 'POST':
        form_data = {
            'name': request.POST.get('name'),
          
            # Add other fields here based on your form
        }
        
        json_file_path = os.path.join('static', 'data.json')

        if os.path.exists(json_file_path):
            with open(json_file_path, 'r') as f:
                        data = json.load(f)
        else:
                    data = []

        #check if item is already exist
        existing_names = {item['name'] for item in data}
        if form_data['name'] not in existing_names:
            print('sorry this item  does not exist')
            message = f'{form_data['name']} is not  exist'
        else:
            print('congrats for deleting')
            #check if item exist  so wecan delete
            data =[item for item in data if item['name'] != form_data['name']]



            with open(json_file_path, 'w') as f:
                json.dump(data, f, indent=4)
            
            return redirect('food_view')
        
    # If request method is GET, render the form page
    return render(request, 'delete_food.html',{'message':message})