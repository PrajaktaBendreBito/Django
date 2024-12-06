from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

# Simple function-based view for home page
def home(request):
    return render(request, 'home.html')

# Function to handle form submission
def submit_form(request):
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        
        try:
            # Process the data
            # Add your business logic here
            messages.success(request, 'Form submitted successfully!')
            return redirect('home')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return redirect('submit_form')
    
    return render(request, 'form.html')

# Function to display data
def display_data(request):
    # Add your data retrieval logic here
    data = {
        'items': ['item1', 'item2', 'item3']
    }
    return render(request, 'display.html', context=data)

# API-like function to return JSON
def get_api_data(request):
    from django.http import JsonResponse
    
    data = {
        'status': 'success',
        'data': {
            'message': 'Hello from API',
            'timestamp': datetime.now().isoformat()
        }
    }
    return JsonResponse(data)

# Error handling function
def handler404(request, exception):
    return render(request, '404.html', status=404)