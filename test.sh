#!/bin/bash
# Test script for Melbourne Housing Price Classifier

# List all test cases
echo "Running all test cases..."
python test.py

# Test high-value property in Toorak
echo -e "\n\nRunning test case: high_value_toorak"
python test.py high_value_toorak

# Test modest property in outer suburb
echo -e "\n\nRunning test case: modest_outer_suburb"
python test.py modest_outer_suburb

# Test small apartment near city
echo -e "\n\nRunning test case: small_apartment_near_city"
python test.py small_apartment_near_city

# Test older property in mid-range suburb
echo -e "\n\nRunning test case: older_mid_range_suburb"
python test.py older_mid_range_suburb

# Test property with large land and old building
echo -e "\n\nRunning test case: large_land_old_building"
python test.py large_land_old_building

# Test new townhouse
echo -e "\n\nRunning test case: new_townhouse"
python test.py new_townhouse

# Test with missing data
echo -e "\n\nRunning test case: missing_data_example"
python test.py missing_data_example

# Test very large property
echo -e "\n\nRunning test case: very_large_property"
python test.py very_large_property

# Test very small property
echo -e "\n\nRunning test case: very_small_property"
python test.py very_small_property

echo -e "\n\nAll tests completed."
