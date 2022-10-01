from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("category", views.categorySelection, name="categorySelection"),
    path("comment/<int:id>", views.AddComment, name="comment"),
    path("bid/<int:id>", views.AddBid, name="bid")
]
