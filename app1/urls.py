from django.urls import path
from . import views	# the . indicates that the views file can be found in the same directory as this file
                    
urlpatterns = [
    path('', views.index),    
    path('Home', views.home),  
    path('LoginUser', views.LoginUser),    
    path('Save', views.SaveUser), 
    path('logout',views.logout), 
    path('SavePie', views.SavePie), 
    path('Remove/<int:id>', views.DeletePie), 
    path('Update/<int:id>', views.UpdatePie),
    path('Update', views.UpdatePieData),  
    path('AllPies', views.Allpies), 
    path('Show/<int:id>', views.ShowPie),
    path('Vote', views.Vote),  
]