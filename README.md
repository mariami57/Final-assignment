# WanderWords

WanderWords is a Django-powered social platform where users can share travel-inspired posts, write reviews, and engage with each other through comments. It provides a seamless way to share experiences, explore destinations, and interact with a community of fellow explorers.

## Features

○ Posts – Create, edit, and delete travel posts with images, books and destinations.  

○ Reviews – Write reviews for books.  

○ Books - Add books you are not able to find on the platform or choose from already existing ones. 

○ Destinations - Add destinations you can`t find on the platform or choose from already existing ones. Nominatim is used to geocode each destination (convert its name and country into coordinates) so that the related location can be displayed on a map.

○ Profiles – User profile pages with profile pictures and info. A profile is automatically created via a signal triggered when a new user registers.

○ Authentication – User registration, login/logout, and secure ownership checks for edits/deletes. Extended Django AbstractBaseUser in order to add custom functionalities.  

○ Image Support – Each post can include up to 3 images, which are displayed in a carousel.  

○ Comments – Engage with posts through threaded comments:  
- Add comments in-line (AJAX, no page refresh).
- Edit comments in place with a smooth UI.
- Delete comments instantly.


## Tech Stack

○ Backend: Django 5.x, Django ORM  

○ Frontend: HTML, CSS (Bootstrap + custom styling), JavaScript (vanilla, fetch API for AJAX)  

○ Database:  PostgreSQL/MySQL  

○ Authentication: Django built-in auth system  

○ Media Storage: Django ImageField  

## Installation & Setup

### 1. Create and activate a virtual environment
<pre>
  python -m venv venv
  source venv/bin/activate   # Mac/Linux
  venv\Scripts\activate      # Windows
</pre>

### 2. Install dependencies
<pre>
  pip install -r requirements.txt
</pre>

### 3. Create and apply migrations
<pre>
  python manage.py makemigrations
  python manage.py migrate
</pre>

### 4. Run the fixtures 
<pre>
  python manage.py loaddata initial_destinations
  python manage.py loaddata initial_books
  python manage.py loaddata permissions_fixture
</pre>

### 5. Create a superuser
<pre>
  python manage.py createsuperuser
</pre>

### 6. Run the development server
<pre>
 python manage.py runserver
</pre>

## Security
○ CSRF protection  

○ Only owners can edit/delete  

○ Validations applied to user input when it comes to books, destinations, profile information  

○ Django auth system  
