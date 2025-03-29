import strawberry
from typing import List, Optional, TYPE_CHECKING
from datetime import date, datetime
import strawberry_django
from django.db.models import QuerySet
from asgiref.sync import sync_to_async

# Import models
from .models import Company, Domain, Task, User, Action, Comment

# Use forward references to avoid circular import issues
if TYPE_CHECKING:
    from .models import Domain as DomainModel
    from .models import Task as TaskModel
    from .models import User as UserModel
    from .models import Company as CompanyModel
    from .models import Action as ActionModel
    from .models import Comment as CommentModel

@strawberry_django.type(User)
class UserType:
    id: strawberry.ID
    first_name: str
    last_name: str
    role: str

@strawberry_django.type(Company)
class CompanyType:
    id: strawberry.ID
    name: str
    logo: Optional[str] = None
    
    @strawberry.field
    async def domains(self, root: 'CompanyModel') -> List['DomainType']:
        get_domains = sync_to_async(lambda: list(root.domains.all()))
        return await get_domains()

@strawberry_django.type(Domain)
class DomainType:
    id: strawberry.ID
    title: str
    description: Optional[str] = None
    document_link: Optional[str] = None
    
    @strawberry.field
    async def responsible(self, root: 'DomainModel') -> Optional[UserType]:
        get_responsible = sync_to_async(lambda: root.responsible)
        return await get_responsible()

    start_date: date
    end_date: date
    mandays: float
    
    @strawberry.field
    async def tasks(self, root: 'DomainModel') -> List['TaskType']:
        get_tasks = sync_to_async(lambda: list(root.tasks.all()))
        return await get_tasks()

@strawberry_django.type(Task)
class TaskType:
    id: strawberry.ID
    title: str
    description: Optional[str] = None
    document_link: Optional[str] = None
    start_date: date
    end_date: date
    mandays: float
    status: int
    
    @strawberry.field
    async def owner(self, root: 'TaskModel') -> Optional[UserType]:
        get_owner = sync_to_async(lambda: root.owner)
        return await get_owner()

    @strawberry.field
    async def subtasks(self, root: 'TaskModel') -> Optional[List['TaskType']]:
        get_subtasks = sync_to_async(lambda: list(root.subtasks.all()) if root.subtasks.exists() else None)
        return await get_subtasks()

    @strawberry.field
    async def actions(self, root: 'TaskModel') -> Optional[List['ActionType']]:
        get_actions = sync_to_async(lambda: list(root.actions.all()) if root.actions.exists() else None)
        return await get_actions()

@strawberry_django.type(Action)
class ActionType:
    id: strawberry.ID
    title: str
    description: Optional[str] = None
    status: int
    start_date: date
    end_date: Optional[date] = None
    
    @strawberry.field
    async def discussion(self, root: 'ActionModel') -> Optional[List['CommentType']]:
        get_discussion = sync_to_async(lambda: list(root.discussion.all()) if root.discussion.exists() else None)
        return await get_discussion()

@strawberry_django.type(Comment)
class CommentType:
    id: strawberry.ID
    
    @strawberry.field
    async def user(self, root: 'CommentModel') -> UserType:
        get_user = sync_to_async(lambda: root.user)
        return await get_user()
    
    date: datetime
    text: str
    document_link: Optional[str] = None

