from django.db import models
from django_admin_geomap import GeoItem


class Target(models.Model, GeoItem):  # Модель цели
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name='Название')
    photo = models.ImageField(null=False, blank=False, upload_to="targets/", verbose_name='Фото')
    time = models.DateField(verbose_name='Дедлайн', null=True, blank=True)
    radius = models.FloatField(default=3, verbose_name='Радиус отображения цели (в км)')
    lon = models.FloatField(null=True, blank=True, verbose_name='Центр (долгота)')
    lat = models.FloatField(null=True, blank=True, verbose_name='Центр (широта)')
    if_season = models.BooleanField(default=False, verbose_name='Сезонная')

    def __str__(self):
        return self.name

    @property  # для грамотной работы библиотеки (по документации
    def geomap_longitude(self):
        return '' if self.lon is None else str(self.lon)

    @property  # для грамотной работы библиотеки (по документации
    def geomap_latitude(self):
        return '' if self.lon is None else str(self.lat)

    class Meta:
        verbose_name = 'Цель'
        verbose_name_plural = 'Цели'


class SolutionTarget(models.Model):  # Выполнение цели (readme)
    class Group(models.TextChoices):
        COMPLETE = 'Принято'
        IN_PROGRESS = 'Ожидание'
        FAILED = 'Отклонено'

    relation = models.ForeignKey('relationship.Relation', on_delete=models.CASCADE, related_name='relations',
                                 verbose_name='Отношения')
    target = models.ForeignKey('targets.Target', on_delete=models.CASCADE, related_name='answers',
                               verbose_name='Цель')
    photo = models.ImageField(null=True, blank=True, upload_to="targets/", verbose_name='Фото')
    verdict = models.CharField(choices=Group.choices, default=Group.IN_PROGRESS, max_length=10, verbose_name="Статус")
    desc = models.CharField(max_length=1000, verbose_name="Комментарий к статусу", null=True, blank=True)

    @property  # В альфа версии поля вердикт и описание оказались не нужны,
    # нужно было сделать автоматическое подтвержение выполнения
    def demo_verdict(self):
        if self.photo:
            return self.Group.COMPLETE
        return self.verdict

    class Meta:
        unique_together = ('relation', 'target')
        verbose_name = 'Отправка цели'
        verbose_name_plural = 'Отправка целей'
