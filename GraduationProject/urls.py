"""GraduationProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin

from Machine import views as views
from Machine.tree import treePlotter as plot
from Machine import restView as rest
from Machine import clean
from rest_framework.routers import DefaultRouter
from Machine.k import views as k

from django.contrib.auth.views import login, logout_then_login

router = DefaultRouter()
router.register(r'tree', rest.TreeViewSet)
router.register(r'twok', rest.TwoKViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', admin.site.urls),
    url(r'^loginaction/', login, {'template_name': 'login.html'}),
    url(r'^logout/', logout_then_login),
    url(r'^login/', views.login),
    url(r'^$', views.index),
    url(r'^a/$', views.adminIndex),
    url(r'^c4dot5/$', views.C4dot5),
    url(r'^tree_ID3/$', views.treeID3),
    url(r'^tree_labels/$', views.treeLabels),
    url(r'^tree_classify/$', views.treeClassify),

    url(r'^k/$', k.towK),
    url(r'^k_view/$', k.k_view),

    url(r'^cleanTree/$', clean.cleanTree),
    url(r'^cleanK/$', clean.cleanK),
]
