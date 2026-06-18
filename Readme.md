# Generador de Cotizaciones PDF

## Descripción

Este proyecto consiste en un sistema desarrollado en Python para generar cotizaciones profesionales en formato PDF utilizando la librería ReportLab.

El programa solicita información desde la terminal, procesa los datos ingresados por el usuario y genera automáticamente una cotización lista para ser compartida con clientes.

---

## Funcionalidades

* Captura de datos de la empresa.
* Captura de datos del cliente.
* Registro de múltiples productos.
* Cálculo automático de:

  * Subtotal
  * Descuento
  * Envío
  * Total final
* Generación automática de PDF.
* Diseño personalizado para presentación profesional.

---

## Tecnologías utilizadas

* Python 3
* ReportLab

---

## Archivos del proyecto

### PDF.PY

Archivo principal del programa.

Contiene:

* Captura de datos.
* Procesamiento de información.
* Cálculos matemáticos.
* Construcción del documento PDF.

---

## Requisitos

Instalar la librería ReportLab:

```bash
pip install reportlab
```

---

## Ejecución

Ejecutar el programa:

```bash
python PDF.py
```

---

## Flujo de funcionamiento

1. El usuario ejecuta el programa.
2. Se solicitan los datos necesarios.
3. Se registran los productos.
4. Se realizan los cálculos correspondientes.
5. Se construye el documento PDF.
6. El archivo se guarda automáticamente en la carpeta del proyecto.

---

## Autor

Pedro Pablo Carrillo

Proyecto académico desarrollado para el curso de Programación.
