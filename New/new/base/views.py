from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Imports for Reordering Feature
from django.views import View
from django.shortcuts import redirect
from django.db import transaction

from .models import Task
from .forms import PositionForm


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].all().exclude(status='Closed').count()
        context['todo_high'] = context['tasks'].filter(status='To-Do', priority ='High')
        context['todo_medium'] = context['tasks'].filter(status='To-Do', priority ='Medium')
        context['todo_low'] = context['tasks'].filter(status='To-Do', priority ='Low')
        context['progress_high'] = context['tasks'].filter(status='In Progress', priority = 'High')
        context['progress_medium'] = context['tasks'].filter(status='In Progress', priority = 'Medium')
        context['progress_low'] = context['tasks'].filter(status='In Progress', priority = 'Low')
        context['review_high'] = context['tasks'].filter(status='In Review', priority = 'High')
        context['review_medium'] = context['tasks'].filter(status='In Review', priority = 'Medium')
        context['review_low'] = context['tasks'].filter(status='In Review', priority = 'Low')
        context['closed_high'] = context['tasks'].filter(status='Closed', priority = 'High')
        context['closed_medium'] = context['tasks'].filter(status='Closed', priority = 'Medium')
        context['closed_low'] = context['tasks'].filter(status='Closed', priority = 'Low')



        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__contains=search_input)

        context['search_input'] = search_input

        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'status', 'priority', 'type', 'description']
    # fields = '__all__'
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    # fields = ['title', 'description', 'complete']
    fields = ['title', 'status', 'priority', 'type', 'description']
    success_url = reverse_lazy('tasks')


class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)

class TaskReorder(View):
    def post(self, request):
        form = PositionForm(request.POST)

        if form.is_valid():
            positionList = form.cleaned_data["position"].split(',')

            with transaction.atomic():
                self.request.user.set_task_order(positionList)

        return redirect(reverse_lazy('tasks'))
