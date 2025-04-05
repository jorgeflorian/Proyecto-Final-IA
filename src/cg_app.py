"""
    Jorge Augusto Cesar Florian Silvestre 
    17-EISN-2-009
"""

"""
Generador de Cómics - Aplicación Principal
==========================================

Este módulo contiene la clase principal para el generador de cómics que utiliza 
modelos de IA para crear viñetas, transformar imágenes y generar contenido visual 
en diferentes estilos de cómic.

El sistema permite:
- Generar viñetas de cómic a partir de descripciones textuales
- Transformar imágenes existentes en estilos de cómic
- Editar imágenes con máscaras y prompts
- Generar variaciones de imágenes
- Optimizar prompts para mejorar la generación

Utiliza la API de OpenAI para la generación de imágenes y procesamiento de prompts.
"""

from typing import List, Tuple
import random
from PIL import Image

from data.comic_prompts import generar_prompt_completo, obtener_categorias, obtener_estilos, obtener_instrucciones_estilo, obtener_lugares, obtener_personajes, obtener_prompt_base, obtener_villanos
from data.modelos_config import (
    obtener_modelos, obtener_tamanios, obtener_estilos as obtener_estilos_modelo,
    obtener_calidades, obtener_transformaciones
)
from core.ai import OpenAIHandler


