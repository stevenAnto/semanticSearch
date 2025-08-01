from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

driver  =webdriver.Chrome()

rutaTasas = "https://www.sbs.gob.pe/app/retasas/paginas/retasasInicio.aspx?p=D"
driver.get(rutaTasas)


try:
    # Esperar a que los elementos estén disponibles
    wait = WebDriverWait(driver, 10)
    
    # Seleccionar el departamento (Lima)
    select_departamento = wait.until(EC.presence_of_element_located((By.ID, "ddlDepartamento")))
    Select(select_departamento).select_by_value("01")  # 15 es Lima
    
    # Esperar un momento para que se cargue el siguiente dropdown
    time.sleep(2)


        # Seleccionar el tipo de producto (DEPOSITOS)
    select_tipo_producto = wait.until(EC.presence_of_element_located((By.ID, "ddlTipoProducto")))
    Select(select_tipo_producto).select_by_value("02")  # 02 es DEPOSITOS
    
    # Esperar un momento para que se cargue el siguiente dropdown
    time.sleep(2)
    
    # Seleccionar el producto (PLAZO FIJO EN SOLES)
    select_producto = wait.until(EC.presence_of_element_located((By.ID, "ddlProducto")))
    Select(select_producto).select_by_value("07")  # 07 es PLAZO FIJO EN SOLES
    
    # Esperar un momento para que se cargue el siguiente dropdown
    time.sleep(2)

        # Esperar un momento para que se cargue el siguiente dropdown
    time.sleep(2)
    
    # Seleccionar la condición (si hay opciones disponibles)
    try:
        select_condicion = wait.until(EC.presence_of_element_located((By.ID, "ddlCondicion")))
        if select_condicion.find_elements(By.TAG_NAME, "option"):
            Select(select_condicion).select_by_index(1)  # Selecciona la primera opción disponible
    except:
        print("No hay opciones de condición para seleccionar")


    print("Ahora procedera a consulta el boton")

        # Hacer clic en el botón de consulta
    btn_consultar = wait.until(EC.element_to_be_clickable((By.ID, "btnConsultar")))
    btn_consultar.click()
    
    # Esperar a que aparezca el botón de Excel
    time.sleep(5)  # Puedes ajustar este tiempo según sea necesario

    print("Haremos click en la imagen")
    print("cambiando de contexto")
    driver.switch_to.frame("ifrmContendedor")
    print("se terminado de cambiar contexto")
    
    # Descargar el archivo Excel
    btn_excel = wait.until(EC.element_to_be_clickable((By.ID, "ImageButton1")))
    btn_excel.click()
    
    # Esperar un momento para que se complete la descarga
    time.sleep(5)
    
    print("Proceso completado correctamente")




except Exception as e:
    print(f"ocurrio un error{str(e)}")

finally:
    driver.quit

