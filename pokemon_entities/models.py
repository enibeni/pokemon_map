from django.db import models  # noqa F401


class Pokemon(models.Model):
    title_ru = models.CharField(max_length=200, verbose_name="Название по-русски")
    title_en = models.CharField(max_length=200, blank=True, verbose_name="Название по-английски")
    title_jp = models.CharField(max_length=200, blank=True, verbose_name="Название по-японски")
    description = models.TextField(blank=True, verbose_name="Описание")
    photo = models.ImageField(
        upload_to='pokemons', verbose_name="Изображение")
    previous_evolution = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="next_evolution",
        verbose_name="Из кого эволюционировал")

    def __str__(self):
        return self.title_ru


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name="entities", verbose_name="Покемон")
    lat = models.FloatField(verbose_name="Широта")
    lon = models.FloatField(verbose_name="Долгота")
    appeared_at = models.DateTimeField(null=True, verbose_name="Появился в")
    disappeared_at = models.DateTimeField(null=True, verbose_name="Исчез в")
    level = models.IntegerField(default=50, null=True, blank=True, verbose_name="Уровень")
    health = models.IntegerField(default=50, null=True, blank=True, verbose_name="Здоровье")
    strength = models.IntegerField(default=50, null=True, blank=True, verbose_name="Сила")
    defence = models.IntegerField(default=50, null=True, blank=True, verbose_name="Защита")
    stamina = models.IntegerField(default=50, null=True, blank=True, verbose_name="Выносливость")

    def __str__(self):
        return self.pokemon.title_ru

