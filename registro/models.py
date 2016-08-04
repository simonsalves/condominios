from django.db import models
from django.core.validators import MaxLengthValidator
from django.core.validators import MaxValueValidator, MinValueValidator

from geoname.models import Ciudad, Comuna


class GrupoGasto(models.Model):
    nombre = models.CharField(max_length=50)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "GruposGasto"

    def __unicode__(self):
        return self.nombre


class TipoGasto(models.Model):
    nombre = models.CharField(max_length=50)
    activo = models.BooleanField(default=True)
    grupoGasto = models.ForeignKey(GrupoGasto)

    class Meta:
        verbose_name_plural = "TiposGasto"

    def __unicode__(self):
        return self.nombre


# TODO: La lista de residentes deberia estar limitada a un condominio?
class Residente(models.Model):
    rut = models.CharField(max_length=13)
    nombres = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    GENDER_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    )
    genero = models.CharField(max_length=1, choices=GENDER_CHOICES)
    fono = models.IntegerField()
    email = models.CharField(max_length=50)
    fecha_ingreso = models.DateField()
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombres


class AdministradorEdificio(models.Model):
    nombreEmpresa = models.CharField(max_length=50)
    rutEmpresa = models.CharField(max_length=13)
    razonSocial = models.CharField(max_length=50)
    fono = models.IntegerField()
    email = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50)
    ciudad = models.ForeignKey(Ciudad)
    comuna = models.ForeignKey(Comuna)
    url = models.CharField(max_length=100)

    def __str__(self):
        return str(self.nombreEmpresa)


class Conserje(models.Model):
    rut = models.CharField(max_length=13)
    nombres = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    GENDER_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    )
    genero = models.CharField(max_length=1, choices=GENDER_CHOICES)
    fono = models.IntegerField()
    email = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50)
    comuna = models.ForeignKey(Comuna)
    ciudad = models.ForeignKey(Ciudad)
    #    TURN_CHOICES = (
    #        ('D', 'Diurno'),
    #        ('N', 'Nocturno'),
    #    )
    #    turno=models.CharField(max_length=1, choices=TURN_CHOICES)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombres


class Condominio(models.Model):
    nombre = models.CharField(max_length=50)
    fono = models.IntegerField()
    direccion = models.CharField(max_length=50)
    reglamento = models.CharField(max_length=100)  # FileField
    ciudad = models.ForeignKey(Ciudad)
    comuna = models.ForeignKey(Comuna)
    administradorEdificio = models.ForeignKey(AdministradorEdificio)
    conserjes = models.ManyToManyField(Conserje, related_name='condominios')

    def __str__(self):
        return str(self.nombre)


class GastoCondominio(models.Model):
    # grupoGasto = models.ForeignKey(GrupoGasto)
    tipoGasto = models.ForeignKey(TipoGasto)
    condominio = models.ForeignKey(Condominio)
    egreso = models.CharField(max_length=50)
    # descripcion = models.TextField(validators=[MaxLengthValidator(500)])
    fecha = models.DateTimeField()  # Se evalua MES-ANO
    valor = models.IntegerField()

    def __str__(self):
        return str(self.valor)


class Glosa (models.Model):
    nombre = models.CharField(max_length=100)
    grupoGasto = models.ForeignKey(GrupoGasto)
    condominio = models.ForeignKey(Condominio)
    descripcion = models.TextField(validators=[MaxLengthValidator(500)])
    nombreDocumento = models.CharField(max_length=300, default="")
    nombreDocumentoOrig = models.CharField(max_length=300, default="")
    fecha = models.DateTimeField()  # Se evalua MES-ANO
    ingreso = models.IntegerField(default=0)
    egreso = models.IntegerField(default=0)

    def __str__(self):
        return str(self.nombre)


class Edificio(models.Model):
    nombre = models.CharField(max_length=30)
    cantidadPisos = models.IntegerField()
    condominio = models.ForeignKey(Condominio);

    def __str__(self):
        return str(self.nombre)


