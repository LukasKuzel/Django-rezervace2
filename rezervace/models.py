import datetime
import os
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.db import models

PSC_REGEX = RegexValidator(r'^\d{5}$', 'Nesprávně zadané poštovní směrovací číslo')
TELEFON_REGEX = RegexValidator(r'^[+]\d{3}( \d{3}){3}$', 'Nesprávně zadané telefonní číslo')


def get_image_path(instance, filename):
    return os.path.join('fotogalerie', '%s' % str(instance.ubytovani.id), filename)


class Klient(models.Model):
    jmeno = models.CharField(max_length=50, verbose_name='Jméno klienta', help_text='Zadejte jméno klienta',
                             error_messages={'blank': 'Jméno klienta musí být vyplněno'})
    prijmeni = models.CharField(max_length=50, verbose_name='Příjmení klienta', help_text='Zadejte příjmení klienta',
                                error_messages={'blank': 'Příjmení klienta musí být vyplněno'})
    email = models.EmailField(unique=True, verbose_name='Email klienta', help_text='Zadejte e-mail klienta',
                              error_messages={'unique': 'E-mailová adresa musí být jedinečná', 'invalid': 'Neplatná e-mailová adresa',
                                              'blank': 'Pole nesmí být prázdné'})
    telefon = models.CharField(max_length=16, verbose_name='Telefon klienta', help_text='Zadejte telefon v podobě: +420 777 777 777',
                               blank=True, validators=[TELEFON_REGEX])

    class Meta:
        ordering = ['prijmeni', 'jmeno']
        verbose_name = 'Klient'
        verbose_name_plural = 'Klienti'

    def __str__(self):
        return f'{self.prijmeni}, {self.jmeno}'


class Vybaveni(models.Model):
    nazev = models.CharField(max_length=30, verbose_name='Název vybavení', help_text='Zadejte název vybavení')
    symbol = models.ImageField(upload_to='symbols', verbose_name='Grafický symbol')

    class Meta:
        ordering = ['nazev']
        verbose_name = 'Vybavení'
        verbose_name_plural = 'Vybavení'

    def __str__(self):
        return f'{self.nazev}'


class Ubytovani(models.Model):
    oznaceni = models.CharField(max_length=100, verbose_name='Označení ubytování', help_text='Zadejte vhodné označení ubytování')
    adresa = models.CharField(max_length=100, verbose_name='Adresa', help_text='Zadejte ulici a číslo popisné (orientační)')
    misto = models.CharField(max_length=50, verbose_name='Město/obec', help_text='Zadejte název města nebo obce')
    psc = models.PositiveIntegerField(verbose_name='PSČ', help_text='Zadejte poštovní směrovací číslo (bez mezery)', validators=[PSC_REGEX])
    kontakt = models.CharField(max_length=50, verbose_name='Kontaktní osoba', help_text='Zadejte jméno a příjmení kontaktní osoby')
    telefon = models.CharField(max_length=16, verbose_name='Telefon', validators=[TELEFON_REGEX],
                               help_text='Zadejte telefon v podobě: +420 777 777 777',
                               error_messages={'blank': 'Telefonní číslo musí být vyplněno'})
    email = models.EmailField(unique=True, verbose_name='Email', help_text='Zadejte e-mail ubytování (kontaktní osoby)',
                              error_messages={'unique': 'E-mailová adresa musí být jedinečná', 'invalid':'Neplatná e-mailová adresa',
                                              'blank': 'Pole nesmí být prázdné'})
    popis = models.TextField(verbose_name='Popis ubytování', help_text='Zadejte podrobnější informace o ubytování')
    pocet_pokoju = models.PositiveSmallIntegerField(verbose_name='Počet pokojů', help_text='Zadejte číselný údaj o počtu pokojů')
    vybaveni = models.ManyToManyField(Vybaveni)

    class Meta:
        ordering = ['oznaceni']
        verbose_name = 'Ubytování'
        verbose_name_plural = 'Ubytování'

    def __str__(self):
        return f'{self.oznaceni} ({self.misto}, {self.adresa})'


class Rezervace(models.Model):
    klient = models.ForeignKey('Klient', on_delete=models.CASCADE, verbose_name='Jméno klienta')
    ubytovani = models.ForeignKey('Ubytovani', on_delete=models.CASCADE, verbose_name='Název ubytování')
    zacatek_pobytu = models.DateField(auto_now=False, auto_now_add=False, verbose_name='Začátek pobytu', help_text='Zadejte datum začátku pobytu')
    konec_pobytu = models.DateField(auto_now=False, auto_now_add=False, verbose_name='Konec pobytu', help_text='Zadejte datum konce pobytu')
    pocet_osob = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)],verbose_name='Počet osob', help_text='Zadejte požadovaný počet ubytovaných osob (max. 9)')
    info = models.TextField(blank=True, verbose_name='Informace od klienta', help_text='Zde můžete zadat další informace nebo požadavky')

    class Meta:
        ordering = ['zacatek_pobytu', 'klient']
        verbose_name = 'Rezervace'
        verbose_name_plural = 'Rezervace'

    def __str__(self):
        return f'{self.klient}: {self.ubytovani}'

    def save(self, *args, **kwargs):
        if self.zacatek_pobytu < datetime.date.today():
            raise ValidationError('Datum začátku pobytu nemůže být zadáno v minulosti')
        if self.konec_pobytu <= self.zacatek_pobytu:
            raise ValidationError('Datum konce pobytu musí být pozdější než datum začátku pobytu')
        super(Rezervace, self).save(*args, **kwargs)


class Foto(models.Model):
    fotka = models.ImageField(upload_to=get_image_path, verbose_name='Fotografie')
    ubytovani = models.ForeignKey('Ubytovani', null=True, on_delete=models.SET_NULL, verbose_name='Název ubytování')
    popis = models.CharField(max_length=200, verbose_name='Popis fotky')

    class Meta:
        ordering = ['popis']
        verbose_name = 'Foto'
        verbose_name_plural = 'Fota'

    def __str__(self):
        return f'{self.ubytovani}: ({self.popis})'

Hodnoceni = (
    ("1", "výborné"),
    ("2", "chválitebné"),
    ("3", "dobré"),
    ("4", "dostačující"),
    ("5", "nedostačující"),
)

class Hodnoceni_pobytu(models.Model):
    klient = models.ForeignKey('Klient', on_delete=models.CASCADE, verbose_name='Jméno klienta')
    nazev_ubytovani = models.ForeignKey('Ubytovani', on_delete=models.CASCADE, verbose_name='Název ubytování')
    pozitiva = models.TextField(max_length=1000, help_text='Napište pozitivní věci ohledně pobytu', verbose_name='Pozitivní recenze', null=True)
    negativa = models.TextField(max_length=1000, help_text='Napište negativní věci ohledně pobytu', verbose_name='Negativní recenze', null=True)
    znamka = models.CharField(max_length=100, choices=Hodnoceni, help_text='Vyberte hodnocení', verbose_name='Známka', null=False)
    datum_recenze = models.DateField(auto_now_add=datetime)

    class Meta:
        ordering = ['nazev_ubytovani','klient']
        verbose_name = 'Hodnocení pobytu'
        verbose_name_plural = 'Hodnocení pobytů'

    def __str__(self):
        return f'{self.nazev_ubytovani}: {self.znamka},({self.klient}, {self.datum_recenze})'

