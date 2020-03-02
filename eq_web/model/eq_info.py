from django.db import models


class EqInfo(models.Model):
    Cata_id = models.CharField(max_length=40, primary_key=True)
    Eq_type = models.IntegerField(default=0)
    O_time = models.DateTimeField(null=True)
    Lat = models.DecimalField(max_digits=6, decimal_places=2)
    Lon = models.DecimalField(max_digits=6, decimal_places=2)
    geom = models.CharField(max_length=100)
    Depth = models.IntegerField(default=0)
    M = models.DecimalField(max_digits=3, decimal_places=1)
    Location_cname = models.CharField(max_length=128)
    is_create_pic = models.IntegerField(default=0)

    # 元类信息 : 修改表名
    class Meta:
        db_table = 'cata7days'
