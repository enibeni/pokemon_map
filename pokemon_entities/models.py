from django.db import models  # noqa F401


# your models here
class Pokemon(models.Model):
    title_ru = models.CharField(max_length=200, null=True)
    title_en = models.CharField(max_length=200, null=True, blank=True)
    title_jp = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    photo = models.ImageField(upload_to='pokemons', blank=True, null=True)
    previous_evolution = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title_ru


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name="entities")
    lat = models.FloatField()
    lon = models.FloatField()
    appeared_at = models.DateTimeField(null=True)
    disappeared_at = models.DateTimeField(null=True)
    level = models.IntegerField(default=50, null=True, blank=True)
    health = models.IntegerField(default=50, null=True, blank=True)
    strength = models.IntegerField(default=50, null=True, blank=True)
    defence = models.IntegerField(default=50, null=True, blank=True)
    stamina = models.IntegerField(default=50, null=True, blank=True)

