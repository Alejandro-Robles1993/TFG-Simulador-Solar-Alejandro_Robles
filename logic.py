def calcular_presupuesto_solar(consumo_anual_kwh, precio_kwh, horas_sol_media=5.0, precio_instalacion=1000.0):
    # 1. Convertimos entradas a números para evitar errores de texto
    consumo = float(consumo_anual_kwh)
    precio = float(precio_kwh)
    
    if consumo <= 0 or precio <= 0:
        return {"kw_instalados": 0, "coste_estimado": 0, "ahorro_estimado": 0, "tiempo_amortizacion": 0}

    # 2. PROPUESTA DE kW INSTALADOS (El corazón del cálculo)
    # Usamos un ratio estándar: 1kWp produce unos 1500kWh al año.
    # Queremos cubrir el consumo que nos ha dicho el cliente.
    # kW = Consumo / 1500
    kw_propuestos = consumo / 1500
    
    # Redondeamos a 2 decimales para que quede profesional (ej: 3.25 kWp)
    kw_finales = round(kw_propuestos, 2)

    # 3. COSTE ESTIMADO
    # Usamos el precio fijo de tu memoria (1000€ por kW)
    coste_total = kw_finales * 1000

    # 4. AHORRO ANUAL ESTIMADO
    # Si el cliente consume lo que producen sus paneles, ahorra:
    # Producción (que es igual a su consumo) * Precio de su factura
    ahorro_anual = consumo * precio

    # 5. TIEMPO DE AMORTIZACIÓN (Años)
    if ahorro_anual > 0:
        # Coste dividido entre lo que te ahorras al año
        años = coste_total / ahorro_anual
        tiempo_amortizacion = round(años, 1)
    else:
        tiempo_amortizacion = 0

    return {
        "kw_instalados": kw_finales,
        "coste_estimado": round(coste_total, 2),
        "ahorro_estimado": round(ahorro_anual, 2),
        "tiempo_amortizacion": tiempo_amortizacion
    }