# -*- coding: utf-8 -*-

import requests
import json
import re
import statistics
import pandas as pd
import matplotlib.pyplot as plt

"""
modulo.py - Funciones para interactuar con la API REST Countries (https://restcountries.com).
Incluye métodos para obtener, estructurar y procesar datos geográficos y demográficos de países.
"""
def obtener_datos_paises():
    """
    Obtiene datos de todos los países desde la API REST Countries.
    
    Realiza una solicitud HTTP GET al endpoint oficial de REST Countries y devuelve 
    información como nombre, población, área, idiomas, monedas, entre otros.
    
    Returns:
        list: Lista de diccionarios con datos de cada país (ej.: [{"nombre": "Colombia", "población": 50_882_891, ...}]). 
        None: Si ocurre un error en la conexión o la respuesta no es válida (ej.: código HTTP != 200).
    
    Ejemplo de dato devuelto:
        {
            "commonName": "Colombia",
            "officialName": "República de Colombia",
            "countryCode": "170",
            "region": "Americas",
            "population": 50882891,
            "area": 1141748,
            "languages": {"spa": "Spanish"},
            "currencies": {"COP": {"name": "Colombian peso", "symbol": "$"}}
        }
    """
    # Endpoint oficial de REST Countries para obtener datos de todos los países
    url = "https://restcountries.com/v3.1/all"
    
    try:
        # Enviar solicitud GET con un tiempo máximo de espera de 10 segundos
        # (Evita que el programa se bloquee indefinidamente por fallos de red)
        respuesta = requests.get(url, timeout=10)
        
        # Verificar si la solicitud fue exitosa (código HTTP 200)
        # Lanza una excepción si el código de estado es 4xx o 5xx
        respuesta.raise_for_status()
        
        # Convertir la respuesta JSON en una lista de diccionarios de Python
        # La API devuelve datos en formato JSON, que Python interpreta automáticamente
        return respuesta.json()
    
    except requests.exceptions.RequestException as e:
        # Manejar errores comunes de red:
        # - Fallos de conexión (DNS, servidor caído)
        # - Tiempo de espera excedido (timeout)
        # - Respuestas inválidas (ej.: JSON malformado)
        print(f"Error al conectar con la API: {e}")
        return None

"""
modulo.py - Funciones para estructurar y transformar datos de países obtenidos desde la API REST Countries.
"""
def estructurar_datos_paises(datos):
    """
    Convierte datos crudos de países en una lista de diccionarios con campos clave y normalizados.
    
    Procesa cada país para extraer y organizar información relevante como nombre, población, área, 
    región, subregión, idiomas, monedas y densidad poblacional. Usa métodos seguros (.get()) 
    para evitar errores por campos inexistentes en la respuesta de la API.
    
    Args:
        datos (list): Lista de diccionarios obtenida desde la API REST Countries. 
                      Cada diccionario representa un país con todos sus datos crudos.
    
    Returns:
        list: Lista de diccionarios con los siguientes campos para cada país:
            - Nombre: Nombre común del país (ej.: "Colombia").
            - Población: Número total de habitantes.
            - Área (km²): Extensión territorial en kilómetros cuadrados.
            - Densidad (hab/km²): Población dividida entre área, redondeado a 2 decimales.
            - Región: Macroregión geográfica (ej.: "América").
            - Subregión: Subdivisión de la región (ej.: "Sudamérica").
            - Idiomas: Idiomas oficiales separados por comas (ej.: "Español, Inglés").
            - Monedas: Monedas oficiales con su nombre completo (ej.: "COP (Peso colombiano)").
    """
    paises_estructurados = []
    
    for pais in datos:
        try:
            # Extraer nombre común del país desde el campo anidado "name"
            nombre = pais["name"]["common"]
            
            # Usar .get() para evitar KeyError si el campo no existe
            poblacion = pais.get("population", 0)  # Población, 0 si no está disponible
            area = pais.get("area", 0)  # Área en km², 0 si no está disponible
            
            # Región y subregión con valor por defecto "N/A" si no están presentes
            region = pais.get("region", "N/A")
            subregion = pais.get("subregion", "N/A")
            
            # Procesar idiomas: obtener valores del diccionario y unirlos en una cadena
            # Ejemplo: {"spa": "Spanish"} -> "Español"
            idiomas = ", ".join(pais.get("languages", {}).values()) or "N/A"
            
            # Procesar monedas: iterar sobre el diccionario de monedas y formatearlas
            # Ejemplo: {"COP": {"name": "Colombian peso"}} -> "COP (Colombian peso)"
            monedas = ", ".join(
                [f"{code} ({info['name']})" for code, info in pais.get("currencies", {}).items()]
            ) or "N/A"
            
            # Calcular densidad poblacional (habitantes por km²)
            # Si el área es 0 (ej.: datos faltantes), la densidad se establece en 0
            densidad = calcular_densidad(poblacion, area)
            
            # Añadir el país procesado a la lista estructurada
            paises_estructurados.append({
                "Nombre": nombre,
                "Población": poblacion,
                "Área (km²)": area,
                "Densidad (hab/km²)": densidad,
                "Región": region,
                "Subregión": subregion,
                "Idiomas": idiomas,
                "Monedas": monedas
            })
        
        except Exception as e:
            # Registrar errores específicos de procesamiento sin detener la ejecución
            print(f"Error procesando país: {e}")
    
    return paises_estructurados

