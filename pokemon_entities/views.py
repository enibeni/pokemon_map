import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from .models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemon_entities = PokemonEntity.objects.all()

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.photo.url)
        )

    pokemons_on_page = []
    pokemons = Pokemon.objects.all()
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.photo.url),
            'title_ru': pokemon.title_ru,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    serialized_pokemon = Pokemon.objects.get(id=pokemon_id)

    pokemon_info = {
        "pokemon_id": serialized_pokemon.id,
        "title_ru": serialized_pokemon.title_ru,
        "title_en": serialized_pokemon.title_en,
        "title_jp": serialized_pokemon.title_jp,
        "description": serialized_pokemon.description,
        "img_url": request.build_absolute_uri(serialized_pokemon.photo.url),
        "previous_evolution": serialized_pokemon.previous_evolution
    }

    if serialized_pokemon.previous_evolution:
        pokemon_info["previous_evolution"] = {
            "title_ru": serialized_pokemon.previous_evolution.title_ru,
            "pokemon_id": serialized_pokemon.previous_evolution.id,
            "img_url": request.build_absolute_uri(serialized_pokemon.previous_evolution.photo.url)
        }

    try:
        next_evolution = serialized_pokemon.next_evolution.get()
        if next_evolution:
            pokemon_info["next_evolution"] = {
                "title_ru": next_evolution.title_ru,
                "pokemon_id": next_evolution.id,
                "img_url": request.build_absolute_uri(next_evolution.photo.url)
            }
    except ObjectDoesNotExist:
        pass

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_entities = serialized_pokemon.entities.all()
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.photo.url)
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_info
    })
