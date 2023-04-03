# Generated by Django 4.2 on 2023-04-03 20:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rezervace', '0002_alter_ubytovani_psc'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hodnoceni_pobytu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pozitiva', models.TextField(help_text='Napište pozitivní věci ohledně pobytu', max_length=1000, null=True, verbose_name='Pozitivní recenze')),
                ('negativa', models.TextField(help_text='Napište negativní věci ohledně pobytu', max_length=1000, null=True, verbose_name='Negativní recenze')),
                ('znamka', models.CharField(choices=[('1', 'výborné'), ('2', 'chválitebné'), ('3', 'dobré'), ('4', 'dostačující'), ('5', 'nedostačující')], help_text='Vyberte hodnocení', max_length=100, verbose_name='Známka')),
                ('datum_recenze', models.DateField(auto_now_add=True)),
                ('klient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rezervace.klient', verbose_name='Jméno klienta')),
                ('nazev_ubytovani', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rezervace.ubytovani', verbose_name='Název ubytování')),
            ],
            options={
                'verbose_name': 'Hodnocení pobytu',
                'verbose_name_plural': 'Hodnocení pobytů',
                'ordering': ['znamka'],
            },
        ),
    ]
