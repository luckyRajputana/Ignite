"""WebService1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from restaurant.views import *
from accounts.views import *
from django.views.generic import *
from django.contrib.auth import views as auth_view  
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

router = routers.DefaultRouter()
router.register('api', ListCreateAssemblyView)

urlpatterns = [
    url('api',include(router.urls)),
    url('^login/$', auth_view.LoginView.as_view() , name = 'login'),
    #url('^logout/$', auth_view.logoutView , name = 'logout'),
    url('^signup/$', signup , name = 'signup'),

    
    url('^$', IgniteV2.as_view() , name = 'ignite2'),
    url('admin/', admin.site.urls),
    url('about/', IgniteV2.as_view(), name ='about'),
    url('ignite/', Ignite.as_view(), name ='ignite'),
    url('ignite2/', IgniteV2.as_view(), name ='ignite2'),
    url('ajax/', get_more_tables.as_view(), name ='get_more_tables'),
    
    #url('api', ListCreateAssemblyView.as_view(), name ='post_api'),

    #url(r'^contact/', contact),
    #url(r'^product/', product),
    #url('product/', ProductView.as_view()),
    #url(r'^contact/', TemplateView.as_view(template_name = 'contact.html')),
    #url('contact/', Contact.as_view()),
    #url('redirect/', redirectPage),
    #url(r'^boards/(?P<pk>\d+)/$',Board_view, name='board_topics'),
    #url(r'^boards/(?P<pk>\d+)/new/$',new_topic, name='new_topic'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
]
if settings.DEBUG: 
        urlpatterns += static(settings.STATIC_URL, 
                              document_root=settings.STATICFILES_DIRS) 