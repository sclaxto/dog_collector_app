from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
# Create your views here.
# Add the following import
from django.http import HttpResponse
from .models import Dog, Toy
from .forms import FeedingForm
# Add the Cat class & list and view function below the imports
# class Dog:  # Note that parens are optional if not inheriting from another class
#   def __init__(self, name, breed, description, age):
#     self.name = name
#     self.breed = breed
#     self.description = description
#     self.age = age

# dogs = [
#   Dog('Lolo', 'tabby', 'foul little demon', 3),
#   Dog('Sachi', 'tortoise shell', 'diluted tortoise shell', 0),
#   Dog('Raven', 'black tripod', '3 legged dog', 4)
# ]

# Define the home view
class DogCreate(CreateView): 
  model = Dog
  fields = '__all__'
  success_url ='/dogs/'
  

class DogUpdate(UpdateView):
  model = Dog
  # Let's disallow the renaming of a cat by excluding the name field!
  fields = ['breed', 'description', 'age']
  success_url = '/dogs/'

class DogDelete(DeleteView):
  model = Dog
  success_url = '/dogs/'


def home(request):
  return render(request, 'home.html')

def about(request): 
    return render(request, 'about.html')

def dogs_index(request):
  dogs = Dog.objects.all()
  return render(request, 'dogs/index.html', { 'dogs': dogs })

def dogs_detail(request, dog_id):
  dog = Dog.objects.get(id=dog_id)
  toys_dog_doesnt_have = Toy.objects.exclude(id__in = dog.toys.all().values_list('id'))
  feeding_form = FeedingForm()
  return render(request, 'dogs/detail.html', { 'dog': dog, 'feeding_form': feeding_form, 'toys': toys_dog_doesnt_have })

def add_feeding(request, dog_id):
  # create a ModelForm instance using the data in request.POST
  form = FeedingForm(request.POST)
  # validate the form
  if form.is_valid():
    # don't save the form to the db until it
    # has the cat_id assigned
    new_feeding = form.save(commit=False)
    new_feeding.dog_id = dog_id
    new_feeding.save()
  return redirect('detail', dog_id=dog_id)

def assoc_toy(request, dog_id, toy_id):
  # Note that you can pass a toy's id instead of the whole object
  Dog.objects.get(id=dog_id).toys.add(toy_id)
  return redirect('detail', cat_id=dog_id)

  

class ToyDetail(DetailView):
  model = Toy

class ToyCreate(CreateView):
  model = Toy
  fields = '__all__'

class ToyUpdate(UpdateView):
  model = Toy
  fields = ['name', 'color']

class ToyDelete(DeleteView):
  model = Toy
  success_url = '/toys/'

class ToyList(ListView):
   model = Toy