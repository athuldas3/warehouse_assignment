# Warehouse Management System

## Project Structure

The architecture used here is designed to separate each section as a package, aiming to reduce dependencies, enhance readability, and promote code reusability.

### Project Components

- **requirements.txt**: Lists all the required packages for the project.

- **app/config**: Contains `config.py` for database connection details and other configurations.

- **app/custom_decorators**: Custom decorators for field validation and role-based access validation.

- **app/models**: Defines models for various tables, including `ProductMeta`, `InventoryLog`, `SellerMeta`, `RoleMapping`, and `User`.

- **app/one_time_scripts**: Scripts for creating dummy users and roles.

- **app/serializers.py**: Serializers for data validation.

- **app/urls.py**: Routing of the API, with separate files for each API endpoint.

- **app/views.py**: Business logic, neatly organized using utilities. Specific logic is split and added to utilities.
  - **auth_view.py**: Contains Auth API to get an access token.
  - **product_view.py**: Contains both the GET API to get products weekly, and POST/PUT API to create and update products.
  - **user_view.py**: Contains the logic to create default users and roles.

- **migrations**: Contains database migration scripts.

- **.env**: Stores sensitive data like database name, password, etc.

- **run.py**: Script to run the Flask application with the development server.

## Project Setup
loom video explaining the setup and working:

# Loom Video Link: 
[Click Here](https://www.loom.com/share/8b8f7a29f64b4898bd8634c3bf063b9f?sid=f8330eb6-0824-4ac1-9d5e-efe763f87a91)


# Setup Instructions
# 1. Create a Virtual Environment
virtualenv myenv
# Activate the virtual environment
# Ubuntu/Linux:
source myenv/bin/activate
# Windows:
myenv\Scripts\activate

# 2. Install Requirements
pip install -r requirements.txt

# 3. Create a .env File
touch .env 

# Database Configuration
DB_NAME=warehouse_db  # Create a database in PostgresSQL and change the dbname
DB_USER=postgres
DB_PASSWORD=postgres
# Flask Configuration
SECRET_KEY=910e7596db07ed20df953d028056603e
SECURITY_PASSWORD_SALT=924ad327f29fe9317db7b54d87f1a77e
JWT_SECRET_KEY=8b6605e8db15bc67dcd88f9d5abf0e05
EOF

# Running the Project
# 1. Run Migrations
flask db upgrade

# 2. Run the Server
python run.py runserver

# API Endpoints
# 1. User Login
# URL: /user/login
# Method: POST
# Input: {"email": "PM@gmail.com", "password": "User@123"}
# Response: {"access_token": "---token----"}

# 2. Create Sellers, Products, and Inventory Logs
# URL: /create/sellers/products/inv-log
# Method: POST
# Authentication Required: Yes
# Role: PM and RM
# Input: Seller, Product, and Inventory Log details
# Response: {"seller_details":{"sellerName": "seller test", "sellerGST": "2"},
# "product_details": {"productName": "product5"}, "inv_log_details": {"quantity": 10, "category":"food"}}

# 3. Update Sellers, Products, and Inventory Logs
# URL: /update/sellers/products/inv-log
# Method: PUT
# Input: {
#    "inv_log_details": {
#        "id": 1,
#        "quantity": 16,
#        "category": "apparel"
#    },
#    "product_details": {
#        "id": 1,
#        "productName": "product7"
#    },
#    "seller_details": {
#        "id": 1,
#        "sellerName": "seller test2",
#        "sellerGST": "2"
#    }
# }
# Response: Updated details

# 4. Retrieve Weekly Product Data
# URL: /products/weekly
# Method: GET
# Authentication Required: Yes
# Role : PM and RM
# Input Parameters: start_date, end_date, seller_name
# Example: /products/weekly?start_date=2024-01-01&end_date=2024-01-25&seller_name=seller2
# Response: Weekly product data


# Note: you can find the postman callouts in the project : Warehouse.postman_collection.json
