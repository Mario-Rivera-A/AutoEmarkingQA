from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException, StaleElementReferenceException

import time

import os

import requests

import random

import logging

from env import USER, PASS, URL, COURSE, DIRECTORIO, DIRECTORIO_DESCARGAS

##########################
chrome_options = webdriver.ChromeOptions()

# Configurar las preferencias para la descarga automática
prefs = {
    "download.default_directory": DIRECTORIO_DESCARGAS,  # Ruta de descarga
    "download.prompt_for_download": False,        # Desactivar el diálogo de descarga
    "download.directory_upgrade": True,           # Permitir que Selenium actualice el directorio de descargas
    "safebrowsing.enabled": False,                  # Habilitar la descarga de archivos inseguros (opcional)
    "safebrowsing.disable_download_protection": True,  # Deshabilitar la protección de descargas (opcional)
    "plugins.always_open_pdf_externally": False     # Forzar la descarga de PDFs en lugar de abrirlos en el navegador
}

# Aplicar las preferencias
chrome_options.add_experimental_option("prefs", prefs)

# Inicializar el driver con las opciones
driver = webdriver.Chrome(options=chrome_options)
##########################

wait = WebDriverWait(driver, 10)

# Configura el logging para escribir en un archivo
logging.basicConfig(
    filename='reporte.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

#Login
def login(ruta = True):
    try:
        if ruta:
            driver.get(F'{URL}/course/view.php?id={COURSE}')
            driver.maximize_window()
        
        # ingresar los datos de usuario
        driver.find_element(By.ID, "username").clear()
        driver.find_element(By.ID, "username").send_keys(USER)
        driver.find_element(By.ID, "password").clear()
        driver.find_element(By.ID, "password").send_keys(PASS)

        # hacer click en el botón acceder
        driver.find_element(By.ID, "loginbtn").click()
    except TimeoutException:
        logging.error("Se agotó el tiempo de espera para realizar el loggin ")
    except:
        logging.error("Hubo un problema en al realizar el loggin")

        
def login_autenticator():
    try:
        driver.get(F'{URL}/course/view.php?id={COURSE}')
        driver.maximize_window()
    except:
        logging.error("Hubo un problema en al realizar el loggin")
        

def wait_for_zip_file(directory, existing_files, timeout=300):
    """
    Esperamos a que un archivo .zip con el nombre especificado aparezca en el directorio.
    """
    start_time = time.time()
    while True:
        current_files = [f for f in os.listdir(directory) if f.endswith('.zip')]
        new_files = set(current_files) - set(existing_files)
        if new_files:
            new_file = new_files.pop()
            file_path = os.path.join(directory, new_file)
            logging.info(f'Nuevo archivo .zip encontrado: {file_path}')
            return file_path
        
        elapsed_time = time.time() - start_time
        if elapsed_time > timeout:
            logging.info("No se encontró un nuevo archivo .zip en el tiempo esperado.")
            return None
        time.sleep(5)


def mode_edit():
    try:    
        # Seleccionar el modo de edición si este está desactivado
        time.sleep(1)

        element = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="usernavigation"]/li/form/div')))

        element_2 = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="usernavigation"]/li/form/div/label')))

        if 'text-primary' in element_2.get_attribute('class'):
            logging.info("Modo de edición activado, no es necesario activarlo")
        else:
            logging.info("Modo de edición desactivado, activando...")
            element.click()
            time.sleep(1)

        driver.refresh()
    except:
        logging.error("No se pudo activar el modo edición")
        
        
def find_emarking_activity():
    try:
        # Buscamos la actividad emarking #

        # Abrimos el selector de actividades
        actividades_btn = wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@data-action="open-chooser"]/span')))
        time.sleep(1)
        actividades_btn.click() 

        # Hacemos click en la actividad requerida
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@data-internal="emarking"]')))
        btn.click() 
    except:
        logging.error("No se encontró la actividad emarking dentro de los recursos")
        
#### TIPOS DE CORRECCIONES ####
SOLO_IMPRESION = 0
IMPRIMIR_Y_DIGITALIZAR = 1
CORRECCION_EN_PANTALLA = 2
REVISION_ENTRE_PARES = 3

def go_to_course():
    driver.get(F'{URL}/course/view.php?id={COURSE}')

