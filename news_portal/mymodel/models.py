from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.urls import reverse

TYPE = [
    ('ARTI', 'Статья'),
    ('NEWS', 'Новость'),
]


# Модель Author
# Модель, содержащая объекты всех авторов.
# Имеет следующие поля:
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Связь «один к одному» с встроенной моделью пользователей User
    rating = models.IntegerField(default=0)  # Рейтинг пользователя. Ниже будет дано описание того, как этот рейтинг можно посчитать
    
    # Метод update_rating() модели Author, который обновляет рейтинг текущего автора (метод принимает в качестве аргумента только self).
    # Он состоит из следующего:
    #     суммарный рейтинг каждой статьи автора умножается на 3;
    #     суммарный рейтинг всех комментариев автора;
    #     суммарный рейтинг всех комментариев к статьям автора.
    def update_rating(self):
        all_post = self.post_set.all()
        all_post_ratings = all_post.values_list('rating', flat=True)
        self.rating = sum(all_post_ratings) * 3  # суммарный рейтинг каждой статьи автора умножается на 3
        
        all_comment = self.user.comment_set.all()
        all_comment_ratings = all_comment.values_list('rating', flat=True)
        self.rating += sum(all_comment_ratings)  # суммарный рейтинг всех комментариев автора

        self.rating += sum([sum(i.comment_set.all().values_list('rating', flat=True)) for i in all_post])  # суммарный рейтинг всех комментариев к статьям автора
        
        self.save()
        
    def __str__(self):
        return f'{self.user.username}'

    
# Модель Category
# Категории новостей/статей — темы, которые они отражают (спорт, политика, образование и т. д.).
# Имеет единственное поле:
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)  # Название категории. Поле должно быть уникальным (в определении поля необходимо написать параметр unique = True)
    
    def __str__(self):
        return f'{self.name}'


# Модель Post
# Эта модель должна содержать в себе статьи и новости, которые создают пользователи.
# Каждый объект может иметь одну или несколько категорий.
# Соответственно, модель должна включать следующие поля:
class Post(models.Model):
    authors = models.ForeignKey('Author', on_delete=models.PROTECT)  # связь «один ко многим» с моделью Author
    type = models.CharField(choices=TYPE, max_length=4)  # поле с выбором — «статья» или «новость»
    creation_time = models.DateTimeField(auto_now_add=True)  # автоматически добавляемая дата и время создания
    category = models.ManyToManyField('Category', through='PostCategory')  # связь «многие ко многим» с моделью Category (с дополнительной моделью PostCategory);
    title = models.CharField(max_length=255)  # заголовок статьи/новости
    text = models.TextField()  # текст статьи/новости
    rating = models.IntegerField(default=0)  # рейтинг статьи/новости
    
    # Методы like() и dislike() в моделях Comment и Post, которые увеличивают/уменьшают рейтинг на единицу
    def like(self):
        self.rating += 1
        self.save()
    
    def dislike(self):
        self.rating -= 1
        self.save()
        
    # Метод preview() модели Post, который возвращает начало статьи (предварительный просмотр) длиной 124 символа и добавляет многоточие в конце
    def preview(self):
        return self.text[:124].replace('\n', ' ') + '...'
        
    def __str__(self):
        return f'{self.title[:25]}: "{self.text[:40]}" ({self.get_type_display()}) Автор: {self.authors}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


# Модель PostCategory
# Промежуточная модель для связи «многие ко многим»:
class PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)  # связь «один ко многим» с моделью Post
    category = models.ForeignKey('Category', on_delete=models.PROTECT)  # связь «один ко многим» с моделью Category
    
    def __str__(self):
        return f'[id: {self.post.pk}] {self.post.title[:25]}: "{self.post.text[:40]}" Автор: {self.post.authors} ::: category ::: {self.category}'


# Модель Comment
# Под каждой новостью/статьёй можно оставлять комментарии,
# поэтому необходимо организовать их способ хранения тоже.
# Модель будет иметь следующие поля:
class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)  # связь «один ко многим» с моделью Post
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # связь «один ко многим» со встроенной моделью User (комментарии может оставить любой пользователь, необязательно автор)
    text = models.TextField()  # текст комментария
    creation_time = models.DateTimeField(auto_now_add=True)  # дата и время создания комментария
    rating = models.IntegerField(default=0)  # рейтинг комментария
    
    # Методы like() и dislike() в моделях Comment и Post, которые увеличивают/уменьшают рейтинг на единицу
    def like(self):
        self.rating += 1
        self.save()
    
    def dislike(self):
        self.rating -= 1
        self.save()
    
    def __str__(self):
        return f'{self.user.username}: {self.text} [{self.creation_time}] to {self.post}'
