// Test cases for Melbourne Housing Price Classifier
const testCases = {
    "high_value_toorak": {
        "suburb": "Toorak",
        "rooms": 5,
        "type": "h",
        "method": "S",
        "distance": 5.0,
        "postcode": 3142,
        "bedroom2": 5.0,
        "bathroom": 3.0,
        "car": 2.0,
        "landsize": 800.0,
        "building_area": 300.0,
        "year_built": 2010,
        "council_area": "Stonnington",
        "lattitude": -37.8410,
        "longtitude": 145.0180,
        "regionname": "Southern Metropolitan",
        "propertycount": 4380.0
    },
    "modest_outer_suburb": {
        "suburb": "Craigieburn",
        "rooms": 3,
        "type": "h",
        "method": "S",
        "distance": 25.0,
        "postcode": 3064,
        "bedroom2": 3.0,
        "bathroom": 1.0,
        "car": 1.0,
        "landsize": 400.0,
        "building_area": 150.0,
        "year_built": 2000,
        "council_area": "Hume",
        "lattitude": -37.6000,
        "longtitude": 144.9400,
        "regionname": "Northern Metropolitan",
        "propertycount": 7500.0
    },
    "small_apartment_near_city": {
        "suburb": "Richmond",
        "rooms": 2,
        "type": "u",
        "method": "PI",
        "distance": 3.0,
        "postcode": 3121,
        "bedroom2": 2.0,
        "bathroom": 1.0,
        "car": 1.0,
        "landsize": 0.0,
        "building_area": 75.0,
        "year_built": 2005,
        "council_area": "Yarra",
        "lattitude": -37.8230,
        "longtitude": 144.9980,
        "regionname": "Northern Metropolitan",
        "propertycount": 5700.0
    },
    "older_mid_range_suburb": {
        "suburb": "Preston",
        "rooms": 3,
        "type": "h",
        "method": "SP",
        "distance": 10.0,
        "postcode": 3072,
        "bedroom2": 3.0,
        "bathroom": 1.0,
        "car": 1.0,
        "landsize": 500.0,
        "building_area": 120.0,
        "year_built": 1950,
        "council_area": "Darebin",
        "lattitude": -37.7400,
        "longtitude": 145.0000,
        "regionname": "Northern Metropolitan",
        "propertycount": 9500.0
    },
    "large_land_old_building": {
        "suburb": "Reservoir",
        "rooms": 3,
        "type": "h",
        "method": "S",
        "distance": 12.0,
        "postcode": 3073,
        "bedroom2": 3.0,
        "bathroom": 1.0,
        "car": 2.0,
        "landsize": 700.0,
        "building_area": 100.0,
        "year_built": 1960,
        "council_area": "Darebin",
        "lattitude": -37.7200,
        "longtitude": 145.0200,
        "regionname": "Northern Metropolitan",
        "propertycount": 11000.0
    },
    "new_townhouse": {
        "suburb": "Brunswick",
        "rooms": 3,
        "type": "t",
        "method": "VB",
        "distance": 6.0,
        "postcode": 3056,
        "bedroom2": 3.0,
        "bathroom": 2.0,
        "car": 1.0,
        "landsize": 150.0,
        "building_area": 140.0,
        "year_built": 2018,
        "council_area": "Moreland",
        "lattitude": -37.7700,
        "longtitude": 144.9600,
        "regionname": "Northern Metropolitan",
        "propertycount": 8000.0
    },
    "missing_data_example": {
        "suburb": "St Kilda",
        "rooms": 2,
        "type": "u",
        "method": "S",
        "distance": 6.0,
        "postcode": 3182,
        "bedroom2": 2.0,
        "bathroom": 1.0,
        "car": 1.0,
        "landsize": 0.0,
        "building_area": "",  // Missing data
        "year_built": "",  // Missing data
        "council_area": "Port Phillip",
        "lattitude": -37.8600,
        "longtitude": 144.9800,
        "regionname": "Southern Metropolitan",
        "propertycount": 12000.0
    },
    "very_large_property": {
        "suburb": "Brighton",
        "rooms": 8,
        "type": "h",
        "method": "S",
        "distance": 11.0,
        "postcode": 3186,
        "bedroom2": 7.0,
        "bathroom": 4.0,
        "car": 3.0,
        "landsize": 1200.0,
        "building_area": 450.0,
        "year_built": 2015,
        "council_area": "Bayside",
        "lattitude": -37.9100,
        "longtitude": 145.0000,
        "regionname": "Southern Metropolitan",
        "propertycount": 6500.0
    },
    "very_small_property": {
        "suburb": "Carlton",
        "rooms": 1,
        "type": "u",
        "method": "S",
        "distance": 1.5,
        "postcode": 3053,
        "bedroom2": 1.0,
        "bathroom": 1.0,
        "car": 0.0,
        "landsize": 0.0,
        "building_area": 35.0,
        "year_built": 1970,
        "council_area": "Melbourne",
        "lattitude": -37.8000,
        "longtitude": 144.9700,
        "regionname": "Northern Metropolitan",
        "propertycount": 4500.0
    }
};

// Function to populate form with test case data
function loadTestCase() {
    const selectElement = document.getElementById('testCaseSelector');
    const selectedCase = selectElement.value;
    
    if (selectedCase && testCases[selectedCase]) {
        const data = testCases[selectedCase];
        
        // Populate form fields
        document.getElementById('suburb').value = data.suburb;
        document.getElementById('rooms').value = data.rooms;
        document.getElementById('type').value = data.type;
        document.getElementById('method').value = data.method;
        document.getElementById('distance').value = data.distance;
        document.getElementById('postcode').value = data.postcode;
        document.getElementById('bedroom2').value = data.bedroom2;
        document.getElementById('bathroom').value = data.bathroom;
        document.getElementById('car').value = data.car;
        document.getElementById('landsize').value = data.landsize;
        document.getElementById('building_area').value = data.building_area;
        document.getElementById('year_built').value = data.year_built;
        document.getElementById('council_area').value = data.council_area;
        document.getElementById('lattitude').value = data.lattitude;
        document.getElementById('longtitude').value = data.longtitude;
        document.getElementById('regionname').value = data.regionname;
        document.getElementById('propertycount').value = data.propertycount;
    }
}

// Initialize the form with test case dropdown
function initTestCases() {
    const selectElement = document.getElementById('testCaseSelector');
    
    if (selectElement) {
        // Add default option
        const defaultOption = document.createElement('option');
        defaultOption.value = "";
        defaultOption.textContent = "-- Select a test case --";
        selectElement.appendChild(defaultOption);
        
        // Add test cases
        for (const [key, value] of Object.entries(testCases)) {
            const option = document.createElement('option');
            option.value = key;
            option.textContent = `${key} (${value.rooms} rooms in ${value.suburb})`;
            selectElement.appendChild(option);
        }
        
        // Add event listener
        selectElement.addEventListener('change', loadTestCase);
    }
}

// Initialize when the document is loaded
document.addEventListener('DOMContentLoaded', initTestCases);
