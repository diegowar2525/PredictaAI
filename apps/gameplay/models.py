from django.db import models

class Conversacion(models.Model):
    """Conversaciones separadas del chatbot"""
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=200, default="Nueva conversación")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    activa = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-fecha_actualizacion']
        verbose_name_plural = "Conversaciones"
    
    def __str__(self):
        return f"{self.titulo} - {self.fecha_creacion.strftime('%d/%m/%Y')}"
    
    def generar_titulo_automatico(self):
        """Genera título basado en el primer mensaje"""
        primer_mensaje = self.mensajes.filter(tipo='user').first()
        if primer_mensaje:
            # Tomar primeras 50 caracteres
            self.titulo = primer_mensaje.mensaje[:50]
            if len(primer_mensaje.mensaje) > 50:
                self.titulo += "..."
            self.save()


class MensajeChat(models.Model):
    """Historial de mensajes del chatbot"""
    TIPO_CHOICES = [
        ('user', 'Usuario'),
        ('bot', 'Bot'),
    ]
    
    conversacion = models.ForeignKey(
        Conversacion, 
        on_delete=models.CASCADE, 
        related_name='mensajes'
    )
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['fecha']
        verbose_name_plural = "Mensajes del Chat"
    
    def __str__(self):
        return f"{self.tipo} - {self.fecha.strftime('%d/%m/%Y %H:%M')}"