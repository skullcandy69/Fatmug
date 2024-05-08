# Fatmug Vendor Management System

This is a Django-based Vendor Management System that allows tracking of vendor profiles, purchase orders, and performance metrics.

## Setup Instructions

Follow these steps to set up the project locally:

### 1. Clone the Repository

```bash
git clone https://github.com/skullcandy69/Fatmug.git 
```
### 2. Create virtual enviorrnment

```bash
cd vendor_management_system
python3 -m venv venv
```
### 3. Activate virtual enviorrnment
windows:
```bash
venv\Scripts\activate
```
macOS/Linux:
```bash
source venv/bin/activate
```

### 4. Install Requirements
```bash
pip install -r requirements.txt
```


### 5. Configure MySQL Database

- Open vendor_management_system/settings.py file.
- Replace the MySQL database credentials in the DATABASES setting with your MySQL database credentials.

### 6. Run Migrations

```bash
python manage.py migrate
```
### 7. Run the Development Server
```bash
python manage.py runserver
```


### Note:
You can find a Postman collection with example requests in the postman_collection directory. Import this collection into Postman to test the API endpoints.




