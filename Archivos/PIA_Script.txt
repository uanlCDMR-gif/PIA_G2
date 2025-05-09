# -*- coding: utf-8 -*-
"""
script.py - Programa principal que utiliza funciones del módulo PIA_Modulo para:
    - Descargar datos de países desde la API REST Countries.
    - Estructurar y limpiar datos.
    - Filtrar con expresiones regulares.
    - Analizar estadísticas y visualizar resultados.
    - Exportar datos a JSON/Excel.
"""

from PIA_Modulo import (
    obtener_datos_paises,
    estructurar_datos_paises,
    guardar_datos_json,
    filtrar_paises_con_regex,
    analizar_estadisticas,
    exportar_datos_excel,
    graficar_datos,
    interpretar_resultados
)

if __name__ == "__main__":
    # 1. Descargar datos originales desde la API REST Countries
    # Esta función es el punto de entrada para acceder a datos globales de países
    datos_crudos = obtener_datos_paises()
    
    if datos_crudos:
        # 2. Transformar datos crudos en estructura tabular (lista de diccionarios)
        # Cada país tendrá campos normalizados como "Nombre", "Población", "Región", etc.
        datos_estructurados = estructurar_datos_paises(datos_crudos)
        
        # 3. Persistir datos en archivo JSON para análisis posterior
        guardar_datos_json(datos_estructurados, "datos_paises.json")
        
        # 4. Filtrar países usando expresiones regulares (ej.: "^A" o "land$")
        # Esto permite búsquedas personalizadas sin modificar la API
        patron = input("Ingrese un patrón de búsqueda (ej.: '^A' o 'land$'): ")
        paises_filtrados = filtrar_paises_con_regex(datos_estructurados, patron)
        
        # 5. Mostrar resultados filtrados en consola
        if paises_filtrados:
            print(f"\nPaíses que coinciden con el patrón '{patron}':")
            for pais in paises_filtrados:
                print(f"- {pais['Nombre']} (Región: {pais['Región']}, Idiomas: {pais['Idiomas']})")
        else:
            print(f"No se encontraron países que coincidan con el patrón '{patron}'.")
        
        # 6. Calcular estadísticas básicas (media, mediana, moda) sobre la población global
        print("\nAnálisis estadístico de población:")
        estadisticas_poblacion = analizar_estadisticas(datos_estructurados, campo="Población")
        if estadisticas_poblacion:
            for clave, valor in estadisticas_poblacion.items():
                print(f"{clave}: {valor}")
        
        # 7. Exportar datos a Excel para uso en herramientas de análisis
        exportar_datos_excel(datos_estructurados, "datos_paises.xlsx")
        if paises_filtrados:
            exportar_datos_excel(paises_filtrados, "paises_filtrados.xlsx")
        
        # 8. Visualizar datos con gráficos para mejorar comprensión de patrones
        print("\nVisualizando datos...")
        
        # Ejemplo 1: Top 10 países más poblados (usando ordenamiento descendente)
        top_poblacion = sorted(datos_estructurados, key=lambda x: x["Población"], reverse=True)[:10]
        graficar_datos(
            top_poblacion,
            tipo_grafico="barras",
            titulo="Top 10 Países por Población",
            eje_x="País",
            eje_y="Población",
            campo_x="Nombre",
            campo_y="Población"
        )
        
        # Ejemplo 2: Densidad poblacional de países filtrados (si hay resultados)
        if paises_filtrados:
            graficar_datos(
                paises_filtrados,
                tipo_grafico="lineas",
                titulo="Densidad Poblacional de Países Filtrados",
                eje_x="País",
                eje_y="Densidad (hab/km²)",
                campo_x="Nombre",
                campo_y="Densidad (hab/km²)"
            )
        
        # 9. Interpretar resultados estadísticos en contexto geográfico/demográfico
        print("\nInterpretación del análisis de población:")
        interpretacion = interpretar_resultados(estadisticas_poblacion, datos_estructurados, campo="Población")
        print(interpretacion)
        
        # 10. Interpretar estadísticas de área para países filtrados (si existen)
        if paises_filtrados:
            print("\nInterpretación del análisis de área en países filtrados:")
            estadisticas_area = analizar_estadisticas(paises_filtrados, campo="Área (km²)")
            if estadisticas_area:
                interpretacion_area = interpretar_resultados(estadisticas_area, paises_filtrados, campo="Área (km²)")
                print(interpretacion_area)
    else:
        print("No se pudieron obtener datos de la API.")