def emarking_settings(type, nombre):
    try:
        # Seleccionamos el tipo de corrección que queremos

        menuopciones = wait.until(EC.visibility_of_element_located((By.XPATH, '//select[@name="type" and @id="id_type"]')))
        menuopciones.click()
        selector = Select(menuopciones)

        selector.select_by_index(type)

        # Ingresamos el nombre del emarking
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@name="name" and @id="id_name"]'))).send_keys(nombre)

        # Directorio del archivo
        archivo = DIRECTORIO + '//Dummy corto.pdf'

        # Filepicker
        wait.until(EC.element_to_be_clickable((By.XPATH, '//div[starts-with(@class,"fp-btn-add")]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@type="file"]'))).send_keys(archivo)

        # Subimos archivo
        wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@class="fp-upload-btn btn-primary btn"]'))).click()

        # Guardamos y mostramos
        wait.until(EC.element_to_be_clickable((By.ID, 'id_submitbutton'))).click()
    except:
        logging.error("Problemas al configurar el Emarking")
        

def rubric():

    try:
        # "Importamos" pauta de evaluación
        wait.until(EC.element_to_be_clickable((By.XPATH, '//table/tbody/tr/td[2]'))).click()

        rubric_text = """Criterio 1	Nivel 1.1	Nivel 1.2	Nivel 1.3
	0 puntos	1.5 puntos	2 puntos
Criterio 2	Nivel 2.1	Nivel 2.2	
	0 puntos	5 puntos	
Criterio 3	Nivel 3.1	Nivel 3.2	Nivel 3.3
	0 puntos	1 punto	3 puntos

    """
        driver.refresh()
        textarea = wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@name="comments"]')))
        textarea.clear()
        time.sleep(1)
                
        for char in rubric_text:
            driver.execute_script("""
                arguments[0].value += arguments[1];
                arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            """, textarea, char)

        # Enviamos, confirmamos la rúbrica y luego continuamos
        wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@type="submit"]'))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@type="submit"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@type="submit"]'))).click()

        # Vamos a la pestaña imprimir y digitalizar para guardar la prueba
        wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@role = "main"]/ul/li[1]'))).click()
    except:
        logging.error("No se logró importar la rúbrica")


def download_exams():

    wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@role = "main"]/ul/li[1]'))).click()
    # Seleccionamos la pestaña "Prueba"
    wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@role = "main"]/ul[2]/li[1]'))).click()
    
    
    try:
        before_download = set(os.listdir(DIRECTORIO_DESCARGAS))

        global original_window 
        original_window = driver.current_window_handle
        assert len(driver.window_handles) == 1

        # Esperar hasta que la prueba sea procesada
        while True:
            try:
                wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[class$="downloadExam"]')))
            except:
                logging.info("Prueba procesando...")
                driver.refresh()
            else:
                logging.info("Prueba procesada")
                break
            
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[class$="downloadExam"]'))).click()
        wait.until(EC.number_of_windows_to_be(2))

        new_window = [window for window in driver.window_handles if window != original_window][0]
        driver.switch_to.window(new_window)

        # Obtenemos el url de la nueva pestaña
        file_url = driver.current_url
        logging.info(f'URL de la nueva pestaña: {file_url}')

        # Descargamos la prueba usando requests
        session = requests.Session()
        for cookie in driver.get_cookies():
            session.cookies.set(cookie['name'], cookie['value'])
            
        # Realizamos la solicitud GET para descargar el archivo
        response = session.get(file_url, verify=False)

        # Guardamos el archivo
        nombre_archivo = os.path.basename(file_url)

        ruta_archivo = os.path.join(DIRECTORIO_DESCARGAS, nombre_archivo)

        with open(ruta_archivo, 'wb') as file:
            file.write(response.content)
        logging.info(f"Archivo descargado en: {ruta_archivo}")

        driver.close()
        driver.switch_to.window(original_window)
    except:
        logging.error("Hubieron problemas al descargar la prueba")

def emarkingDesktop_process():
    try:
        # Hay que esperar a procesar las pruebas antes de continuar
        logging.info('Procesa el archivo descargado ')
        print("Procesa la prueba descargada en Emarking Desktop")
        existing_zip_files = [f for f in os.listdir(DIRECTORIO_DESCARGAS) if f.endswith('.zip')]
        zip_file_path = wait_for_zip_file(DIRECTORIO_DESCARGAS, existing_zip_files)

        while not zip_file_path:
            logging.info('Procesa el archivo descargado ')
            zip_file_path = wait_for_zip_file(DIRECTORIO_DESCARGAS, existing_zip_files)

        # Una vez ya procesadas las respuestas, hay que subirlas
        wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@role = "main"]/ul[2]/li[2]'))).click()

        # Subimos el archivo .zip que encontramos
        wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@type="button"]'))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@type="file"]'))).send_keys(zip_file_path)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//button[starts-with(@class,"fp-upload-btn")]'))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@data-fieldtype="submit"]/input[@name="submitbutton"]'))).click()
    except:
        logging.error("Problemas al procesar las pruebas")

