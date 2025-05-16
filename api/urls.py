from django.urls import path
from api import views
urlpatterns=[
    path('signup/',views.UserCreationView.as_view()),
    path('expenses/',views.ExpenseCreateView.as_view()),
    path('expenses/<int:pk>/',views.ExpenseRetrieceUpdateDeleteView.as_view()),
    path('expenses/summary/',views.ExpenseSummaryView.as_view())
]