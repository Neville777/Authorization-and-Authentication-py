**Project Name: Flask RESTful API with Authentication and Authorization**

---

## Overview:

This project is a Flask RESTful API with authentication using JWT (JSON Web Tokens) and endpoints for managing collections. It provides functionality for user registration, login, and CRUD operations on collections.

---

## Installation:

### 1. Clone the Repository:

```bash
git clone git@github.com:Neville777/Authorization-and-Authentication-py.git
cd Authorization-and-Authentication-py
```

### 2. Set Up Virtual Environment (Optional but Recommended):

```bash
python3 -m venv venv
source venv/bin/activate  # For Unix/macOS
venv\Scripts\activate  # For Windows
```

### 3. Install Dependencies:

```bash
pip install -r requirements.txt
```

### 4. Set Up the Database:

```bash
flask db init
flask db migrate
flask db upgrade
```

### 5. Seed the Database with Fake Data:

```bash
python3 seed.py
```

### 6. Configure Environment Variables:

Create a `.env` file in the project root and add the following:

```
SECRET_KEY=<your_secret_key>
```

### 7. Run the Application:

```bash
flask run
```

---

## Usage:

### Authentication Endpoints:

- **Register User:**

  - Endpoint: `/register`
  - Method: `POST`
  - Payload: `{ "email": "<user_email>", "password": "<user_password>" }`
  - Description: Registers a new user.

- **Login User:**
  - Endpoint: `/login`
  - Method: `POST`
  - Payload: `{ "email": "<user_email>", "password": "<user_password>" }`
  - Description: Logs in an existing user and returns a JWT token.

### Collection Endpoints:

- **Get Collections:**

  - Endpoint: `/collections`
  - Method: `GET`
  - Description: Retrieves collections associated with the authenticated user.

- **Create Collection:**

  - Endpoint: `/collections`
  - Method: `POST`
  - Payload: `{ "name": "<collection_name>", "photo_url": "<photo_url>" }`
  - Description: Creates a new collection for the authenticated user.

- **Get Collection by ID:**

  - Endpoint: `/collections/<collection_id>`
  - Method: `GET`
  - Description: Retrieves a specific collection by its ID.

- **Update Collection:**

  - Endpoint: `/collections/<collection_id>`
  - Method: `PATCH`
  - Payload: `{ "name": "<new_name>", "photo_url": "<new_photo_url>" }`
  - Description: Updates a specific collection.

- **Delete Collection:**
  - Endpoint: `/collections/<collection_id>`
  - Method: `DELETE`
  - Description: Deletes a specific collection.

---

## Notes:

- Ensure you replace `<your_secret_key>` in the `.env` file with your own secret key.
- This README assumes you have basic knowledge of Flask, RESTful APIs, and JWT authentication.

---

## Contributors:

- [NEVILLE JAMES](https://github.com/neville777) - Project Lead & Developer

---

## License:

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Feel free to customize this README according to your project's specific needs and requirements.
