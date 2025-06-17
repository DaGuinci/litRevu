# 📚 LitReview

LitReview is a platform for readers to share reviews and opinions about the books they have read.

![Language](https://img.shields.io/badge/Code-Django-blue?logo=django)
![Status](https://img.shields.io/badge/status-development-orange)

---

## 📖 Overview

LitReview provides a friendly space for book enthusiasts where they can:
- Publish reviews and opinions about their readings
- Discover recommendations from other users
- Interact with a community of readers

---

## 🌟 Features

LitReview offers the following functionalities:
- **Request a review**: Users can open a ticket to request feedback on a book.
- **Follow other users**: Stay updated with the activity of other readers.
- **Respond to tickets**: Provide feedback on a ticket, as long as no one else has already responded.
- **View personalized feed**: Display a feed that includes reviews and tickets from followed users, as well as the user's own reviews and tickets.
- **Manage profile**: Users can create, update, and delete their profile.

---

## 🖥️ Demo

> 📷 *Screenshot*
![Demo](assets/screenshot.png)

---

## 🚀 Installation

1. **Create a virtual environment**:
   ```bash
   python -m venv env
   ```

2. **Activate the virtual environment**:
   ```bash
   source env/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Modify styles (optional)**:
   If you want to customize the styles, install [Sass](https://sass-lang.com/install) and use the following command:
   ```bash
   sass static/styles/styles.scss static/styles/styles.css --watch
   ```

---

## 🖥️ Running the Project

1. **Start the server**:
   ```bash
   python manage.py runserver
   ```

2. **Access the site**:
   Open your browser and go to [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

## 👤 Test Users

You can use the following accounts to test the site:

| Username          | Password    |
|-------------------|-------------|
| JeanDupont        | oc-pass23   |
| PierreDuchemein   | oc-pass23   |
| JacquesDurand     | oc-pass23   |
| MarcDumoulin      | oc-pass23   |

---

## 💡 Technologies Used

- **Django** (main framework)
- **Pillow** (image processing)
- **sqlparse** (SQL parsing)
- **flake8** (code linting)
- **django-browser-reload** (automatic browser reload)

---

## 👤 About the Developer

<div align="center">
  <p>Developed by <a href="https://evendev.net"><strong>Guillaume Even</strong></a></p>
  <a href="https://evendev.net">
    <img src="https://evendev.net/img/logo.svg" alt="evendev logo" width="100"/>
  </a>
</div>