def process_exams():
    try:
        # Esperamos a que la prueba esté procesada
        while True:
            status = wait.until(EC.visibility_of_element_located((By.XPATH, '//table[@class = "generaltable"]/tbody/tr/td[5]')))
            if status.text == 'Processed' or status.text == 'Procesada':
                break
            else:
                logging.info('Procesando respuestas...')
                time.sleep(20)
                driver.refresh()

        # Vamos a corrección en pantalla para empezar a revisar las pruebas
        wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@role = "main"]/ul/li[2]'))).click()
        global emarking_url
        emarking_url = driver.current_url
        
    except:
        logging.error("Hubo un error interno al procesar las pruebas, intentar todo de nuevo")

def show_emarking():
    driver.get(F'{URL}/course/view.php?id={COURSE}')
    mode_edit()
    # Mostramos el emarking
    try:
        # Intentamos seleccionar el modal
        opciones_actividad=wait.until(EC.presence_of_element_located((By.XPATH, '//div[@id="coursecontentcollapse0"]/ul/li[last()]/div/div/div[2]/div/div')))
        opciones_actividad.click()
        opciones_actividad.find_element(By.XPATH,'div/div/div/a[3]').click()
        
        
    except:
        logging.error("Problemas con mostrar el emarking a los alumnos")
    
    
    
def correct_button(type, info_estudiantes = [], fast = True):
    
    pruebas_no_corregidas = []
    
    if type == CORRECCION_EN_PANTALLA:
        
        # Buscamos los elementos tr
        trs = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//table[@id="emarking-main"]/tbody/tr[not(@class="emptyrow")]')))
        logging.info(f'Cantidad de pruebas a corregir: {len(trs)}')
        
        # Obtener el atributo 'href' de cada elemento 'tr' en la lista 'trs'
        hrefs_pruebas = [tr.find_element(By.XPATH,'td[5]/div/a[1]').get_attribute('href') for tr in trs]
        logging.info(f'hrefs: {hrefs_pruebas}')
        
        for i, href in enumerate(hrefs_pruebas):
            try:
                if fast and i == 5:
                    wait.until(EC.presence_of_element_located((By.XPATH, 'div[@class="html-face"]/i[@class="icon-save"]'))).click()
                    driver.close()
                    driver.switch_to.window(original_window)
                    go_to_course()
                    break
                    
                driver.get(href)
                logging.info(f'Corrigiendo prueba {i+1} de {len(trs)}')
                
                # Ya sabemos la cantidad de criterios y de niveles por criterio que hay en la rúbrica
                niveles = {1:random.randint(2,4), 2:random.randint(2,3), 3:random.randint(2,4)}
            
                for criterio in range(1,4):
                    # Para corregir, podemos hacer un click en la página de la prueba para que se despliegue el modal de corrección 
                    wait.until(EC.visibility_of_element_located((By.XPATH, '//div/table/tbody/tr[1]/td/div/div/canvas'))).click()
                    logging.info(f'Corrigiendo criterio {criterio}')
                    
                    # Seleccionamos un nivel al azar
                    wait.until(EC.visibility_of_element_located((By.XPATH, f'//tbody/tr[2]/td/div/div/table/tbody/tr[{criterio}]/td/div/div[{niveles[criterio]}]/div/div'))).click()
                    
                    # Guardamos el nivel
                    wait.until(EC.element_to_be_clickable((By.XPATH, '//tr[4]/td/table/tbody/tr/td[1]/button'))).click()
                time.sleep(2)
                if i == len(trs) - 1:
                    logging.info('Última prueba corregida')
                
            except:
                logging.warning(f'No se pudo corregir la prueba {href}')                
                time.sleep(4)
                pruebas_no_corregidas.append(href)
                continue
                    
        
        
    elif type == REVISION_ENTRE_PARES:
        # Mostramos el modal  
    
        for i, corrector in enumerate(info_estudiantes):
            try:
                if fast and i == 5 :
                    logging.info("Pruebas entre pares revisadas con éxito")
                    go_to_course()
                    break
                
                # Iniciamos sesión como el estudiante
                driver.get(info_estudiantes[i][2])
                
                
                # Pestaña configuración
                wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="edw-tabs-navigation"]/ul/li[3]'))).click()
                student_login= wait.until(EC.presence_of_element_located((By.XPATH, '//section[contains(@class,"administration")]/div/ul/li[2]/span/a'))).get_attribute('href')
                driver.get(student_login)
                wait.until(EC.presence_of_element_located((By.XPATH, '//button[@type="submit" and @class="btn btn-primary"]'))).click()
                
                # Una vez iniciado sesión, vamos a la prueba y la corregimos
                driver.get(info_estudiantes[i][4])
                
                logging.info(f'Corrigiendo prueba {i+1} de {len(info_estudiantes)}')
                        
                # Ya sabemos la cantidad de criterios y de niveles por criterio que hay en la rúbrica
                niveles = {1:random.randint(2,4), 2:random.randint(2,3), 3:random.randint(2,4)}

                for criterio in range(1,4):
                    try:
                        # Para corregir, podemos hacer un click en la página de la prueba para que se despliegue el modal de corrección 
                        wait.until(EC.visibility_of_element_located((By.XPATH, '//div/table/tbody/tr[1]/td/div/div/canvas'))).click()
                        logging.info(f'Corrigiendo criterio {criterio}')
                        
                        # Seleccionamos un nivel al azar
                        wait.until(EC.visibility_of_element_located((By.XPATH, f'//tbody/tr[2]/td/div/div/table/tbody/tr[{criterio}]/td/div/div[{niveles[criterio]}]/div/div'))).click()
                        
                        # Guardamos el nivel
                        wait.until(EC.element_to_be_clickable((By.XPATH, '//tr[4]/td/table/tbody/tr/td[1]/button'))).click()
                    
                    except:
                        logging.error("Criterio ya seleccionado") 
                        # time.sleep(4)
                        driver.get(info_estudiantes[i][4])
                        continue
                    if criterio == 3:
                        logging.info("Criterios corregidos")
                        driver.get(emarking_url)
                        
                
                # Cerramos sesión
                wait.until(EC.presence_of_element_located((By.XPATH, '//span[@class="userbutton"]'))).click()
                session = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@id="user-action-menu"]/div/div/div/a[last()]'))).get_attribute('href')
                
                logging.info(f"Se revisó la prueba de {info_estudiantes[i][1]} con éxito")
                
                driver.get(session)
                login(False)
            
            except:
                logging.error(f"Hubo un problema al revisar la prueba de {info_estudiantes[i][1]}")
                time.sleep(4)
                pruebas_no_corregidas.append(info_estudiantes[i][4])
                continue
    
    
    
    
    if len(pruebas_no_corregidas)>1:
        logging.warning("Proceso de corrección de pruebas finalizado con algunos errores.")
        logging.warning(f"Hubieron {len(pruebas_no_corregidas)} pruebas que no se procesaron.\n Estas son:\n{pruebas_no_corregidas}")
    else:
        logging.info("Proceso de corrección de pruebas finalizado con éxito.")
    