def calcular_densidad(poblacion, area):
    """
    Calcula la densidad poblacional de un país (habitantes por km²).
    
    Evita divisiones por cero y redondea el resultado a 2 decimales.
    
    Args:
        poblacion (int): Población total del país.
        area (float): Área territorial del país en km².
    
    Returns:
        float: Densidad poblacional calculada o 0 si el área es inválida (<= 0).
    """
    try:
        # Calcular densidad y redondear para mejorar legibilidad
        return round(poblacion / area, 2) if area > 0 else 0
    except ZeroDivisionError:
        # Manejar explícitamente división por cero (aunque ya está cubierto por el condicional)
        return 0

"""
modulo.py - Funciones adicionales para manejo de archivos y filtrado con expresiones regulares.
"""
def guardar_datos_json(datos, nombre_archivo="datos_paises.json"):
    """
    Guarda datos estructurados (lista de diccionarios) en un archivo JSON con formato legible.
    
    Este método asegura que los caracteres no ASCII (ej.: tildes, símbolos) se conserven correctamente.
    El archivo generado puede usarse para persistencia de datos, análisis posterior o compartir información estructurada.
    
    Args:
        datos (list): Lista de diccionarios con datos de países (ej.: [{"Nombre": "Colombia", ...}]). 
        nombre_archivo (str): Nombre del archivo JSON de salida. Por defecto: "datos_paises.json".
    
    Returns:
        None: La función no devuelve valores, pero imprime mensajes de éxito o error.
    
    Ejemplo de uso:
        guardar_datos_json(datos_estructurados, "paises_filtrados.json")
    """
    try:
        # Abrir el archivo en modo escritura ('w') con codificación UTF-8 para soportar caracteres especiales
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            # Guardar datos en formato JSON con indentación para mejorar legibilidad
            # ensure_ascii=False: Mantiene caracteres no ASCII (ej.: "España" en lugar de "Espa\\u00f1a")
            json.dump(datos, f, indent=4, ensure_ascii=False)
        
        # Confirmación de guardado exitoso
        print(f"Datos guardados en {nombre_archivo}")
        
    except Exception as e:
        # Capturar errores comunes como permisos insuficientes o rutas inválidas
        print(f"Error al guardar el archivo: {e}")

