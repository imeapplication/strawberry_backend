from django.contrib import admin
from .models import Company, Domain, Task, User, Action, Comment

admin.site.register(Company)
admin.site.register(Domain)
admin.site.register(Task)
admin.site.register(User)
admin.site.register(Action)
admin.site.register(Comment)
