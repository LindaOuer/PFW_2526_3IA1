from django.shortcuts import render
from django.http import HttpResponse
from .models import Conference
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy

from .forms import ConferenceForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from rest_framework import viewsets
from .serializers import ConferenceSerializer

# Create your views here.
class ConferenceViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing conference instances.
    - list()   -> GET /conferences/
    - retrieve() -> GET /conferences/{id}/
    - create() -> POST /conferences/
    - update() -> PUT /conferences/{id}/
    - partial_update() -> PATCH /conferences/{id}/
    - destroy() -> DELETE /conferences/{id}/
    """
    queryset = Conference.objects.all()
    serializer_class = ConferenceSerializer





def home(request):
    return HttpResponse("<h1>Welcome to the Conference App Home Page!</h1>")

def about(request):
    return render(request, 'ConferenceApp/about.html')

def welcome(request, name):
    return render(
        request, 
        'ConferenceApp/welcome.html', 
        {'n': name} # context dictionary : passing 'name' as 'n' to the template
    )
    
def listConferences(request):
    conferences = Conference.objects.all().order_by('name')
    return render(request, 'ConferenceApp/conference_list.html', {'conferences': conferences})

class ConferenceListView(ListView):
    model = Conference
    context_object_name = 'conferences'
    template_name = 'ConferenceApp/conference_list.html'
    
class ConferenceDetailView(DetailView):
    model = Conference
    
class ConferenceCreateView(LoginRequiredMixin, UserPassesTestMixin,  CreateView):
    model = Conference
    # fields ="__all__"
    form_class = ConferenceForm
    success_url = reverse_lazy('conference_listLV')
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.role == 'organizer'
    
class ConferenceUpdateView(UpdateView):
    model = Conference
    fields ="__all__"
    success_url = reverse_lazy('conference_listLV')