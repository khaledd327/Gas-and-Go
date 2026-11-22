
from flask import Flask, request, render_template_string
from datetime import datetime
import uuid

app = Flask(__name__)

# -------------------------------------------------
# GAS & GO - DEMONSTRATION DATA
# -------------------------------------------------

VEHICLES = {
    "golf": {
        "name": "Volkswagen Golf",
        "tank": 50,
        "consumption": 7.0,
        "grade": "Special 95"
    },
    "corolla": {
        "name": "Toyota Corolla",
        "tank": 50,
        "consumption": 6.5,
        "grade": "Special 95"
    },
    "patrol": {
        "name": "Nissan Patrol",
        "tank": 100,
        "consumption": 14.0,
        "grade": "Super 98"
    }
}

FUEL_PRICES = {
    "Special 95": 2.50,
    "Super 98": 2.70
}

DELIVERY_SLOTS = [
    "09:00 - 11:00",
    "11:00 - 13:00",
    "14:00 - 16:00",
    "17:00 - 19:00"
]

# In-memory demo storage. Data resets when app restarts.
ORDERS = {}
DELIVERIES = {}

STYLE = """
<style>
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: #f2f5f9;
    color: #172b45;
}

header {
    background: #142d4e;
    color: white;
    text-align: center;
    padding: 28px 15px;
}

header h1 {
    font-size: 38px;
    margin: 0 0 12px;
}

header p {
    margin: 0 0 22px;
    font-size: 18px;
}

nav {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 12px;
}

nav a {
    color: white;
    text-decoration: none;
    border: 1px solid white;
    border-radius: 7px;
    padding: 12px 17px;
}

nav a:hover {
    background: #254a75;
}

main {
    max-width: 850px;
    margin: 40px auto;
    background: white;
    border-radius: 14px;
    padding: 35px;
    box-shadow: 0 4px 15px #00000012;
}

h2 {
    margin-top: 0;
    font-size: 28px;
}

label {
    display: block;
    font-weight: bold;
    margin-top: 18px;
    margin-bottom: 8px;
}

input, select {
    width: 100%;
    padding: 14px;
    border: 1px solid #ccc;
    border-radius: 7px;
    font-size: 16px;
}

input[type=checkbox] {
    width: auto;
    margin-right: 8px;
}

button {
    width: 100%;
    padding: 16px;
    margin-top: 24px;
    border: 0;
    border-radius: 7px;
    background: #16865f;
    color: white;
    font-size: 18px;
    font-weight: bold;
    cursor: pointer;
}

button:hover {
    background: #116e4e;
}

.result {
    background: #e5f6eb;
    padding: 25px;
    border-radius: 10px;
    margin-top: 25px;
}

.result p {
    line-height: 1.7;
}

.error {
    background: #ffe8e8;
    padding: 15px;
    border-radius: 7px;
    color: #a11919;
    margin-top: 20px;
}

.note {
    background: #edf3fc;
    padding: 15px;
    border-radius: 8px;
    margin-top: 20px;
    font-size: 14px;
    line-height: 1.6;
}

a.link {
    display: inline-block;
    margin-top: 18px;
    color: #142d4e;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
}

th, td {
    padding: 12px;
    text-align: left;
    border-bottom: 1px solid #ddd;
}

th {
    background: #edf3fc;
}

@media (max-width: 600px) {
    main {
        margin: 18px 10px;
        padding: 22px;
    }
}
</style>
"""

HEADER = """
<header>
    <h1>Gas & Go</h1>
    <p>Fuel Delivery System</p>
    <nav>
        <a href="/">Home</a>
        <a href="/order">Place Fuel Order</a>
        <a href="/recommendation">Get Fuel Recommendation</a>
        <a href="/driver">Fulfil Delivery</a>
    </nav>
</header>
"""

def page(content, **context):
    return render_template_string(
        STYLE + HEADER + "<main>" + content + "</main>",
        **context
    )


# -------------------------------------------------
# HOME PAGE
# -------------------------------------------------

@app.route("/")
def home():
    return page("""
        <h2>Welcome to Gas & Go</h2>
        <p>
            A fuel delivery system prototype that
            allows customers to place orders, receive
            fuel recommendations, and track delivery
            fulfilment.
        </p>

        <div class="note">
            <strong>Available Features</strong>
            <p>UC 01 - Place Fuel Order</p>
            <p>UC 02 - Get Fuel Recommendation</p>
            <p>UC 03 - Fulfil Delivery</p>
        </div>

        <p>
            Use the navigation menu above to test
            each feature.
        </p>
    """)


