import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import streamlit as st

# Configuración inicial de Streamlit
st.title("Scraping de Ofertas Laborales de Computrabajo.cl")
st.markdown("Esta herramienta permite buscar ofertas laborales según palabras clave definidas.")
st.markdown("Importante: Debe tener instalado Chrome")

# Entrada de palabras clave
keywords_input = st.text_input("Ingrese palabras clave separadas por comas", "analista, ejecutivo, software, desarrollador")
keywords = [keyword.strip().lower() for keyword in keywords_input.split(',')]

# Entrada de URL
# url = st.text_input("Ingrese el enlace del sitio web", "https://cl.computrabajo.com/empleos-en-rmetropolitana?pubdate=1&by=publicationtime")
url = "https://cl.computrabajo.com/empleos-en-rmetropolitana?pubdate=1&by=publicationtime"

# Botón para iniciar el scraping
if st.button("Iniciar scraping"):
    st.write("Iniciando scraping...")
    driver = webdriver.Chrome()
    driver.get(url)

    # Lista para almacenar los resultados
    job_results = []
    page_number = 1

    try:
        while True:
            st.write(f"Procesando página {page_number}...")

            # Esperar a que los trabajos estén cargados
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a.js-o-link.fc_base"))
            )

            # Encontrar todos los elementos <a> con la clase js-o-link fc_base
            job_elements = driver.find_elements(By.CSS_SELECTOR, "a.js-o-link.fc_base")

            # Extraer el título y el enlace de cada trabajo
            for job_element in job_elements:
                title = job_element.text  # Texto del título del trabajo
                link = job_element.get_attribute("href")  # Enlace de la oferta

                # Inicializar una variable para guardar la palabra que coincide
                matching_keyword = None

                # Filtrar por las palabras clave en el título
                for keyword in keywords:
                    if keyword in title.lower():
                        matching_keyword = keyword  # Guardar la palabra que coincide
                        break  # Si encuentra una coincidencia, no es necesario seguir buscando

                # Si se encontró una coincidencia
                if matching_keyword:
                    # Agregar el diccionario a la lista
                    job_data = {
                        "title": title,
                        "matching_keyword": matching_keyword,
                        "link": link
                    }
                    job_results.append(job_data)

            # Mostrar resultados parciales en Streamlit
            # st.write(f"Resultados encontrados: {len(job_results)}")
            # st.json(job_results[-5:])  # Mostrar los últimos 5 resultados

            # Intentar ir a la siguiente página
            try:
                next_button = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[@title='Siguiente' and contains(@data-path, 'p=')]"))
                )
                driver.execute_script("arguments[0].click();", next_button)
                time.sleep(3)
                page_number += 1

            except Exception as e:
                st.write("No se pudo encontrar el botón de 'Siguiente' o no hay más páginas.")
                break

    except Exception as e:
        st.error(f"Error: {e}")

    finally:
        driver.quit()
        st.success("Scraping finalizado.")
        if job_results:
            # Mostrar opción para descargar los resultados
            st.download_button(
                label="Descargar resultados como JSON",
                data=json.dumps(job_results, indent=4),
                file_name="resultados_scraping.json",
                mime="application/json"
            )