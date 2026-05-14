def calcular_presupuesto_solar(consumo_anual_kwh, precio_kwh, horas_sol_media, precio_instalacion):
    
    # Realiza el cálculo de los parámetros técnicos y económicos 
    # para una instalación fotovoltaica.

    # 1. Cálculo de potencia pico necesaria (kWp)
    # Se basa en la relación entre el consumo anual y la radiación solar media
    kw_necesarios = consumo_anual_kwh / (horas_sol_media * 365 * 0.85)

    # 2. Coste estimado de la inversión
    # Basado en el precio por kW instalado definido en la configuración
    coste_total = kw_necesarios * precio_instalacion

    # 3. Estimación de ahorro anual
    # Cálculo del impacto económico según producción real estimada
    produccion_anual_estimada = kw_necesarios * horas_sol_media * 365 * 0.85
    ahorro_anual = produccion_anual_estimada * precio_kwh

    # 4. Periodo de retorno de la inversión (ROI) en años
    if ahorro_anual > 0:
        tiempo_amortizacion = coste_total / ahorro_anual
    else:
        tiempo_amortizacion = 0

    return {
        "kw_instalados": round(kw_necesarios, 2),
        "coste_estimado": round(coste_total, 2),
        "ahorro_estimado": round(ahorro_anual, 2),
        "tiempo_amortizacion": round(tiempo_amortizacion, 1)
    }