def filtrar_paises_con_regex(datos_estructurados, patron_regex):
    """
    Filtra países cuyo nombre cumple con un patrón de expresión regular.
    
    Las expresiones regulares permiten búsquedas avanzadas (ej.: países que comienzan con "A", terminan en "land", etc.).
    Se usa `re.IGNORECASE` para hacer la búsqueda insensible a mayúsculas/minúsculas.
    
    Args:
        datos_estructurados (list): Lista de diccionarios con datos de países. 
        patron_regex (str): Patrón de expresión regular válido (ej.: "^A" para nombres que empiezan con A).
    
    Returns:
        list: Lista de países que coinciden con el patrón. Vacía si hay errores o no hay coincidencias.
    
    Ejemplos de patrones útiles:
        - "^A": Países que comienzan con "A" (ej.: Argentina, Alemania).
        - "land$": Países que terminan con "land" (ej.: Finlandia, Islandia).
        - "[0-9]": Países con números en su nombre (ej.: 3 de Mayo en Colombia).
    """
    try:
        # Compilar el patrón de expresión regular con bandera para ignorar mayúsculas/minúsculas
        regex = re.compile(patron_regex, re.IGNORECASE)
        
        # Usar comprensión de listas para filtrar países cuyo nombre cumple el patrón
        return [pais for pais in datos_estructurados if regex.search(pais["Nombre"])]
    
    except re.error as e:
        # Manejar errores de sintaxis en el patrón de regex (ej.: patrón inválido)
        print(f"Error en la expresión regular: {e}")
        return []

"""
modulo.py - Funciones adicionales para análisis estadístico de datos de países.
"""
def analizar_estadisticas(datos_estructurados, campo="Población"):
    """
    Calcula y organiza estadísticas descriptivas para un campo numérico específico en una lista de diccionarios.
    
    Esta función permite analizar campos como "Población", "Área (km²)" o "Densidad (hab/km²)" 
    de los datos estructurados de países, proporcionando métricas clave para interpretación geográfica/demográfica.
    
    Args:
        datos_estructurados (list): Lista de diccionarios con datos de países (ej.: [{"Nombre": "Colombia", "Población": 50_882_891, ...}]). 
        campo (str): Nombre del campo numérico a analizar. Por defecto: "Población".
    
    Returns:
        dict: Diccionario con las siguientes estadísticas:
            - Campo: Nombre del campo analizado.
            - Media: Valor promedio del campo.
            - Mediana: Valor central del campo ordenado.
            - Moda: Valor más frecuente.
            - Varianza: Dispersión de los valores respecto a la media.
            - Desviación Estándar: Variabilidad promedio de los valores.
        None: Si no hay datos válidos o el campo no es numérico.
    
    Ejemplo de retorno exitoso:
        {
            "Campo": "Población",
            "Media": 39378755.88,
            "Mediana": 6888660.0,
            "Moda": 50882891,
            "Varianza": 12516570609612345,
            "Desviación Estándar": 111877480.37
        }
    """
    # Extraer valores del campo especificado, filtrando valores <= 0 (ej.: países sin dato disponible)
    valores = [pais[campo] for pais in datos_estructurados if pais.get(campo, 0) > 0]
    
    if not valores:
        print(f"No hay datos válidos en el campo '{campo}'.")
        return None

    try:
        # Calcular estadísticas básicas usando el módulo statistics
        # Media: Promedio aritmético de los valores
        media = round(statistics.mean(valores), 2)
        
        # Mediana: Valor que divide los datos ordenados en dos partes iguales
        mediana = statistics.median(valores)
        
        # Moda: Valor que aparece con mayor frecuencia
        moda = statistics.mode(valores)
        
        # Varianza: Promedio del cuadrado de las diferencias respecto a la media (mide dispersión)
        varianza = round(statistics.variance(valores), 2)
        
        # Desviación estándar: Raíz cuadrada de la varianza (más interpretable que la varianza)
        desviacion_std = round(statistics.stdev(valores), 2)
        
        # Devolver estadísticas en un diccionario estructurado
        return {
            "Campo": campo,
            "Media": media,
            "Mediana": mediana,
            "Moda": moda,
            "Varianza": varianza,
            "Desviación Estándar": desviacion_std
        }
    
    except statistics.StatisticsError as e:
        # Manejar errores comunes en cálculos estadísticos:
        # - StatisticsError: Si hay múltiples modas (en versiones antiguas de Python) o pocos datos para varianza
        print(f"Error al calcular estadísticas: {e}")
        return None

