from django.shortcuts import render
from django.views.generic import View
from taskapp.forms import SigninForm, loginForm, TaskForm, TaskCompletionReportForm
from django.shortcuts import redirect ,render, get_object_or_404
from django.http import HttpResponse
from taskapp.models import User, Task, TaskCompletionReport,DeletedTask
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView,FormView,TemplateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

class AdminPermissionmixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def handle_no_permission(self):
        return HttpResponse("You do not have permission to access this page.")
    
class SuperAdminPermissionmixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser 

    def handle_no_permission(self):
        return HttpResponse("You do not have permission to access this page.")
   


# Create your views here.

class HomeView(TemplateView):
    template_name = 'home.html'
    
    
class UsercreateView(AdminPermissionmixin,View):
    
    form = SigninForm
    
    template_name = "signup.html"
    
    def get(self,request,*args,**kwargs):
        
        form = self.form()
        
        return render(request, self.template_name, {'form': form})
    
    def post(self,request,*args,**kwargs):
        
        form = self.form(request.POST)
        
        if form.is_valid():
            
            user = form.save(commit=False)
            
            user.user_type = form.cleaned_data.get('user_type')
            
            if user.user_type == 'superadmin':
                user.is_superuser = True
            if user.user_type == 'admin':
                user.is_staff = True
                
         
            user.save()
            form.save()
            return redirect('admin-dash')
           
        return render(request, self.template_name, {'form': form})
    
@method_decorator(never_cache, name='dispatch')
class LoginView(View):
    form = loginForm
    template_name = 'login.html'
    
    def get(self,request,*args,**kwargs):
        form = self.form()
        return render(request, self.template_name, {'form': form})
    
    def post(self,request,*args,**kwargs):
        form = self.form(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                
                if user.is_superuser:
                    
                    return redirect('admin-dash')
                elif user.is_staff:
                    return redirect('admin-dash')
                
                return redirect('user-dash')
            else:
                return HttpResponse("Invalid credentials")
        return render(request, self.template_name, {'form': form})
    
class LogoutView(LoginRequiredMixin,View):
    
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect('home')

    
class AdminDashboardView(AdminPermissionmixin,TemplateView):
    template_name = 'admindash.html'
    
class UserDashboardView(LoginRequiredMixin,TemplateView):
    template_name = 'userdash.html'
    

    
class UserListView(AdminPermissionmixin,ListView):
    model = User
    template_name = 'user_list.html'
    context_object_name = 'user'
    
    def get_queryset(self):
        return User.objects.all().exclude(user_type = 'superadmin')

class RemoveAdminView(SuperAdminPermissionmixin,View):
    
    def get(self,request,*args,**kwargs):
        
        id = kwargs.get('pk')
        user = get_object_or_404(User,id=id)
        
        if user.user_type == 'admin':
            user.is_staff = False
            user.user_type = 'user'
            user.save()
            return redirect('user-list')
        
    
class CreateAdminView(SuperAdminPermissionmixin,View):
    
    def get(self,request,*args,**kwargs):
        
        id = kwargs.get('pk')
        user = get_object_or_404(User,id=id)
        
        if user.user_type == 'user':
            user.is_staff = True
            user.user_type = 'admin'
            user.save()
            return redirect('user-list')
        
    
class DeleteAdminView(SuperAdminPermissionmixin,View):
    
    def get(self,request,*args,**kwargs):
        
        id = kwargs.get('pk')
        user = get_object_or_404(User,id=id)
        if user.user_type == 'admin':
            user.delete()
            return redirect('user-list')
        
class UserDeleteView(SuperAdminPermissionmixin,View):
    def get(self,request,*args,**kwargs):
        
        id = kwargs.get('pk')
        user = get_object_or_404(User,id=id)
        if user.user_type == 'user':
            user.delete()
            return redirect('user-list')
        
       

@method_decorator(never_cache, name='dispatch')
class TaskCreateView(View):
    form = TaskForm
    template_name = 'task_form.html'
    
    def get(self,request,*args,**kwargs):
        form = self.form()
        form.fields['admin'].queryset = User.objects.filter(user_type='admin')
        form.fields['assigned_to'].queryset = User.objects.filter(user_type='user')
        return render(request, self.template_name, {'form': form})
    
    def post(self,request,*args,**kwargs):
        form = self.form(request.POST)
        
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            return redirect('task-list')
        return render(request, self.template_name, {'form': form})
    
class TaskListView(LoginRequiredMixin,ListView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'tasks'
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return Task.objects.all()
        return Task.objects.filter(assigned_to=user)
    
class TaskPendingListView(LoginRequiredMixin,ListView):
    model = Task
    template_name = 'task_pending.html'
    context_object_name = 'tasks'
    
    def get_queryset(self):
            return Task.objects.filter(status__in=['pending', 'in_progress'])

class TaskCompletedListView(LoginRequiredMixin,ListView):
    model = Task
    template_name = 'task_completedlist.html'
    context_object_name = 'tasks'
    
    def get_queryset(self):
        return Task.objects.filter(status = 'completed')
    
class TaskProgressView(LoginRequiredMixin,View):
    
    def get(self,request,*args,**kwargs):
        id = kwargs.get('pk')
        task = get_object_or_404(Task,id=id)
        if task.status == 'pending':
            task.status = 'in_progress'
            task.save()
            return redirect('task-list')



    
class TaskDeletedListView(AdminPermissionmixin,ListView):
    model = DeletedTask
    template_name = 'task_deleted_list.html'
    context_object_name = 'deleted_tasks'
    
    def get_queryset(self):
        
        return DeletedTask.objects.all()
    
    
class TaskUpdateView(AdminPermissionmixin,UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'
    
    def get_success_url(self):
        return reverse_lazy('task-list')
    
class TaskDeleteView(AdminPermissionmixin,View):
   
    
    def get(self,request,*args,**kwargs):
        id = kwargs.get('pk')
        task = get_object_or_404(Task,id=id)
        
        data = {
            'org_id': task.id,
            'title': task.title,
            'description': task.description,
            'assigned_to': task.assigned_to,
        }
        
        DeletedTask.objects.create(**data)
        task.delete()
        return redirect('task-list')
    
class TaskCompletionFormView(LoginRequiredMixin,View):
    
    template_name = 'task_completion_form.html'
    
    def get(self,request,*args,**kwargs):
        id = kwargs.get('pk')
        task = get_object_or_404(Task,id=id)
        form = TaskCompletionReportForm(instance=task)
        return render(request, self.template_name, {'form': form, 'task': task})
    
    def post(self,request,*args,**kwargs):
        id = kwargs.get('pk')
        task = get_object_or_404(Task,id=id)
        form = TaskCompletionReportForm(request.POST)
        
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            report.task = task
            report.save()
            task.status = 'completed'
            task.save()
            return redirect('task-list')
        return render(request, self.template_name, {'form': form, 'task': task})

class TaskCompletionReportListView(LoginRequiredMixin,View):
    
    template_name = 'task_completion_report.html'
    
    def get(self,request,*args,**kwargs):
        id = kwargs.get('pk')
        task = get_object_or_404(TaskCompletionReport,id=id)
        return render(request, self.template_name, {'task': task})
        
    
    
   
        
        
        

    

    

    
    
    
  
        
        
        
        

        




