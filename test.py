import requests
import json
import os
import sys
import pandas as pd

# Define test cases
test_cases = {
    "high_value_toorak": {
        "suburb": "Toorak",
        "rooms": 5,
        "type": "h",
        "method": "S",
        "distance": 5.0,
        "postcode": 3142,
        "bedroom2": 5,
        "bathroom": 3,
        "car": 2,
        "landsize": 800,
        "building_area": 300,
        "year_built": 2010,
        "council_area": "Stonnington",
        "lattitude": -37.8410,
        "longtitude": 145.0180,
        "regionname": "Southern Metropolitan",
        "propertycount": 4380
    },
    "modest_outer_suburb": {
        "suburb": "Craigieburn",
        "rooms": 3,
        "type": "h",
        "method": "S",
        "distance": 25.0,
        "postcode": 3064,
        "bedroom2": 3,
        "bathroom": 1,
        "car": 1,
        "landsize": 400,
        "building_area": 150,
        "year_built": 2000,
        "council_area": "Hume",
        "lattitude": -37.6000,
        "longtitude": 144.9400,
        "regionname": "Northern Metropolitan",
        "propertycount": 7500
    },
    "small_apartment_near_city": {
        "suburb": "Richmond",
        "rooms": 2,
        "type": "u",
        "method": "PI",
        "distance": 3.0,
        "postcode": 3121,
        "bedroom2": 2,
        "bathroom": 1,
        "car": 1,
        "landsize": 0,
        "building_area": 75,
        "year_built": 2005,
        "council_area": "Yarra",
        "lattitude": -37.8230,
        "longtitude": 144.9980,
        "regionname": "Northern Metropolitan",
        "propertycount": 5700
    },
    "older_mid_range_suburb": {
        "suburb": "Preston",
        "rooms": 3,
        "type": "h",
        "method": "SP",
        "distance": 10.0,
        "postcode": 3072,
        "bedroom2": 3,
        "bathroom": 1,
        "car": 1,
        "landsize": 500,
        "building_area": 120,
        "year_built": 1950,
        "council_area": "Darebin",
        "lattitude": -37.7400,
        "longtitude": 145.0000,
        "regionname": "Northern Metropolitan",
        "propertycount": 9500
    },
    "large_land_old_building": {
        "suburb": "Reservoir",
        "rooms": 3,
        "type": "h",
        "method": "S",
        "distance": 12.0,
        "postcode": 3073,
        "bedroom2": 3,
        "bathroom": 1,
        "car": 2,
        "landsize": 700,
        "building_area": 100,
        "year_built": 1960,
        "council_area": "Darebin",
        "lattitude": -37.7200,
        "longtitude": 145.0200,
        "regionname": "Northern Metropolitan",
        "propertycount": 11000
    },
    "new_townhouse": {
        "suburb": "Brunswick",
        "rooms": 3,
        "type": "t",
        "method": "VB",
        "distance": 6.0,
        "postcode": 3056,
        "bedroom2": 3,
        "bathroom": 2,
        "car": 1,
        "landsize": 150,
        "building_area": 140,
        "year_built": 2018,
        "council_area": "Moreland",
        "lattitude": -37.7700,
        "longtitude": 144.9600,
        "regionname": "Northern Metropolitan",
        "propertycount": 8000
    },
    "missing_data_example": {
        "suburb": "St Kilda",
        "rooms": 2,
        "type": "u",
        "method": "S",
        "distance": 6.0,
        "postcode": 3182,
        "bedroom2": 2,
        "bathroom": 1,
        "car": 1,
        "landsize": 0,
        "building_area": None,  # Missing data
        "year_built": None,  # Missing data
        "council_area": "Port Phillip",
        "lattitude": -37.8600,
        "longtitude": 144.9800,
        "regionname": "Southern Metropolitan",
        "propertycount": 12000
    },
    "very_large_property": {
        "suburb": "Brighton",
        "rooms": 8,
        "type": "h",
        "method": "S",
        "distance": 11.0,
        "postcode": 3186,
        "bedroom2": 7,
        "bathroom": 4,
        "car": 3,
        "landsize": 1200,
        "building_area": 450,
        "year_built": 2015,
        "council_area": "Bayside",
        "lattitude": -37.9100,
        "longtitude": 145.0000,
        "regionname": "Southern Metropolitan",
        "propertycount": 6500
    },
    "very_small_property": {
        "suburb": "Carlton",
        "rooms": 1,
        "type": "u",
        "method": "S",
        "distance": 1.5,
        "postcode": 3053,
        "bedroom2": 1,
        "bathroom": 1,
        "car": 0,
        "landsize": 0,
        "building_area": 35,
        "year_built": 1970,
        "council_area": "Melbourne",
        "lattitude": -37.8000,
        "longtitude": 144.9700,
        "regionname": "Northern Metropolitan",
        "propertycount": 4500
    }
}

def test_prediction(test_case_name):
    """Make prediction with a specific test case"""
    if test_case_name not in test_cases:
        print(f"Test case '{test_case_name}' not found. Available test cases: {list(test_cases.keys())}")
        return
    
    test_data = test_cases[test_case_name]
    print(f"\nTesting with case: {test_case_name}")
    print(json.dumps(test_data, indent=2))
      # Use the model to make a prediction
    model_path = 'house_price_model.joblib'
    if os.path.exists(model_path):
        import joblib
        
        # Load the model
        model = joblib.load(model_path)
        
        # Handle None values and ensure correct column names
        test_data_adjusted = {
            # Ensure column names match exactly what was used in training
            # Convert first letters to uppercase where needed
            'Suburb': test_data['suburb'],
            'Rooms': test_data['rooms'],
            'Type': test_data['type'],
            'Method': test_data['method'],
            'Distance': test_data['distance'],
            'Postcode': test_data['postcode'],
            'Bedroom2': test_data['bedroom2'],
            'Bathroom': test_data['bathroom'],
            'Car': test_data['car'],
            'Landsize': test_data['landsize'],
            'BuildingArea': test_data['building_area'],
            'YearBuilt': test_data['year_built'],
            'CouncilArea': test_data['council_area'],
            'Lattitude': test_data['lattitude'],
            'Longtitude': test_data['longtitude'],
            'Regionname': test_data['regionname'],
            'Propertycount': test_data['propertycount']
        }
        
        df = pd.DataFrame([test_data_adjusted])
        
        # Make prediction
        prediction = model.predict(df)[0]
        confidence = model.predict_proba(df)[0][1]
        confidence = confidence if prediction == 1 else 1 - confidence
        
        result = "Above median price" if prediction == 1 else "Below median price"
        print(f"\nPrediction: {result}")
        print(f"Confidence: {confidence:.2%}")
    else:
        print(f"Model file '{model_path}' not found. Please train the model first.")

def list_test_cases():
    """List all available test cases"""
    print("\nAvailable test cases:")
    for i, (name, data) in enumerate(test_cases.items(), 1):
        print(f"{i}. {name}: {data['rooms']} rooms in {data['suburb']}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_case = sys.argv[1]
        test_prediction(test_case)
    else:
        print("Melbourne Housing Price Classifier - Test Cases")
        list_test_cases()
        print("\nUsage: python test.py [test_case_name]")
        print("Example: python test.py high_value_toorak")
