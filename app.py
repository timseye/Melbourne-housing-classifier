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
    global model, feature_names
    model = joblib.load("house_price_model.joblib")
    
    # Get the feature names used during training
    # Assuming the first step in the pipeline is the preprocessor
    feature_names = {
        'numerical': model.named_steps['preprocessor'].transformers_[0][2],
        'categorical': model.named_steps['preprocessor'].transformers_[1][2]
    }

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

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
    building_area: float = Form(None),
    year_built: float = Form(None),
    council_area: str = Form(...),
    lattitude: float = Form(...),
    longtitude: float = Form(...),
    regionname: str = Form(...),
    propertycount: float = Form(...)
):
    # Create input DataFrame
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
        'BuildingArea': [building_area],
        'YearBuilt': [year_built],
        'CouncilArea': [council_area],
        'Lattitude': [lattitude],
        'Longtitude': [longtitude],
        'Regionname': [regionname],
        'Propertycount': [propertycount]
    }
    
    # Create DataFrame
    df = pd.DataFrame(input_data)
      # Make prediction
    prediction = model.predict(df)[0]
    probability = model.predict_proba(df)[0][1]
    
    # Get confidence in the predicted class (always show confidence in the predicted outcome)
    confidence = probability if prediction == 1 else 1 - probability
    
    # Prepare result
    result = {
        "prediction": "Above median price" if prediction == 1 else "Below median price",
        "probability": f"{confidence:.2%}",  # Show confidence in the prediction
        "input_data": input_data
    }
    
    return templates.TemplateResponse(
        "result.html", {"request": request, "result": result}
    )

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