# -------------------------------------------------
# UC 01 - PLACE FUEL ORDER
# -------------------------------------------------

@app.route("/order", methods=["GET", "POST"])
def order():
    error = None
    confirmed = None

    if request.method == "POST":
        try:
            customer = request.form.get("customer", "").strip()
            vehicle_id = request.form.get("vehicle", "")
            grade = request.form.get("grade", "")
            litres = float(request.form.get("litres", "0"))
            location = request.form.get("location", "").strip()
            slot = request.form.get("slot", "")

            if not customer:
                raise ValueError("Enter customer name.")

            if vehicle_id not in VEHICLES:
                raise ValueError("Select a valid vehicle.")

            if grade not in FUEL_PRICES:
                raise ValueError("Select a valid fuel grade.")

            if grade != VEHICLES[vehicle_id]["grade"]:
                raise ValueError(
                    "Fuel grade is not compatible with "
                    "the selected vehicle."
                )

            if litres <= 0:
                raise ValueError(
                    "Fuel quantity must be greater than zero."
                )

            if litres > VEHICLES[vehicle_id]["tank"]:
                raise ValueError(
                    "Quantity exceeds the vehicle tank capacity."
                )

            if not location:
                raise ValueError("Enter delivery location.")

            if slot not in DELIVERY_SLOTS:
                raise ValueError("Select a delivery slot.")

            total = round(litres * FUEL_PRICES[grade], 2)
            order_id = uuid.uuid4().hex[:8].upper()

            confirmed = {
                "id": order_id,
                "customer": customer,
                "vehicle": VEHICLES[vehicle_id]["name"],
                "vehicle_id": vehicle_id,
                "grade": grade,
                "litres": litres,
                "location": location,
                "slot": slot,
                "total": total,
                "status": "Confirmed",
                "payment": "Demo authorization only",
                "driver": None
            }

            ORDERS[order_id] = confirmed

        except (ValueError, TypeError) as exc:
            error = str(exc)

    return page("""
        <h2>UC 01 - Place Fuel Order</h2>

        {% if error %}
            <div class="error">{{ error }}</div>
        {% endif %}

        {% if confirmed %}
            <div class="result">
                <h2>Order Confirmed!</h2>

                <p><strong>Order ID:</strong>
                    {{ confirmed.id }}</p>

                <p><strong>Customer:</strong>
                    {{ confirmed.customer }}</p>

                <p><strong>Vehicle:</strong>
                    {{ confirmed.vehicle }}</p>

                <p><strong>Fuel:</strong>
                    {{ confirmed.grade }}</p>

                <p><strong>Quantity:</strong>
                    {{ confirmed.litres }} litres</p>

                <p><strong>Location:</strong>
                    {{ confirmed.location }}</p>

                <p><strong>Delivery Slot:</strong>
                    {{ confirmed.slot }}</p>

                <p><strong>Total:</strong>
                    AED {{ "%.2f"|format(confirmed.total) }}</p>

                <p><strong>Payment:</strong>
                    {{ confirmed.payment }}</p>
            </div>

            <a class="link" href="/driver">
                Continue to UC 03 - Fulfil Delivery
            </a>

            <br>

            <a class="link" href="/order">
                Place another order
            </a>

        {% else %}

            <form method="POST">

                <label>Customer Name</label>
                <input name="customer" required>

                <label>Vehicle</label>
                <select name="vehicle" required>
                    <option value="">Select vehicle</option>
                    {% for key, vehicle in vehicles.items() %}
                        <option value="{{ key }}">
                            {{ vehicle.name }}
                        </option>
                    {% endfor %}
                </select>

                <label>Fuel Grade</label>
                <select name="grade" required>
                    {% for grade, price in prices.items() %}
                        <option value="{{ grade }}">
                            {{ grade }} -
                            AED {{ "%.2f"|format(price) }}/L
                        </option>
                    {% endfor %}
                </select>

                <label>Fuel Quantity (Litres)</label>
                <input
                    type="number"
                    name="litres"
                    min="0.1"
                    step="0.1"
                    required
                >

                <label>Delivery Location</label>
                <input
                    name="location"
                    placeholder="Example: Abu Dhabi"
                    required
                >

                <label>Delivery Slot</label>
                <select name="slot" required>
                    {% for slot in slots %}
                        <option value="{{ slot }}">
                            {{ slot }}
                        </option>
                    {% endfor %}
                </select>

                <button type="submit">
                    Confirm Fuel Order
                </button>

            </form>

            <div class="note">
                This prototype uses example vehicle data,
                fixed fuel prices, and simulated payment
                authorization. No real payment is processed.
            </div>

        {% endif %}
    """,
    vehicles=VEHICLES,
    prices=FUEL_PRICES,
    slots=DELIVERY_SLOTS,
    confirmed=confirmed,
    error=error)


