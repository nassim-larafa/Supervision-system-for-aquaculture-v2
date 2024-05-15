from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.contrib.gis.db import models
from location_field.models.plain import PlainLocationField
from django.utils import timezone

# Create your models here.
#supervisor
class supervisor(models.Model):
    nom = models.CharField(max_length=100, null=True)
    prenom = models.CharField(max_length=100, null=True)
    NB_GSM = models.CharField(max_length=100, null=True)
    pseudo = models.CharField(max_length=100, null=True)
    e_mail = models.EmailField(max_length=100, null=True)
    password = models.CharField(max_length=100, null=True)
    image = models.FileField(null=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True,blank=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"
    
    def save(self, *args, **kwargs):
        # Create User instance if it doesn't exist
        if not self.user:
            self.user = User.objects.create_user(self.pseudo, self.e_mail, self.password)
        
        super().save(*args, **kwargs)
#client
class client(models.Model):
    nom=models.CharField(max_length=100,null=True,blank=True)
    prenom=models.CharField(max_length=100,null=True,blank=True)
    NB_GSM=models.CharField(max_length=100,null=True)
    pseudo=models.CharField(max_length=100,null=True)
    e_mail=models.EmailField(max_length=100,null=True)
    image=models.FileField(null=True)
    supervisor = models.ForeignKey(supervisor, on_delete=models.CASCADE, null=True, related_name='%(class)s_related')

    def __str__(self):
        return f"{self.prenom} {self.nom}"

class myProject(models.Model):
    nomp = models.CharField(max_length=50, null=True)
    geomp = models.MultiPolygonField(null=True)
    descp = models.TextField(null=True)
    debutp = models.DateTimeField(default=timezone.now,null=True)
    finp = models.DateTimeField(null=True)
    cityp = models.CharField(max_length=255,null=True)
    piece_joinde = models.FileField(upload_to='uploads/%Y/%m/%d/', null=True, blank=True)
    locationp = PlainLocationField(based_fields=['cityp'], zoom=7,null=True)
    clientp = models.ForeignKey(client, on_delete=models.CASCADE,null=True)
    supervisorp = models.ForeignKey(supervisor, on_delete=models.CASCADE, null=True)
    polygon_id = models.BigAutoField(primary_key=True, default=None)
    
    
    def __str__(self):
        return f' Project: {self.nomp}'
    
class parcelle(models.Model):
    namep = models.CharField(max_length=50, null=True, blank=True)
    poly = models.PolygonField(null=True)
    project = models.ForeignKey(myProject, on_delete=models.CASCADE, null=True, blank=True,related_name='parcelle')

    def __str__(self):
        if self.project:
            return f'Parcelle of project: {self.project.nomp}'
        else:
            return 'Parcelle with no project assigned for now'

class cage(models.Model):
    Idcage=models.AutoField(primary_key=True, default=None)
    nom=models.CharField(max_length=50,blank=True,null=True)
    centre=models.PointField(null=True)
    latitude_centre=models.CharField(max_length=50, null=True , blank=True)
    longitude_centre =models.CharField(max_length=50, null=True,blank=True)
    cage_range=models.BigIntegerField(null=True,blank=True)
    diametre = models.FloatField(null=True, blank=True)
    description = models.TextField(null=True)
    polyg = models.ForeignKey(myProject, on_delete=models.CASCADE, null=True, blank=True,related_name='%(class)s_related')
    parc = models.ForeignKey(parcelle, on_delete=models.CASCADE, null=True, blank=True,related_name='%(class)s_related')

    def __str__(self):
        return f' {self.nom}'  

class node(models.Model):
    Idnode = models.AutoField(primary_key=True, default=None)
    nom = models.CharField(max_length=50,blank=True, null=True)
    position=models.PointField(null=True)
    latitude =models.CharField(max_length=50, null=True , blank=True)
    longitude =models.CharField(max_length=50, null=True,blank=True)

    reference =  models.CharField(max_length=50, null=True)
    node_range = models.BigIntegerField(null=True,blank=True)
    Sensors = models.CharField(max_length=50, null=True)
    RSSI = models.BigIntegerField(null=True)
    Battery_value = models.BigIntegerField(null=True)
    detection = models.BigIntegerField(null=True)
    polyg = models.ForeignKey(myProject, on_delete=models.CASCADE, null=True, blank=True,related_name='%(class)s_related')
    parc = models.ForeignKey(parcelle, on_delete=models.CASCADE, null=True, blank=True,related_name='%(class)s_related')
    cage = models.ForeignKey(cage, on_delete=models.CASCADE, null=True, blank=True,related_name='%(class)s_related')
    def __str__(self):
        return f' {self.nom}'
    
class Data(models.Model):
    IdData = models.AutoField(primary_key=True,default=None)
   
    distance = models.FloatField(default=0,null=True)
    published_date = models.DateTimeField(blank=True, null=True)
    node = models.ForeignKey(node, on_delete=models.CASCADE, null=True, related_name='datas')
    
    def publish(self):
        self.published_date = timezone.now()
        self.save()
    
    def __str__(self):
        return f' node : {self.node},Distance: {self.distance} date: {self.published_date}'
