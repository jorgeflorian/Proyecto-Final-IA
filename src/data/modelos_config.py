"""
    Jorge Augusto Cesar Florian Silvestre 
    17-EISN-2-009
"""

"""
Archivo de configuración para los modelos DALL-E disponibles.
Contiene información sobre los modelos, tamaños, estilos y calidades disponibles.
Este módulo centraliza la configuración de parámetros para la generación de imágenes
y proporciona funciones de ayuda para acceder a estos parámetros.
"""

# Lista de modelos DALL-E actualmente soportados por la API de OpenAI
# Estos modelos se utilizan para la generación de imágenes a partir de texto
MODELOS_DISPONIBLES = [
    "dall-e-3",  # Modelo más reciente con mayor capacidad y calidad
    "dall-e-2"   # Modelo anterior, con diferentes capacidades
]

# Diccionario que mapea cada modelo a sus tamaños de imagen disponibles
# Las dimensiones están expresadas como "ancho x alto" en píxeles
TAMANIOS_DISPONIBLES = {
    "dall-e-3": ["1024x1024", "1792x1024", "1024x1792"],  # Soporta formato rectangular
    "dall-e-2": ["256x256", "512x512", "1024x1024"]       # Solo formatos cuadrados
}

# Diccionario que mapea cada modelo a sus estilos de generación disponibles
# - vivid: Colores más intensos y contrastados
# - natural: Representación más realista y sutil
ESTILOS_DISPONIBLES = {
    "dall-e-3": ["vivid", "natural"],
    "dall-e-2": ["vivid", "natural"]
}

# Diccionario que mapea cada modelo a sus niveles de calidad disponibles
# - standard: Calidad estándar de generación
# - hd: Alta definición (solo disponible en DALL-E 3)
CALIDADES_DISPONIBLES = {
    "dall-e-3": ["standard", "hd"],
    "dall-e-2": ["standard"]
}

# Diccionario que mapea cada modelo a los tipos de transformaciones que puede realizar
# - generation: Creación de imágenes desde cero a partir de una descripción
# - variation: Creación de variaciones de una imagen existente
# - edit: Modificación de partes específicas de una imagen existente
TRANSFORMACIONES_DISPONIBLES = {
    "dall-e-3": ["generation"],  # DALL-E 3 solo soporta generación de nuevas imágenes
    "dall-e-2": ["generation", "variation", "edit"]  # DALL-E 2 es más versátil en operaciones
}

# Mensajes de error predefinidos para situaciones comunes de uso incorrecto
# Estos mensajes se utilizan para proporcionar feedback claro al usuario
MENSAJES_ERROR = {
    "API_KEY_REQUERIDA": "Por favor, inicializa el cliente con tu API key primero",
    "VARIACIONES_SOLO_DALLE2": "Las variaciones de imágenes solo están disponibles con el modelo DALL-E 2",
    "EDICIONES_SOLO_DALLE2": "Las ediciones de imágenes solo están disponibles con el modelo DALL-E 2"
}


def obtener_modelos():
    """
    Retorna la lista de modelos DALL-E disponibles.
    
    Returns:
        list: Lista con los nombres de los modelos DALL-E soportados.
    """
    return MODELOS_DISPONIBLES


def obtener_tamanios(modelo):
    """
    Retorna los tamaños disponibles para un modelo específico.
    
    Args:
        modelo (str): Nombre del modelo DALL-E ('dall-e-2' o 'dall-e-3').
        
    Returns:
        list: Lista de tamaños disponibles para el modelo especificado.
              Retorna lista vacía si el modelo no existe.
    """
    return TAMANIOS_DISPONIBLES.get(modelo, [])


def obtener_estilos(modelo):
    """
    Retorna los estilos disponibles para un modelo específico.
    
    Args:
        modelo (str): Nombre del modelo DALL-E ('dall-e-2' o 'dall-e-3').
        
    Returns:
        list: Lista de estilos disponibles para el modelo especificado.
              Retorna lista vacía si el modelo no existe.
    """
    return ESTILOS_DISPONIBLES.get(modelo, [])


def obtener_calidades(modelo):
    """
    Retorna las calidades disponibles para un modelo específico.
    
    Args:
        modelo (str): Nombre del modelo DALL-E ('dall-e-2' o 'dall-e-3').
        
    Returns:
        list: Lista de calidades disponibles para el modelo especificado.
              Retorna lista vacía si el modelo no existe.
    """
    return CALIDADES_DISPONIBLES.get(modelo, [])


def obtener_transformaciones(modelo):
    """
    Retorna las transformaciones disponibles para un modelo específico.
    
    Args:
        modelo (str): Nombre del modelo DALL-E ('dall-e-2' o 'dall-e-3').
        
    Returns:
        list: Lista de transformaciones disponibles para el modelo especificado.
              Retorna lista vacía si el modelo no existe.
    """
    return TRANSFORMACIONES_DISPONIBLES.get(modelo, [])


def obtener_mensaje_error(clave):
    """
    Retorna un mensaje de error según la clave proporcionada.
    
    Args:
        clave (str): Identificador del mensaje de error requerido.
        
    Returns:
        str: Mensaje de error correspondiente a la clave.
              Retorna cadena vacía si la clave no existe.
    """
    return MENSAJES_ERROR.get(clave, "")
