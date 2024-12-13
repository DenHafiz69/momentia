# Momentia

**Momentia** is a minimalist social media platform where users can "live in the moment." Posts are temporary and disappear after a set period, encouraging users to focus on the present rather than the past.

---

## **Features**

- **User Authentication**: Register, login, and logout functionality.
- **Create Temporary Posts**: Share text or images that automatically disappear after 24 hours.
- **Dynamic Feed**: View active posts from all users in a clean, simple feed.
- **Profile Pages**: Check out a user's active posts.
- **Responsive Design**: Mobile-friendly interface using Bootstrap.

---

## **Technologies Used**

- **Frontend**:
  - HTML, CSS, JavaScript
  - [Bootstrap](https://getbootstrap.com/)
- **Backend**:
  - [Flask](https://flask.palletsprojects.com/): Python-based web framework
- **Database**:
  - SQLite: Lightweight database for managing users and posts
- **Version Control**:
  - [Git](https://git-scm.com/): Version control system
  - [GitHub](https://github.com/): Code hosting platform

---

## **Setup Instructions**

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/DenHafiz69/momentia.git
   cd momentia
   ```

2. **Create a Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate   # For Windows
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up the Database**:
   ```bash
   flask db upgrade
   ```

5. **Run the Application**:
   ```bash
   flask run
   ```
   Access the app at `http://127.0.0.1:5000/`

---

## **Project Structure**

```
Momentia/
├── static/                # Static files (CSS, JavaScript, images)
├── templates/             # HTML templates
├── app.py                 # Main Flask app
├── models.py              # Database models
├── routes.py              # App routes
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

---

## **Future Enhancements**

- **Search and Filters**: Add functionality to search and filter posts.
- **Notifications**: Notify users when posts are about to expire.
- **Image Uploads**: Allow users to upload images with their posts.
- **Deployment**: Deploy the app on platforms like Heroku.

---

## **Contributing**

Contributions are welcome! Feel free to fork the repository and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

---

## **License**

This project is licensed under the MIT License. See the `LICENSE` file for more information.

---

## **Acknowledgments**

Special thanks to the [CS50](https://cs50.harvard.edu/) course for introducing the foundational technologies used in this project.
