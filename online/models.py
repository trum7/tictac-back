# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Game(models.Model):
    session = models.CharField(max_length=100)
    gamer = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'game'


class Round(models.Model):
    game = models.CharField(max_length=100)
    invited = models.CharField(max_length=100)
    turn = models.CharField(max_length=100)
    move = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'round'
