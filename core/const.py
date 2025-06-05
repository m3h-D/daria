from django.db.models import TextChoices

class Mf(TextChoices):
    M = 'M', 'M'
    F = 'F', 'F'

class Hand(TextChoices):
    R = 'R', 'R'
    L = 'L', 'L'
    
    
class LongGroup(TextChoices):
    NONDEMENTED = "Nondemented", "Nondemented"
    DEMENTED = "Demented", "Demented"
    CONVERTED = "Converted", "Converted"
