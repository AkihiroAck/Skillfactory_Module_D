from celery import shared_task
from datetime import datetime, timedelta

from django.core.mail import EmailMultiAlternatives

from .models import Subscriptions
from mymodel.models import Post, Category
from django.contrib.auth.models import User


@shared_task
def notice_of_creation(post_id):
    post = Post.objects.get(id=post_id)
    
    categories = post.category.all()
    unique_users = Subscriptions.objects.filter(category__in=categories).values('user').distinct()
    subscribers_with_email = User.objects.filter(id__in=unique_users, email__isnull=False)

    subject = 'Что-то интересное!'
    text_content = f'Новый пост в вашей любимой категории: {post.title} (http://127.0.0.1:8000{post.get_absolute_url()})'
    html_content = f'<p>Новый пост в вашей любимой категории: <a href="http://127.0.0.1:8000{post.get_absolute_url()}">{post.title}</a></p>'

    for user in subscribers_with_email:
        users_email = [user.email]
        email = EmailMultiAlternatives(subject, text_content, None, users_email)
        email.attach_alternative(html_content, "text/html")
        email.send()
    

@shared_task
def weekly_notice():
    current_time = datetime.now()
    subscriptions = Subscriptions.objects.select_related('user', 'category').all()

    unique_users = Subscriptions.objects.all().values('user').distinct()  # <QuerySet [{'user': 3}, {'user': 4}]>
    subscribers_with_email = User.objects.filter(id__in=unique_users, email__isnull=False)  # <QuerySet [<User: user1>, <User: user2>]>

    for user in subscribers_with_email:
        subscriptions_categories_ids = subscriptions.filter(user=user).values_list('category', flat=True)  # <QuerySet [3, 2, 1, 4]>
    
        # <QuerySet [<Category: Спорт>, <Category: Политика>, <Category: Биржа>, <Category: Фильмография>]>
        categories = Category.objects.filter(id__in=subscriptions_categories_ids)
    
        # Последние 7 дней
        last_week = current_time - timedelta(days=7)
    
        # <QuerySet [<Post: title1: "content1" (Статья) Автор: admin>, <Post: title2: "content2" (Новость) Автор: admin>]>
        new_posts = Post.objects.filter(category__in=categories, creation_time__gte=last_week).distinct()
    
        if new_posts.exists():
            # Отправляем электронное письмо
            subject = 'Новые записи в вашей подписанной категории!'
            text_content = f'Новые записи в ваших любимых категориях:\n\n'
            html_content = f'<p>Новые записи в ваших любимых категориях":</p><ul>'

            for post in new_posts:
                text_content += f'- {post.title} (http://127.0.0.1:8000{post.get_absolute_url()})\n'
                html_content += f'<li><a href="http://127.0.0.1:8000{post.get_absolute_url()}">{post.title}</a></li>'

            html_content += '</ul>'

            to_email = [user.email]

            email = EmailMultiAlternatives(subject, text_content, None, to_email)
            email.attach_alternative(html_content, "text/html")
            email.send()
