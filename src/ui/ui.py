"""
    Jorge Augusto Cesar Florian Silvestre
    17-EISN-2-009
"""

"""    
    Interfaz de usuario para el Generador de Cómics con IA
    Este módulo implementa la interfaz gráfica utilizando Gradio
    para permitir a los usuarios generar viñetas de cómics personalizadas
    mediante modelos de IA de OpenAI (DALL-E).
"""

import gradio as gr
import os
from data.comic_prompts import obtener_personajes, obtener_villanos


class UI:
    """
    Clase que implementa la interfaz de usuario del Generador de Cómics.

    Esta clase maneja todos los componentes visuales y la lógica de interacción
    para permitir a los usuarios configurar y generar viñetas de cómics usando IA.
    """

    def __init__(self):
        # Importamos GeneradorDeComics dentro del método para evitar la importación circular
        from cg_app import GeneradorDeComics

        # Crear una instancia de nuestro generador de cómics
        generador = GeneradorDeComics()
        self.generador = generador

        # Crear la interfaz de usuario con Gradio
        with gr.Blocks(title="Generador de Cómics", theme=gr.themes.Soft()) as self.app:
            gr.Markdown("# 🎨 ¡Generador de Cómics con IA! 🚀✨")
            gr.Markdown(
                "✨ Genera viñetas de cómics personalizadas usando modelos DALL-E de OpenAI 🤖")

            with gr.Tabs() as tabs:
                # Pestaña de Configuración - Permite al usuario configurar la API de OpenAI
                with gr.TabItem("⚙️ Configuración", id=1):
                    with gr.Row():
                        with gr.Column():
                            gr.Markdown("### 🔑 Configuración de API 🔐")
                            with gr.Group():
                                api_key = gr.Textbox(
                                    label="OpenAI API Key 🔐",
                                    placeholder="sk-...",
                                    type="password",
                                    value=os.environ.get("OPENAI_API_KEY", "")
                                )
                                init_btn = gr.Button(
                                    "🚀 Inicializar Cliente", variant="primary")
                                api_status = gr.Textbox(
                                    label="Estado de la API 📊", interactive=False)

                    gr.Markdown("### 💡 Ayuda e Información 📚")
                    gr.Markdown("""
                    **🔍 Cómo utilizar el generador de cómics:**

                    - 1️⃣ Introduce tu API Key de OpenAI y haz clic en "🚀 Inicializar Cliente".
                    - 2️⃣ Navega a la pestaña "🖌️ Generar" para crear viñetas personalizadas.
                    - 3️⃣ Puedes usar plantillas predefinidas en la pestaña "📚 Plantillas" o crear tu propia descripción.
                    - 4️⃣ Ajusta la configuración del modelo según tus preferencias ✨.
                    - 5️⃣ ¡Haz clic en "✨ Generar Viñeta" y disfruta del resultado! 🎉

                    **📝 Nota:** Necesitas una API Key válida de OpenAI para utilizar esta aplicación. 🔒
                    """)

                # Pestaña de Generación - Permite al usuario generar viñetas mediante texto o imagen
                with gr.TabItem("🖌️ Generar", id=2):
                    with gr.Row():
                        with gr.Column(scale=1):
                            gr.Markdown("### ⚙️ Configuración del Modelo 🛠️")
                            with gr.Group():
                                # Selector de modelo de IA a utilizar
                                modelo_dropdown = gr.Dropdown(
                                    label="Modelo 🤖",
                                    choices=generador.modelos_disponibles,
                                    value=generador.modelos_disponibles[0]
                                )

                                # Selector de tamaño de imagen
                                tamanio_dropdown = gr.Dropdown(
                                    label="Tamaño de Imagen 📏",
                                    choices=generador.tamanios_disponibles[generador.modelos_disponibles[0]],
                                    value=generador.tamanios_disponibles[generador.modelos_disponibles[0]][0]
                                )

                                # Selector de estilo de generación
                                estilo_dropdown = gr.Dropdown(
                                    label="Estilo 🎭",
                                    choices=generador.estilos_disponibles[generador.modelos_disponibles[0]],
                                    value=generador.estilos_disponibles[generador.modelos_disponibles[0]][0]
                                )

                                # Selector de calidad de imagen
                                calidad_dropdown = gr.Dropdown(
                                    label="Calidad ✨",
                                    choices=generador.calidades_disponibles[generador.modelos_disponibles[0]],
                                    value=generador.calidades_disponibles[generador.modelos_disponibles[0]][0]
                                )

                                # Control para el número de imágenes a generar
                                num_imagenes = gr.Slider(
                                    label="Número de Imágenes 🖼️",
                                    minimum=1,
                                    maximum=4,
                                    value=1,
                                    step=1
                                )

                            # Checkbox para mostrar el prompt optimizado que se envía al modelo
                            with gr.Group():
                                mostrar_prompt_optimizado = gr.Checkbox(
                                    label="👀 Mostrar prompt optimizado",
                                    value=False,
                                    info="🔍 Muestra el prompt optimizado que se envía al modelo de generación de imágenes"
                                )

                            # Sección para generar viñetas a partir de texto
                            with gr.Accordion("✍️ Generar con Texto 📝", open=True):
                                gr.Markdown("### 💡 Descripción de la Viñeta 📝")
                                with gr.Group():
                                    prompt_input = gr.Textbox(
                                        label="Descripción detallada ✏️",
                                        placeholder="✨ Describe tu viñeta de cómic aquí...",
                                        lines=5
                                    )
                                generar_texto_btn = gr.Button(
                                    "✨ Generar con Texto 🚀", variant="primary")

                            # Sección para generar viñetas a partir de una imagen
                            with gr.Accordion("🖼️ Generar con Imagen 🎨", open=False):

                                with gr.Row(scale=1):
                                    with gr.Column(scale=1):
                                        # Carga de imagen para transformación
                                        imagen_input = gr.Image(
                                            label="Imagen a transformar 🖼️",
                                            type="pil",
                                            sources="upload"
                                        )
                                    with gr.Column(scale=2):
                                        gr.Markdown(
                                            "#### 🛠️ Configuración de Transformación")
                                        # Selector del tipo de transformación a aplicar
                                        transformacion_dropdown = gr.Dropdown(
                                            label="Tipo de Transformación 🔄",
                                            choices=["generation",
                                                     "variation", "edit"],
                                            value="generation",
                                        )

                                        # Explicación de los tipos de transformación
                                        gr.Markdown("""
                                            **✨ Generation**: Usa texto + imagen como referencia (funciona con DALL·E 2 y 3).

                                            **🔄 Variation**: Genera variaciones de la imagen subida (solo DALL·E 2).
                                                                    
                                            **✏️ Edit**: Edita la imagen con una máscara automática (solo DALL·E 2).
                                            """)

                                with gr.Row():
                                    with gr.Column(scale=3):
                                        gr.Markdown(
                                            "#### 📚 Categoría y Estilo de Cómic")
                                        # Selector de categoría de cómic
                                        categoria_transform = gr.Dropdown(
                                            label="Categoría de Cómic 📚",
                                            choices=generador.categorias_comics,
                                            value=generador.categorias_comics[0]
                                        )
                                    with gr.Column(scale=4):
                                        # Selector de estilo de cómic
                                        estilo_transform = gr.Dropdown(
                                            label="Estilo de Cómic 🎭",
                                            choices=generador.estilos_comics[generador.categorias_comics[0]],
                                            value=generador.estilos_comics[generador.categorias_comics[0]][0]
                                        )

                                gr.Markdown("#### 📝 Descripción")

                                with gr.Row():
                                    with gr.Column(scale=5):
                                        # Campo para descripción adicional
                                        prompt_adicional = gr.Textbox(
                                            label="Descripción adicional (opcional) ✏️",
                                            placeholder="✨ Añade detalles sobre cómo transformar la imagen...",
                                            lines=2
                                        )
                                    with gr.Column(scale=6):
                                        # Campo para mostrar y editar el prompt generado
                                        prompt_transform = gr.Textbox(
                                            label="Prompt generado (puedes editarlo) 📝",
                                            lines=3,
                                            interactive=True,
                                            visible=False
                                        )

                                with gr.Row():
                                    # Botón para iniciar la generación basada en imagen
                                    generar_imagen_btn = gr.Button(
                                        "✨ Generar con Imagen 🚀", variant="primary")

                        with gr.Column(scale=2):
                            gr.Markdown("### 🖼️ Viñetas Generadas ✨")
                            # Galería para mostrar las imágenes generadas
                            galeria = gr.Gallery(
                                label="Viñetas Generadas ✨",
                                columns=2,
                                rows=2,
                                object_fit="contain",
                                height="600px"
                            )
                            # Campo para mostrar el estado de la generación
                            estado_generacion = gr.Textbox(
                                label="Estado de la Generación 📊", interactive=False)

                # Pestaña de Plantillas - Ofrece plantillas predefinidas para diferentes estilos de cómics
                with gr.TabItem("📚 Plantillas", id=3):
                    with gr.Row():
                        with gr.Column(scale=1):
                            gr.Markdown("### 🏷️ Seleccionar Estilo de Cómic 🎭")

                            # Selector de categoría de cómic para plantillas
                            categoria_dropdown = gr.Dropdown(
                                label="Categoría 📂",
                                choices=generador.categorias_comics,
                                value=generador.categorias_comics[0]
                            )

                            # Selector de estilo específico dentro de la categoría
                            estilo_comic_dropdown = gr.Dropdown(
                                label="Estilo 🎨",
                                choices=generador.estilos_comics[generador.categorias_comics[0]],
                                value=generador.estilos_comics[generador.categorias_comics[0]][0]
                            )

                            gr.Markdown("### 🎭 Personalización ✨")

                            # Opciones avanzadas para personalizar las plantillas
                            with gr.Accordion("✨ Opciones Avanzadas", open=False):
                                personaje_input = gr.Textbox(
                                    label="Personaje 🦸",
                                    placeholder="✨ Nombre del personaje..."
                                )

                                villano_input = gr.Textbox(
                                    label="Villano (si aplica) 😈",
                                    placeholder="✨ Nombre del villano..."
                                )

                                lugar_input = gr.Textbox(
                                    label="Lugar (si aplica) 🏙️",
                                    placeholder="✨ Describe el lugar..."
                                )

                                estilo_adicional_dropdown = gr.Dropdown(
                                    label="Estilo Adicional 🎨",
                                    choices=["Ninguno", "Detallado", "Minimalista",
                                             "Acuarela", "Retro", "Digital", "3D"],
                                    value="Ninguno"
                                )

                            # Botones para ver y usar plantillas
                            generar_ejemplo_btn = gr.Button(
                                "👁️ Ver Prompt de Ejemplo", variant="secondary")
                            usar_plantilla_btn = gr.Button(
                                "✅ Usar esta Plantilla", variant="primary")

                        with gr.Column(scale=1):
                            gr.Markdown("### 📝 Prompt Generado ✨")
                            # Campo para mostrar el prompt de ejemplo
                            prompt_ejemplo = gr.Textbox(
                                label="Prompt de ejemplo 📄",
                                lines=8,
                                interactive=False
                            )

                            gr.Markdown("### 🦸‍♂️ Personajes Sugeridos ✨")
                            # Tabla de personajes sugeridos
                            personajes_ejemplos = gr.Dataframe(
                                headers=["Personajes 🦸"],
                                datatype=["str"],
                                col_count=1,
                                row_count=5,
                                interactive=False
                            )

                            gr.Markdown("### 😈 Villanos Sugeridos ✨")
                            # Tabla de villanos sugeridos
                            villanos_ejemplos = gr.Dataframe(
                                headers=["Villanos 😈"],
                                datatype=["str"],
                                col_count=1,
                                row_count=5,
                                interactive=False
                            )

                # Pestaña de Galería - Muestra las viñetas generadas durante la sesión
                with gr.TabItem("🖼️ Galería", id=4):
                    gr.Markdown("### 🎭 Galería de Viñetas ✨")
                    gr.Markdown(
                        "✨ Aquí se mostrarán tus viñetas generadas recientemente 🎨")

                    # Galería histórica para mostrar todas las imágenes generadas
                    galeria_historica = gr.Gallery(
                        label="Viñetas Recientes ✨",
                        columns=3,
                        rows=3,
                        object_fit="contain",
                        height="500px",
                        show_label=False
                    )

                    # Botón para limpiar la galería
                    limpiar_galeria_btn = gr.Button(
                        "🧹 Limpiar Galería", variant="secondary")

                    gr.Markdown("""
                    **💡 Consejo**: Puedes hacer clic en cualquier imagen para verla a tamaño completo.
                    Las imágenes se almacenarán solo durante la sesión actual, así que guarda las que te gusten. 💾
                    """)

                # Pestaña Acerca de - Información sobre la aplicación
                with gr.TabItem("ℹ️ Acerca de", id=5):
                    gr.Markdown("""
                    # ✨ Generador de Cómics con IA 🚀🎨

                    Esta aplicación utiliza modelos de inteligencia artificial de OpenAI (DALL-E) para generar viñetas de cómics personalizadas basadas en tus descripciones textuales o imágenes de referencia. Puedes elegir entre diferentes estilos de cómics y personalizar personajes, villanos y escenarios. 😎

                    ## ✅ Características ✨

                    - 🖼️ Generación de imágenes con diferentes estilos de cómics
                    - 📚 Plantillas predefinidas para diferentes universos (Marvel, DC, Manga, etc.)
                    - 🦸 Personalización de personajes, villanos y escenarios
                    - ⚙️ Múltiples opciones de calidad y tamaño
                    - 💡 ¡Fácil de usar y personalizar!

                    ## 🔍 Cómo funciona 🤖

                    - 1️⃣ La aplicación toma tu descripción textual ✏️
                    - 2️⃣ Envía esta descripción a los modelos DALL-E de OpenAI 🚀
                    - 3️⃣ Procesa las imágenes generadas y las muestra en la galería ✨

                    ## 👏 Créditos 💻

                    - 👨‍💻 Desarrollado por: Jorge Augusto Cesar Florian Silvestre
                    - 🎓 Matricula: 17-EISN-2-009
                    - 🛠 Tecnologías: Python, Gradio, OpenAI
                    - 📅 Año: 2025

                    ## ⚠️ Limitaciones ⏳

                    - 🔑 Se requiere una API key válida de OpenAI
                    - 🎨 La calidad de las imágenes puede variar según la descripción proporcionada
                    """)

            # === MANEJO DE EVENTOS Y CALLBACKS ===

            # Función para inicializar el cliente de OpenAI con la API key proporcionada
            def init_cliente(api_key):
                """
                Inicializa el cliente de OpenAI con la API key proporcionada.

                Args:
                    api_key (str): Clave de API para autenticación con OpenAI

                Returns:
                    str: Mensaje de estado de la inicialización
                """
                success, mensaje = generador.inicializar_cliente(api_key)
                if success or "éxito" in mensaje.lower() or "correctamente" in mensaje.lower():
                    return "✅ " + mensaje + " 🚀"
                else:
                    return "❌ " + mensaje + " 🔑"

            # Evento para inicializar el cliente al hacer clic en el botón
            init_btn.click(
                fn=init_cliente,
                inputs=[api_key],
                outputs=[api_status]
            )

            # Función para actualizar las opciones disponibles según el modelo seleccionado
            def actualizar_opciones_modelo(nombre_modelo):
                """
                Actualiza las opciones disponibles según el modelo de IA seleccionado.

                Args:
                    nombre_modelo (str): Nombre del modelo seleccionado

                Returns:
                    tuple: Componentes actualizados para tamaños, estilos y calidades
                """
                tamanios, estilos, calidades = generador.actualizar_configuracion_modelo(
                    nombre_modelo)
                return gr.Dropdown(choices=tamanios, value=tamanios[0]), gr.Dropdown(choices=estilos, value=estilos[0]), gr.Dropdown(choices=calidades, value=calidades[0])

            # Evento para actualizar opciones al cambiar el modelo
            modelo_dropdown.change(
                fn=actualizar_opciones_modelo,
                inputs=[modelo_dropdown],
                outputs=[tamanio_dropdown, estilo_dropdown, calidad_dropdown]
            )

            # Función para actualizar los estilos disponibles según la categoría de cómic
            def actualizar_estilos_comics(categoria):
                """
                Actualiza los estilos disponibles según la categoría de cómic seleccionada.

                Args:
                    categoria (str): Categoría de cómic seleccionada

                Returns:
                    gr.Dropdown: Componente actualizado con los estilos disponibles
                """
                estilos = generador.estilos_comics.get(categoria, [])
                return gr.Dropdown(choices=estilos, value=estilos[0] if estilos else None)

            # Evento para actualizar estilos al cambiar la categoría
            categoria_dropdown.change(
                fn=actualizar_estilos_comics,
                inputs=[categoria_dropdown],
                outputs=[estilo_comic_dropdown]
            )

            # Función para mostrar el prompt de ejemplo según las opciones seleccionadas
            def mostrar_prompt_ejemplo(categoria, estilo_comic, personaje, villano, lugar, estilo_adicional):
                """
                Genera y muestra un prompt de ejemplo según las opciones seleccionadas.

                Args:
                    categoria (str): Categoría de cómic
                    estilo_comic (str): Estilo de cómic
                    personaje (str): Nombre del personaje
                    villano (str): Nombre del villano
                    lugar (str): Descripción del lugar
                    estilo_adicional (str): Estilo adicional a aplicar

                Returns:
                    tuple: Prompt generado y listas de personajes y villanos sugeridos
                """
                # Generar prompt de ejemplo
                prompt = generador.generar_prompt_ejemplo(
                    categoria,
                    estilo_comic,
                    personaje,
                    villano,
                    lugar,
                    None if estilo_adicional == "Ninguno" else estilo_adicional
                )

                # Obtener personajes y villanos ejemplo
                personajes = obtener_personajes(
                    categoria)
                villanos = obtener_villanos(categoria)

                # Formatear para dataframe
                personajes_df = [[p] for p in personajes[:5]]
                villanos_df = [[v] for v in villanos[:5]]

                return prompt, personajes_df, villanos_df

            # Evento para mostrar el prompt de ejemplo
            generar_ejemplo_btn.click(
                fn=mostrar_prompt_ejemplo,
                inputs=[
                    categoria_dropdown,
                    estilo_comic_dropdown,
                    personaje_input,
                    villano_input,
                    lugar_input,
                    estilo_adicional_dropdown
                ],
                outputs=[
                    prompt_ejemplo,
                    personajes_ejemplos,
                    villanos_ejemplos
                ]
            )

            # Función para usar la plantilla seleccionada
            def usar_plantilla(prompt_plantilla):
                """
                Transfiere el prompt de la plantilla al campo de entrada de texto.

                Args:
                    prompt_plantilla (str): Prompt generado por la plantilla

                Returns:
                    str: El mismo prompt para colocarlo en el campo de entrada
                """
                return prompt_plantilla

            # Evento para usar la plantilla seleccionada
            usar_plantilla_btn.click(
                fn=usar_plantilla,
                inputs=[prompt_ejemplo],
                outputs=[prompt_input]
            )

            # Evento JavaScript para cambiar a la pestaña de generación al usar una plantilla
            usar_plantilla_btn.click(
                fn=None,  # No necesitamos una función para el cambio de pestañas
                inputs=None,
                outputs=None,
                js="() => {document.querySelector('button[aria-controls=\"component-16\"]').click();}"
            )

            # Función principal para generar viñetas de cómic
            def generar_comic(prompt_input, imagen_input, categoria_transform, estilo_transform, prompt_adicional, prompt_transform, tab_index, modelo, tamanio, calidad, estilo, n, tipo_transformacion=None, mostrar_prompt=False):
                """
                Función principal para generar viñetas de cómic según las opciones seleccionadas.

                Puede generar a partir de texto o transformar una imagen existente según los parámetros.

                Args:
                    prompt_input (str): Descripción textual para la generación
                    imagen_input (PIL.Image): Imagen para transformación
                    categoria_transform (str): Categoría de cómic para transformación
                    estilo_transform (str): Estilo de cómic para transformación
                    prompt_adicional (str): Descripción adicional para transformación
                    prompt_transform (str): Prompt generado/editado para transformación
                    tab_index (int): Índice de la pestaña (0=texto, 1=imagen)
                    modelo (str): Modelo de IA a utilizar
                    tamanio (str): Tamaño de imagen a generar
                    calidad (str): Nivel de calidad de la imagen
                    estilo (str): Estilo de generación
                    n (int): Número de imágenes a generar
                    tipo_transformacion (str): Tipo de transformación (generation/variation/edit)
                    mostrar_prompt (bool): Si se debe mostrar el prompt optimizado

                Returns:
                    tuple: Imágenes generadas, mensaje de estado, actualización de galería histórica y prompt optimizado
                """
                prompt_final = ""
                prompt_optimizado = ""

                # Verificar en qué tab estamos (0 = prompt de texto, 1 = transformar imagen)
                if tab_index == 0:  # Estamos usando prompt de texto
                    # Validar que haya un texto para generar
                    if not prompt_input.strip():
                        return [], "❌ Por favor, proporciona una descripción para la viñeta 📝", [], ""

                    prompt_final = prompt_input
                    # Optimizar el prompt antes de generar la imagen
                    contexto = f"Estilo de cómic: {estilo}. Calidad: {calidad}."
                    prompt_optimizado = generador.optimizar_prompt(
                        prompt_final, contexto)

                    # Usar el prompt optimizado para generar usando el método estándar
                    imagenes, mensaje = generador.generar_vineta(
                        prompt=prompt_final,  # Enviamos el prompt original a generar_vineta que ya lo optimiza
                        modelo=modelo,
                        tamanio=tamanio,
                        calidad=calidad,
                        estilo=estilo,
                        n=n
                    )
                else:  # Estamos transformando una imagen
                    # Validar que se haya cargado una imagen
                    if imagen_input is None:
                        return [], "❌ Por favor, carga una imagen primero 🖼️", [], ""

                    # Si es variación no necesitamos un prompt, de lo contrario lo requerimos
                    if tipo_transformacion == "variation":
                        # Para variaciones, no necesitamos prompt
                        prompt_final = ""
                    else:
                        # Para generation o edit, necesitamos un prompt
                        # Si no hay prompt generado, crearlo automáticamente
                        if not prompt_transform or not prompt_transform.strip():
                            prompt_final, _ = generador.procesar_imagen(
                                imagen_input, categoria_transform, estilo_transform, prompt_adicional
                            )
                        else:
                            prompt_final = prompt_transform

                        # Verificamos si después de intentar generar/usar el prompt, sigue vacío
                        if not prompt_final.strip() and tipo_transformacion != "variation":
                            return [], "❌ Se requiere una descripción para este tipo de transformación 📝", [], ""

                        # Optimizar el prompt si no es variación
                        if tipo_transformacion != "variation":
                            contexto = f"Transformación de imagen a {categoria_transform} estilo {estilo_transform}. Estilo: {estilo}. Calidad: {calidad}."
                            prompt_optimizado = generador.optimizar_prompt(
                                prompt_final, contexto)

                    # Usar el método transformar_imagen para manejar los diferentes tipos
                    imagenes, mensaje = generador.transformar_imagen(
                        imagen_input=imagen_input,
                        tipo_transformacion=tipo_transformacion,
                        prompt=prompt_final,  # El método transformar_imagen también usa optimizar_prompt
                        modelo=modelo,
                        tamanio=tamanio,
                        calidad=calidad,
                        estilo=estilo,
                        n=n
                    )

                # Si el usuario quiere ver el prompt optimizado, añadirlo al mensaje
                if mostrar_prompt and prompt_optimizado:
                    mensaje = f"📝 Prompt original: \"{prompt_final}\"\n\n✨ Prompt optimizado: \"{prompt_optimizado}\"\n\n{mensaje}"

                # Añadir emojis a los mensajes de éxito/error
                if imagenes and len(imagenes) > 0:
                    mensaje = f"✅ {mensaje} 🎉"
                else:
                    mensaje = f"❌ {mensaje}"

                # Actualizar también la galería histórica
                return imagenes, mensaje, imagenes, prompt_optimizado

            # Evento para generar cómic a partir de texto
            generar_texto_btn.click(
                fn=generar_comic,
                inputs=[
                    prompt_input,
                    imagen_input,
                    categoria_transform,
                    estilo_transform,
                    prompt_adicional,
                    prompt_transform,
                    gr.State(value=0),  # estado fijo para tab de texto
                    modelo_dropdown,
                    tamanio_dropdown,
                    calidad_dropdown,
                    estilo_dropdown,
                    num_imagenes,
                    transformacion_dropdown,
                    mostrar_prompt_optimizado  # Pasamos el checkbox para mostrar el prompt optimizado
                ],
                # Actualizado para mostrar el prompt optimizado cuando sea necesario
                outputs=[galeria, estado_generacion,
                         galeria_historica, prompt_input]
            )

            # Evento para generar cómic a partir de imagen
            generar_imagen_btn.click(
                fn=generar_comic,
                inputs=[
                    prompt_input,
                    imagen_input,
                    categoria_transform,
                    estilo_transform,
                    prompt_adicional,
                    prompt_transform,
                    gr.State(value=1),  # estado fijo para tab de imagen
                    modelo_dropdown,
                    tamanio_dropdown,
                    calidad_dropdown,
                    estilo_dropdown,
                    num_imagenes,
                    transformacion_dropdown,
                    mostrar_prompt_optimizado  # Añadimos el checkbox para mostrar el prompt optimizado
                ],
                outputs=[galeria, estado_generacion,
                         galeria_historica, gr.Textbox(visible=False)]
            )

            # Función para limpiar la galería histórica
            def limpiar_galeria():
                """
                Limpia la galería histórica de imágenes.

                Returns:
                    list: Lista vacía para limpiar la galería
                """
                return []

            # Evento para limpiar la galería
            limpiar_galeria_btn.click(
                fn=limpiar_galeria,
                inputs=[],
                outputs=[galeria_historica]
            )

            # Función para mostrar u ocultar el prompt generado
            def mostrar_prompt_oculto(prompt, _):
                """
                Controla la visibilidad del campo de prompt generado.

                Args:
                    prompt (str): El prompt actual
                    _ (any): Parámetro no utilizado

                Returns:
                    gr.update: Actualización de visibilidad para el componente
                """
                return gr.update(visible=True if prompt else False)

            # Evento para mostrar/ocultar el prompt generado
            prompt_transform.change(
                fn=mostrar_prompt_oculto,
                inputs=[prompt_transform, prompt_transform],
                outputs=[prompt_transform]
            )

            # Evento para actualizar estilos de transformación al cambiar la categoría
            categoria_transform.change(
                fn=actualizar_estilos_comics,
                inputs=[categoria_transform],
                outputs=[estilo_transform]
            )

            # Función para actualizar la visibilidad de elementos según el tipo de transformación
            def actualizar_visibilidad_prompt(tipo_transformacion):
                """
                Actualiza la visibilidad de componentes según el tipo de transformación seleccionado.

                Args:
                    tipo_transformacion (str): Tipo de transformación seleccionado

                Returns:
                    tuple: Actualizaciones de visibilidad para varios componentes
                """
                # Si es variación, no necesitamos prompt, así que ocultamos elementos relacionados
                if (tipo_transformacion == "variation"):
                    return gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)
                else:
                    return gr.update(visible=True), gr.update(visible=True), gr.update(visible=True), gr.update(visible=True)

            # Evento para actualizar visibilidad según el tipo de transformación
            transformacion_dropdown.change(
                fn=actualizar_visibilidad_prompt,
                inputs=[transformacion_dropdown],
                outputs=[categoria_transform, estilo_transform,
                         prompt_adicional, prompt_transform]
            )
