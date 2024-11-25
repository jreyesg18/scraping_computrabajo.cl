# Scraper de Ofertas Laborales en CompuTrabajo

Este proyecto es un scraper de ofertas laborales que utiliza Selenium para extraer títulos, enlaces, y las palabras clave coincidentes de trabajos desde la página de Computrabajo en Chile. Permite buscar trabajos que contengan una o más palabras clave ingresadas por el usuario.
## Requisitos

- Python 3.x
- Selenium
- Chrome WebDriver (debe ser compatible con tu versión de Chrome)

## Instalación

1. Clona este repositorio o descarga los archivos.

2. Instala las dependencias requeridas:

       pip install selenium
3. Asegúrate de tener Chrome WebDriver instalado y que esté en tu PATH. 

## Uso

1. Abre una terminal y navega hasta el directorio del proyecto.

2. Ejecuta el script:

         python main.py
3. Cuando se te solicite, ingresa la palabra clave que deseas buscar en los títulos de trabajo.

4. El script navegará por las páginas de ofertas laborales y extraerá los trabajos que coincidan con tu búsqueda. Los resultados se guardarán en un archivo job_offers.json.

## Ejemplo

Si deseas buscar trabajos que contengan las palabras "Ventas, Marketing, Programación", simplemente ingresa esas palabras separadas por comas cuando se te solicite.
## Estructura de los Datos

Los datos extraídos se guardarán en un archivo JSON con la siguiente estructura:


        [
            {
                "title": "Ejecutivo de Ventas Part time de 10 a 16:30 hrs de lunes a viernes",
                "link": "https://cl.computrabajo.com/ofertas-de-trabajo/oferta-de-trabajo-de-ejecutivo-de-ventas-part-time-de-10-a-1630-hrs-de-lunes-a-viernes-en-santiago-centro-2DC9E14A19608C9661373E686DCF3405#lc=ListOffers-Score-0"
                "matching_keyword": "ventas"
            },
            ...
        ]

## Notas

- Asegúrate de que tu conexión a internet esté activa durante la ejecución del script.
- El script puede tardar un tiempo en completarse, dependiendo de la cantidad de páginas de resultados.
- Las palabras clave son insensibles a mayúsculas/minúsculas, por lo que "ventas" y "Ventas" se tratarán como iguales.