# -------------------------------------------------
# UC 02 - GET FUEL RECOMMENDATION
# -------------------------------------------------

@app.route("/recommendation", methods=["GET", "POST"])
def recommendation():
    error = None
    result = None

    if request.method == "POST":
        try:
            vehicle_id = request.form.get("vehicle", "")
            fuel_percent = float(
                request.form.get("fuel_percent", "0")
            )
            planned_distance = float(
                request.form.get("planned_distance", "0")
            )
            daily_distance = float(
                request.form.get("daily_distance", "0")
            )
            consent = (
                request.form.get("history_consent") == "yes"
            )

            if vehicle_id not in VEHICLES:
                raise ValueError("Select a valid vehicle.")

            if not 0 <= fuel_percent <= 100:
                raise ValueError(
                    "Fuel level must be between 0 and 100."
                )

            if planned_distance <= 0:
                raise ValueError(
                    "Planned distance must be greater than zero."
                )

            if daily_distance <= 0:
                raise ValueError(
                    "Daily distance must be greater than zero."
                )

            vehicle = VEHICLES[vehicle_id]

            tank = vehicle["tank"]
            consumption = vehicle["consumption"]
            grade = vehicle["grade"]

            current_litres = tank * fuel_percent / 100

            required_litres = (
                planned_distance * consumption / 100
            )

            suggested = max(
                0,
                required_litres - current_litres
            )

            available_space = tank - current_litres

            suggested = min(
                suggested,
                available_space
            )

            suggested = round(suggested, 1)

            total_fuel = current_litres + suggested

            available_distance = (
                total_fuel / consumption * 100
            )

            days = round(
                available_distance / daily_distance,
                1
            )

            cost = round(
                suggested * FUEL_PRICES[grade],
                2
            )

            result = {
                "vehicle": vehicle["name"],
                "grade": grade,
                "litres": suggested,
                "days": days,
                "cost": cost,
                "consent": "Yes" if consent else "No",
                "tank": tank,
                "consumption": consumption
            }

        except (ValueError, TypeError) as exc:
            error = str(exc)

    return page("""
        <h2>UC 02 - Get Fuel Recommendation</h2>

        {% if error %}
            <div class="error">{{ error }}</div>
        {% endif %}

        {% if result %}
            <div class="result">

                <h2>Your Fuel Recommendation</h2>

                <p><strong>Vehicle:</strong>
                    {{ result.vehicle }}</p>

                <p><strong>Recommended Fuel Grade:</strong>
                    {{ result.grade }}</p>

                <p><strong>Suggested Fuel Quantity:</strong>
                    {{ result.litres }} litres</p>

                <p><strong>Estimated Duration:</strong>
                    {{ result.days }} days</p>

                <p><strong>Estimated Fuel Cost:</strong>
                    AED {{ "%.2f"|format(result.cost) }}</p>

                <p><strong>Driving History Consent:</strong>
                    {{ result.consent }}</p>

                <p><strong>Assumptions:</strong>
                    {{ result.tank }}L tank and
                    {{ result.consumption }}L/100km
                    average fuel consumption.
                </p>

            </div>

            <a class="link" href="/recommendation">
                Get another recommendation
            </a>

        {% else %}

            <p>
                Enter your driving information to receive
                an estimated fuel recommendation.
            </p>

            <form method="POST">

                <label>Vehicle</label>
                <select name="vehicle" required>
                    <option value="">Select Vehicle</option>
                    {% for key, vehicle in vehicles.items() %}
                        <option value="{{ key }}">
                            {{ vehicle.name }}
                        </option>
                    {% endfor %}
                </select>

                <label>Current Fuel Level (%)</label>
                <input
                    type="number"
                    name="fuel_percent"
                    min="0"
                    max="100"
                    step="0.1"
                    placeholder="Example: 20"
                    required
                >

                <label>Planned Distance (km)</label>
                <input
                    type="number"
                    name="planned_distance"
                    min="0.1"
                    step="0.1"
                    placeholder="Example: 400"
                    required
                >

                <label>Daily Driving Distance (km)</label>
                <input
                    type="number"
                    name="daily_distance"
                    min="0.1"
                    step="0.1"
                    placeholder="Example: 40"
                    required
                >

                <label>
                    <input
                        type="checkbox"
                        name="history_consent"
                        value="yes"
                    >
                    I agree to use driving history
                </label>

                <button type="submit">
                    Get Recommendation
                </button>

            </form>

        {% endif %}

        <div class="note">
            This prototype uses rule-based calculations
            and example vehicle data, not a trained
            AI model. Actual fuel consumption may differ.
            Driving history is not collected or analysed.
        </div>

    """,
    vehicles=VEHICLES,
    result=result,
    error=error)