class GeneradorDeComics:
    """
    Clase principal que gestiona la generación de cómics mediante IA.
    
    Esta clase coordina la interacción entre la interfaz de usuario y los modelos
    de IA, gestionando la configuración de los modelos, la generación de prompts y
    el procesamiento de imágenes para crear viñetas de cómic personalizadas.
    """
    def __init__(self):
        """
        Inicializa el generador de cómics cargando todas las configuraciones necesarias.
        
        Configura:
        - El manejador de la API de OpenAI
        - Los modelos disponibles
        - Las configuraciones específicas para cada modelo (tamaños, estilos, calidades)
        - Las categorías y estilos de cómics disponibles
        """
        # Crear una instancia del manejador de OpenAI
        self.ai_handler = OpenAIHandler()

        # Usar las funciones de modelos_config para obtener las configuraciones
        self.modelos_disponibles = obtener_modelos()

        # Inicializar diccionarios de configuraciones para cada modelo
        self.tamanios_disponibles = {modelo: obtener_tamanios(
            modelo) for modelo in self.modelos_disponibles}
        self.estilos_disponibles = {modelo: obtener_estilos_modelo(
            modelo) for modelo in self.modelos_disponibles}
        self.calidades_disponibles = {modelo: obtener_calidades(
            modelo) for modelo in self.modelos_disponibles}

        # Cargar categorías y estilos de cómics
        self.categorias_comics = obtener_categorias()
        self.estilos_comics = {categoria: obtener_estilos(
            categoria) for categoria in self.categorias_comics}

    def inicializar_cliente(self, api_key: str) -> Tuple[bool, str]:
        """
        Inicializa el cliente OpenAI con la API key proporcionada.
        
        Args:
            api_key (str): Clave de API para autenticación con OpenAI.
            
        Returns:
            Tuple[bool, str]: Una tupla con un booleano indicando éxito/fallo y un mensaje descriptivo.
        """
        return self.ai_handler.inicializar_cliente(api_key)

    def actualizar_configuracion_modelo(self, nombre_modelo: str) -> Tuple[List[str], List[str], List[str]]:
        """
        Actualiza las opciones disponibles según el modelo de IA seleccionado.
        
        Esta función recupera las configuraciones específicas del modelo seleccionado
        para presentar al usuario solo las opciones compatibles.
        
        Args:
            nombre_modelo (str): Nombre del modelo de IA seleccionado.
            
        Returns:
            Tuple[List[str], List[str], List[str]]: Tupla con listas de tamaños, estilos y calidades disponibles.
        """
        tamanios = obtener_tamanios(nombre_modelo)
        estilos = obtener_estilos_modelo(nombre_modelo)
        calidades = obtener_calidades(nombre_modelo)
        return tamanios, estilos, calidades

    def generar_vineta(self, prompt: str, modelo: str, tamanio: str, calidad: str, estilo: str, n: int) -> Tuple[List[str], str]:
        """
        Genera una viñeta de cómic basada en la entrada del usuario.
        
        Utiliza el modelo de IA especificado para crear una imagen que coincida con
        la descripción proporcionada en el prompt, aplicando el estilo y calidad seleccionados.
        
        Args:
            prompt (str): Descripción textual de la viñeta a generar.
            modelo (str): Modelo de IA a utilizar.
            tamanio (str): Tamaño de la imagen a generar.
            calidad (str): Nivel de calidad de la imagen.
            estilo (str): Estilo visual a aplicar.
            n (int): Número de imágenes a generar.
            
        Returns:
            Tuple[List[str], str]: Lista de URLs de las imágenes generadas y mensaje de estado.
        """
        return self.ai_handler.generar_vineta(prompt, modelo, tamanio, calidad, estilo, n)

    def procesar_imagen(
        self,
        imagen_input: Image.Image,
        categoria: str,
        estilo_comic: str,
        prompt_adicional: str = ""
    ) -> Tuple[str, str]:
        """
        Procesa una imagen existente para convertirla en una viñeta de cómic.
        
        Esta función prepara un prompt adecuado para transformar una imagen normal
        en una viñeta con el estilo de cómic especificado.
        
        Args:
            imagen_input (Image.Image): Imagen a procesar.
            categoria (str): Categoría de cómic deseada.
            estilo_comic (str): Estilo de cómic deseado.
            prompt_adicional (str, optional): Descripción adicional para guiar la transformación.
            
        Returns:
            Tuple[str, str]: Prompt generado y mensaje de estado.
        """
        if not imagen_input:
            return "", "Por favor, proporciona una imagen para procesar"

        # Generar un prompt base según la categoría y estilo seleccionados
        prompt_base = obtener_prompt_base(categoria, estilo_comic)
        if not prompt_base:
            return "", f"No se encontró un estilo válido para {categoria}/{estilo_comic}"

        # Crear un prompt para transformar la imagen
        prompt = f"Transforma esta imagen en una viñeta de cómic con el siguiente estilo: {prompt_base}"

        # Añadir prompt adicional si se proporcionó
        if prompt_adicional:
            prompt += f". {prompt_adicional}"

        return prompt, "Imagen lista para procesar"

    def imagen_a_base64(self, imagen: Image.Image) -> str:
        """
        Convierte una imagen PIL a base64 para su descarga.
        
        Args:
            imagen (Image.Image): Imagen PIL a convertir.
            
        Returns:
            str: Representación en base64 de la imagen.
        """
        return self.ai_handler.imagen_a_base64(imagen)

    def descargar_imagen(self, url_imagen: str) -> Tuple[str, str]:
        """
        Prepara una imagen para su descarga.
        
        Convierte una imagen desde su URL a un formato descargable para el usuario.
        
        Args:
            url_imagen (str): URL de la imagen a descargar.
            
        Returns:
            Tuple[str, str]: Datos de la imagen en formato base64 y nombre de archivo.
        """
        return self.ai_handler.descargar_imagen(url_imagen)

    def generar_prompt_ejemplo(self, categoria: str, estilo_comic: str,
                               personaje: str = "", villano: str = "",
                               lugar: str = "", estilo_adicional: str = "") -> str:
        """
        Genera un prompt de ejemplo basado en la categoría y estilo seleccionados.
        
        Esta función ayuda al usuario proporcionando un ejemplo de prompt bien formado
        que puede usar o modificar para obtener mejores resultados.
        
        Args:
            categoria (str): Categoría de cómic seleccionada.
            estilo_comic (str): Estilo de cómic seleccionado.
            personaje (str, optional): Personaje principal. Si está vacío, se selecciona aleatoriamente.
            villano (str, optional): Villano de la historia. Si está vacío, se selecciona aleatoriamente.
            lugar (str, optional): Escenario. Si está vacío, se selecciona aleatoriamente.
            estilo_adicional (str, optional): Estilo visual adicional a aplicar.
            
        Returns:
            str: Prompt de ejemplo completo.
        """
        prompt_base = obtener_prompt_base(categoria, estilo_comic)
        if not prompt_base:
            return ""

        # Si no se proporcionaron valores, seleccionar aleatoriamente
        if not personaje:
            personajes = obtener_personajes(categoria)
            personaje = random.choice(
                personajes) if personajes else "superhéroe"

        if not villano and "{villano}" in prompt_base:
            villanos = obtener_villanos(categoria)
            villano = random.choice(villanos) if villanos else "villano"

        if not lugar and "{lugar}" in prompt_base:
            lugares = obtener_lugares()
            lugar = random.choice(lugares) if lugares else "lugar"

        # Generar prompt completo
        prompt_completo = generar_prompt_completo(
            prompt_base, personaje, villano, lugar)

        # Añadir instrucciones de estilo adicionales si se solicitaron
        if estilo_adicional:
            instrucciones = obtener_instrucciones_estilo(estilo_adicional)
            prompt_completo += instrucciones

        return prompt_completo

    def generar_variacion_imagen(self, imagen_input: Image.Image, modelo: str, tamanio: str, n: int) -> Tuple[List[str], str]:
        """
        Genera variaciones de una imagen existente.
        
        Esta función crea diferentes versiones de una imagen manteniendo
        sus características esenciales pero con variaciones estilísticas.
        
        Args:
            imagen_input (Image.Image): Imagen para generar variaciones.
            modelo (str): Modelo a utilizar (solo compatible con dall-e-2).
            tamanio (str): Tamaño de la imagen de salida.
            n (int): Número de variaciones a generar.
            
        Returns:
            Tuple[List[str], str]: URLs de las imágenes generadas y mensaje de estado.
        """
        return self.ai_handler.generar_variacion_imagen(imagen_input, modelo, tamanio, n)

    def editar_imagen(self, imagen_input: Image.Image, mascara_input: Image.Image, prompt: str, modelo: str, tamanio: str, n: int) -> Tuple[List[str], str]:
        """
        Edita una imagen existente utilizando una máscara y un prompt.
        
        Permite modificar solo ciertas áreas de una imagen (definidas por la máscara)
        según la descripción proporcionada en el prompt.
        
        Args:
            imagen_input (Image.Image): Imagen base a editar.
            mascara_input (Image.Image): Máscara que indica qué áreas editar (áreas transparentes).
            prompt (str): Descripción de la imagen deseada.
            modelo (str): Modelo a utilizar (solo compatible con dall-e-2).
            tamanio (str): Tamaño de la imagen de salida.
            n (int): Número de ediciones a generar.
            
        Returns:
            Tuple[List[str], str]: URLs de las imágenes generadas y mensaje de estado.
        """
        return self.ai_handler.editar_imagen(imagen_input, mascara_input, prompt, modelo, tamanio, n)

    def generar_mascara_imagen(self, imagen: Image.Image) -> Image.Image:
        """
        Genera una máscara transparente para toda la imagen.
        
        Crea una máscara que se puede utilizar para editar la imagen completa.
        
        Args:
            imagen (Image.Image): Imagen para la que se generará la máscara.
            
        Returns:
            Image.Image: Máscara con transparencia.
        """
        return self.ai_handler.generar_mascara_imagen(imagen)

    def transformar_imagen(self, imagen_input: Image.Image, tipo_transformacion: str, prompt: str, modelo: str, tamanio: str, calidad: str, estilo: str, n: int) -> Tuple[List[str], str]:
        """
        Transforma una imagen según el tipo de transformación especificado.
        
        Función unificada que puede realizar diferentes tipos de transformaciones
        en una imagen según los parámetros especificados.
        
        Args:
            imagen_input (Image.Image): Imagen a transformar.
            tipo_transformacion (str): Tipo de transformación ("generation", "variation", "edit").
            prompt (str): Descripción para la transformación (en caso de generation o edit).
            modelo (str): Modelo a utilizar.
            tamanio (str): Tamaño de la imagen.
            calidad (str): Calidad de la imagen.
            estilo (str): Estilo de la imagen.
            n (int): Número de imágenes a generar.
            
        Returns:
            Tuple[List[str], str]: URLs de las imágenes generadas y mensaje de estado.
        """
        # Obtener las transformaciones disponibles para este modelo
        transformaciones_disponibles = obtener_transformaciones(modelo)

        return self.ai_handler.transformar_imagen(
            imagen_input,
            tipo_transformacion,
            prompt,
            modelo,
            tamanio,
            calidad,
            estilo,
            n,
            transformaciones_disponibles
        )

    def optimizar_prompt(self, prompt_original: str, contexto: str = "", modelo: str = "", categoria: str = "general") -> str:
        """
        Optimiza un prompt en español con un modelo de lenguaje para mejorar la generación de imágenes.
        
        Esta función reformula y mejora un prompt para obtener mejores resultados
        de los modelos de generación de imágenes.
        
        Args:
            prompt_original (str): El prompt original en español.
            contexto (str, optional): Contexto adicional sobre el tipo de imagen o estilo deseado.
            modelo (str, optional): Modelo de lenguaje a utilizar para la optimización.
            categoria (str, optional): Categoría de cómic o estilo para seleccionar las instrucciones adecuadas.
            
        Returns:
            str: Prompt optimizado en inglés.
        """
        return self.ai_handler.optimizar_prompt(prompt_original, contexto, modelo, categoria)


if __name__ == "__main__":
    """
    Punto de entrada principal de la aplicación.
    
    Inicializa la interfaz de usuario y lanza la aplicación web de Gradio.
    """
    from ui.ui import UI

    # Crear la interfaz de usuario con nuestra clase UI
    ui = UI()
    # Lanzar la aplicación
    ui.app.launch(share=False)