"""
modulo.py - Funciones adicionales para exportar datos estructurados a Excel usando pandas.
"""
def exportar_datos_excel(datos, nombre_archivo="datos_paises.xlsx"):
    """
    Exporta una lista de diccionarios a un archivo Excel (.xlsx) y muestra una vista previa en consola.
    
    Este método convierte los datos estructurados (ej.: países con campos como nombre, población, región)
    en un DataFrame de pandas, lo que permite generar archivos Excel con formato tabular limpio y legible.
    
    Args:
        datos (list): Lista de diccionarios con datos de países (ej.: [{"Nombre": "Colombia", "Población": 50_882_891, ...}]). 
        nombre_archivo (str): Nombre del archivo Excel de salida. Por defecto: "datos_paises.xlsx".
    
    Returns:
        None: La función no devuelve valores, pero imprime mensajes de éxito o error.
    
    Ejemplo de salida en Excel:
        | Nombre      | Población | Área (km²) | Densidad (hab/km²) | Región  | Subregión     | Idiomas         | Monedas                |
        |-------------|-----------|------------|---------------------|---------|---------------|-----------------|------------------------|
        | Colombia    | 50882891  | 1141748    | 44.56               | América | Sudamérica    | Español         | COP (Peso colombiano)  |
        | ...         | ...       | ...        | ...                 | ...     | ...           | ...             | ...                    |
    """
    try:
        # Convertir la lista de diccionarios a un DataFrame de pandas
        # Un DataFrame es una estructura tabular ideal para análisis y exportación a Excel
        df = pd.DataFrame(datos)
        
        # Mostrar una vista previa de los datos que se exportarán (primeras 5 filas)
        # Esto permite verificar que los campos estén correctamente estructurados antes de guardar
        print(f"\nMostrando las primeras filas que se exportarán a {nombre_archivo}:")
        print(df.head())
        
        # Guardar el DataFrame en un archivo Excel (.xlsx)
        # Parámetros clave:
        # - index=False: Evita guardar el índice numérico por defecto de pandas
        # - engine="openpyxl": Especifica el motor para trabajar con archivos .xlsx modernos
        df.to_excel(nombre_archivo, index=False, engine="openpyxl")
        print(f"Datos exportados exitosamente a {nombre_archivo}")
    
    except Exception as e:
        # Manejar errores comunes:
        # - Falta de bibliotecas (pandas, openpyxl no instaladas)
        # - Datos con tipos no compatibles (ej.: objetos complejos en lugar de valores atómicos)
        print(f"Error al exportar a Excel: {e}")