# -------------------------------------------------
# UC 03 - FULFIL DELIVERY
# -------------------------------------------------

@app.route("/driver", methods=["GET", "POST"])
def driver():
    error = None
    message = None
    receipt = None

    if request.method == "POST":
        action = request.form.get("action", "")
        order_id = request.form.get("order_id", "")

        selected_order = ORDERS.get(order_id)

        if not selected_order:
            error = "Order not found."

        elif action == "accept":
            driver_name = request.form.get(
                "driver_name", ""
            ).strip()

            if not driver_name:
                error = "Enter driver name."

            elif selected_order["status"] != "Confirmed":
                error = (
                    "Only confirmed orders can be accepted."
                )

            else:
                selected_order["driver"] = driver_name
                selected_order["status"] = "Accepted"

                message = (
                    "Delivery job accepted successfully."
                )

        elif action == "complete":
            try:
                if selected_order["status"] != "Accepted":
                    raise ValueError(
                        "The driver must accept the job first."
                    )

                access_ok = (
                    request.form.get("access_ok") == "yes"
                )

                safety_ok = (
                    request.form.get("safety_ok") == "yes"
                )

                if not access_ok:
                    raise ValueError(
                        "Parking access must be confirmed."
                    )

                if not safety_ok:
                    raise ValueError(
                        "Safety checks must be completed."
                    )

                actual_litres = float(
                    request.form.get("actual_litres", "0")
                )

                meter_reference = request.form.get(
                    "meter_reference", ""
                ).strip()

                if actual_litres <= 0:
                    raise ValueError(
                        "Delivered litres must be greater than zero."
                    )

                if actual_litres > selected_order["litres"]:
                    raise ValueError(
                        "Delivered quantity cannot exceed "
                        "the ordered quantity."
                    )

                if not meter_reference:
                    raise ValueError(
                        "Enter the meter reference."
                    )

                if order_id in DELIVERIES:
                    raise ValueError(
                        "This delivery was already recorded."
                    )

                grade = selected_order["grade"]

                final_amount = round(
                    actual_litres * FUEL_PRICES[grade],
                    2
                )

                delivery_id = uuid.uuid4().hex[:8].upper()
                receipt_id = uuid.uuid4().hex[:8].upper()

                receipt = {
                    "receipt_id": receipt_id,
                    "delivery_id": delivery_id,
                    "order_id": order_id,
                    "customer": selected_order["customer"],
                    "driver": selected_order["driver"],
                    "vehicle": selected_order["vehicle"],
                    "grade": grade,
                    "actual_litres": actual_litres,
                    "meter_reference": meter_reference,
                    "amount": final_amount,
                    "time": datetime.now().strftime(
                        "%Y-%m-%d %H:%M"
                    ),
                    "payment": "Demo capture completed"
                }

                DELIVERIES[order_id] = receipt

                selected_order["status"] = "Delivered"

                message = (
                    "Delivery completed successfully."
                )

            except (ValueError, TypeError) as exc:
                error = str(exc)

        else:
            error = "Invalid action."

    pending_orders = [
        order for order in ORDERS.values()
        if order["status"] in ("Confirmed", "Accepted")
    ]

    return page("""
        <h2>UC 03 - Fulfil Delivery</h2>

        <p>
            Driver workflow: accept an assigned job,
            confirm access and safety checks, record
            the delivered fuel quantity, and generate
            a receipt.
        </p>

        {% if error %}
            <div class="error">{{ error }}</div>
        {% endif %}

        {% if message %}
            <div class="result">
                <strong>{{ message }}</strong>
            </div>
        {% endif %}

        {% if receipt %}
            <div class="result">
                <h2>Delivery Receipt</h2>

                <p><strong>Receipt ID:</strong>
                    {{ receipt.receipt_id }}</p>

                <p><strong>Delivery ID:</strong>
                    {{ receipt.delivery_id }}</p>

                <p><strong>Order ID:</strong>
                    {{ receipt.order_id }}</p>

                <p><strong>Customer:</strong>
                    {{ receipt.customer }}</p>

                <p><strong>Driver:</strong>
                    {{ receipt.driver }}</p>

                <p><strong>Vehicle:</strong>
                    {{ receipt.vehicle }}</p>

                <p><strong>Fuel Grade:</strong>
                    {{ receipt.grade }}</p>

                <p><strong>Delivered Quantity:</strong>
                    {{ receipt.actual_litres }} litres</p>

                <p><strong>Meter Reference:</strong>
                    {{ receipt.meter_reference }}</p>

                <p><strong>Final Amount:</strong>
                    AED {{ "%.2f"|format(receipt.amount) }}</p>

                <p><strong>Completion Time:</strong>
                    {{ receipt.time }}</p>

                <p><strong>Payment:</strong>
                    {{ receipt.payment }}</p>
            </div>
        {% endif %}

        <h3>Delivery Orders</h3>

        {% if orders %}
            <table>
                <tr>
                    <th>Order ID</th>
                    <th>Location</th>
                    <th>Status</th>
                </tr>

                {% for order in orders %}
                <tr>
                    <td>{{ order.id }}</td>
                    <td>{{ order.location }}</td>
                    <td>{{ order.status }}</td>
                </tr>
                {% endfor %}
            </table>

            {% for order in orders %}

                {% if order.status == "Confirmed" %}

                    <form method="POST">
                        <h3>Accept Job - {{ order.id }}</h3>

                        <input
                            type="hidden"
                            name="order_id"
                            value="{{ order.id }}"
                        >

                        <input
                            type="hidden"
                            name="action"
                            value="accept"
                        >

                        <label>Driver Name</label>
                        <input
                            name="driver_name"
                            required
                        >

                        <button type="submit">
                            Accept Delivery Job
                        </button>
                    </form>

                {% elif order.status == "Accepted" %}

                    <form method="POST">
                        <h3>Complete Delivery - {{ order.id }}</h3>

                        <p><strong>Driver:</strong>
                            {{ order.driver }}</p>

                        <p><strong>Ordered Quantity:</strong>
                            {{ order.litres }} litres</p>

                        <p><strong>Delivery Location:</strong>
                            {{ order.location }}</p>

                        <input
                            type="hidden"
                            name="order_id"
                            value="{{ order.id }}"
                        >

                        <input
                            type="hidden"
                            name="action"
                            value="complete"
                        >

                        <label>
                            <input
                                type="checkbox"
                                name="access_ok"
                                value="yes"
                                required
                            >
                            Parking access confirmed
                        </label>

                        <label>
                            <input
                                type="checkbox"
                                name="safety_ok"
                                value="yes"
                                required
                            >
                            Safety checks completed
                        </label>

                        <label>Actual Delivered Litres</label>
                        <input
                            type="number"
                            name="actual_litres"
                            min="0.1"
                            max="{{ order.litres }}"
                            step="0.1"
                            required
                        >

                        <label>Meter Reference</label>
                        <input
                            name="meter_reference"
                            placeholder="Example: MTR-1001"
                            required
                        >

                        <button type="submit">
                            Complete Delivery
                        </button>
                    </form>

                {% endif %}

            {% endfor %}

        {% else %}

            <div class="note">
                No pending delivery orders.

                <p>
                    First create an order in UC 01,
                    then return to this page.
                </p>

                <a class="link" href="/order">
                    Place Fuel Order
                </a>
            </div>

        {% endif %}

        <div class="note">
            Demo implementation only. Driver assignment,
            safety verification, payment capture, and
            receipt generation are simulated.
            No real fuel delivery or payment occurs.
        </div>

    """,
    orders=pending_orders,
    error=error,
    message=message,
    receipt=receipt)


# -------------------------------------------------
# START APPLICATION
# -------------------------------------------------

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
