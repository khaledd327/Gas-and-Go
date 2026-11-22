
# Gas-and-Go
AI-Based Fuel Delivery System

## Project Description
Gas-and-Go is a web-based fuel delivery prototype that allows customers to place fuel orders, receive estimated fuel recommendations, and track the delivery process.

The project aims to make fuel ordering more convenient by allowing customers to request fuel delivery to an eligible parked vehicle.

## Team Members
- Khaled Salaas
- [Sultan Alyafei]
- [Khaled Ahmed]

## Problem
Traditional refuelling requires drivers to visit a petrol station. This may be inconvenient for customers with busy schedules.

Gas-and-Go proposes a website where customers can request fuel delivery and receive recommendations based on their driving information.

## Key Features

### UC01 - Place Fuel Order
- Select a vehicle and fuel grade.
- Enter the required fuel quantity.
- Choose a delivery location and time slot.
- Review the estimated total.
- Confirm an order with simulated payment authorization.

### UC02 - Get Fuel Recommendation
- Select a vehicle.
- Enter the current fuel percentage.
- Enter planned and daily driving distances.
- Receive an estimated fuel quantity, cost, and duration.
- Display the assumptions used in the calculation.

### UC03 - Fulfil Delivery
- View confirmed delivery orders.
- Accept an assigned delivery job.
- Confirm parking access and safety checks.
- Record actual delivered litres and meter reference.
- Complete the delivery and generate a receipt.

## Technologies Used
- Python
- Flask
- HTML
- CSS
- Git and GitHub
- GitHub Codespaces

## Design Decisions
Flask was selected because it supports a simple web application with Python.

HTML and CSS are used to create the website interface.

The implementation follows the three main use cases identified during the earlier project phases.

The prototype uses rule-based fuel calculations rather than a trained AI model.

Payment authorization, payment capture, and delivery operations are simulated.

## Prerequisites
- Python 3
- pip
- Flask
- A web browser

## Installation and Configuration

1. Clone the repository:

   git clone https://github.com/khaledd327/Gas-and-Go.git

2. Open the project folder:

   cd Gas-and-Go

3. Install Flask:

   pip install flask

4. Start the application:

   python app.py

5. Open the website using the local address or the forwarded port 5000 in GitHub Codespaces.

## How to Run
Run the application using:

python app.py

In GitHub Codespaces, open the forwarded address for port 5000.

## How to Test

### Test UC01
1. Open the fuel order page.
2. Select a vehicle and fuel grade.
3. Enter a valid quantity, location, and delivery slot.
4. Submit the order.
5. Check that an order confirmation and total are displayed.

### Test UC02
1. Open the fuel recommendation page.
2. Select a vehicle.
3. Enter valid fuel and driving information.
4. Click Get Recommendation.
5. Check the suggested fuel quantity, estimated duration, and cost.

### Test UC03
1. Create a fuel order using UC01.
2. Open the driver delivery page.
3. Accept the delivery job.
4. Confirm parking access and safety checks.
5. Enter the delivered quantity and meter reference.
6. Complete the delivery.
7. Check that a delivery receipt is generated.

## Prototype Limitations
- Fuel recommendations use rule-based calculations and example vehicle data.
- Driving history is not collected or analysed.
- Payments and deliveries are simulated.
- No real fuel delivery or financial transaction takes place.

## GitHub Repository
https://github.com/khaledd327/Gas-and-Go
