from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, redirect

from .forms import LoginForm
from django.contrib.auth import get_user_model

User = get_user_model()

# @method_decorator(login_required, name='dispatch')
# class ProfileListView(PermissionRequiredMixin, View):
#     permission_required = 'account.view_profile'

#     def get(self, request):
#         user = request.user
#         workplaces = user.profile.workplaces_tab
#         users = User.objects.filter(is_active=True)
#         workplace_active = user.profile.workplace_active
#         profiles = Profile.objects.filter(user__in=users).filter(
#             workplace=workplace_active)
#         emp_position = EMPLOYEE_POSITION
#         form_pswd = PasswordChangeForm()
#         ctx = {
#             'q': -1,
#             'user': user,
#             'profiles': profiles,
#             'emp_position': emp_position,
#             'workplaces': workplaces,
#             'workplace_active': workplace_active,
#             'form_pswd': form_pswd
#         }
#         return render(request, "account/profile_list.html", ctx)

#     def post(self, request):
#         emp_position = EMPLOYEE_POSITION
#         user = request.user
#         users = User.objects.filter(is_active=True)
#         q = request.POST.get('q')
#         drivers = False
#         if 'driver_permission' in request.POST:
#             drivers = True
#             q = 4
#             driver_permission = request.POST.get('driver_permission')
#             driver = Profile.objects.get(pk=request.POST.get('driver_id'))
#             if str(driver_permission) == "True":
#                 driver.day_permission = datetime.now().date()
#             else:
#                 driver.day_permission = None
#             driver.save()
#             profiles = Profile.objects.filter(user__in=users).filter(
#                 worker_position=q).order_by('user')

#         if 'workers' in request.POST:
#             q = int(request.POST.get('q'))

#         if q == -1:
#             profiles = Profile.objects.filter(user__in=users).order_by('user')
#         else:
#             profiles = Profile.objects.filter(user__in=users).filter(
#                 worker_position=q).order_by('user')
#         if int(q) == 4:
#             drivers = True
#         form_pswd = PasswordChangeForm(request.POST)
#         ctx = {
#             'q': int(q),
#             'drivers': drivers,
#             'user': user,
#             'profiles': profiles,
#             'form_pswd': form_pswd,
#             'emp_position': emp_position,
#         }
#         return render(request, "account/profile_list.html", ctx)

# @method_decorator(login_required, name='dispatch')
# class ProfileListView(PermissionRequiredMixin, ListView):
#     permission_required = 'account.view_profile'
#     model = Profile
#     paginate_by = 1

#     def get_context_data(self, **kwargs):
#         context = super(ProfileListView, self).get_context_data(**kwargs)
#         workplaces = self.user.profile.workplaces_tab
#         users = User.objects.filter(is_active=True)
#         workplace_active = self.user.profile.workplace_active
#         profiles = Profile.objects.filter(user__in=users).filter(
#             workplace=workplace_active)
#         paginator = Paginator(profiles, self.paginate_by)
#         page = self.request.GET.get('page')
#         try:
#             profiles = paginator.page(page)
#         except PageNotAnInteger:
#             profiles = paginator.page(1)
#         except EmptyPage:
#             profiles = paginator.page(paginator.num_pages)
#         context['profiles'] = profiles
#         context['form_pswd'] = PasswordChangeForm()
#         return context

# @method_decorator(login_required, name='dispatch')
# class AddProfileView(PermissionRequiredMixin, View):
#     permission_required = 'account.add_profile'

#     def get(self, request, pk):
#         position = EMPLOYEE_POSITION[pk]
#         form_u = UserForm()
#         form_p = ProfileForm(initial={'worker_position': position})
#         ctx = {'form_u': form_u, 'form_p': form_p}
#         return render(request, "account/profile_form.html", ctx)

#     def post(self, request, pk):
#         position = EMPLOYEE_POSITION[pk]
#         form_u = UserForm(request.POST)
#         form_p = ProfileForm(request.POST)
#         form_pswd = PasswordChangeForm(request.POST)
#         if form_u.is_valid() and form_p.is_valid():
#             user = form_u.save(commit=False)
#             user.set_password(form_u.cleaned_data['password'])
#             user.is_active = True
#             user.save()
#             user.groups.add(form_u.cleaned_data['group'])
#             user.save()
#             profile = form_p.save(commit=False)
#             profile.user = user
#             profile.worker_position = position[0]
#             profile.save()
#             profile.worker_position = pk
#             profile.workplace.set(form_p.cleaned_data['workplace'])
#             profile.save()

#             messages.error(request, 'Utworzono konto użytkownika')
#             return redirect('profile_list')
#         else:
#             messages.error(request, 'Wystąpił błąd')
#             ctx = {'form_u': form_u, 'form_p': form_p, 'form_pswd': form_pswd}
#             return render(request, "account/profile_form.html", ctx)

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
            username = form.cleaned_data['username']
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
