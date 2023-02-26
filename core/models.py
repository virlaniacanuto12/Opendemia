from django.db import models

# Create your models here.

# Tabela que armazena as doenças disponíveis no sistema
class Doencas(models.Model):
    nome = models.CharField(max_length=100)
    origem = models.CharField(max_length=50)
    tipo = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

    class Meta:
        db_table = 'doencas'

# Tabela que armazena todos os usuários logados no sistema
class Usuarios(models.Model):
    nome = models.CharField(max_length=100)
    idade = models.IntegerField(null=False)
    cidade = models.CharField(max_length=100)
    id_facebook = models.CharField(max_length=15)
    locaisvisitados = models.ForeignKey("LocaisVisitados", on_delete=models.CASCADE, related_name='Usuarios', null=True, blank=True)

    def __str__(self):
        return str(self.nome)

    class Meta:
        db_table = 'usuarios'

#Tabela de cruzamento para referenciar as doenças marcadas pelos usuários
class Cruzamento(models.Model):
    usuario_id = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    doenca_id = models.ForeignKey(Doencas,  on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    class Meta:
        unique_together = [['usuario_id', 'doenca_id']]

#Tabela que armazena os dados demográficos dos países
class DadosDemograficos(models.Model):
    populacao = models.IntegerField(null=False)
    area = models.IntegerField(null=False)
    estado = models.CharField(max_length=100, null=False)
    pais = models.CharField(max_length=100, null=False)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=False)
    longitude = models.DecimalField(max_digits=10, decimal_places=8, null=False)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'dadosdemograficos'

# Tabela que armazena informações dos locais visitados informados pelo usuário
class LocaisVisitados(models.Model):
    cep = models.CharField(max_length=10)
    cidade = models.CharField(max_length=100, null=False)
    estado = models.CharField(max_length=100, null=False)
    pais = models.CharField(max_length=100, null=False)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=False)
    longitude = models.DecimalField(max_digits=10, decimal_places=8, null=False)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'locaisvisitados'

#Tabela de relatórios diários das doenças
class Relatorios(models.Model):
    doenca = models.ForeignKey("Doencas", on_delete=models.CASCADE, related_name='Relatorios')
    dadosdemograficos = models.ForeignKey("DadosDemograficos", on_delete=models.CASCADE, related_name='Relatorios')
    casos = models.IntegerField(null=False)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'relatorios'