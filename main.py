import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import streamlit as st
import chromedriver_autoinstaller

# Configuración inicial de Streamlit
st.title("Scraping de Ofertas Laborales de Computrabajo.cl")
st.markdown("Esta herramienta permite buscar ofertas laborales según palabras clave definidas.")
st.markdown("Importante: Se utiliza un navegador en modo headless.")

# Configurar Chrome en modo headless
def initialize_driver():
    chromedriver_autoinstaller.install()  # Instala automáticamente el ChromeDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ejecutar sin interfaz gráfica
    chrome_options.add_argument("--no-sandbox")  # Requerido en algunos entornos
    chrome_options.add_argument("--disable-dev-shm-usage")  # Optimizar para entornos limitados
    chrome_options.add_argument("--disable-gpu")  # Evitar problemas gráficos
    return webdriver.Chrome(options=chrome_options)

# Entrada de palabras clave
keywords_input = st.text_input("Ingrese palabras clave separadas por comas", "analista, ejecutivo, software, desarrollador")
keywords = [keyword.strip().lower() for keyword in keywords_input.split(',')]

# URL a procesar
url = "https://cl.computrabajo.com/empleos-en-rmetropolitana?pubdate=1&by=publicationtime"

# Botón para iniciar el scraping
if st.button("Iniciar scraping"):
    st.write("Iniciando scraping...")
    driver = initialize_driver()  # Inicializar el navegador
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

            # Intentar ir a la siguiente página
            try:
                next_button = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[@title='Siguiente' and contains(@data-path, 'p=')]"))
                )
                driver.execute_script("arguments[0].click();", next_button)
                time.sleep(3)
                page_number += 1

            except Exception:
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
