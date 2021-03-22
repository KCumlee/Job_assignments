This is a project to automate the following actions using the Page Object Model: 
1)	Go to Cars.com and:
•	Select `Used Cars`
•	Select Make `Honda`
•	Select Model `Pilot`
•	Select Price `50000`
•	Select Distance `100 miles`
•	Enter Zip Code 60008
•	Click `Search`

2)	Validate using assertions that 4 filters are displayed next to `Clear All` 
*	Max Price is 50000
*	Selected Make is Honda
*	Selected Model is Pilot
*	Selected `Used`

3)	Select `New` radio button from New/Used
4)	Validate using assertion that the `New` filter is displayed and `Used` is NOT displayed
5)	Select Touring 8-Passemger from Trim 
6)	Validate using assertion that the `Touring 8-Passenger` filter is displayed
7)	Select the second available car
8)	Validate using assertions: 
*	Selected car title contains `Honda Pilot 8-Passenger For Sale`
*	`Check Availability` button is displayed 

9)	In the Contact Seller section enter:
*	First Name: Car
*	Last Name: Owner
*	Email: carowner@yahoo.com

10)	Scroll down to `Payment Calculator` and take a screenshot


Test
----

You can use [`Pytest`](https://docs.pytest.org/en/stable/). You can find documentation for Selenium [here](https://selenium-python.readthedocs.io/index.html).

To run the test script:

* Need to have Pytest, Selenium, and Chrome and the [`Chrome web-driver`](https://chromedriver.chromium.org/downloads) installed
* open Terminal/cmd prompt
* cd to the directory with test_serach_for_cars.py
* run the "pytest" command
