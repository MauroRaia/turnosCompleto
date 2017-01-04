from django.db import models
from django.utils import timezone
#from django.utils import datetime
import datetime
# Create your models here.

class Especialidad(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    nombre = models.CharField(max_length=50,blank=False)

    def __str__(self):
        return self.nombre

class HorarioTrabajo(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    '''
    lunes = 1
    martes = 2
    miercoles = 3
    jueves = 4
    viernes = 5
    sabado = 6
    domingo = 0
    '''

    lunes = 'lunes'
    martes = 'martes'
    miercoles = 'miercoles'
    jueves = 'jueves'
    viernes = 'viernes'
    sabado = 'sabado'
    domingo = 'domingo'

    opcionesDias = (
        (lunes,'Lunes'),
        (martes,'Martes'),
        (miercoles,'Miercoles'),
        (jueves,'Jueves'),
        (viernes,'Viernes'),
        (sabado,'Sabado'),
        (domingo,'Domingo')
        )
    dia = models.CharField(choices=opcionesDias,default=domingo, max_length = 9)
    horaInicio = models.TimeField()
    horaFin = models.TimeField()

    def __str__(self):
        return str(self.dia)+' | '+str(self.horaInicio)+ ' | '+str(self.horaFin)

class Medico(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    nombre = models.CharField(max_length=30,blank=False)
    apellido = models.CharField(max_length=30,blank=False)
    dni = models.IntegerField(blank=False)
    telefono = models.IntegerField(blank=True)
    correo = models.CharField(max_length=100,blank=True)
    espec = models.ManyToManyField('Especialidad')
    horario = models.ManyToManyField('HorarioTrabajo')
    estaActivo = models.BooleanField(default=True)
    #duracionMinimaTurno

    def __str__ (self):
        return str(self.nombre)+' '+str(self.apellido)
class ObraSocial(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    nombre = models.CharField(max_length=40,blank=False)

    def __str__(self):
        return self.nombre

class Paciente(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    nombre = models.CharField(max_length=30,blank=False)
    apellido = models.CharField(max_length=30,blank=False)
    dni = models.IntegerField(blank=False)
    telefono = models.IntegerField()
    fechaNacimiento = models.DateField()
    obraSocial = models.ForeignKey('ObraSocial')
    numeroObraSocial = models.CharField(max_length=20,blank=True)
    estaActivo = models.BooleanField(default=True)

    def __str__(self):

        return self.nombre+' '+self.apellido+' | '+str(self.dni)

class Tratamiento(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    #http://stackoverflow.com/questions/16027516/can-i-set-a-specific-default-time-for-a-django-datetime-field
    #creo un "objeto" hora para llamarlo como default
    def default_start_time():
        now = datetime.datetime.now()
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        return start

    nombre = models.CharField(max_length=100,blank=False)
    duracion = models.TimeField(default=default_start_time())
    precio = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.nombre+' | '+str(self.duracion)


class Turno(models.Model):
    '''
    creo las opciones que puede elegirse en estado
    '''
    pendiente = 'Pend'
    atendido = 'Aten'
    canceladoMedico = 'CM'
    canceladoPaciente = 'CP'
    ausente = 'Ause'

    opcionesEstado = (
        (pendiente,'Pendiente'),
        (atendido,'Atendido'),
        (canceladoMedico,'Cancelado por Medico'),
        (canceladoPaciente,'Cancelado por Paciente'),
        (ausente,'Ausente')
        )

    estado = models.CharField(max_length=4,choices=opcionesEstado,default=pendiente)
    medico = models.ForeignKey('Medico')
    paciente = models.ForeignKey('Paciente')
    dia = models.DateField()

    horario = models.TimeField()

    especialidad = models.ForeignKey('Especialidad')
    tratamiento = models.ForeignKey('Tratamiento')
    estaActivo = models.BooleanField(default=True)

    def __str__(self):
        return str(self.pk) + ' | ' + str(self.estado)+' | '+str(self.horario)+' | '+str(self.medico)+' | '+str(self.paciente)+' | '+str(self.tratamiento)
