# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-21 17:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('peasantlegaldb', '0005_auto_20170919_1747'),
    ]

    operations = [
        migrations.AddField(
            model_name='litigant',
            name='chevage',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='litigant_chevage', to='peasantlegaldb.Money'),
        ),
        migrations.AddField(
            model_name='litigant',
            name='chevage_notes',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='litigant',
            name='crossed',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='litigant',
            name='habet_terram',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='litigant',
            name='heriot_animal',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='heriot_animal', to='peasantlegaldb.Chattel'),
        ),
        migrations.AddField(
            model_name='litigant',
            name='heriot_assessment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='heriot_assessment', to='peasantlegaldb.Money'),
        ),
        migrations.AddField(
            model_name='litigant',
            name='heriot_quantity',
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AddField(
            model_name='litigant',
            name='impercamentum_amercement',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='impercamentaum_amercement', to='peasantlegaldb.Money'),
        ),
        migrations.AddField(
            model_name='litigant',
            name='impercamentum_animal',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='impercamentum_animal', to='peasantlegaldb.Chattel'),
        ),
        migrations.AddField(
            model_name='litigant',
            name='impercamentum_notes',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='litigant',
            name='impercamentum_quantity',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='litigant',
            name='recessit',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='case',
            name='ad_legem',
            field=models.NullBooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='case',
            name='court_type',
            field=models.IntegerField(choices=[(6, 'Account Roll'), (5, 'Unknown'), (3, 'Impercamentum'), (2, 'Tourn'), (4, 'Chevage'), (1, 'Hallmoot')]),
        ),
        migrations.AlterField(
            model_name='casepeopleland',
            name='villeinage',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='litigant',
            name='ad_proximum',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='litigant',
            name='attached',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='litigant',
            name='bail',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='litigant',
            name='damage_notes',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='litigant',
            name='distrained',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='person',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('I', 'Institution'), ('F', 'Female'), ('U', 'Unknown')], max_length=1),
        ),
        migrations.AlterField(
            model_name='person',
            name='status',
            field=models.IntegerField(choices=[(1, 'Villein'), (3, 'Unknown'), (4, 'Institution'), (2, 'Free')]),
        ),
        migrations.AlterField(
            model_name='record',
            name='record_type',
            field=models.IntegerField(choices=[(6, 'Account Roll'), (2, 'Extant'), (4, 'Custumal'), (3, 'Survey'), (5, 'Patent Roll'), (1, 'Court Roll')]),
        ),
        migrations.AlterField(
            model_name='session',
            name='law_term',
            field=models.IntegerField(choices=[(4, 'Michaelmas'), (3, 'Trinity'), (2, 'Easter'), (1, 'Hilary')]),
        ),
    ]