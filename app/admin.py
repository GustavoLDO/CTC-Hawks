from django.contrib import admin
from .models import Pagina
from .models import Produto
from .models import Pedido
from .models import Planos
from .models import Contato
# Register your models here.

admin.site.register(Pagina)
admin.site.register(Produto)
admin.site.register(Contato)
admin.site.register(Pedido)
admin.site.register(Planos)


