from django.db import models

# Create your models here.

ARTISTES = {
    'ld2j': {'name': 'LD2J'},
    'xzero': {'name': 'XZero'},
    'youken': {'name': 'Youken'},
    'ryg': {'name': 'RYG'},
}

ALBUMS = [
    {'name': 'Montagne Russe', 'artistes': [ARTISTES['ld2j']]},
    {'name': 'Flow Nocif', 'artistes': [ARTISTES['xzero']]},
    {'name': 'Carte Etudiante', 'artistes': [ARTISTES['youken'], ARTISTES['ryg']]},
]