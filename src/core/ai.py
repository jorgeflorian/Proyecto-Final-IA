"""
    Jorge Augusto Cesar Florian Silvestre 
    17-EISN-2-009
"""

"""
Módulo de manejo de OpenAI para generación de imágenes y edición de cómics.
Este módulo proporciona una interfaz para interactuar con la API de OpenAI, permitiendo
la generación de imágenes, variaciones y ediciones de imágenes existentes. 
"""

# Importación de bibliotecas necesarias para la funcionalidad del módulo
from data.prompt_optimizer import MODELO_PREDETERMINADO, seleccionar_instruccion_sistema
from PIL import Image
from typing import List, Tuple
import base64
import io
from dotenv import load_dotenv  # type: ignore
import os
import openai  # type: ignore


# Cargar variables de entorno desde archivo .env
# Esto permite mantener información sensible como claves API fuera del código
load_dotenv()


class OpenAIHandler:
    """
    Clase que maneja todas las interacciones con la API de OpenAI.

    Proporciona métodos para generar, editar y transformar imágenes 
    utilizando los modelos DALL-E de OpenAI.
    """

    def __init__(self):
        """
        Inicializa el manejador de OpenAI.

        Intenta obtener la API key desde las variables de entorno y 
        configura el cliente si la clave está disponible.
        """
        # Inicializar cliente OpenAI - intentar obtener API key desde variables de entorno
        self.cliente = None
        self.api_key = os.environ.get("OPENAI_API_KEY")
        if (self.api_key):
            self.inicializar_cliente(self.api_key)

        # Guardar imágenes generadas durante la sesión para mantener un historial
        self.imagenes_generadas = []

    def inicializar_cliente(self, api_key: str) -> Tuple[bool, str]:
        """
        Inicializa el cliente OpenAI con la API key proporcionada.

        Args:
            api_key: Clave de API de OpenAI

        Returns:
            Tuple[bool, str]: Tupla con estado de éxito (True/False) y mensaje descriptivo
        """
        try:
            self.cliente = openai.OpenAI(api_key=api_key)
            # Probar la API key con una simple petición para verificar su validez
            self.cliente.models.list()
            return True, "API key válida, cliente inicializado correctamente!"
        except Exception as e:
            return False, f"Error al inicializar el cliente: {str(e)}"

    def generar_vineta(
        self,
        prompt: str,
        modelo: str,
        tamanio: str,
        calidad: str,
        estilo: str,
        n: int
    ) -> Tuple[List[str], str]:
        """
        Genera una viñeta de cómic basada en la entrada del usuario.

        Args:
            prompt: Descripción textual de la viñeta a generar
            modelo: Modelo de OpenAI a utilizar (ej. "dall-e-3")
            tamanio: Tamaño de la imagen a generar (ej. "1024x1024")
            calidad: Nivel de calidad de la imagen ("standard" o "hd")
            estilo: Estilo visual de la imagen ("vivid" o "natural")
            n: Número de imágenes a generar

        Returns:
            Tuple[List[str], str]: Lista de URLs de las imágenes generadas y mensaje de estado
        """
        if not self.cliente:
            return [], "API Key requerida para generar imágenes"

        try:
            # Optimizar el prompt antes de enviarlo a DALL-E
            # Añadimos contexto para la optimización indicando que es para un cómic
            contexto = f"Estilo de cómic: {estilo}. Quiero una alta calidad: {calidad}."
            prompt_optimizado = self.optimizar_prompt(prompt, contexto)

            # Generar la imagen con el prompt optimizado
            respuesta = self.cliente.images.generate(
                model=modelo,
                prompt=prompt_optimizado,
                size=tamanio,
                quality=calidad,
                style=estilo,
                n=n
            )

            # Extraer URLs de imágenes de la respuesta
            urls_imagenes = [imagen.url for imagen in respuesta.data]
            # Guardar en historial de imágenes
            self.imagenes_generadas.extend(urls_imagenes)
            return urls_imagenes, "¡Viñeta generada correctamente!"
        except Exception as e:
            return [], f"Error al generar la imagen: {str(e)}"

    def generar_variacion_imagen(
        self,
        imagen_input: Image.Image,
        modelo: str,
        tamanio: str,
        n: int
    ) -> Tuple[List[str], str]:
        """
        Genera variaciones de una imagen existente.

        Esta función utiliza la API de OpenAI para crear diferentes versiones
        de una imagen manteniendo su esencia pero con variaciones visuales.

        Args:
            imagen_input: Imagen para generar variaciones
            modelo: Modelo a utilizar (solo compatible con dall-e-2)
            tamanio: Tamaño de la imagen de salida
            n: Número de variaciones a generar

        Returns:
            Tuple[List[str], str]: URLs de las imágenes generadas y mensaje de estado
        """
        if not self.cliente:
            return [], "API Key requerida para generar variaciones"

        # Verificar que el modelo soporta variaciones
        if modelo != "dall-e-2":
            return [], "Las variaciones de imágenes solo están disponibles con el modelo DALL-E 2"

        # Convertir la imagen PIL a bytes
        byte_stream = io.BytesIO()
        imagen_input.save(byte_stream, format='PNG')
        byte_array = byte_stream.getvalue()

        try:
            respuesta = self.cliente.images.create_variation(
                model=modelo,
                image=byte_array,
                n=n,
                size=tamanio
            )

            # Extraer URLs de imágenes de la respuesta
            urls_imagenes = [imagen.url for imagen in respuesta.data]
            # Guardar en historial de imágenes
            self.imagenes_generadas.extend(urls_imagenes)
            return urls_imagenes, "¡Variaciones generadas correctamente!"
        except Exception as e:
            return [], f"Error al generar variaciones: {str(e)}"

    def editar_imagen(
        self,
        imagen_input: Image.Image,
        mascara_input: Image.Image,
        prompt: str,
        modelo: str,
        tamanio: str,
        n: int
    ) -> Tuple[List[str], str]:
        """
        Edita una imagen existente utilizando una máscara y un prompt.

        Permite modificar áreas específicas de una imagen según la máscara
        proporcionada, reemplazando esas áreas según el prompt de texto.

        Args:
            imagen_input: Imagen base a editar
            mascara_input: Máscara que indica qué áreas editar (áreas transparentes)
            prompt: Descripción de la imagen deseada
            modelo: Modelo a utilizar (solo compatible con dall-e-2)
            tamanio: Tamaño de la imagen de salida
            n: Número de ediciones a generar

        Returns:
            Tuple[List[str], str]: URLs de las imágenes generadas y mensaje de estado
        """
        if not self.cliente:
            return [], "API Key requerida para editar imágenes"

        # Verificar que el modelo soporta ediciones
        if modelo != "dall-e-2":
            return [], "Las ediciones de imágenes solo están disponibles con el modelo DALL-E 2"

        # Convertir las imágenes PIL a bytes
        imagen_bytes = io.BytesIO()
        imagen_input.save(imagen_bytes, format='PNG')

        mascara_bytes = io.BytesIO()
        mascara_input.save(mascara_bytes, format='PNG')

        try:
            respuesta = self.cliente.images.edit(
                model=modelo,
                image=imagen_bytes.getvalue(),
                mask=mascara_bytes.getvalue(),
                prompt=prompt,
                n=n,
                size=tamanio
            )

            # Extraer URLs de imágenes de la respuesta
            urls_imagenes = [imagen.url for imagen in respuesta.data]
            # Guardar en historial de imágenes
            self.imagenes_generadas.extend(urls_imagenes)
            return urls_imagenes, "¡Imagen editada correctamente!"
        except Exception as e:
            return [], f"Error al editar la imagen: {str(e)}"

    def generar_mascara_imagen(self, imagen: Image.Image) -> Image.Image:
        """
        Genera una máscara transparente para toda la imagen.

        Crea una imagen RGBA completamente transparente del mismo tamaño
        que la imagen original para ser usada en operaciones de edición.

        Args:
            imagen: Imagen para la que se generará la máscara

        Returns:
            Image.Image: Máscara con transparencia
        """
        # Crear una máscara transparente del mismo tamaño
        mascara = Image.new("RGBA", imagen.size, (0, 0, 0, 0))
        return mascara

    def transformar_imagen(
        self,
        imagen_input: Image.Image,
        tipo_transformacion: str,
        prompt: str,
        modelo: str,
        tamanio: str,
        calidad: str,
        estilo: str,
        n: int,
        transformaciones_disponibles: List[str]
    ) -> Tuple[List[str], str]:
        """
        Transforma una imagen según el tipo de transformación especificado.

        Actúa como función unificadora para los diferentes tipos de transformaciones
        disponibles: generación, variación y edición de imágenes.

        Args:
            imagen_input: Imagen a transformar
            tipo_transformacion: Tipo de transformación ("generation", "variation", "edit")
            prompt: Descripción para la transformación (en caso de generation o edit)
            modelo: Modelo a utilizar
            tamanio: Tamaño de la imagen
            calidad: Calidad de la imagen
            estilo: Estilo de la imagen
            n: Número de imágenes a generar
            transformaciones_disponibles: Lista de transformaciones disponibles para el modelo

        Returns:
            Tuple[List[str], str]: URLs de las imágenes generadas y mensaje de estado
        """
        if not imagen_input:
            return [], "Por favor, proporciona una imagen para transformar"

        # Asegurarse de que la imagen esté en formato RGB o RGBA
        if imagen_input.mode not in ('RGB', 'RGBA'):
            imagen_input = imagen_input.convert('RGBA')

        # Verificar primero si el tipo de transformación es compatible con el modelo seleccionado
        if tipo_transformacion not in transformaciones_disponibles:
            return [], f"El tipo de transformación '{tipo_transformacion}' no está disponible para el modelo {modelo}. Opciones disponibles: {', '.join(transformaciones_disponibles)}"

        # Seleccionar la transformación según el tipo
        if tipo_transformacion == "generation":
            # Para DALL-E-3, simplemente usamos la generación normal con texto
            # Para DALL-E-2, podemos incluir la imagen como referencia pero
            # actualmente la API no soporta directamente esto, así que usamos texto-a-imagen
            if not prompt.strip():
                return [], "Para la generación se requiere un prompt descriptivo"

            # Añadir al prompt una referencia de que está basado en la imagen
            prompt_completo = f"{prompt} (basado en la imagen de referencia proporcionada)"

            # Optimizar el prompt con contexto específico para transformación
            contexto = f"Transformación de imagen a estilo de cómic. Modelo: {modelo}, Estilo: {estilo}, Calidad: {calidad}."
            prompt_optimizado = self.optimizar_prompt(
                prompt_completo, contexto)

            # Usar el método estándar de generación pero con nuestro prompt optimizado directamente
            try:
                respuesta = self.cliente.images.generate(
                    model=modelo,
                    prompt=prompt_optimizado,
                    size=tamanio,
                    quality=calidad,
                    style=estilo,
                    n=n
                )

                # Extraer URLs de imágenes de la respuesta
                urls_imagenes = [imagen.url for imagen in respuesta.data]
                # Guardar en historial de imágenes
                self.imagenes_generadas.extend(urls_imagenes)
                return urls_imagenes, "¡Imagen transformada correctamente!"
            except Exception as e:
                return [], f"Error al transformar la imagen: {str(e)}"

        elif tipo_transformacion == "variation":
            # Este es un image-to-image (variación)
            if modelo != "dall-e-2":
                return [], "Las variaciones de imágenes solo están disponibles con el modelo DALL-E 2"

            # Aquí sí usamos la imagen directamente
            return self.generar_variacion_imagen(imagen_input, modelo, tamanio, n)

        elif tipo_transformacion == "edit":
            # Este es un image-to-image (edición con máscara)
            if modelo != "dall-e-2":
                return [], "Las ediciones de imágenes solo están disponibles con el modelo DALL-E 2"

            if not prompt.strip():
                return [], "Para la edición se requiere un prompt descriptivo"

            # Optimizar el prompt específicamente para edición
            contexto = f"Edición de imagen para convertirla a estilo cómic. Modelo: {modelo}, Calidad: {calidad}."
            prompt_optimizado = self.optimizar_prompt(prompt, contexto)

            # Crear una máscara y usar la imagen directamente
            mascara = self.generar_mascara_imagen(imagen_input)

            # Modificamos la llamada a editar_imagen para usar el prompt optimizado
            try:
                imagen_bytes = io.BytesIO()
                imagen_input.save(imagen_bytes, format='PNG')

                mascara_bytes = io.BytesIO()
                mascara.save(mascara_bytes, format='PNG')

                respuesta = self.cliente.images.edit(
                    model=modelo,
                    image=imagen_bytes.getvalue(),
                    mask=mascara_bytes.getvalue(),
                    prompt=prompt_optimizado,
                    n=n,
                    size=tamanio
                )

                # Extraer URLs de imágenes de la respuesta
                urls_imagenes = [imagen.url for imagen in respuesta.data]
                # Guardar en historial de imágenes
                self.imagenes_generadas.extend(urls_imagenes)
                return urls_imagenes, "¡Imagen editada correctamente!"
            except Exception as e:
                return [], f"Error al editar la imagen: {str(e)}"

        else:
            return [], f"Tipo de transformación no reconocido: {tipo_transformacion}"

    def optimizar_prompt(
        self,
        prompt_original: str,
        contexto: str = "",
        modelo: str = MODELO_PREDETERMINADO,
        categoria: str = "general"
    ) -> str:
        """
        Optimiza un prompt en español con un modelo de lenguaje para mejorar la generación de imágenes.

        Utiliza modelos de OpenAI para reformular y mejorar el prompt original,
        haciéndolo más efectivo para la generación de imágenes de cómics.

        Args:
            prompt_original: El prompt original en español
            contexto: Contexto adicional sobre el tipo de imagen o estilo deseado
            modelo: Modelo de lenguaje a utilizar para la optimización
            categoria: Categoría de cómic o estilo para seleccionar las instrucciones adecuadas

        Returns:
            str: Prompt optimizado en inglés
        """
        if not self.cliente:
            # Si no hay cliente OpenAI, devolver el prompt original
            return prompt_original

        try:
            # Asegurar que siempre haya un modelo válido (nunca vacío)
            if not modelo:
                modelo = MODELO_PREDETERMINADO

            # Seleccionar la instrucción del sistema según la categoría
            system_prompt = seleccionar_instruccion_sistema(categoria)

            # Añadir contexto si está disponible
            user_prompt = prompt_original
            if contexto:
                user_prompt = f"Contexto: {contexto}\nPrompt original: {prompt_original}"

            # Crear base de mensajes para cualquier modelo
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]

            # Configurar parámetros básicos que funcionan con todos los modelos
            params = {
                "model": modelo,
                "messages": messages
            }

            # Para simplificar y evitar errores de tipo, no usamos el parámetro temperature
            # Llamar al modelo de chat para optimizar el prompt
            respuesta = self.cliente.chat.completions.create(**params)

            # Extraer y devolver el prompt optimizado
            prompt_optimizado = respuesta.choices[0].message.content.strip()
            return prompt_optimizado

        except Exception as e:
            # En caso de error, devolver el prompt original e imprimir el error
            print(f"Error al optimizar prompt: {str(e)}")
            return prompt_original

    def imagen_a_base64(self, imagen: Image.Image) -> str:
        """
        Convierte una imagen PIL a base64 para su descarga.

        Útil para preparar imágenes para ser descargadas o
        mostradas directamente en navegadores.

        Args:
            imagen: Imagen PIL a convertir

        Returns:
            str: Representación en base64 de la imagen
        """
        buffered = io.BytesIO()
        imagen.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return img_str

    def descargar_imagen(self, url_imagen: str) -> Tuple[str, str]:
        """
        Prepara una imagen para su descarga.

        Genera un nombre de archivo único y devuelve la URL de la imagen
        para facilitar la descarga desde la interfaz de usuario.

        Args:
            url_imagen: URL de la imagen a descargar

        Returns:
            Tuple[str, str]: Datos de la imagen en formato base64 y nombre de archivo
        """
        try:
            # Nombre de archivo con timestamp para evitar duplicados
            import time
            filename = f"comic_vineta_{int(time.time())}.png"

            return url_imagen, filename
        except Exception as e:
            return "", f"Error al preparar la imagen para descarga: {str(e)}"
