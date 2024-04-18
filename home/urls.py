from django.urls import path
from home.views import *
urlpatterns = [
    path('', MainPage.as_view()),
    path('about/',ABOUT.as_view()),
    path('gallery/',GALLERY.as_view()),
    path('project/',PROJECT.as_view()),
    path('getknowledgelist/',GET_KNOWLEDGELIST.as_view()),
    
    path('knowledge/',KNOWLEDGE.as_view()),
    path('knowledge/<int:pk>/',KNOWLEDGE_DETAILS.as_view()),

    path('knowledge/postDetails/',PostDetails.as_view()),

    path('contact/',CONTACT.as_view()),
    path('project/dragongame/',DRAGON_GAME.as_view()),
    
    path('test/',TEST.as_view()),
    path('test2/',TEST2.as_view()),
    path('contact/submit/', CONTACTS.as_view())
  
]


