#!/bin/bash

# Cambia al directorio donde están tus archivos
cd ~/TopicosAvanzadoDb/proyecto/data

# Recorre todos los archivos .xls del directorio
for archivo in *.xls; do
  # Convertir nombre a minúsculas y reemplazar espacios por guiones bajos
  nuevo_nombre=$(echo "$archivo" | tr '[:upper:]' '[:lower:]' | tr ' ' '_' )
  
  # Agregar el prefijo soles_
  nuevo_nombre="soles_${nuevo_nombre}"

  # Renombrar el archivo
  mv "$archivo" "$nuevo_nombre"
done

echo "Renombrado completado."

