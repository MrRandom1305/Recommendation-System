from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load the CSV file into a DataFrame
laptops_data = pd.read_csv('C:\\Users\\Parth  Deo\\Downloads\\reccomendation system\\datasets\\laptops.csv')


# Function to filter laptops based on user input
def filter_laptops(preferences):
    filtered_data = laptops_data[
        (laptops_data['price'].astype(float) >= preferences['min_budget']) & 
        (laptops_data['price'].astype(float) <= preferences['max_budget']) &
        (laptops_data['usecases'].str.lower().str.contains(preferences['use_case'])) &
        (laptops_data['os'].str.lower().str.contains(preferences['os_preference'])) &
        (laptops_data['ram'].str.lower().str.contains(preferences['min_ram']))
    ]
    
    if preferences['storage_type']:
        filtered_data = filtered_data[filtered_data['storage'].str.lower().str.contains(preferences['storage_type'])]
    
    if preferences['min_display_size']:
        filtered_data = filtered_data[filtered_data['display'] >= float(preferences['min_display_size'])]
    
    if preferences['brand_preference']:
        filtered_data = filtered_data[filtered_data['laptop_brand'].str.lower().str.contains(preferences['brand_preference'])]

    return filtered_data

@app.route('/')
def home():
    print("Home route accessed")  # Debugging output to check if the route is hit
    try:
        return render_template('index.html')  # Render the template
    except Exception as e:
        print(f"Error: {e}")  # Catch and print any template errors
        return "Error loading template"

@app.route('/recommend', methods=['POST'])
def recommend():
    # Get user preferences from the form
    preferences = {
        'min_budget': float(request.form['min_budget']),
        'max_budget': float(request.form['max_budget']),
        'use_case': request.form['use_case'].lower(),
        'os_preference': request.form['os_preference'].lower(),
        'min_ram': request.form['min_ram'].lower(),
        'storage_type': request.form.get('storage_type', '').lower(),
        'min_display_size': request.form.get('min_display_size', ''),
        'brand_preference': request.form.get('brand_preference', '').lower()
    }

    # Filter laptops based on preferences
    filtered_laptops = filter_laptops(preferences)
    
    # Convert filtered data to a list of dictionaries for rendering
    laptop_list = filtered_laptops.to_dict(orient='records')

    return render_template('results.html', laptops=laptop_list)

if __name__ == '__main__':
    if app.debug:
        webbrowser.open('http://127.0.0.1:5000/', new=2)
    app.run(debug=True,port=5001)