@strawberry.type
class Query:
    @strawberry.field
    async def companies(self) -> List[CompanyType]:
        get_companies = sync_to_async(lambda: list(Company.objects.all()))
        return await get_companies()

    @strawberry.field
    async def company(self, id: strawberry.ID) -> Optional[CompanyType]:
        get_company = sync_to_async(lambda: Company.objects.filter(id=id).first())
        return await get_company()

    @strawberry.field
    async def domains(self) -> List[DomainType]:
        get_domains = sync_to_async(lambda: list(Domain.objects.all()))
        return await get_domains()

    @strawberry.field
    async def domain(self, id: strawberry.ID) -> Optional[DomainType]:
        get_domain = sync_to_async(lambda: Domain.objects.filter(id=id).first())
        return await get_domain()

    @strawberry.field
    async def tasks(self) -> List[TaskType]:
        get_tasks = sync_to_async(lambda: list(Task.objects.filter(parent_task__isnull=True)))
        return await get_tasks()

    @strawberry.field
    async def task(self, id: strawberry.ID) -> Optional[TaskType]:
        get_task = sync_to_async(lambda: Task.objects.filter(id=id).first())
        return await get_task()

    @strawberry.field
    async def users(self) -> List[UserType]:
        get_users = sync_to_async(lambda: list(User.objects.all()))
        return await get_users()

    @strawberry.field
    async def user(self, id: strawberry.ID) -> Optional[UserType]:
        get_user = sync_to_async(lambda: User.objects.filter(id=id).first())
        return await get_user()

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_user(
        self,
        first_name: str,
        last_name: str,
        role: str
    ) -> UserType:
        create_user_func = sync_to_async(
            lambda: User.objects.create(
                first_name=first_name,
                last_name=last_name,
                role=role
            )
        )
        return await create_user_func()

    @strawberry.mutation
    async def create_company(self, name: str, logo: Optional[str] = None) -> CompanyType:
        create_company_func = sync_to_async(
            lambda: Company.objects.create(name=name)
        )
        return await create_company_func()

    @strawberry.mutation
    async def create_domain(
        self, 
        company_id: strawberry.ID, 
        title: str, 
        responsible_id: strawberry.ID,
        start_date: date,
        end_date: date,
        description: Optional[str] = None,
        document_link: Optional[str] = None
    ) -> DomainType:
        create_domain_func = sync_to_async(
            lambda: Domain.objects.create(
                company_id=company_id,
                title=title,
                responsible_id=responsible_id,
                start_date=start_date,
                end_date=end_date,
                description=description or '',
                document_link=document_link or ''
            )
        )
        return await create_domain_func()

    @strawberry.mutation
    async def create_task(
        self,
        title: str,
        owner_id: strawberry.ID,
        start_date: date,
        end_date: date,
        domain_id: Optional[strawberry.ID] = None,
        parent_task_id: Optional[strawberry.ID] = None,
        description: Optional[str] = None,
        document_link: Optional[str] = None,
        mandays: float = 0
    ) -> TaskType:
        create_task_func = sync_to_async(
            lambda: Task.objects.create(
                title=title,
                owner_id=owner_id,
                start_date=start_date,
                end_date=end_date,
                domain_id=domain_id,
                parent_task_id=parent_task_id,
                description=description or '',
                document_link=document_link or '',
                mandays=mandays
            )
        )
        return await create_task_func()
        
    @strawberry.mutation
    async def create_action(
        self,
        task_id: strawberry.ID,
        title: str,
        status: int,
        start_date: date,
        description: Optional[str] = None,
        end_date: Optional[date] = None
    ) -> ActionType:
        create_action_func = sync_to_async(
            lambda: Action.objects.create(
                task_id=task_id,
                title=title,
                status=status,
                start_date=start_date,
                description=description or '',
                end_date=end_date
            )
        )
        return await create_action_func()
        
    @strawberry.mutation
    async def create_comment(
        self,
        action_id: strawberry.ID,
        user_id: strawberry.ID,
        text: str,
        document_link: Optional[str] = None
    ) -> CommentType:
        create_comment_func = sync_to_async(
            lambda: Comment.objects.create(
                action_id=action_id,
                user_id=user_id,
                text=text,
                document_link=document_link or ''
            )
        )
        return await create_comment_func()

    @strawberry.mutation
    async def update_task_status(
        self,
        task_id: strawberry.ID,
        status: int
    ) -> TaskType:
        update_task_status_func = sync_to_async(
            lambda: Task.objects.get(id=task_id)
        )
        task = await update_task_status_func()
        
        def save_task():
            task.status = status
            task.save()
            return task
        
        save_task_func = sync_to_async(save_task)
        return await save_task_func()

# Create the schema
schema = strawberry.Schema(query=Query, mutation=Mutation)