"""
modulo.py - Funciones para generar gráficos con matplotlib basados en datos estructurados.
"""
def graficar_datos(datos, tipo_grafico="barras", titulo="Gráfico", eje_x="X", eje_y="Y", campo_x="Nombre", campo_y="Población"):
    """
    Genera gráficos de barras o líneas a partir de datos estructurados de países.
    
    Esta función usa matplotlib para visualizar datos como población, área o densidad de países. 
    Permite personalizar el tipo de gráfico, etiquetas y campos a representar.
    
    Args:
        datos (list): Lista de diccionarios con datos de países (ej.: [{"Nombre": "Colombia", "Población": 50_882_891, ...}]). 
        tipo_grafico (str): Tipo de gráfico ("barras" o "lineas").
        titulo (str): Título del gráfico (ej.: "Top 10 Países por Población").
        eje_x (str): Etiqueta del eje X (ej.: "País").
        eje_y (str): Etiqueta del eje Y (ej.: "Población").
        campo_x (str): Campo de los datos para el eje X (ej.: "Nombre", "Región").
        campo_y (str): Campo de los datos para el eje Y (ej.: "Población", "Área (km²)").
    
    Returns:
        None: La función no devuelve valores, pero imprime mensajes de éxito o error.
    
    Ejemplo de uso:
        graficar_datos(
            top_poblacion,
            tipo_grafico="barras",
            titulo="Top 10 Países por Población",
            eje_x="País",
            eje_y="Población",
            campo_x="Nombre",
            campo_y="Población"
        )
    """
    try:
        # Extraer valores para los ejes X e Y desde los datos estructurados
        # Ejemplo: Si campo_x="Nombre", valores_x = ["Colombia", "Brasil", ...]
        valores_x = [pais[campo_x] for pais in datos]
        valores_y = [pais[campo_y] for pais in datos]
        
        # Configurar estilo y tamaño del gráfico
        # Tamaño grande (12x6 pulgadas) para mejorar legibilidad
        plt.figure(figsize=(12, 6))
        
        # Título y etiquetas de ejes (alineado con estándares internacionales de gráficas)
        # Ejemplo: "Relación entre temperatura y tiempo de ebullición"
        plt.title(titulo)
        plt.xlabel(eje_x)  # Ejemplo: "País"
        plt.ylabel(eje_y)  # Ejemplo: "Población"
        
        # Agregar rejilla con estilo punteado y transparencia para no sobrecargar la visualización
        plt.grid(True, linestyle='--', alpha=0.5)
        
        # Seleccionar y dibujar el tipo de gráfico especificado
        if tipo_grafico == "barras":
            # Gráfico de barras para comparar categorías (ej.: países)
            plt.bar(valores_x, valores_y, color='skyblue')
        elif tipo_grafico == "lineas":
            # Gráfico de líneas para mostrar tendencias (ej.: cambio de población en el tiempo)
            plt.plot(valores_x, valores_y, marker='o', color='green', linestyle='-')
        else:
            # Validación de tipo de gráfico permitido
            print("Tipo de gráfico no válido. Use 'barras' o 'lineas'.")
            return
        
        # Rotar etiquetas del eje X para evitar solapamiento (ej.: nombres largos)
        # Alineación a la derecha para mejor visualización
        plt.xticks(rotation=45, ha='right')
        
        # Guardar gráfico como imagen PNG con nombre basado en el título
        # Ejemplo: "top_10_países_por_población.png"
        nombre_archivo = f"{titulo.lower().replace(' ', '_')}.png"
        plt.tight_layout()  # Evitar recortes en etiquetas largas
        plt.savefig(nombre_archivo)  # Guardar gráfico
        print(f"Gráfico guardado como {nombre_archivo}")
        
        # Mostrar gráfico temporalmente y cerrarlo automáticamente (no bloquea ejecución)
        plt.show(block=False)
        plt.pause(2)  # Mantener ventana abierta 2 segundos
        plt.close()  # Cerrar figura para liberar memoria
    
    except Exception as e:
        # Manejar errores comunes:
        # - Claves inexistentes en los datos (ej.: campo_x o campo_y no válidos)
        # - Tipos de datos no compatibles (ej.: valores no numéricos en gráficos de línea)
        print(f"Error al crear el gráfico: {e}")
        
