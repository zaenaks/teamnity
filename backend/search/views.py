from django.views.generic import ListView # базовий клас CBV для відображення списку об'єктів з бази даних
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.db.models import Case, When, Value, IntegerField #  для анотації пріоритету
from django.db.models.functions import Lower # для сортування без урахування регістру
from accounts.models import UserProfile, Tag
# from teams.models import TeamProfile

User = get_user_model()

# Create your views here.
class SearchView(ListView):
    template_name = 'Search.html'
    context_object_name = 'results'
    paginate_by = 4 # Кількість результатів на сторінку для пагінації
    
    def get_queryset(self):
        query = self.request.GET.get('q', '') # Пошуковий запит нікнейму в вигляді тексту
        search_type = self.request.GET.get('type', '') # Тип пошуку '1' - команди, '2' - користувачі
        selected_tags_ids = self.request.GET.getlist('tags') # Список ID обраних тегів

        if search_type not in ['1', '2']:
            return UserProfile.objects.none()
        
        if not query and not selected_tags_ids:
            if search_type == '2':
                return UserProfile.objects.none()
            elif search_type == '1':
                # return TeamProfile.objects.none() # розкоментувати коли буде модель TeamProfile
                return UserProfile.objects.none() # Тимчасовий заглушка
        
        # пошук користувачів
        if search_type == '2':
            queryset = UserProfile.objects.all()
            if selected_tags_ids:
                for tag_id in selected_tags_ids:
                    queryset = queryset.filter(tags__id = tag_id)
                queryset = queryset.distinct()
            if query:
                queryset = queryset.annotate(
                    priority = Case(
                        When(user__username__iexact = query, then = Value(0)), # 0 - точний збіг 
                        When(user__username__icontains = query,then = Value(1)), # 1 - частковий збіг
                        default=Value(2),
                        output_field=IntegerField()
                    )
                ).filter(
                    Q(user__username__iexact=query) | Q(user__username__icontains = query)
                ).order_by('priority', Lower('user__username'))
            else:
                queryset = queryset.order_by(Lower('user__username'))
            return queryset
        
        # пошук команд
        elif search_type == '1':
            return UserProfile.objects.none()

        return UserProfile.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_tags'] = Tag.objects.all()
        context['current_query'] = self.request.GET.get('q', '')
        context['current_type'] = self.request.GET.get('type', '')
        context['current_tags'] = self.request.GET.getlist('tags')

        return context
