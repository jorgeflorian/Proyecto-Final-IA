"""
    Jorge Augusto Cesar Florian Silvestre 
    17-EISN-2-009
"""

"""
Archivo que contiene configuraciones y funciones para optimizar prompts usando modelos de lenguaje.
Permite mejorar los prompts en español convirtiéndolos a inglés y enriqueciéndolos para generar mejores imágenes.
Este módulo es parte del sistema generador de cómics y se encarga de la optimización de las descripciones
textuales para convertirlas en instrucciones efectivas para los modelos de generación de imágenes.
"""

# Importaciones necesarias

# Configuración de modelos de lenguaje
# Modelo predeterminado (más económico/rápido para uso general)
from typing import List
MODELO_PREDETERMINADO: str = "o3-mini"
# Modelo alternativo (más avanzado, mejor calidad pero más costoso)
MODELO_ALTERNATIVO: str = "gpt-4o"

# Instrucciones del sistema para diferentes estilos de optimización
# Estas plantillas guían al modelo de lenguaje sobre cómo mejorar los prompts según cada estilo de cómic
INSTRUCCIONES_SISTEMA = {
    "comic": """
    Tu tarea es optimizar prompts para generar imágenes de cómics.
    Para cada prompt que recibas:
    1. Tradúcelo al inglés
    2. Añade detalles estilísticos relevantes (iluminación, perspectiva, acabado)
    3. Expande la descripción de personajes, escenas y acciones
    4. Incluye términos técnicos de arte secuencial
    5. Mantén la esencia y estilo del prompt original
    6. NO cambies personajes, lugares o conceptos fundamentales
    7. Siempre devuelve SOLAMENTE el prompt mejorado en inglés, sin explicaciones
    """,

    "manga": """
    Tu tarea es optimizar prompts para generar imágenes de estilo manga/anime.
    Para cada prompt que recibas:
    1. Tradúcelo al inglés
    2. Añade términos específicos del manga (efectos visuales, expresiones faciales)
    3. Expande la descripción de personajes, escenas y emociones
    4. Incluye términos técnicos de arte de manga y anime
    5. Mantén la esencia y estilo del prompt original
    6. NO cambies personajes, lugares o conceptos fundamentales
    7. Siempre devuelve SOLAMENTE el prompt mejorado en inglés, sin explicaciones
    """,

    "europeo": """
    Tu tarea es optimizar prompts para generar imágenes de cómics de estilo europeo.
    Para cada prompt que recibas:
    1. Tradúcelo al inglés
    2. Añade detalles de línea clara, colores planos, y fondos detallados
    3. Expande la descripción para reflejar el estilo franco-belga o europeo
    4. Incluye términos técnicos del arte secuencial europeo
    5. Mantén la esencia y estilo del prompt original
    6. NO cambies personajes, lugares o conceptos fundamentales
    7. Siempre devuelve SOLAMENTE el prompt mejorado en inglés, sin explicaciones
    """,

    "general": """
    Tu tarea es optimizar prompts para generar imágenes de alta calidad.
    Para cada prompt que recibas:
    1. Tradúcelo al inglés
    2. Añade detalles visuales relevantes (iluminación, perspectiva, acabado)
    3. Expande la descripción para hacerla más vívida y específica
    4. Incluye términos técnicos de arte digital y composición
    5. Mantén la esencia y estilo del prompt original
    6. NO cambies personajes, lugares o conceptos fundamentales
    7. Siempre devuelve SOLAMENTE el prompt mejorado en inglés, sin explicaciones
    """
}

# Parámetros de generación para diferentes modelos
# Configuración específica para cada modelo de lenguaje soportado
PARAMETROS_GENERACION = {
    "gpt-3.5-turbo": {
        # Control de creatividad (mayor valor = más variabilidad)
        "temperature": 0.7,
        "max_tokens": 300    # Límite máximo de tokens en la respuesta
    },
    "gpt-4": {
        "temperature": 0.6,
        "max_tokens": 350
    },
    "o3-mini": {
        # El modelo o3-mini no soporta el parámetro temperature
        "max_tokens": 300
    },
    "gpt-4o": {
        "temperature": 0.6,
        "max_tokens": 350
    }
}


def seleccionar_instruccion_sistema(categoria: str) -> str:
    """
    Selecciona la instrucción del sistema más adecuada según la categoría de cómic.

    Esta función mapea diferentes categorías y estilos de cómics a las instrucciones
    predefinidas más apropiadas para optimizar los prompts.

    Args:
        categoria: Categoría de cómic o estilo ('Marvel', 'DC Comics', 'Manga', 'Europeo', etc.)

    Returns:
        str: Instrucción del sistema a utilizar para el modelo de lenguaje
    """
    # Mapear categorías específicas a nuestras instrucciones del sistema
    if categoria.lower() in ['marvel', 'dc comics', 'alternativo', 'superhéroes']:
        return INSTRUCCIONES_SISTEMA["comic"]
    elif categoria.lower() in ['manga', 'anime', 'shonen', 'seinen', 'shojo']:
        return INSTRUCCIONES_SISTEMA["manga"]
    elif categoria.lower() in ['europeo', 'franco-belga', 'línea clara', 'aventura', 'tintin']:
        return INSTRUCCIONES_SISTEMA["europeo"]
    else:
        return INSTRUCCIONES_SISTEMA["general"]


def extraer_categoria_desde_contexto(contexto: str) -> str:
    """
    Extrae la categoría de cómic desde el texto de contexto proporcionado.

    Analiza el texto de contexto para identificar términos clave que indiquen
    el estilo o género de cómic más adecuado.

    Args:
        contexto: Texto de contexto que puede contener información sobre la categoría del cómic

    Returns:
        str: Categoría inferida ('Marvel', 'DC Comics', 'Manga', 'Europeo') o 'general' si no se puede determinar
    """
    contexto_lower = contexto.lower()

    # Búsqueda de términos clave relacionados con cada categoría
    if any(term in contexto_lower for term in ['marvel', 'superhéroe', 'superhero', 'avengers']):
        return "Marvel"
    elif any(term in contexto_lower for term in ['dc', 'batman', 'superman', 'justice league']):
        return "DC Comics"
    elif any(term in contexto_lower for term in ['manga', 'anime', 'shonen', 'seinen', 'shojo']):
        return "Manga"
    elif any(term in contexto_lower for term in ['europeo', 'franco-belga', 'línea clara', 'tintin']):
        return "Europeo"
    else:
        return "general"


def obtener_modelos_disponibles() -> List[str]:
    """
    Retorna la lista de modelos de lenguaje disponibles para la optimización de prompts.

    Esta función permite a la interfaz de usuario conocer qué modelos pueden utilizarse
    para el proceso de optimización de prompts.

    Returns:
        List[str]: Lista de identificadores de modelos disponibles para su uso
    """
    return list(PARAMETROS_GENERACION.keys())
