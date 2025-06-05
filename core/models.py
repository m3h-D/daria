from djongo import models

from core import const
from core.managers import BaseManager

class Cross(models.Model):
    id = models.CharField(max_length=50, primary_key=True, db_column="ID")
    mf = models.CharField(max_length=1, choices=const.Mf.choices, db_column="M/F")
    hand = models.CharField(max_length=1, choices=const.Hand.choices, db_column="Hand")
    age = models.IntegerField(db_column="Age")
    educ = models.FloatField(blank=True, null=True, db_column="Educ")
    ses = models.FloatField(blank=True, null=True, db_column="SES")
    mmse = models.FloatField(blank=True, null=True, db_column="MMSE")
    cdr = models.FloatField(blank=True, null=True, db_column="CDR")
    etiv = models.IntegerField(db_column="eTIV")
    nwbv = models.FloatField(db_column="nWBV")
    asf = models.FloatField(db_column="ASF")
    delay = models.FloatField(null=True, blank=True, db_column="Delay")
    
    objects = BaseManager()
    
    
class Long(models.Model):
    subject_id = models.CharField(max_length=50, primary_key=True, db_column="Subject ID")
    mri_id = models.CharField(max_length=50, db_index=True, db_column="MRI ID")
    group = models.CharField(max_length=50, choices=const.LongGroup.choices, db_column="Group")
    visit = models.IntegerField(db_column="Visit")
    mr_delay = models.IntegerField(db_column="MR Delay")
    mf = models.CharField(max_length=1, choices=const.Mf.choices, db_column="M/F")
    hand = models.CharField(max_length=1, choices=const.Hand.choices, db_column="Hand")
    age = models.IntegerField(db_column="Age")
    educ = models.IntegerField(db_column="EDUC")
    ses = models.FloatField(blank=True, null=True, db_column="SES")
    mmse = models.FloatField(db_column="MMSE")
    cdr = models.FloatField(db_column="CDR")
    etiv = models.IntegerField(db_column="eTIV")
    nwbv = models.FloatField(db_column="nWBV")
    asf = models.FloatField(db_column="ASF")
    
    objects = BaseManager()
    
    
class Result(models.Model):
    user_id = models.BigIntegerField()
    result = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)