# Triaje Automatico de Tickets de TI

## Resumen
Este repositorio organiza un prototipo academico y profesional de Machine Learning para el triaje automatico de tickets de TI en portugues de Brasil. La aplicacion combina un pipeline de `Scikit-Learn` entrenado con tickets sinteticos y una interfaz `Streamlit` para la clasificacion simultanea de categoria y prioridad.

## Problema resuelto
Las mesas de soporte suelen recibir descripciones de incidentes y solicitudes cortas, ruidosas y heterogeneas. Este proyecto busca reducir el tiempo de enrutamiento inicial proponiendo una clasificacion automatica basada en palabras clave tecnicas de ITSM, sin depender de frases completas ni de un contexto narrativo largo.

## Arquitectura de la aplicacion
El flujo principal esta compuesto por:

- entrada de texto en `app.py`;
- carga del artefacto `pipeline_itsm.joblib` con `@st.cache_resource`;
- vectorizacion con `TfidfVectorizer` en unigramas;
- eliminacion manual de stop words en portugues;
- clasificacion multi-salida con `MultiOutputClassifier(RandomForestClassifier)`;
- retorno simultaneo de `categoria` y `prioridade`.

El diagrama de arquitectura esta disponible en `assets/diagrams/architecture.mmd`.

## Flujo de clasificacion
1. El usuario informa palabras clave cortas del incidente, por ejemplo `vpn falha mfa dns`.
2. El texto se normaliza y se transforma en un vector TF-IDF.
3. El clasificador multi-salida estima la categoria operativa y la prioridad del ticket.
4. La interfaz muestra el resultado de inmediato para apoyar el enrutamiento inicial.

## Tipos de entrada y salida
Entrada:

- texto libre corto con jerga de ITSM;
- ejemplos: `reset senha ad`, `tela azul memoria`, `outlook erro smtp`.

Salida:

- `categoria`: clase funcional predicha;
- `prioridade`: nivel inicial de atencion predicho.

## Instalacion local
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python train.py
streamlit run app.py
```

## Despliegue en Streamlit Cloud
1. Publicar el repositorio en GitHub.
2. Configurar la aplicacion de Streamlit Cloud apuntando a `app.py`.
3. Verificar que `requirements.txt` este en la raiz del repositorio.
4. Opcionalmente definir variables basadas en `.env.example` solo para entornos de demostracion.
5. Volver a desplegar cada vez que cambien el pipeline o las dependencias.

## Metodologia de entrenamiento
El entrenamiento usa un conjunto sintetico con jerga de soporte tecnico y operaciones de TI. El archivo `train.py` separa explicitamente el texto de las etiquetas para evitar fuga de datos entre atributos y objetivos.

### Representacion textual
El modulo textual fue disenado para priorizar robustez lexical:

- normalizacion a minusculas;
- eliminacion de acentos;
- `TfidfVectorizer` con unigramas solamente;
- lista manual de stop words en portugues enfocada en conectores y terminos de baja informacion.

Esta configuracion favorece palabras clave tecnicas cortas y reduce el sesgo de clasificacion basado en formulaciones largas o frases completas demasiado especificas.

### Modelo
El clasificador utiliza `MultiOutputClassifier` con `RandomForestClassifier`, lo que permite inferencia conjunta de categoria y prioridad dentro de un unico pipeline.

## Resultados
La interfaz de demostracion siguiente registra una clasificacion ejecutada localmente por la aplicacion Streamlit.

![Clasificacion Streamlit](../../assets/screenshots/streamlit-classification.png)

## Limitaciones del modelo

- la base de entrenamiento es sintetica y no reemplaza tickets reales curados;
- no existe evaluacion estadistica formal de entrenamiento-validacion-prueba en el estado actual del proyecto;
- el modelo no incorpora contexto temporal, historial del usuario ni relaciones entre incidentes;
- el comportamiento depende fuertemente de la cobertura del vocabulario tecnico en la base sintetica.

## Riesgos eticos en entornos de soporte

- clasificaciones incorrectas pueden inducir enrutamiento inadecuado y aumentar el tiempo de respuesta;
- los vocabularios sinteticos pueden reflejar sesgos del curador y subrepresentar equipos o servicios;
- las predicciones automaticas no deben sustituir el analisis humano en escenarios criticos;
- registros, ejemplos y capturas deben permanecer sanitizados para evitar exposicion operativa.

## Proximos pasos

- agregar evaluacion cuantitativa con metricas por clase;
- introducir pruebas automatizadas de regresion para el pipeline;
- incorporar configuracion externa de clases y prioridades;
- agregar una API de inferencia para integracion con plataformas ITSM;
- evaluar modelos lineales y embeddings ligeros para comparacion.

## Referencias BibTeX
```bibtex
@misc{python,
  author       = {{Python Software Foundation}},
  title        = {Python Language Reference},
  year         = {2026},
  howpublished = {\url{https://www.python.org/}},
  note         = {Accessed 2026-06-07}
}

@misc{numpy,
  author       = {{NumPy Developers}},
  title        = {NumPy},
  year         = {2026},
  howpublished = {\url{https://numpy.org/}},
  note         = {Accessed 2026-06-07}
}

@misc{joblib,
  author       = {{joblib developers}},
  title        = {joblib: Python utilities for lightweight pipelining},
  year         = {2026},
  howpublished = {\url{https://joblib.readthedocs.io/}},
  note         = {Accessed 2026-06-07}
}

@misc{scikit-learn,
  author       = {{Scikit-learn developers}},
  title        = {Scikit-learn: Machine Learning in Python},
  year         = {2026},
  howpublished = {\url{https://scikit-learn.org/}},
  note         = {Accessed 2026-06-07}
}

@misc{streamlit,
  author       = {{Streamlit Inc.}},
  title        = {Streamlit: The fastest way to build and share data apps},
  year         = {2026},
  howpublished = {\url{https://streamlit.io/}},
  note         = {Accessed 2026-06-07}
}
```
