from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from .models import ToDoItem, ToDoList

class ListListView(ListView):
    model = ToDoList
    template_name = "todo_app/index.html"

class ItemListView(ListView):
    model = ToDoItem
    template_name = "todo_app/todo_list.html"

    def get_queryset(self):
        return ToDoItem.objects.filter(todo_list_id=self.kwargs["list_id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todo_list"] = ToDoList.objects.get(id=self.kwargs["list_id"])
        return context

class ListCreate(CreateView):
    model = ToDoList
    fields = ["title"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add a new list"
        return context

class ItemCreate(CreateView):
    model = ToDoItem
    fields = ["todo_list", "title", "description", "due_date"]

    def get_initial(self):
        initial = super().get_initial()
        todo_list = ToDoList.objects.get(id=self.kwargs["list_id"])
        initial["todo_list"] = todo_list
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todo_list"] = ToDoList.objects.get(id=self.kwargs["list_id"])
        context["title"] = "Create a new item"
        return context

    def get_success_url(self):
        return reverse_lazy("list", args=[self.object.todo_list_id])

class ItemUpdate(UpdateView):
    model = ToDoItem
    fields = ["todo_list", "title", "description", "due_date"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todo_list"] = self.object.todo_list
        context["title"] = "Edit item"
        return context

    def get_success_url(self):
        return reverse_lazy("list", args=[self.object.todo_list_id])

class ListDelete(DeleteView):
    model = ToDoList
    success_url = reverse_lazy("index")

class ItemDelete(DeleteView):
    model = ToDoItem

    def get_success_url(self):
        return reverse_lazy("list", args=[self.object.todo_list_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todo_list"] = self.object.todo_list
        return context
