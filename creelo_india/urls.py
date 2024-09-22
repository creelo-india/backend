
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('accounts.urls')),
    path('master-config/',include('master_config.urls')),
    path('api/',include('creelo_app.urls')),

]
 