"""
    Jorge Augusto Cesar Florian Silvestre 
    17-EISN-2-009
"""

"""
Archivo que contiene prompts base para diferentes estilos de cómics.
Estos prompts se pueden utilizar como plantillas para generar imágenes con estilos específicos.

Este módulo proporciona:
- Diccionarios de prompts organizados por categorías y estilos
- Colecciones de personajes, villanos y lugares para completar los prompts
- Funciones para obtener y manipular los diferentes elementos del prompt
- Generador de prompts completos a partir de plantillas base
"""

# Diccionario de prompts base organizados por categorías
COMIC_PROMPTS = {
    "Marvel": {
        "Superhéroes": "Ilustración de estilo Marvel Comics, con colores vibrantes y líneas dinámicas, mostrando {personaje} en una pose heroica con su traje característico, estilo de arte de Jack Kirby.",
        "Acción": "Escena de acción al estilo Marvel, con {personaje} luchando contra {villano}, con efectos de explosión y líneas de movimiento, estilo de arte de Jim Lee.",
        "Portada": "Portada de cómic al estilo Marvel, con {personaje} en primer plano, título dramático en la parte superior, fondo con ciudad en perspectiva, estilo de arte de Alex Ross."
    },
    "DC Comics": {
        "Superhéroes": "Ilustración al estilo DC Comics, con tonos oscuros y dramáticos, mostrando {personaje} vigilando la ciudad desde lo alto, estilo de arte de Jim Lee.",
        "Gotham": "Escena nocturna de Gotham City al estilo DC Comics, con {personaje} entre gárgolas, niebla y luces de ciudad, estilo de arte de Greg Capullo.",
        "Portada": "Portada épica al estilo DC Comics, con {personaje} en pose imponente, logo icónico, fondo con cielo tormentoso, estilo de arte de Ivan Reis."
    },
    "Manga": {
        "Shonen": "Ilustración de estilo manga shonen, con {personaje} en pose de batalla, ojos grandes expresivos, líneas de velocidad, estilo de arte de Akira Toriyama.",
        "Seinen": "Panel de manga seinen detallado, mostrando {personaje} con expresión seria, sombreado detallado en blanco y negro, estilo de arte de Kentaro Miura.",
        "Shojo": "Escena de manga shojo, con {personaje} rodeado de flores y brillos, ojos grandes y expresivos, fondos detallados, estilo de arte de CLAMP."
    },
    "Europeo": {
        "Franco-Belga": "Ilustración de estilo línea clara franco-belga, mostrando {personaje} en escena detallada, colores planos vibrantes, estilo de arte de Hergé.",
        "Aventura": "Panel de cómic europeo de aventura, con {personaje} explorando {lugar}, perspectiva panorámica detallada, estilo de arte de Moebius.",
        "Fantasía": "Escena de fantasía al estilo europeo, con {personaje} en un mundo imaginario con criaturas fantásticas, estilo de arte de Enki Bilal."
    },
    "Alternativo": {
        "Indie": "Ilustración de estilo indie/alternativo, con {personaje} en escena minimalista, estilo artístico experimental, como el arte de Daniel Clowes.",
        "Novela Gráfica": "Panel de novela gráfica, con {personaje} en momento contemplativo, uso dramático de sombras y luz, estilo de arte de Dave McKean.",
        "Underground": "Arte de cómic underground, con {personaje} en estilo caricaturesco exagerado, líneas expresivas, como el arte de Robert Crumb."
    }
}

# Ejemplos de personajes por categoría para completar los prompts
PERSONAJES_EJEMPLO = {
    "Marvel": ["Spider-Man", "Iron Man", "Captain America", "Thor", "Black Widow", "Hulk", "Doctor Strange"],
    "DC Comics": ["Batman", "Superman", "Wonder Woman", "Flash", "Aquaman", "Green Lantern", "Harley Quinn"],
    "Manga": ["Naruto", "Goku", "Luffy", "Ichigo", "Mikasa", "Sailor Moon", "Spike Spiegel"],
    "Europeo": ["Tintin", "Asterix", "Corto Maltese", "Lucky Luke", "Spirou", "Blake y Mortimer"],
    "Alternativo": ["Ghost World", "Sandman", "V de Vendetta", "American Splendor", "Persepolis"]
}

# Villanos comunes para escenas de acción
VILLANOS_EJEMPLO = {
    "Marvel": ["Thanos", "Green Goblin", "Magneto", "Loki", "Doctor Doom", "Venom"],
    "DC Comics": ["Joker", "Lex Luthor", "Darkseid", "Bane", "Sinestro", "Deathstroke"],
    "Manga": ["Frieza", "Madara", "Cell", "Pain", "Aizen", "Dio Brando"],
    "Europeo": ["Rastapopoulos", "Dalton Brothers", "Olrik", "Darth Vader"],
    "Alternativo": ["Personaje sombrío", "Entidad cósmica", "Figura misteriosa encapuchada"]
}

