# WishNet - From Wishlist to Gift List, Without the Drama

## Project Description
WishNet is a user-friendly platform designed to simplify the art of gifting and wishlist management. It solves the common problem of figuring out what to gift someone by allowing users to create and share wishlists, track budgets, and even organize Secret Santa groups. Built with Django, WishNet ensures thoughtful gifting without breaking the bank, making every celebration extra special.
---

## Features

### 1. Wishlist Management
- Create, edit, and delete wishlists.
- Categorize wishlists into tangible and intangible items.
- Track budgets to ensure thoughtful yet affordable gifting.

### 2. Secret Santa Group Feature
- Join or create Secret Santa groups.
- Assign members randomly and securely.
- View assigned member’s wishlist for gift ideas.

### 3. Budget Tracking
- Validate that wishlists adhere to group-defined budget limits.
- Provide real-time feedback when budgets are exceeded.

### 4. User Authentication
- Register and log in securely.
- Forgot password functionality with OTP verification.
- Manage user profiles seamlessly.

### 5. Friendships
- Search for friends, send friend requests, and manage connections.
- Accept or reject friend requests directly from the dashboard.

### 6. Aesthetic and Functional UI
-  Minimal red-and-white theme for a festive vibe.
- Fully responsive design with a dynamic navbar.
- Smooth animations and confetti effects on Secret Santa assignments.

---

## Live Demo
Check out the live demo here: [Live Demo](https://wishnet.pythonanywhere.com/)

## Tech Stack
- **Backend:** Django
- **Frontend:** HTML, CSS, Bootstrap
- **Database:**  Db.SQLite
- **Hosting Platform:**  PythonAnywhere

---
## Future Improvements
- Integration with social media to share wishlists.
- Customizable themes for users.
- Gift tracking feature to see when gifts have been purchased or received.

## How to Run Locally

### Step 1: Clone the repository
```bash
git clone https://github.com/your-username/wishnet.git
```


### Step 2. Navigate to the project directory:
   ```bash
   cd your-repo-name
   ```
### Step 3. Create a virtual environment (optional):
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: .\env\Scripts\activate
   ```
### Step 4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Step 5. Apply migrations:
   ```bash
   python manage.py migrate
   ```

### Step 6. Run the development server:
   ```bash
   python manage.py runserver
   ```

### Admin Setup
To access the admin panel, create a superuser:
```bash
python manage.py createsuperuser
```
Follow the prompts to set a username, email, and password.

## Usage
1. Create an account and log in.
2. Add wishlists and items with budgets.
3. Join or create a Secret Santa group.
4. Share your wishlist with friends and family.

## Technologies Used
- Django 4.0
- Bootstrap 5
- SQLite
- PythonAnywhere (for deployment)

## Contributing
Contributions are welcome! Please fork this repository, make your changes, and create a pull request. You can contribute by:

Fixing bugs
Adding new features
Improving documentation

## Contact
For any questions or suggestions, feel free to reach out to me at [shlokamdar@gmail.com].
