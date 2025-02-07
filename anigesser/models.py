from django.db import models
import datetime


class Source(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Источник"
        verbose_name_plural = "Источники"


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Theme(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тема"
        verbose_name_plural = "Темы тайтлов"


class Type(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип"
        verbose_name_plural = "Типы тайтлов"


class Studio(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Студия"
        verbose_name_plural = "Студии"


class Title(models.Model):
    original_name = models.CharField("Оригинальное название", max_length=300, help_text="Оригинальное название, например 'Sousou no Frieren'.")
    description = models.CharField("Описание", max_length=500, help_text="Короткое описание, до 500 символов.")
    image_url = models.URLField("URL обложки", blank=True, max_length=300)
    title_type = models.ForeignKey(Type, on_delete=models.PROTECT, related_name='titles', verbose_name="Тип")
    rating = models.FloatField("Рейтинг", help_text="Дробь от 0 до 10.")
    members = models.PositiveIntegerField("Пользователи", help_text="Количество пользователей у тайтла на MAL.")
    release_date = models.DateField("Дата выхода")
    studios = models.ManyToManyField(Studio, related_name="titles", verbose_name="Студии")
    source = models.ForeignKey(Source, on_delete=models.PROTECT, related_name='titles', verbose_name="Источник")
    genres = models.ManyToManyField(Genre, blank=True, related_name='titles', verbose_name="Жанры")
    themes = models.ManyToManyField(Theme, blank=True, related_name='titles', verbose_name="Темы")

    def __str__(self):
        return f'{self.original_name} - {self.release_date}'

    class Meta:
        ordering = ['-members']
        verbose_name = "Тайтл"
        verbose_name_plural = "Тайтлы"


class TitleName(models.Model):
    name = models.CharField("Альтернативное название", max_length=300, unique=True)
    title = models.ForeignKey(Title,
        on_delete=models.CASCADE,
        related_name='title_names',
        verbose_name="Тайтл",
        help_text="Тайтл, к которому относится это название."
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Название"
        verbose_name_plural = "Названия"


class Screenshots(models.Model):
    first_url = models.URLField("URL адрес первого изображения", max_length=300)
    second_url = models.URLField("URL адрес второго изображения", max_length=300)
    third_url = models.URLField("URL адрес третьего изображения", max_length=300)
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name="screenshots", verbose_name="Тайтл")

    def __str__(self):
        return f'{self.title} - {self.first_url}'

    class Meta:
        order_with_respect_to = "title"
        verbose_name = "Скриншот"
        verbose_name_plural = "Скриншоты"


class Character(models.Model):
    name = models.CharField(max_length=200, verbose_name="Имя персонажа")
    url = models.URLField("URL адрес изображения", max_length=300)
    titles = models.ManyToManyField(Title, related_name="characters", verbose_name="Тайтлы")

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Персонаж"
        verbose_name_plural = "Персонажи"


class Day(models.Model):
    date = models.DateField("Дата")
    screenshots = models.ManyToManyField(Screenshots, blank=True, related_name="days", verbose_name="Скриншоты")
    characters = models.ManyToManyField(Character, blank=True, related_name="days", verbose_name="Персонажи")
    titles = models.ManyToManyField(Title, blank=True, related_name="days", verbose_name="Тайтлы")

    def __str__(self):
        return self.date
    
    class Meta:
        ordering = ['-date']
        verbose_name = "День"
        verbose_name_plural = "Дни"


class Suggestion(models.Model):
    date = models.DateField("Дата", default=datetime.date.today)
    url = models.URLField("URL", max_length=300)
    data = models.CharField("Дополнительно", max_length=500, blank=True)

    def __str__(self):
        return self.url
    
    class Meta:
        ordering = ['-date']
        verbose_name = "Предложение"
        verbose_name_plural = "Предложения"
