from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView, CreateView, UpdateView, ListView
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Contact


@login_required
def register(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)


@login_required
def profile(request):
    return render(request, 'users/profile.html')


@login_required
def contacts(request):
    context = {'objects': Contact.objects.all()
               }
    return render(request, 'users/contact_list.html', context=context)


class ContactListView(ListView):
    model = Contact
    context_object_name = 'objects'
    ordering = ['contact_name']


class ContactDetailView(DetailView):
    model = Contact


class ContactCreateView(LoginRequiredMixin, CreateView):
    model = Contact
    fields = ['contact_name', 'platform', 'comment', 'location',
              'zone_name', 'utc_offset']

    def form_valid(self, form):
        form.instance.owner = self.request.user  # take current logged in user
        return super().form_valid(form)


class ContactUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Contact
    fields = ['contact_name', 'platform', 'comment', 'location',
              'zone_name', 'utc_offset']

    def form_valid(self, form):
        form.instance.owner = self.request.user  # take current logged in user
        return super().form_valid(form)

    def test_func(self):
        contact = self.get_object()
        if self.request.user == contact.owner:
            return True
        return False
