from django.db import models  # noqa F401


# your models here
class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='pokemons', blank=True, null=True)

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    lat = models.FloatField()
    lon = models.FloatField()
    appeared_at = models.DateTimeField(null=True)
    disappeared_at = models.DateTimeField(null=True)
    level = models.IntegerField(default=50, null=True, blank=True,)
    health = models.IntegerField(default=50, null=True, blank=True,)
    strength = models.IntegerField(default=50, null=True, blank=True,)
    defence = models.IntegerField(default=50, null=True, blank=True,)
    stamina = models.IntegerField(default=50, null=True, blank=True,)

