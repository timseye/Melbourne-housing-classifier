import pandas as pd
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import joblib
import os
import uvicorn

# Create FastAPI app
app = FastAPI(title="House Price Classifier")

# Set up templates directory
templates = Jinja2Templates(directory="templates")

# Mount static files directory
os.makedirs("static", exist_ok=True)
os.makedirs("static/js", exist_ok=True)  # Ensure js directory exists
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load the model
@app.on_event("startup")
async def startup_event():
    global model, feature_names, model_loaded, median_price
    model_loaded = False
    try:
        model = joblib.load("house_price_model.joblib")
        
        # Get the feature names used during training
        # Assuming the first step in the pipeline is the preprocessor
        feature_names = {
            'numerical': model.named_steps['preprocessor'].transformers_[0][2],
            'categorical': model.named_steps['preprocessor'].transformers_[1][2]
        }
        
        # Get the median price from the original data
        try:
            data = pd.read_csv('melb_data.csv')
            median_price = data['Price'].median()
            print(f"Median price: ${median_price}")
        except Exception as e:
            print(f"Error loading median price: {e}")
            median_price = 903000.0  # Default if unable to load
            
        model_loaded = True
        print("Model loaded successfully!")
    except FileNotFoundError:
        print("Error: Model file 'house_price_model.joblib' not found.")
        print("Please run ml_model.py first to train and save the model.")
    except Exception as e:
        print(f"Error loading model: {e}")
        print("Please check if the model file is valid or retrain the model.")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # Check if test cases file exists
    test_cases_path = os.path.join("static", "js", "test_cases.js")
    js_exists = os.path.exists(test_cases_path)
    
    if not js_exists:
        print(f"Warning: Test cases file not found at {test_cases_path}")
    
    # Format median price for display
    formatted_median = f"${median_price:,.0f}" if 'median_price' in globals() else "$980,000"
        
    return templates.TemplateResponse("index.html", {
        "request": request,
        "js_loaded": js_exists,
        "median_price": formatted_median
    })

@app.post("/predict", response_class=HTMLResponse)
async def predict(
    request: Request,
    suburb: str = Form(...),
    rooms: int = Form(...),
    type: str = Form(...),
    method: str = Form(...),
    distance: float = Form(...),
    postcode: float = Form(...),
    bedroom2: float = Form(...),
    bathroom: float = Form(...),
    car: float = Form(...),
    landsize: float = Form(...),
    building_area: str = Form(""),
    year_built: str = Form(""),
    council_area: str = Form(...),
    lattitude: float = Form(...),
    longtitude: float = Form(...),
    regionname: str = Form(...),
    propertycount: float = Form(...)
):
    # Check if model is loaded
    if not model_loaded:
        error_message = {
            "error": "Model not loaded",
            "message": "The prediction model has not been loaded. Please run ml_model.py first to train and save the model."
        }
        return templates.TemplateResponse(
            "error.html", {"request": request, "error": error_message, "median_price": f"${median_price:,.0f}"}
        )
    
    # Debug log input values
    print(f"DEBUG: Received form data: Rooms={rooms}, Bedroom2={bedroom2}, Bathroom={bathroom}, Car={car}, Postcode={postcode}")
    
    # Round integer fields
    rooms_int = int(rooms) if rooms else 0
    bedroom2_int = int(bedroom2) if bedroom2 else 0
    bathroom_int = int(bathroom) if bathroom else 0
    car_int = int(car) if car else 0
    postcode_int = int(postcode) if postcode else 0
    
    # Create input DataFrame (using original values for prediction)
    input_data = {
        'Suburb': [suburb],
        'Rooms': [rooms],
        'Type': [type],
        'Method': [method],
        'Distance': [distance],
        'Postcode': [postcode],
        'Bedroom2': [bedroom2],
        'Bathroom': [bathroom],
        'Car': [car],
        'Landsize': [landsize],
        'BuildingArea': [float(building_area) if building_area and building_area.strip() else None],
        'YearBuilt': [float(year_built) if year_built and year_built.strip() else None],
        'CouncilArea': [council_area],
        'Lattitude': [lattitude],
        'Longtitude': [longtitude],
        'Regionname': [regionname],
        'Propertycount': [propertycount]
    }
    
    # Log the debug info
    print(f"DEBUG: Formatted data: Rooms={input_data['Rooms'][0]}, Bedroom2={input_data['Bedroom2'][0]}, Bathroom={input_data['Bathroom'][0]}, Car={input_data['Car'][0]}")
    
    # Create DataFrame
    df = pd.DataFrame(input_data)
    
    try:
        # Make prediction
        prediction = model.predict(df)[0]
        probability = model.predict_proba(df)[0][1]
    except Exception as e:
        error_message = {
            "error": "Prediction Error",
            "message": f"An error occurred during prediction: {str(e)}",
            "input_data": input_data
        }
        return templates.TemplateResponse(
            "error.html", {"request": request, "error": error_message}
        )
    
    # Get confidence in the predicted class (always show confidence in the predicted outcome)
    confidence = probability if prediction == 1 else 1 - probability
    
    # Create a clean display version of the input data (for template display)
    display_data = {
        'Suburb': suburb,
        'Rooms': rooms_int,
        'Type': type,
        'Method': method,
        'Distance': distance,
        'Postcode': postcode_int,
        'Bedroom2': bedroom2_int,
        'Bathroom': bathroom_int,
        'Car': car_int,
        'Landsize': landsize,
        'BuildingArea': float(building_area) if building_area and building_area.strip() else None,
        'YearBuilt': int(float(year_built)) if year_built and year_built.strip() else None,
        'CouncilArea': council_area,
        'Lattitude': lattitude,
        'Longtitude': longtitude,
        'Regionname': regionname,
        'Propertycount': propertycount
    }
    
    # Format median price
    formatted_median = f"${median_price:,.0f}" if 'median_price' in globals() else "$980,000"
    
    # Prepare result
    result = {
        "prediction": "Above median price" if prediction == 1 else "Below median price",
        "probability": f"{confidence:.2%}",  # Show confidence in the prediction
        "display_data": display_data,  # New clean format for display
        "median_price": formatted_median
    }
    
    return templates.TemplateResponse(
        "result.html", {"request": request, "result": result}
    )

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
