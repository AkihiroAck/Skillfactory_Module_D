# from datetime import datetime, timedelta
# import logging
#
# from apscheduler.schedulers.blocking import BlockingScheduler
# from apscheduler.triggers.cron import CronTrigger
# from django.conf import settings
# from django.core.management.base import BaseCommand
# from django_apscheduler import util
# from django_apscheduler.jobstores import DjangoJobStore
#
# from django.core.mail import EmailMultiAlternatives
#
# from django.contrib.auth.models import User
#
# from mymodel.models import Post, Category
# from subscriptions.models import Subscriptions
#
# logger = logging.getLogger(__name__)
#
#
# def my_job():
#     current_time = datetime.now()
#     subscriptions = Subscriptions.objects.select_related('user', 'category').all()
#
#     unique_users = Subscriptions.objects.all().values('user').distinct()  # <QuerySet [{'user': 3}, {'user': 4}]>
#     subscribers_with_email = User.objects.filter(id__in=unique_users, email__isnull=False)  # <QuerySet [<User: user1>, <User: user2>]>
#
#     for user in subscribers_with_email:
#         subscriptions_categories_ids = subscriptions.filter(user=user).values_list('category', flat=True)  # <QuerySet [3, 2, 1, 4]>
#
#         # <QuerySet [<Category: Спорт>, <Category: Политика>, <Category: Биржа>, <Category: Фильмография>]>
#         categories = Category.objects.filter(id__in=subscriptions_categories_ids)
#
#         # Последние 7 дней
#         last_week = current_time - timedelta(days=7)
#
#         # <QuerySet [<Post: title1: "content1" (Статья) Автор: admin>, <Post: title2: "content2" (Новость) Автор: admin>]>
#         new_posts = Post.objects.filter(category__in=categories, creation_time__gte=last_week).distinct()
#
#         if new_posts.exists():
#             # Отправляем электронное письмо
#             subject = 'Новые записи в вашей подписанной категории!'
#             text_content = f'Новые записи в ваших любимых категориях:\n\n'
#             html_content = f'<p>Новые записи в ваших любимых категориях":</p><ul>'
#
#             for post in new_posts:
#                 text_content += f'- {post.title} (http://127.0.0.1:8000{post.get_absolute_url()})\n'
#                 html_content += f'<li><a href="http://127.0.0.1:8000{post.get_absolute_url()}">{post.title}</a></li>'
#
#             html_content += '</ul>'
#
#             to_email = [user.email]
#
#             email = EmailMultiAlternatives(subject, text_content, None, to_email)
#             email.attach_alternative(html_content, "text/html")
#             email.send()
#
#             logger.info(f"Sent email to {user.username} for new posts {post.title}")
#
#
# # The `close_old_connections` decorator ensures that database connections,
# # that have become unusable or are obsolete, are closed before and after your
# # job has run. You should use it to wrap any jobs that you schedule that access
# # the Django database in any way.
# @util.close_old_connections
# class Command(BaseCommand):
#     help = "Runs APScheduler."
#
#     def handle(self, *args, **options):
#         scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
#         scheduler.add_jobstore(DjangoJobStore(), "default")
#
#         scheduler.add_job(
#             my_job,
#             # trigger=CronTrigger(second="*/5"),  # second="*/10" Every 10 seconds
#             trigger=CronTrigger(day_of_week='fri', hour='18', minute='0'),  # Каждую пятницу в 18:00
#             id="my_job",  # The `id` assigned to each job MUST be unique
#             max_instances=1,
#             replace_existing=True,
#         )
#         logger.info("Added job 'my_job'.")
#
#         try:
#             logger.info("Starting scheduler...")
#             scheduler.start()
#         except KeyboardInterrupt:
#             logger.info("Stopping scheduler...")
#             scheduler.shutdown()
#             logger.info("Scheduler shut down successfully!")
#