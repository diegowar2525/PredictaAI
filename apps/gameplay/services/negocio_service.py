from apps.companies.models import Producto
from django.db.models import Sum

def ejecutar_accion(data):
    accion = data.get("accion")

    # 🛒 REGISTRAR VENTA
    if accion == "registrar_venta":
        producto = Producto.objects.filter(
            nombre__icontains=data.get("producto", "")
        ).first()

        if not producto:
            return "❌ No encontré ese producto"

        cantidad = data.get("cantidad", 1)

        if producto.stock_actual < cantidad:
            return (
                f"⚠️ Stock insuficiente.\n"
                f"Disponible: {producto.stock_actual}"
            )

        producto.stock_actual -= cantidad
        producto.ventas += cantidad
        producto.save()

        return (
            f"✅ Venta registrada.\n"
            f"📦 Stock actual de {producto.nombre}: {producto.stock_actual}"
        )

    # 📦 CONSULTAR STOCK
    if accion == "consultar_stock":
        producto = Producto.objects.filter(
            nombre__icontains=data.get("producto", "")
        ).first()

        if not producto:
            return "❌ Producto no encontrado"

        return f"📦 {producto.nombre}: {producto.stock_actual} unidades"

    if accion == "productos_mas_vendidos":
        productos = (
            Producto.objects
            .annotate(total_vendido=Sum("ventas__cantidad"))
            .filter(total_vendido__isnull=False)
            .order_by("-total_vendido")[:5]
        )

        if not productos:
            return "📊 Aún no hay ventas registradas."

        respuesta = "🔥 Productos más vendidos:\n"
        for p in productos:
            respuesta += f"- {p.nombre}: {p.total_vendido} unidades\n"

        return respuesta

    # 🤔 ACLARACIÓN
    if accion == "pedir_aclaracion":
        return "🤔 ¿Podrías darme más detalles?"

    return "❌ No entendí la acción"

