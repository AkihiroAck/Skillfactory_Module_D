from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver

from django.core.mail import EmailMultiAlternatives

from django.contrib.auth.models import User

from mymodel.models import Post
from subscriptions.models import Subscriptions


@receiver(m2m_changed, sender=Post.category.through)
def update_post_categories(sender, instance, action, **kwargs):
    if action == 'post_add' or action == 'post_changed':
        # instance - объект Post, у которого произошли изменения в поле category
        categories = instance.category.all()
        unique_users = Subscriptions.objects.filter(category__in=categories).values('user').distinct()
        subscribers_with_email = User.objects.filter(id__in=unique_users, email__isnull=False)

        subject = 'Что-то интересное!'
        text_content = f'Новый пост в вашей любимой категории: {instance.title} (http://127.0.0.1:8000{instance.get_absolute_url()})'
        html_content = f'<p>Новый пост в вашей любимой категории: <a href="http://127.0.0.1:8000{instance.get_absolute_url()}">{instance.title}</a></p>'

        for user in subscribers_with_email:
            users_email = [user.email]
            email = EmailMultiAlternatives(subject, text_content, None, users_email)
            email.attach_alternative(html_content, "text/html")
            email.send()
        

m2m_changed.connect(update_post_categories, sender=Post.category.through)