"""
modulo.py - Funciones para interpretar resultados estadísticos de datos de países.
"""
def interpretar_resultados(estadisticas, datos_originales=None, campo="Población"):
    """
    Interpreta estadísticas descriptivas (media, mediana, moda, varianza) y las relaciona con contexto geográfico/demográfico.
    
    Esta función transforma números abstractos en conclusiones interpretables, explicando patrones como asimetría, dispersión o valores extremos.
    Es especialmente útil para contextualizar análisis estadísticos en campos como población, área o densidad de países.
    
    Args:
        estadisticas (dict): Diccionario con estadísticas calculadas (ej.: {"Media": 39378755.88, "Mediana": 6888660.0, ...}).
        datos_originales (list): Lista de diccionarios con datos completos de países (opcional, para identificar máximos/mínimos).
        campo (str): Campo analizado (ej.: "Población", "Área (km²)"). Usado junto con datos_originales.
    
    Returns:
        str: Texto con interpretaciones claras, listo para imprimir o guardar en informes.
    
    Ejemplo de retorno:
        ## Interpretación de Estadísticas: Población ##
        - La **media** (39378755.88) y la **mediana** (6888660.0) muestran alta asimetría, 
          indicando que hay valores extremos influyendo en el promedio.
        - El valor más frecuente (**moda**) es 50882891, lo cual podría representar un grupo de países con características similares.
        - La **varianza** (12516570609612345) y la **desviación estándar** (111877480.37) indican alta dispersión entre los valores.
        
        ## Contexto Geográfico/Demográfico ##
        - El país con mayor Población es China (1402112000).
        - El país con menor Población es Vatican City (451).
    """
    # Validación inicial: si no hay estadísticas, retornar mensaje informativo
    if not estadisticas:
        return "No hay estadísticas disponibles para interpretar."
    
    interpretacion = []
    
    # Título de sección para organizar resultados
    interpretacion.append(f"## Interpretación de Estadísticas: {estadisticas['Campo']} ##")
    
    # Comparar Media y Mediana para detectar asimetría
    media = estadisticas["Media"]
    mediana = estadisticas["Mediana"]
    diferencia = abs(media - mediana)
    
    # Calcular el umbral del 20% para evaluar asimetría (recomendado en análisis estadístico)
    umbral = 0.2 * max(media, mediana)
    
    if diferencia > umbral:
        # Alta asimetría: media > mediana -> colas positivas (ej.: países muy poblados)
        tendencia = "alta asimetría" if media > mediana else "baja asimetría"
        interpretacion.append(
            f"- La **media** ({media}) y la **mediana** ({mediana}) muestran {tendencia}, "
            "indicando que hay valores extremos influyendo en el promedio. "
            "Esto suele ocurrir cuando unos pocos países (ej.: China, India) dominan el total global."
        )
    else:
        interpretacion.append(
            f"- La **media** ({media}) y la **mediana** ({mediana}) son similares, "
            "sugiriendo una distribución relativamente simétrica. "
            "Los países tienen tamaños comparables en este campo."
        )
    
    # Moda: valor más frecuente
    moda = estadisticas["Moda"]
    interpretacion.append(
        f"- El valor más frecuente (**moda**) es {moda}, lo cual podría representar un grupo de países con características similares. "
        "Ejemplo: múltiples pequeñas naciones insulares con poblaciones cercanas a 50 millones."
    )
    
    # Varianza y Desviación Estándar: dispersión de datos
    varianza = estadisticas["Varianza"]
    desviacion_std = estadisticas["Desviación Estándar"]
    coeficiente_variacion = desviacion_std / media if media != 0 else float('inf')
    
    # Clasificar dispersión usando el coeficiente de variación (CV)
    # - CV < 0.5: baja dispersión | 0.5 < CV < 1: moderada | CV > 1: alta
    if coeficiente_variacion > 1:
        dispersión = "alta dispersión"
    elif coeficiente_variacion > 0.5:
        dispersión = "dispersión moderada"
    else:
        dispersión = "baja dispersión"
    
    interpretacion.append(
        f"- La **varianza** ({varianza}) y la **desviación estándar** ({desviacion_std}) indican {dispersión} entre los valores. "
        "Esto refleja si los países son homogéneos (baja dispersión) o muy diversos (alta dispersión)."
    )
    
    # Contexto geográfico/demográfico (si se proporcionan datos originales y el campo es población)
    if datos_originales and campo == "Población":
        # Identificar países con máximos y mínimos usando funciones lambda
        pais_max = max(datos_originales, key=lambda x: x.get(campo, 0))
        pais_min = min(datos_originales, key=lambda x: x.get(campo, 0))
        
        interpretacion.append("\n## Contexto Geográfico/Demográfico ##")
        interpretacion.append(
            f"- El país con mayor {campo} es **{pais_max['Nombre']}** ({pais_max[campo]})."
        )
        interpretacion.append(
            f"- El país con menor {campo} es **{pais_min['Nombre']}** ({pais_min[campo]})."
        )
    
    # Unir todas las líneas de interpretación en un solo texto
    return "\n".join(interpretacion)