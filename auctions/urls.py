from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("create/", views.create_listing, name="create_listing"),
    path("listing/<int:listing_id>/", views.listing_detail, name="listing_detail"),
    path("listing/<int:listing_id>/add_to_watchlist/", views.add_to_watchlist, name="add_to_watchlist"),
    path("listing/<int:listing_id>/remove_from_watchlist/", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("listing/<int:listing_id>/bid/", views.bid_on_listing, name="bid_on_listing"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("categories/", views.category, name="categories"),
    path("category/<int:category_id>/", views.category_listings, name="category_listings")
]
