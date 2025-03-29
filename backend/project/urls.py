from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from strawberry.django.views import GraphQLView, AsyncGraphQLView
from core.schema import schema

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Pour les requêtes synchrones
    path('graphql/', csrf_exempt(GraphQLView.as_view(schema=schema))),
    
    # Pour les requêtes asynchrones (si votre schéma est async)
    path('graphql/async/', csrf_exempt(AsyncGraphQLView.as_view(schema=schema))),
]