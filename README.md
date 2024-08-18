# Commerce - Auction Site



https://github.com/user-attachments/assets/bac37ac4-4f2e-434a-b619-4bac081654c5


## Overview
Commerce is a web-based auction platform that allows users to create and participate in online auctions. Users can create listings for items they wish to sell, place bids on active listings, comment on listings, and manage a watchlist of items they are interested in..

## Features
- **User Authentication**: Secure user registration and login.
- **Create Listings**: Users can create auction listings with a title, description, starting bid, image URL, and select from predefined categories.
- **Bidding System**: Users can place bids on active listings. The highest bid is always displayed.
- **Comments**: Users can add and view comments on each listing.
- **Watchlist**: Users can add listings to their watchlist for easy access and management.
- **Categories**: Browse listings by predefined categories.

## Demo

Watch the [video demo](https://youtu.be/P0c9BHUrrVA) on YouTube.


## Technologies Used
- **Django**: A high-level Python web framework that encourages rapid development.
- **Bootstrap**: A popular CSS framework for building responsive and mobile-first websites.
- **SQLite**: A lightweight, file-based database for storing auction data.

## Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/commerce.git
   cd commerce
   ```

2. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

3. **Create A Superuser**:
   ```bash
   python manage.py createsuperuser
   ```

4. **Run the Development Server**:
   Start the server and navigate to http://127.0.0.1:8000/ to use the application

   ```bash
   python manage.py runserver
   ```

## Usage
- **Create A Listing**: Log in and navigate to the "Create Listing" page to auction an item.
- **Browse Listings**: Explore active listings on the homepage or filter by category.
- **Place Bids**: Click on a listing to view details and place a bid.
- **Manage Watchlist**: Add items to your watchlist for easy access.
- **Comment on Listings**: Share your thoughts or ask questions about a listing by leaving a comment.

## Project Structure
- **auctions/**: Contains the Django app that handles the auction functionalities.
- **commerce/**: Main project directory containing settings, URLs, and configurations.
- **manage.py**: Django's command-line utility for administrative tasks.

## Acknowledgements
 This project was developed as part of the CS50 Web Programming with Python and JavaScript course.
