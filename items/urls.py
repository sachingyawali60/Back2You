from django.urls import path
from . import views
from .views import home
from .views import lost_items, found_items, my_items, edit_item, delete_item

urlpatterns = [
    path('', home, name='home'),
    path('lost/', lost_items, name='lost_items'),
    path('found/', found_items, name='found_items'),
    path('add/', views.add_item, name='add_item'),
    path('my-items/', views.my_items, name='my_item'),
    path('manage-claims/', views.manage_claims, name='manage-claims'),
    path('profile/', views.profile, name='profile'),
    path('about/', views.about, name='about'),
    path('edit/<int:item_id>/', edit_item, name='edit_item'),
    path('delete/<int:item_id>/', delete_item, name='delete_item'),
    path('claim/<int:item_id>/', views.claim_item, name='claim_item'),
    path('my-claims/', views.my_claims, name='my_claims'),
    path('manage-claims/', views.manage_claims, name='manage_claims'),
    path('claim/<int:item_id>/', views.claim_item, name='claim_item'),
    path('update_claim/<int:claim_id>/<str:status>/', views.update_claim_status, name='update_claim_status'),
    path('claim/<int:claim_id>/returned/', views.mark_as_returned, name='mark_as_returned'),
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),

]
