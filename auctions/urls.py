from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<str:listing>", views.listing, name = "listing"),
    path("bid/<str:listing>", views.bid, name="bid"),
    path("closebid/<str:listing>", views.closebid, name="closebid"),
    path("create_comment/<str:listing>", views.create_comment, name="create_comment"),
    path("newlisting/", views.new_listing, name="new_listing"),
    path("createnewlisting/", views.createnew_listing, name="createnew_listing"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("addwatchlist/<str:listing>", views.addwatchlist, name="addwatchlist"),
    path("categories/", views.categories, name="category"),
    path("categorypage/<str:listing>", views.categorypage, name="categorypage")
  
]
