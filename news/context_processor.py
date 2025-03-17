from .models import News
from .models import Category
def latest_news(request):
    latest_news = News.published.all().order_by('-publish_time')[:2]
    
    context = {
        'latest_news': latest_news
    }

    return context
def categories_processor(request):
    return {'categories': Category.objects.all()}