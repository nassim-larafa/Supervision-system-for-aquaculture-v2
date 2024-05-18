from django.urls import path
from . import views
from django.contrib.auth import views as mdp
from django.conf import settings
from django.conf.urls.static import static  # Import static here

urlpatterns=[
    path('',views.connectas,name='connectas'),
    path('client/',views.connectasclient,name='connectasclient'),
    path('supervisor/',views.connectassupervisor,name='connectassupervisor'),
    path('reset_password/', mdp.PasswordResetView.as_view(template_name='password_reset.html'), name="password_reset"),
    path('reset_password_done/', mdp.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', mdp.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset_password_complete/', mdp.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('_<str:pk>/',views.compte,name='compte'),
    path('<str:variable>/add_client/<str:pseudo>', views.compte, name='add_client'),
    path('sup_<str:pseudo>/Projects_List/', views.projectList, name='projectList'),
    path('sup_<str:pseud>/p<int:idd>/add_client/2', views.add_client, name='add_client'),
    path('sup_<str:pseudo>/add_project/1', views.add_project, name='add_project'),
    path('sup_<str:pseudo>/p<int:id>/add_polygs/3', views.add_polygones, name='add_polygones'),
    
    path('sup_<str:pseudo>/display_plots/<int:id>/', views.display_polygone, name='display_polygone'),
    path('sup_<str:pseudo>/p<int:id>/add_node/5', views.add_node, name='addnode'),
    path('sup_<str:pseudo>/p_<int:id>/add_cage/4', views.addcage, name='addcage'),
    path('sup_<str:pseudo>/p_<int:iid>/last_node', views.all_node, name='all'),
   
    path('sup_<str:pseudo>/p_<int:id>/modification', views.ALL, name='ALL_node'),
    path('sup_<str:pseudo>/p_<int:id>/supervision', views.final, name='final'),
    path('sup_<str:pseudo>/p_<int:id>/node_detail/n_<int:idnode>', views.final2, name='final2'),
    path('sup_<str:pseudo>/p_<int:id>/node_locate/n_<int:idnode>', views.final3, name='final3'),
    

  
    path('update_distance/<int:id>/', views.update_distance, name='update_distance'),
    path('update_color/<int:id>/', views.update_color, name='update_color'),
    #path('update/<int:id>/', views.start_mqtt, name='update'),
    
    path('sup_<str:pseudo>/delete/<int:id>/', views.delete_project, name='delete_project'),
    path('sup_<str:pseudo>/modify_1/<int:id>/', views.modify_1, name='modify_1'),
    path('sup_<str:pseudo>/modify_2/<int:id>/', views.modify_2, name='modify_2'),
    path('sup_<str:pseudo>/modify_3/<int:id>/', views.modify_3, name='modify_3'),
    

    #------------partie client--------------------------------------#
    path('interface/<str:pseudo>/<int:id>/', views.interface_c, name='interface_c'),
    path('Client_<str:pseudo>/', views.client_project, name='client_project'),
    path('<int:id>/Client_<str:pseudo>/', views.clientd, name='clientd'),
    path('<int:id>/Client_<str:pseudo>/nodes', views.clientn, name='clientn'),
    path('sup_<str:pseudo>/p_<int:id>/locate/n_<int:idnode>', views.locate, name='locate'),
    path('sup_<str:pseudo>/p_<int:id>/details/n_<int:idnode>', views.details, name='details'),



#you need to add configurations to serve media files during development. This is crucial because Django does not serve media files in production environments; they should be handled by a web server like Nginx or Apache.

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



