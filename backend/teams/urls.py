from django.urls import path
from . import views

app_name = 'teams'

urlpatterns = [
    path('', views.TeamListView.as_view(), name='teams'),
    path('create/', views.TeamCreateView.as_view(), name='create_team'),
    path('<int:pk>/', views.TeamDetailView.as_view(), name='team_profile'),
    path('<int:pk>/edit/', views.TeamUpdateView.as_view(), name='edit_team'),
    path('<int:pk>/join/', views.TeamJoinView.as_view(), name='join_team'),
    path('<int:pk>/leave/', views.TeamLeaveView.as_view(), name='leave_team'),
    path('<int:team_pk>/remove_member/<int:member_pk>/', views.TeamRemoveMemberView.as_view(), name='remove_member'),
    path('<int:pk>/delete/', views.TeamDeleteView.as_view(), name='delete_team'),
]