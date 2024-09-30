from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select

import time

from env import USER, PASS, URL, CURSO, DIRECTORIO

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

rubrica = [["p1	0	1	2	3"], ["	0 puntos	1 puntos	2 puntos	3 puntos"],
           ["p2	0	1	2	3"], ["	0 puntos	1 puntos	2 puntos	3 puntos"]]

rubrica2 = f"p1	0	1	2	3 "+"\n	0 puntos	1 puntos	2 puntos	3 puntos"+"\np2	0	1	2	3"+"\n	0 puntos	1 puntos	2 puntos	3 puntos"


#Login
def login():
    driver.get(F'{URL}/course/view.php?id={CURSO}')
    driver.maximize_window()
    
    # ingresar los datos de usuario
    driver.find_element(By.ID, "username").send_keys(USER)
    driver.find_element(By.ID, "password").send_keys(PASS)

    # hacer click en el botón acceder
    driver.find_element(By.ID, "loginbtn").click()
    
def login_autenticator():
    driver.get(F'{URL}/course/view.php?id={CURSO}')
    driver.maximize_window()

login()




# # Seleccionar el modo de edición si este está desactivado
# time.sleep(1)
# wait = WebDriverWait(driver, 10)

# element = wait.until(EC.element_to_be_clickable(
#     (By.XPATH, '//*[@id="usernavigation"]/li/form/div')))

# element_2 = wait.until(EC.element_to_be_clickable(
#     (By.XPATH, '//*[@id="usernavigation"]/li/form/div/label')))

# if 'text-primary' in element_2.get_attribute('class'):
#     print("Modo de edición activado, no es necesario activarlo")
# else:
#     print("Modo de edición desactivado, activando...")
#     element.click()
#     time.sleep(1)

# driver.refresh()

# # Buscamos la actividad emarking

# wait = WebDriverWait(driver, 10)

# # Abrimos el selector de actividades
# actividades_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-action="open-chooser"]')))
# actividades_btn.click() 

# # Hacemos click en la actividad requerida
# btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@data-internal="emarking"]')))
# btn.click() 

# # Seleccionamos el tipo de corrección que queremos

# menuopciones = wait.until(EC.visibility_of_element_located((By.XPATH, '//select[@name="type" and @id="id_type"]')))
# menuopciones.click()
# selector = Select(menuopciones)
# opciones = selector.options

# #### TIPOS DE CORRECCIONES ####
# SOLO_IMPRESION = 0
# IMPRIMIR_Y_DIGITALIZAR = 1
# CORRECCION_EN_PANTALLA = 2
# REVISION_ENTRE_PARES = 3

# selector.select_by_index(CORRECCION_EN_PANTALLA)

# # Ingresamos el nombre del emarking
# nombre = 'AutoEmarkingQA'
# wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@name="name" and @id="id_name"]'))).send_keys(nombre)

# # Directorio del archivo
# archivo = DIRECTORIO + '//Dummy corto.pdf'

# # Filepicker
# wait.until(EC.element_to_be_clickable((By.XPATH, '//div[starts-with(@class,"fp-btn-add")]'))).click()
# wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@type="file"]'))).send_keys(archivo)

# # Subimos archivo
# wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@class="fp-upload-btn btn-primary btn"]'))).click()

# # Guardamos y mostramos
# wait.until(EC.element_to_be_clickable((By.ID, 'id_submitbutton'))).click()
driver.get('http://localhost/mod/emarking/view.php?id=4466')

# Importamos pauta de evaluación
wait.until(EC.element_to_be_clickable((By.XPATH, '//table/tbody/tr/td[2]'))).click()

# Ingresamos la rúbrica
if wait.until(EC.presence_of_element_located((By.XPATH, '//textarea[@name="comments"]'))):
    print('Textarea encontrado')
    wait.until(EC.presence_of_element_located((By.XPATH, '//textarea[@name="comments"]'))).send_keys(rubrica2)





time.sleep(10)