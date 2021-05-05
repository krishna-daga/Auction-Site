from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlisting",views.create_listings,name="create"),
    path("<int:id>",views.listing,name="listing"),
    path("watchlist/<int:id>",views.watchlist,name="watchlist"),
    path("closebid/<int:id>",views.closebid,name="closebid"),
    path("mywatchlist",views.mywatchlist,name="mywatchlist"),
    path("categories",views.categories,name="categories"),
    path("category/<str:category>",views.category,name="category"),
    path("addcomment/<int:id>",views.addcomment,name="addcomment"),
    path("closedlisting", views.closedlisting, name="closedlisting")
]
