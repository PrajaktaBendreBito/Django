from django import forms

def validate_name(value):
    if len(value) < 2:
        raise forms.ValidationError("Name must be at least 2 characters long")
    return value

# Form processing functions
def process_form_data(form_data):
    """
    Process the form data
    """
    cleaned_data = {}
    errors = {}
    
    # Name validation
    name = form_data.get('name', '').strip()
    if not name:
        errors['name'] = 'Name is required'
    elif len(name) < 2:
        errors['name'] = 'Name must be at least 2 characters long'
    else:
        cleaned_data['name'] = name
    
    # Email validation
    email = form_data.get('email', '').strip()
    if not email:
        errors['email'] = 'Email is required'
    elif '@' not in email:
        errors['email'] = 'Invalid email format'
    else:
        cleaned_data['email'] = email
    
    return cleaned_data, errors

def save_form_data(cleaned_data):
    """
    Save the form data (example function)
    """
    try:
        # Add your database saving logic here
        # For example:
        # new_entry = YourModel.objects.create(**cleaned_data)
        return True, "Data saved successfully"
    except Exception as e:
        return False, str(e)

# Form data validation function
def validate_form_data(data):
    """
    Validate form data and return bool and error message
    """
    required_fields = ['name', 'email']
    
    for field in required_fields:
        if field not in data or not data[field]:
            return False, f"{field} is required"
    
    return True, "Validation successful"