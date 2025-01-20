# Stock Price Dashboard

The tool is deployed on **AWS EC2**: [http://54.196.221.193/](http://54.196.221.193/)

---

## 🚀 **Project Tech Stack**
- **Backend**: Python, Django, SQLite
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **WebSocket**: Daphne

---

## ✨ **Features / Functionality**

### 1️⃣ Login Page
- Users can log in by entering their email address and password.

### 2️⃣ Registration Page
- Users can register by providing:
  - Username
  - Email address
  - Password
  - Phone number
  - Date of birth

### 3️⃣ Dashboard
#### 🏠 **Home Section**
- Displays **historical data** from a provided file.
- Time-series data with:
  - **Price** on the Y-axis
  - **Date** on the X-axis
- Includes a date filter and dropdown with options:
  - **NIFT 50**
  - **BANK NIFT**

#### 👤 **Profile Page**
- User information displayed:
  - Username
  - User ID (auto-generated)
  - Email address
  - Phone number
  - Date of birth
  - User type
  - Broker

#### 📊 **Holdings Section**
- Displays data from `holding_response.json` in a table.
- Calculates total **profit/loss** based on holdings.

#### 🛒 **Place Order Section**
- Users can:
  - Enter stock, price, and quantity.
  - View the history of all placed orders in a table.

#### 📡 **WebSocket Data Section**
- Simulates live stock updates using WebSocket:
  - Updates every 5 seconds: `price + (price * 0.01)`.

---

## 🛠️ **Steps to Run Locally**

```bash
# 1. Install dependencies:
pip install -r requirements.txt

# 2. Enable Debug Mode:
# In settings.py, set:
DEBUG = True

# 3. Set up Database:
python manage.py makemigrations
python manage.py migrate

# 4. Run the Application:
# Start the Django app:
python manage.py runserver

# Start WebSocket:
daphne my_project.asgi:application --port 8001
