from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.views.generic.edit \
    import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, UserForm, BusinessForm, AddressBasketForm
from products.models import Category
from django.contrib.auth import get_user_model
from .models import Profile, Address

User = get_user_model()


class ChoiceAccountReqisterView(View):
    def get(self, request):
        categorys = Category.objects.filter(is_active=True)
        form = LoginForm()
        ctx = {'form': form, 'categorys': categorys}
        return render(request, "account/choice_account_register.html", ctx)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                # token = Token.objects.get_or_create(user=user)
                login(request, user)
                return redirect('order_details')
            else:
                messages.error(request, 'Błędne hasło lub login')
                ctx = {'form': form}
                return render(request, "account/choice_account_register.html",
                              ctx)
        else:
            messages.error(request, 'Błędne hasło lub login')
            ctx = {'form': form}
            return render(request, "account/choice_account_register.html", ctx)


# @method_decorator(login_required, name='dispatch')
class AddClientFromBasketView(View):
    def get(self, request):
        form = UserForm()
        categorys = Category.objects.filter(is_active=True)
        ctx = {'form': form, 'categorys': categorys}
        return render(request, "account/register_user.html", ctx)

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['email']
            new_user.email = form.cleaned_data['email']
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            profile = Profile()
            profile.user_id = new_user.id
            profile.phone_number = form.cleaned_data['phone_number']
            profile.save()
            login(request, new_user)
            messages.error(request, 'Utworzono konto')
            return redirect('cart_details')
        else:
            messages.error(request, 'Wystąpił błąd')
            categorys = Category.objects.filter(is_active=True)
            ctx = {'form': form, 'categorys': categorys}
            return render(request, "account/register_user.html", ctx)


class AddBusinessClientFromBasketView(View):
    def get(self, request):
        form = BusinessForm()
        categorys = Category.objects.filter(is_active=True)
        ctx = {'form': form, 'categorys': categorys}
        return render(request, "account/register_business.html", ctx)

    def post(self, request):
        form = BusinessForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['email']
            new_user.email = form.cleaned_data['email']
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            profile = Profile()
            profile.user_id = new_user.id
            profile.business_name = form.cleaned_data['business_name']
            profile.business_name_l = form.cleaned_data['business_name_l']
            profile.phone_number = form.cleaned_data['phone_number']
            profile.nip_number = form.cleaned_data['nip_number']
            profile.company = True
            profile.save()
            login(request, new_user)
            messages.error(request, 'Utworzono konto')
            return redirect('cart_details')
        else:
            messages.error(request, 'Wystąpił błąd')
            categorys = Category.objects.filter(is_active=True)
            ctx = {'form': form, 'categorys': categorys}
            return render(request, "account/register_business.html", ctx)


# @method_decorator(login_required, name='dispatch')
# class ChangeOnlyPasswordView(View):
#     permission_required = 'account.add_profile'

#     def get(self, request, pk):
#         profile = Profile.objects.get(pk=pk)
#         form_pswd = PasswordChangeForm()
#         ctx = {'form_pswd': form_pswd, 'profile': profile}
#         return render(request, "account/change_only_password.html", ctx)

#     def post(self, request, pk):
#         form_pswd = PasswordChangeForm(request.POST)
#         profile = Profile.objects.get(pk=pk)
#         user = User.objects.get(pk=profile.user.id)
#         if form_pswd.is_valid():
#             user.set_password(form_pswd.cleaned_data['password'])
#             user.save()
#             messages.error(request, 'Hasło zostało zmienione')
#             return redirect('profile_list')
#         else:
#             messages.error(request, 'Wystąpił błąd')
#             ctx = {'form_pswd': form_pswd, 'profile': profile}
#             return render(request, "account/change_only_password.html", ctx)

# @method_decorator(login_required, name="dispatch")
# class UpdateUserView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
#     permission_required = "account.change_user"
#     model = User
#     # fields = "__all__"
#     form_class = UserProfileForm
#     template_name_suffix = "_update_form"
#     success_url = reverse_lazy("profile_list")
#     success_message = 'Zaktualizowano konto użytkownika'

# @method_decorator(login_required, name="dispatch")
# class UpdateProfileView(PermissionRequiredMixin, SuccessMessageMixin,
#                         UpdateView):
#     permission_required = "account.change_profile"
#     model = Profile
#     # fields = "__all__"
#     form_class = ProfileForm
#     template_name_suffix = "_update_form"
#     success_url = reverse_lazy("profile_list")
#     success_message = 'Zaktualizowano profil użytkownika'

#     # def form_valid(self, form):
#     #     form.instance.user = SubCategory.objects.get(
#     #         pk=self.kwargs.get('pk'))
#     #     return super().form_valid(form)

# @method_decorator(login_required, name="dispatch")
# class DeleteProfileView(PermissionRequiredMixin, SuccessMessageMixin,
#                         DeleteView):
#     permission_required = "account.delete_profile"
#     model = Profile
#     fields = "__all__"
#     template_name_suffix = "_confirm_delete"
#     success_url = reverse_lazy("profile_list")
#     success_message = 'Usunięto konto'

#     def delete(self, request, *args, **kwargs):
#         messages.success(self.request, self.success_message)
#         return super(DeleteProfileView, self).delete(request, *args, **kwargs)


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        ctx = {'form': form}
        return render(request, "registration/login.html", ctx)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # token = Token.objects.get_or_create(user=user)
                login(request, user)
                return redirect('welcome')
            else:
                messages.error(request, 'Błędne hasło lub login')
                ctx = {'form': form}
                return render(request, "registration/login.html", ctx)
        else:
            messages.error(request, 'Błędne hasło lub login')
            ctx = {'form': form}
            return render(request, "registration/login.html", ctx)


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('welcome')


@method_decorator(login_required, name='dispatch')
class AddAddressBasketView(SuccessMessageMixin, CreateView):

    model = Address
    form_class = AddressBasketForm

    success_message = 'Dodano adres klienta'
    success_url = ("")

    def get_initial(self, *args, **kwargs):
        initial = super(AddAddressBasketView, self).get_initial(**kwargs)
        initial['user'] = self.request.user
        return initial

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user_id = self.request.user
        self.object.save()
        print(form.instance.user_id, )
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self, *args, **kwargs):
        return reverse('order_details')


@method_decorator(login_required, name='dispatch')
class UpdateAddressBasketView(SuccessMessageMixin, UpdateView):

    model = Address
    form_class = AddressBasketForm
    template_name_suffix = "_update_form"
    success_message = 'Dodano adres klienta'
    success_url = ("")

    def get_initial(self, *args, **kwargs):
        initial = super(UpdateAddressBasketView, self).get_initial(**kwargs)
        initial['user'] = self.request.user
        return initial

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user_id = self.request.user
        self.object.save()
        print(form.instance.user_id, )
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self, *args, **kwargs):
        return reverse('order_details')