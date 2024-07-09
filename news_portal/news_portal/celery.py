import os
from celery import Celery
# В первую очередь мы импортируем библиотеку для взаимодействия с операционной системой и саму библиотеку Celery.

from celery.schedules import crontab

# Второй строчкой мы связываем настройки Django с настройками Celery через переменную окружения.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_portal.settings')


# Далее мы создаем экземпляр приложения Celery и устанавливаем для него файл конфигурации.
app = Celery('news_portal')


# Мы также указываем пространство имен, чтобы Celery сам находил все необходимые
# настройки в общем конфигурационном файле settings.py.
# Он их будет искать по шаблону «CELERY_***».
app.config_from_object('django.conf:settings', namespace='CELERY')


# Последней строчкой мы указываем Celery автоматически искать задания в файлах tasks.py каждого приложения проекта.
app.autodiscover_tasks()


# @app.task(bind=True, ignore_result=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')

# __init__.py
# from .celery import app as celery_app
# __all__ = ('celery_app',)


# Добавление периодических заданий
app.conf.beat_schedule = {
    'weekly_notice': {  # Имя периодической задачи от себя (принято давать осмысленные названия)
        'task': 'subscriptions.tasks.weekly_notice',  # Сама задача, которая будет выполняться
        'schedule': crontab(hour=8, minute=0, day_of_week=1),  # Параметры расписания (можно пользоваться crontab или просто написать целое число - сек)
    },
}
