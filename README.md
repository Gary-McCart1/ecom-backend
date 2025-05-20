# 🛒 E-commerce Backend API (Django + DRF)

Website URL: https://foamhead-a8f24bda0c5b.herokuapp.com/

Youtube Demo Link: https://youtu.be/WErxf3E5_MM

This is the backend API for a full-featured e-commerce application built using **Django** and the **Django REST Framework (DRF)**. It provides core functionality for both the customer-facing store and the admin dashboard.

The API handles user authentication (via **Simple JWT** stored in **HttpOnly cookies**), product and order management, and support for admin features like message viewing. It integrates seamlessly with:

- A **storefront frontend** where customers can browse products and place orders
- An **admin dashboard** where business users can manage products, view orders, and read messages

---

## Endpoints
- /admin/: Access to django admin page.
- /api/token/ and /api/refresh/: allows a user to log in with their username and password and get an access token and refresh token
- /api/: Access to data for following routes:
  - /login/ - POST Request for logging in
  - /logout/ - POST Request for logging out
  - /products/: CRUD operations for products
  - /orders/: CRUD operations for orders
  - /messages/: CRUD operations for messages
  - /orderitems/: View items involved in each order
  - /reviews/: View and create reviews for products
  - /images/: View and create images for products
  - /cumulative-monthly-stats/: View monthly sales data
  - /create-checkout-session/: Stripe checkout integration
---

## 🚀 Features

- ✅ Simple JWT authentication using HttpOnly cookies  
- ✅ User registration, login, and logout  
- ✅ Full CRUD functionality for product catalog  
- ✅ Order management with status updates  
- ✅ Secure, permission-based API access  
- ✅ CORS configured for frontend integrations  
- ✅ Token refresh logic for maintaining sessions  

---

## 🧱 Tech Stack

- **Python 3.10+**  
- **Django 4.x**  
- **Django REST Framework**  
- **Simple JWT (djangorestframework-simplejwt)**  
- **PostgreSQL** (production-ready)

---

## 👨‍💻 Mock User

Use this test user to interact with the API or connected frontends:

- **Username:** `mock_user`  
- **Password:** `password12345678`

---

## Future Improvements

- ** Support direct photo file uploads so that images are stored and managed by the API (e.g., using AWS S3), instead of relying on external image URLs.
- ** Implement Docker with the other applications
- ** Implement a homepage for better accessibility to endpoints

## 📬 Contact Info

For questions, contributions, or support:

- **Email:** gwmccart3@gmail.com
- Storefront Github link: https://github.com/Gary-McCart1/ecom-storefront-foamhead
- Dashboard Github link: https://github.com/Gary-McCart1/ecom-dashboard








