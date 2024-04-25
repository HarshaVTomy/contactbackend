#from contacts_api.views import contact_list, add_contact, contact
from django.urls import path
from contacts_api.views import ContactList, ContactDetail, ContactCreate
from .import views

urlpatterns = [
    path('list/', ContactList.as_view()),
    path('', ContactCreate.as_view()),
    path('<int:pk>', ContactDetail.as_view()),
    # path('signup/', views.signup),  # Corrected line with comma
    # path('login/', views.login), 
]

    