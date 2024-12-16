import pandas as pd

# Load the CSV file into a Pandas DataFrame
file_path = 'laptops.csv'
laptops_data = pd.read_csv(file_path)

# Function to get user preferences
def get_user_preferences():
    # Asking user for their preferences
    min_budget = float(input("Enter minimum budget: "))
    max_budget = float(input("Enter maximum budget: "))
    use_case = input("Enter use case (e.g., Gaming, Business, Home/Everyday use): ")
    os_preference = input("Enter preferred operating system (e.g., Windows, MacOS, DOS): ")
    min_ram = input("Enter minimum RAM (e.g., 4 GB, 8 GB, 16 GB): ")
    storage_type = input("Preferred storage type (SSD, HDD, or leave blank if no preference): ")
    min_display_size = input("Enter minimum screen size in inches (optional): ")
    brand_preference = input("Preferred laptop brand (optional): ")
    
    return {
        "min_budget": min_budget,
        "max_budget": max_budget,
        "use_case": use_case.lower(),
        "os_preference": os_preference.lower(),
        "min_ram": min_ram.lower(),
        "storage_type": storage_type.lower(),
        "min_display_size": min_display_size,
        "brand_preference": brand_preference.lower()
    }

# Function to filter laptops based on user preferences
def filter_laptops(data, preferences):
    filtered_data = data[
        (data['price'].astype(float) >= preferences['min_budget']) & 
        (data['price'].astype(float) <= preferences['max_budget']) &
        (data['usecases'].str.lower().str.contains(preferences['use_case'])) &
        (data['os'].str.lower().str.contains(preferences['os_preference'])) &
        (data['ram'].str.lower().str.contains(preferences['min_ram']))
    ]
    
    # If storage type is provided
    if preferences['storage_type']:
        filtered_data = filtered_data[filtered_data['storage'].str.lower().str.contains(preferences['storage_type'])]
    
    # If display size is provided
    if preferences['min_display_size']:
        filtered_data = filtered_data[filtered_data['display'] >= float(preferences['min_display_size'])]
    
    # If brand preference is provided
    if preferences['brand_preference']:
        filtered_data = filtered_data[filtered_data['laptop_brand'].str.lower().str.contains(preferences['brand_preference'])]
    
    return filtered_data

# Function to display the results
def display_results(filtered_data):
    if filtered_data.empty:
        print("No laptops match your criteria.")
    else:
        print(f"Found {len(filtered_data)} matching laptops:\n")
        for index, row in filtered_data.iterrows():
            print(f"Laptop ID: {row['laptop_id']}")
            print(f"Name: {row['name']}")
            print(f"Price: {row['price']}")
            print(f"Processor: {row['processor']}")
            print(f"RAM: {row['ram']}")
            print(f"Storage: {row['storage']}")
            print(f"OS: {row['os']}")
            print(f"Rating: {row['rating']} (based on {row['no_of_ratings']} ratings)")
            print(f"Use case: {row['usecases']}")
            print(f"Image Link: {row['img_link']}")
            print("-" * 40)

# Main function to run the expert system
def laptop_recommendation_system():
    preferences = get_user_preferences()
    filtered_laptops = filter_laptops(laptops_data, preferences)
    display_results(filtered_laptops)

# Run the recommendation system
laptop_recommendation_system()
