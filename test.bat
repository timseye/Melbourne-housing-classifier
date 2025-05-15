@echo off
REM Test script for Melbourne Housing Price Classifier

REM List all test cases
echo Running all test cases...
python test.py

REM Test high-value property in Toorak
echo. 
echo Running test case: high_value_toorak
python test.py high_value_toorak

REM Test modest property in outer suburb
echo.
echo Running test case: modest_outer_suburb
python test.py modest_outer_suburb

REM Test small apartment near city
echo.
echo Running test case: small_apartment_near_city
python test.py small_apartment_near_city

REM Test older property in mid-range suburb
echo.
echo Running test case: older_mid_range_suburb
python test.py older_mid_range_suburb

REM Test property with large land and old building
echo.
echo Running test case: large_land_old_building
python test.py large_land_old_building

REM Test new townhouse
echo.
echo Running test case: new_townhouse
python test.py new_townhouse

REM Test with missing data
echo.
echo Running test case: missing_data_example
python test.py missing_data_example

REM Test very large property
echo.
echo Running test case: very_large_property
python test.py very_large_property

REM Test very small property
echo.
echo Running test case: very_small_property
python test.py very_small_property

echo.
echo All tests completed.
pause
