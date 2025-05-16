from django.contrib import admin
from django.urls import path
from taskapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
     path('',views. HomeView.as_view(), name='home'),
     path('signup/',views. UsercreateView.as_view(), name='signup'),
     path('login/', views.LoginView.as_view(), name='login'),
     path('logout/', views.LogoutView.as_view(), name='logout'),
     path('admindash/', views.AdminDashboardView.as_view(), name='admin-dash'),
   
     path('adminremove/<int:pk>/',views.RemoveAdminView.as_view(), name='admin-remove'),
     path('admindelete/<int:pk>/',views.DeleteAdminView.as_view(), name='admin-delete'),
     path('admincreate/<int:pk>/',views.CreateAdminView.as_view(), name='admin-create'),
     path('userdash/',views.UserDashboardView.as_view(), name='user-dash'),
     path('userlist/',views.UserListView.as_view(), name='user-list'),
     path('userdelete/<int:pk>/',views.UserDeleteView.as_view(), name='user-delete'),
     path('taskadd/',views.TaskCreateView.as_view(), name='task-add'),
     path('task-list/',views.TaskListView.as_view(), name='task-list'),
     path('taskcompleted/',views.TaskCompletedListView.as_view(), name='task-completed'),
     path('taskpending/',views.TaskPendingListView.as_view(), name='task-pending'),
     path('taskdeleted/',views.TaskDeletedListView.as_view(), name='deleted-task'),
     path('taskupdate/<int:pk>/',views.TaskUpdateView.as_view(), name='task-update'),
     path('taskdelete/<int:pk>/',views.TaskDeleteView.as_view(), name='task-delete'),
     path('taskprogress/<int:pk>/',views.TaskProgressView.as_view(), name='task-progress'),
     path('taskcompleted/<int:pk>/',views.TaskCompletionReportListView.as_view(), name='task-completed-report'),
     path('taskcomplete/<int:pk>/',views.TaskCompletionFormView.as_view(), name='task-complete-form'),
     
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)