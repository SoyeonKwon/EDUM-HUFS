from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from notifier.views import HomeView
from django.conf import settings
from django.conf.urls.static import static
#from notifier import views

urlpatterns = [
    path('monitor/', HomeView.as_view()),
    #path('monitor/',views.homeview),
    #path('home/alert.html', AlertView.as_view()),
    path('admin/', admin.site.urls),
    url(r'^', include('notifier.urls')), 
    #path('notifier/', include('notifier.urls')),
]
# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
