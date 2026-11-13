from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('detail/<int:listing_id>/', views.detail_view, name='detail'),
    path('elan/', views.elan_view, name='elan'),
    path('verify-email/', views.verify_email_view, name='verify_email'),
    path('resend-verification/', views.resend_verification_view, name='resend_verification'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('listing/<int:listing_id>/pin/', views.toggle_pin_view, name='toggle_pin'),
    path('listing/<int:listing_id>/compare/', views.toggle_compare_view, name='toggle_compare'),
    path('compare/', views.compare_view, name='compare'),
    path('listing/<int:listing_id>/edit/', views.edit_listing_view, name='edit_listing'),
    path('listing/<int:listing_id>/delete/', views.delete_listing_view, name='delete_listing'),
    path('listing/<int:listing_id>/chat/', views.start_or_open_chat, name='start_chat'),
    path('chat/<int:conversation_id>/', views.chat_room_view, name='chat_room'),
    path('chat/', views.chat_room_view, name='chat_inbox'),
]