class Departamento(models.Model):
    numero = models.IntegerField()
    metrosCuadrados = models.CharField(max_length=100)
    cantidadBanos = models.IntegerField(default=1)
    cantidadPiezas = models.IntegerField(default=1)
    walkInCloset = models.BooleanField(default=True)
    edificio = models.ForeignKey(Edificio)
    porcentajeDominio = models.DecimalField(max_digits=7, decimal_places=6,
                                            validators=[MaxValueValidator(1),
                                                        MinValueValidator(0)])

    def __str__(self):
        return str(self.numero)


class Estacionamiento(models.Model):
    numero = models.IntegerField()
    departamento = models.ForeignKey(Departamento)
    porcentajeDominio = models.DecimalField(max_digits=7, decimal_places=6,
                                            validators=[MaxValueValidator(1),
                                                        MinValueValidator(0)])

    def __str__(self):
        return str(self.numero)


class Bodega(models.Model):
    numero = models.IntegerField()
    departamento = models.ForeignKey(Departamento)
    porcentajeDominio = models.DecimalField(max_digits=7, decimal_places=6,
                                            validators=[MaxValueValidator(1),
                                                        MinValueValidator(0)])

    def __str__(self):
        return str(self.numero)


class CargoComite(models.Model):
    nombre = models.CharField(max_length=30)

    def __str__(self):
        return str(self.nombre)


class Comite(models.Model):
    cargo = models.ForeignKey(CargoComite)
    nombre = models.CharField(max_length=30)
    fecha_inicio = models.DateTimeField()
    fecha_termino = models.DateTimeField(blank=True)
    activo = models.BooleanField(default=True)
    condominio = models.ForeignKey(Condominio)

    def __str__(self):
        return str(self.nombre)


class Contrato(models.Model):
    departamento = models.ForeignKey(Departamento)
    residente = models.ForeignKey(Residente)
    fecha_inicio = models.DateTimeField()
    fecha_termino = models.DateTimeField(blank=True)
    RESIDENT_CHOICES = (
        ('P', 'Propietario'),
        ('A', 'Arrendatario'),
    )
    tipo = models.CharField(max_length=1, choices=RESIDENT_CHOICES)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return str(self.tipo)


class Servicio(models.Model):
    nombre = models.CharField(max_length=30)
    unidad_medida = models.CharField(max_length=8)

    def __str__(self):
        return str(self.nombre)

class LecturaServicio(models.Model):
    servicio = models.ForeignKey(Servicio)
    departamento = models.ForeignKey(Departamento)
    fecha = models.DateTimeField()
    lectura = models.IntegerField()


class TipoMultaEInteres(models.Model):
    nombre = models.CharField(max_length=80)


class MultaCondominio(models.Model):
    tipoMultaEInteres = models.ForeignKey(TipoMultaEInteres)
    condominio = models.ForeignKey(Condominio)
    porcentajeMulta = models.IntegerField()


class MultaEInteres(models.Model):
    departamento = models.ForeignKey(Departamento)
    monto = models.IntegerField()
    fecha = models.DateTimeField()


class PagoYAbono(models.Model):
    departamento = models.ForeignKey(Departamento)
    monto = models.IntegerField()
    fecha = models.DateTimeField()


class BalanceMensual(models.Model):
    departamento = models.ForeignKey(Departamento)
    monto = models.IntegerField()
    fecha = models.DateTimeField()


# MODELO DE PRUEBA (SOLO PARA FINES VISUALES)
class Cobranza(models.Model):
    torre = models.ForeignKey(Edificio)
    departamento = models.ForeignKey(Departamento)
    porcentajeDominio = porcentajeDominio = models.DecimalField(max_digits=7, decimal_places=6,
                                                                validators=[MaxValueValidator(1),
                                                                            MinValueValidator(0)]);
    gastosComunes = models.IntegerField()
    fondoDeReserva = models.IntegerField()
    lecturaAnterior = models.IntegerField()
    lecturaActual = models.IntegerField()
    aguaCalienteM3 = models.IntegerField()
    aguaCalienteCosto = models.IntegerField()
    multasEIntereses = models.IntegerField()
    morosidad = models.IntegerField()
    diferenciaAFavor = models.IntegerField()
    cobroTransbank = models.IntegerField()
    totalACobrar = models.IntegerField()
    observaciones = models.CharField(max_length=200)