# Lugares para escenas de aventura
LUGARES_EJEMPLO = [
    "una antigua ciudad perdida", "un templo extraterrestre", "una ciudad futurista",
    "un planeta alienígena", "un bosque encantado", "un paisaje post-apocalíptico",
    "una nave espacial abandonada", "un castillo medieval", "una dimensión paralela"
]

# Instrucciones adicionales para mejorar los prompts
INSTRUCCIONES_ESTILO = {
    "Detallado": ", con detalles ultra finos, iluminación cinematográfica, composición profesional",
    "Minimalista": ", estilo minimalista, pocos colores, líneas simples pero expresivas",
    "Acuarela": ", técnica de acuarela, colores fluidos y transparentes, bordes difuminados",
    "Retro": ", estilo retro de los años 70/80, grano de papel antiguo, colores desaturados",
    "Digital": ", arte digital moderno, colores vibrantes, efectos de iluminación avanzados",
    "3D": ", efecto de renderizado 3D, texturas detalladas, iluminación volumétrica"
}


def obtener_categorias():
    """
    Retorna todas las categorías de cómics disponibles.
    
    Returns:
        list: Lista con los nombres de todas las categorías de cómics disponibles.
    """
    return list(COMIC_PROMPTS.keys())


def obtener_estilos(categoria):
    """
    Retorna los estilos disponibles para una categoría específica.
    
    Args:
        categoria (str): Nombre de la categoría de cómic.
        
    Returns:
        list: Lista con los nombres de los estilos disponibles para la categoría especificada.
              Devuelve una lista vacía si la categoría no existe.
    """
    return list(COMIC_PROMPTS.get(categoria, {}).keys())


def obtener_prompt_base(categoria, estilo):
    """
    Retorna el prompt base para una categoría y estilo específicos.
    
    Args:
        categoria (str): Nombre de la categoría de cómic.
        estilo (str): Nombre del estilo dentro de la categoría.
        
    Returns:
        str: Texto del prompt base correspondiente a la categoría y estilo.
             Devuelve una cadena vacía si la categoría o estilo no existen.
    """
    return COMIC_PROMPTS.get(categoria, {}).get(estilo, "")


def obtener_personajes(categoria):
    """
    Retorna ejemplos de personajes para una categoría específica.
    
    Args:
        categoria (str): Nombre de la categoría de cómic.
        
    Returns:
        list: Lista con los nombres de personajes de ejemplo para la categoría.
              Devuelve una lista vacía si la categoría no existe.
    """
    return PERSONAJES_EJEMPLO.get(categoria, [])


def obtener_villanos(categoria):
    """
    Retorna ejemplos de villanos para una categoría específica.
    
    Args:
        categoria (str): Nombre de la categoría de cómic.
        
    Returns:
        list: Lista con los nombres de villanos de ejemplo para la categoría.
              Devuelve una lista vacía si la categoría no existe.
    """
    return VILLANOS_EJEMPLO.get(categoria, [])


def obtener_lugares():
    """
    Retorna ejemplos de lugares para escenas de aventura.
    
    Returns:
        list: Lista con descripciones de lugares que pueden utilizarse en los prompts.
    """
    return LUGARES_EJEMPLO


def obtener_instrucciones_estilo(estilo):
    """
    Retorna instrucciones adicionales para un estilo específico.
    
    Args:
        estilo (str): Nombre del estilo de ilustración.
        
    Returns:
        str: Texto con instrucciones adicionales para el estilo específico.
             Devuelve una cadena vacía si el estilo no existe.
    """
    return INSTRUCCIONES_ESTILO.get(estilo, "")


def generar_prompt_completo(prompt_base, personaje="superhéroe", villano="villano", lugar="lugar"):
    """
    Genera un prompt completo reemplazando las variables en el prompt base.
    
    Esta función toma un prompt base que contiene marcadores entre llaves y los
    reemplaza con los valores proporcionados para crear un prompt final personalizado.

    Args:
        prompt_base (str): String con el prompt base que contiene variables entre llaves
        personaje (str, opcional): Nombre del personaje a incluir. Por defecto "superhéroe".
        villano (str, opcional): Nombre del villano a incluir. Por defecto "villano".
        lugar (str, opcional): Nombre del lugar a incluir. Por defecto "lugar".

    Returns:
        str: String con el prompt completo, con todas las variables reemplazadas
             por los valores proporcionados.
    """
    prompt_completo = prompt_base.replace("{personaje}", personaje)
    prompt_completo = prompt_completo.replace("{villano}", villano)
    prompt_completo = prompt_completo.replace("{lugar}", lugar)
    return prompt_completo
