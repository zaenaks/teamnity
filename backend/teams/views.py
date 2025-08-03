from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from .models import Team, TeamMembership
from .forms import TeamForm
from accounts.models import Tag
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.db.models import F
from django.db.models import Case, When, Value, IntegerField # Додати для складного сортування
from django.db.models.functions import Lower # Для сортування без урахування регістру

User = get_user_model()

# Create your views here.
class TeamListView(LoginRequiredMixin, ListView):
    model = Team
    template_name = 'Teams.html'
    context_object_name = 'all_user_teams_except_owned'
    paginate_by = 4

    def get_queryset(self):
        user = self.request.user
        # повертає команди членом яких є користувач, але не власником
        queryset = Team.objects.filter(memberships__user=user).exclude(owner=user).order_by('name').distinct()

        query = self.request.GET.get('q', '')
        selected_tags_ids = self.request.GET.getlist('tags')

        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(description__icontains=query) | Q(location__icontains=query)
            ).distinct()
            
        if selected_tags_ids:
            for tag_id in selected_tags_ids:
                queryset = queryset.filter(tags__id=tag_id)
            queryset = queryset.distinct()

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        owned_teams_queryset = Team.objects.filter(owner=user).order_by('name')
        
        my_teams_paginate_by = self.paginate_by
        my_teams_paginator = Paginator(owned_teams_queryset, my_teams_paginate_by)
        my_teams_page_number = self.request.GET.get('my_teams_page')
        my_teams_page_obj = my_teams_paginator.get_page(my_teams_page_number)

        context['owned_teams_page_obj'] = my_teams_page_obj
        context['owned_teams_is_paginated'] = my_teams_page_obj.has_other_pages()

        context['all_tags'] = Tag.objects.all()
        context['current_query'] = self.request.GET.get('q', '')
        context['current_tags'] = self.request.GET.getlist('tags')

        return context
    

class TeamDetailView(LoginRequiredMixin, DetailView):
    model = Team
    template_name = 'Team profile.html'
    context_object_name = 'team'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = self.get_object()
        user = self.request.user

        context['is_owner'] = (user == team.owner)
        context['is_member'] = TeamMembership.objects.filter(team=team, user=user).exists()

        all_memberships_queryset = TeamMembership.objects.filter(team=team)\
            .select_related('user__userprofile')\
            .annotate(
                sort_priority=Case(
                    When(user=team.owner, then=Value(0)),
                    When(user=user, then=Value(1)),
                    default=Value(2),
                    output_field=IntegerField()
                )
            ).order_by('sort_priority', Lower('user__username'))
        
        paginator = Paginator(all_memberships_queryset, 4)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['is_paginated'] = page_obj.has_other_pages()
        context['page_obj'] = page_obj

        return context
    

class TeamCreateView(LoginRequiredMixin, CreateView):
    model = Team
    form_class = TeamForm
    template_name = 'Create team.html'
    success_url = reverse_lazy('teams:teams')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form) 
        TeamMembership.objects.create(team=self.object, user=self.request.user, role='owner')
        messages.success(self.request, f"Команда '{self.object.name}' успішно створена!")
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = "Створити команду"
        return context
    

class TeamUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Team
    form_class = TeamForm
    template_name = 'Create team.html'
    context_object_name = 'team'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Команда '{self.object.name}' успішно оновлена!")
        return response

    def get_success_url(self):
        return reverse_lazy('teams:team_profile', kwargs={'pk': self.object.pk})
    
    def test_func(self):
        team = self.get_object()
        return self.request.user == team.owner
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = "Редагувати команду"    
        return context
    

# класи для управління членством (Class-Based RedirectViews)
class TeamJoinView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('teams:team_profile', kwargs={'pk': self.kwargs['pk']})

    def post(self, request, *args, **kwargs):
        team_pk = self.kwargs['pk']
        team = get_object_or_404(Team, pk=team_pk)
        user = self.request.user

        if TeamMembership.objects.filter(team=team, user=user).exists():
            messages.info(self.request, "Ви вже є членом цієї команди.")
        elif not team.is_public:
            messages.error(self.request, "Ця команда не є публічною і до неї неможливо приєднатися напряму.")
        else:
            TeamMembership.objects.create(team=team, user=user, role='member')
            messages.success(self.request, f"Ви успішно приєдналися до команди '{team.name}'.")
        
        return super().post(request, *args, **kwargs)
    

class TeamLeaveView(LoginRequiredMixin, UserPassesTestMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('teams:teams') 
    
    def post(self, request, *args, **kwargs):
        team_pk = self.kwargs['pk']
        team = get_object_or_404(Team, pk=team_pk)
        user = self.request.user

        try:
            membership = TeamMembership.objects.get(team=team, user=user)
            if membership.role == 'owner':
                messages.error(self.request, "Власник не може покинути команду.")
            else:
                membership.delete()
                messages.success(self.request, f"Ви покинули команду '{team.name}'.")
        except TeamMembership.DoesNotExist:
            messages.error(self.request, "Ви не є членом цієї команди.")
        
        return super().post(request, *args, **kwargs)
    
    def test_func(self):
        team_pk = self.kwargs['pk']
        team = get_object_or_404(Team, pk=team_pk)
        return TeamMembership.objects.filter(team=team, user=self.request.user).exists()


class TeamRemoveMemberView(LoginRequiredMixin, UserPassesTestMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('teams:team_profile', kwargs={'pk': self.kwargs['team_pk']})

    def post(self, request, *args, **kwargs):
        team_pk = self.kwargs['team_pk']
        member_pk = self.kwargs['member_pk']
        team = get_object_or_404(Team, pk=team_pk)
        member_user = get_object_or_404(User, pk=member_pk)

        if member_user == team.owner:
            messages.error(self.request, "Ви не можете видалити власника команди.")
        else:
            try:
                membership = TeamMembership.objects.get(team=team, user=member_user)
                membership.delete()
                messages.success(self.request, f"Користувач '{member_user.username}' видалений з команди '{team.name}'.")
            except TeamMembership.DoesNotExist:
                messages.error(self.request, "Цей користувач не є членом цієї команди.")

        return super().post(request, *args, **kwargs)

    def test_func(self):
        team = get_object_or_404(Team, pk=self.kwargs['team_pk'])
        return self.request.user == team.owner
    

class TeamDeleteView(LoginRequiredMixin, UserPassesTestMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('teams:teams')
    
    def post(self, request, *args, **kwargs):
        team_pk = self.kwargs['pk']
        team = get_object_or_404(Team, pk=team_pk)

        try:
            team_name = team.name
            team.delete()
            messages.success(self.request, f"Команда '{team_name}' успішно видалена.")
        except Exception as e:
            messages.error(self.request, f"Сталася помилка при видаленні команди: {e}")

        return super().post(request, *args, **kwargs)
    
    def test_func(self):
        team = get_object_or_404(Team, pk=self.kwargs['pk'])
        return self.request.user == team.owner