def show_pairs_of_students(fast = True):
    
    driver.get(emarking_url)

    info_estudiantes = []
    
    # Buscamos los elementos tr
    trs = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//table[@id="emarking-main"]/tbody/tr[not(@class="emptyrow")]')))
    logging.info(f'Cantidad de pruebas a corregir: {len(trs)}')
    
    # Obtenemos el nombre del estudiante a corregir, el href de este usuario, href de la prueba y el estudiante corrector
    hrefs_estudiantes_correctores = [tr.find_element(By.XPATH, 'td[1]/a[1]').get_attribute('href') for tr in trs]
    nombre_estudiantes_correctores = [tr.find_element(By.XPATH, 'td[1]/a[2]').text for tr in trs]
    hrefs_estudiantes_a_corregir = [tr.find_element(By.XPATH, 'td[2]/a[1]').get_attribute('href') for tr in trs]
    nombre_estudiantes_a_corregir = [tr.find_element(By.XPATH, 'td[2]/a[1]').text.strip() for tr in trs]
    hrefs_pruebas = [tr.find_element(By.XPATH,'td[6]/div/a[1]').get_attribute('href') for tr in trs]
    
    for href_corrector, nombre_corrector, href_a_corregir, nombre_a_corregir, href_prueba in zip(hrefs_estudiantes_correctores, nombre_estudiantes_correctores, hrefs_estudiantes_a_corregir, nombre_estudiantes_a_corregir, hrefs_pruebas):
        info = [href_corrector, nombre_corrector, href_a_corregir, nombre_a_corregir, href_prueba]
        info_estudiantes.append(info)
    
    correct_button(type=REVISION_ENTRE_PARES, info_estudiantes=info_estudiantes, fast=True)
    
        
login()

def normal_emarking():
    
    mode_edit()
    find_emarking_activity()
    emarking_settings(CORRECCION_EN_PANTALLA, "AutoEmarking tipo corrección en pantalla")
    rubric()    
    download_exams()
    emarkingDesktop_process()
    process_exams()
    correct_button(CORRECCION_EN_PANTALLA)    
    
def revision_pares():
    # Hay un pequeño cambio, en revisión entre pares la rúbrica se hace unos pasos después que un emarking normal
    
    mode_edit()
    find_emarking_activity()
    emarking_settings(REVISION_ENTRE_PARES, "AutoEmarking tipo revisión entre pares")
    logging.info("Realizando un emarking de tipo revisión entre pares.")
    download_exams()
    emarkingDesktop_process()
    process_exams()
    rubric()
    show_emarking() 
    show_pairs_of_students()



revision_pares()
normal_emarking()


time.sleep(10)