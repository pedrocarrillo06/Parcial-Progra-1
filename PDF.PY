from datetime import datetime
import os
import re

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

# =========================================================
# CALYPSO TEXTILE STUDIO
# GENERADOR DE COTIZACIONES EN PDF
# =========================================================
#
# Este programa tiene un objetivo principal:
# 1. Pedir datos al usuario desde la terminal.
# 2. Guardar esos datos en variables.
# 3. Realizar cálculos automáticos.
# 4. Construir una cotización elegante en PDF.
#
# La idea es que el usuario pueda leer este archivo y entender claramente qué hace cada parte.
# =========================================================

# =========================================================
# UTILIDADES DE ENTRADA
# =========================================================

#  

def ask_str(prompt, default=None, allow_empty=False):
    while True:
        if default is not None:
            value = input(f"{prompt} [{default}]: ").strip()
            if value == "":
                value = default
        else:
            value = input(f"{prompt}: ").strip()

        if value or allow_empty:
            return value

        print("Este campo no puede quedar vacío.")


def ask_float(prompt, default=0.0):
    while True:
        raw = input(f"{prompt} [{default}]: ").strip()
        if raw == "":
            return float(default)

        raw = raw.replace("Q", "").replace("q", "").replace(",", "")
        try:
            return float(raw)
        except ValueError:
            print("Ingresa un número válido.")

#     Solicita un número decimal al usuario.

# ¿Qué hace?
    #- Lee texto desde la terminal.
    #- Limpia símbolos como Q o comas.
    #- Convierte el texto en un número decimal.

    #¿Por qué existe?
    #Porque precios y montos normalmente tienen decimales.


def ask_int(prompt, default=0):
    while True:
        raw = input(f"{prompt} [{default}]: ").strip()
        if raw == "":
            return int(default)

        try:
            return int(raw)
        except ValueError:
            print("Ingresa un número entero válido.")

    #Solicita un número entero al usuario. ¿Qué hace? Lee texto desde la terminal. Intenta convertirlo a entero. Si falla, vuelve a pedirlo. Se usa para cantidades de prendas, número de productos, etc.

def money_q(value):
    return f"Q{value:,.2f}"

#     Formatea un número como moneda de Guatemala. Ejemplo: 65 -> Q65.00

def safe_text(value):
    return xml_escape(str(value))

#Escapa caracteres especiales para que ReportLab no interprete símbolos raros dentro de los párrafos.


def sanitize_filename(name):
    name = re.sub(r"[^\w\-]+", "_", name.strip(), flags=re.UNICODE)
    name = re.sub(r"_+", "_", name)
    return name.strip("_") or "cotizacion"

    # Limpia un texto para convertirlo en nombre de archivo. Ejemplo: 'COT-2025/06/17' -> 'COT-2025_06_17'


def file_exists(path):
    return bool(path) and os.path.isfile(path)

#    Verifica si existe un archivo en la ruta indicada. Se usa principalmente para comprobar si el logo fue agregado.


# =========================================================
# COLORES Y ESTILO
# =========================================================
# Esta sección define la personalidad visual del documento. Los colores elegidos buscan transmitir una identidad elegante, limpia y cálida, parecida al estilo de Calypso.
# =========================================================

BEIGE = colors.HexColor("#f7f1e8")
CREAM = colors.HexColor("#fbf7f1")
GREEN = colors.HexColor("#173d2a")
GREEN_DARK = colors.HexColor("#102a1f")
GOLD = colors.HexColor("#c79f67")
LIGHT_GOLD = colors.HexColor("#e3c9a4")
GRAY = colors.HexColor("#5f5f5f")
LIGHT_GRAY = colors.HexColor("#d8d0c6")
LINE = colors.HexColor("#d7c9b7")

styles = getSampleStyleSheet()

TITLE = ParagraphStyle(
    "TITLE",
    parent=styles["Heading1"],
    fontName="Times-Roman",
    fontSize=26,
    leading=30,
    textColor=GREEN,
    alignment=TA_LEFT,
    spaceAfter=2,
)

SUBTITLE = ParagraphStyle(
    "SUBTITLE",
    parent=styles["BodyText"],
    fontName="Helvetica",
    fontSize=9.5,
    leading=11,
    textColor=GREEN,
    alignment=TA_LEFT,
)

SECTION = ParagraphStyle(
    "SECTION",
    parent=styles["BodyText"],
    fontName="Helvetica-Bold",
    fontSize=9.5,
    leading=11,
    textColor=GREEN,
    alignment=TA_LEFT,
)

BODY = ParagraphStyle(
    "BODY",
    parent=styles["BodyText"],
    fontName="Helvetica",
    fontSize=9,
    leading=11,
    textColor=GRAY,
    alignment=TA_LEFT,
)

BODY_GREEN = ParagraphStyle(
    "BODY_GREEN",
    parent=styles["BodyText"],
    fontName="Helvetica",
    fontSize=9,
    leading=11,
    textColor=GREEN,
    alignment=TA_LEFT,
)

SMALL = ParagraphStyle(
    "SMALL",
    parent=styles["BodyText"],
    fontName="Helvetica",
    fontSize=8,
    leading=10,
    textColor=GRAY,
    alignment=TA_LEFT,
)

SMALL_CENTER = ParagraphStyle(
    "SMALL_CENTER",
    parent=styles["BodyText"],
    fontName="Helvetica",
    fontSize=8,
    leading=10,
    textColor=GRAY,
    alignment=TA_CENTER,
)

CARD_LABEL = ParagraphStyle(
    "CARD_LABEL",
    parent=styles["BodyText"],
    fontName="Helvetica-Bold",
    fontSize=9,
    leading=10,
    textColor=CREAM,
    alignment=TA_LEFT,
)

CARD_VALUE = ParagraphStyle(
    "CARD_VALUE",
    parent=styles["BodyText"],
    fontName="Helvetica",
    fontSize=9,
    leading=11,
    textColor=CREAM,
    alignment=TA_LEFT,
)

TABLE_HEADER = ParagraphStyle(
    "TABLE_HEADER",
    parent=styles["BodyText"],
    fontName="Helvetica-Bold",
    fontSize=8.2,
    leading=9,
    textColor=colors.white,
    alignment=TA_CENTER,
)

TABLE_CELL = ParagraphStyle(
    "TABLE_CELL",
    parent=styles["BodyText"],
    fontName="Helvetica",
    fontSize=8.1,
    leading=9.2,
    textColor=GREEN,
    alignment=TA_LEFT,
)

TABLE_CELL_CENTER = ParagraphStyle(
    "TABLE_CELL_CENTER",
    parent=styles["BodyText"],
    fontName="Helvetica",
    fontSize=8.1,
    leading=9.2,
    textColor=GREEN,
    alignment=TA_CENTER,
)

TOTAL_LABEL = ParagraphStyle(
    "TOTAL_LABEL",
    parent=styles["BodyText"],
    fontName="Helvetica-Bold",
    fontSize=10,
    leading=12,
    textColor=GREEN,
    alignment=TA_LEFT,
)

TOTAL_VALUE = ParagraphStyle(
    "TOTAL_VALUE",
    parent=styles["BodyText"],
    fontName="Helvetica-Bold",
    fontSize=10,
    leading=12,
    textColor=GREEN,
    alignment=TA_RIGHT,
)


# =========================================================
# ENTRADA DE DATOS
# =========================================================
# Aquí empieza el flujo interactivo del programa.
# El usuario responde preguntas desde la terminal y con eso
# se construye toda la información de la cotización.
# =========================================================

print("\n" + "=" * 52)
print("  CALYPSO TEXTILE STUDIO - GENERADOR DE COTIZACIÓN")
print("=" * 52 + "\n")

company_name = ask_str("Nombre de la marca", "Calypso Textile Studio")
slogan = ask_str("Slogan", "Creamos piezas que cuentan historias.")
website = ask_str("Sitio web", "calypsotex.com")
email = ask_str("Correo", "info@calypsotex.com")
phone = ask_str("Teléfono", "+502 1234 5678")
instagram = ask_str("Instagram", "@calypsotextile")
address = ask_str("Dirección o ubicación", "Ciudad de Guatemala, Guatemala")

logo_path = ask_str("Ruta del logo (Enter si no usarás logo)", "", allow_empty=True)

quote_no = ask_str("Número de cotización", f"COT-{datetime.now().strftime('%Y-%m%d-%H%M')}")
issue_date = ask_str("Fecha de emisión", datetime.now().strftime("%d/%m/%Y"))
expiry_date = ask_str("Fecha de vencimiento", ask_str("Fecha de vencimiento", "", allow_empty=True))

client_name = ask_str("Nombre del cliente")
client_phone = ask_str("Teléfono del cliente", "", allow_empty=True)
client_email = ask_str("Correo del cliente", "", allow_empty=True)
client_location = ask_str("Ubicación del cliente", "", allow_empty=True)

num_items = ask_int("¿Cuántos productos deseas agregar?", 1)

items = []
for i in range(num_items):
    print(f"\n--- Producto #{i + 1} ---")
    product_name = ask_str("Nombre de la prenda")
    description = ask_str("Descripción / tela / gramaje", "", allow_empty=True)
    technique = ask_str("Técnica", "", allow_empty=True)
    color = ask_str("Color", "", allow_empty=True)
    qty = ask_int("Cantidad", 1)
    unit_price = ask_float("Precio unitario", 0.0)

    items.append({
        "no": f"{i + 1:02d}",
        "name": product_name,
        "description": description,
        "technique": technique,
        "color": color,
        "qty": qty,
        "unit_price": unit_price,
    })

discount_percent = ask_float("Descuento porcentual (ej. 5 para 5%)", 0.0)
shipping = ask_float("Costo de envío", 0.0)
notes = ask_str(
    "Notas finales",
    "Tiempo de entrega sujeto a confirmación. Precios sujetos a disponibilidad.",
    allow_empty=True
)


# =========================================================
# CÁLCULOS
# =========================================================
#
# En esta parte hacemos la matemática automática:
# - Subtotal
# - Descuento
# - Total final
#
# Esto evita que el usuario tenga que calcular manualmente.
# =========================================================

subtotal = sum(item["qty"] * item["unit_price"] for item in items)
discount_amount = subtotal * (discount_percent / 100)
total = subtotal - discount_amount + shipping


# =========================================================
# CONSTRUCCIÓN DEL PDF
# =========================================================
#
# Esta función toma toda la información obtenida
# y la transforma en un documento PDF profesional.
# =========================================================

def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=15 * mm,
        rightMargin=15 * mm,
        topMargin=14 * mm,
        bottomMargin=14 * mm,
        title=f"Cotización {quote_no}",
        author=company_name,
        subject="Cotización de prendas personalizadas",
    )

    story = []

    # -----------------------------------------------------
    # ENCABEZADO SUPERIOR
    # -----------------------------------------------------
    #
    # Se compone del nombre de la empresa a la izquierda
    # y del logo / slogan a la derecha.
    # -----------------------------------------------------

    brand_left = Paragraph(
        f"<font size=24 face='Times-Roman'>{safe_text(company_name.upper())}</font><br/>"
        f"<font size=9>{safe_text('TEXTILE STUDIO')}</font>",
        TITLE,
    )

    brand_right_content = []
    if file_exists(logo_path):
        brand_right_content.append(Image(logo_path, width=22 * mm, height=22 * mm))
        brand_right_content.append(Spacer(1, 2))
    else:
        brand_right_content.append(Paragraph("<b>C</b>", ParagraphStyle(
            "LOGO",
            parent=styles["BodyText"],
            fontName="Times-Roman",
            fontSize=18,
            textColor=GREEN,
            alignment=TA_CENTER,
            leading=18,
        )))

    brand_right_content.append(Paragraph(
        safe_text(slogan.upper()),
        ParagraphStyle(
            "SLOGAN",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=8.5,
            leading=10,
            textColor=GREEN,
            alignment=TA_CENTER,
        )
    ))

    right_table = Table([[brand_right_content]], colWidths=[65 * mm])
    right_table.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))

    header = Table([[brand_left, right_table]], colWidths=[92 * mm, 65 * mm])
    header.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(header)
    story.append(Spacer(1, 8 * mm))

    # -----------------------------------------------------
    # TÍTULO DE LA COTIZACIÓN Y BLOQUE DE FECHAS
    # -----------------------------------------------------
    #
    # Aquí se destaca el número de cotización,
    # la fecha de emisión y la fecha de vencimiento.
    # -----------------------------------------------------

    title_left = [
        Paragraph("COTIZACIÓN", TITLE),
        Paragraph(f"No. <font color='{GOLD.hexval()}'> {safe_text(quote_no)}</font>", SUBTITLE),
        Spacer(1, 2 * mm),
        Paragraph(
            f"<font color='{GREEN.hexval()}'><b>Gracias por confiar en {safe_text(company_name)}.</b></font><br/>"
            f"Esta cotización presenta el detalle solicitado y puede ajustarse a tu proyecto.",
            BODY,
        ),
    ]

    date_card = Table([
        [Paragraph("FECHA", CARD_LABEL)],
        [Paragraph(safe_text(issue_date), CARD_VALUE)],
        [Spacer(1, 1)],
        [Paragraph("VÁLIDA HASTA", CARD_LABEL)],
        [Paragraph(safe_text(expiry_date or "—"), CARD_VALUE)],
    ], colWidths=[55 * mm])
    date_card.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), GREEN_DARK),
        ("BOX", (0, 0), (-1, -1), 0, GREEN_DARK),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))

    title_table = Table([[title_left, date_card]], colWidths=[100 * mm, 57 * mm])
    title_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(title_table)
    story.append(Spacer(1, 8 * mm))

    # -----------------------------------------------------
    # DATOS DEL CLIENTE
    # -----------------------------------------------------
    #
    # Este bloque resume quién es el cliente y
    # cómo contactarlo, para que la cotización quede formal.
    # -----------------------------------------------------

    client_lines = []
    client_lines.append(Paragraph("DATOS DEL CLIENTE", SECTION))
    client_lines.append(Spacer(1, 2 * mm))

    client_data = []
    if client_name:
        client_data.append(Paragraph(f"<b>Nombre:</b> {safe_text(client_name)}", BODY_GREEN))
    if client_phone:
        client_data.append(Paragraph(f"<b>Teléfono:</b> {safe_text(client_phone)}", BODY_GREEN))
    if client_email:
        client_data.append(Paragraph(f"<b>Correo:</b> {safe_text(client_email)}", BODY_GREEN))
    if client_location:
        client_data.append(Paragraph(f"<b>Ubicación:</b> {safe_text(client_location)}", BODY_GREEN))

    if not client_data:
        client_data.append(Paragraph("Sin datos del cliente.", BODY_GREEN))

    client_block = [Paragraph("DATOS DEL CLIENTE", SECTION)] + client_data

    message_block = [
        Paragraph("GRACIAS POR CONFIAR EN CALYPSO TEXTILE STUDIO.", SECTION),
        Spacer(1, 2 * mm),
        Paragraph(
            "Nos emociona poder ser parte de tu proyecto. "
            "A continuación encontrarás el detalle de la cotización solicitada.",
            BODY,
        )
    ]

    info_table = Table([[client_block, message_block]], colWidths=[79 * mm, 76 * mm])
    info_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 8 * mm))

    # -----------------------------------------------------
    # TABLA DE PRODUCTOS
    # -----------------------------------------------------
    #
    # Esta es una de las partes más importantes:
    # muestra cada producto con cantidad, precio y subtotal.
    # -----------------------------------------------------

    table_data = [[
        Paragraph("NO.", TABLE_HEADER),
        Paragraph("DESCRIPCIÓN", TABLE_HEADER),
        Paragraph("TÉCNICA", TABLE_HEADER),
        Paragraph("COLOR", TABLE_HEADER),
        Paragraph("CANTIDAD", TABLE_HEADER),
        Paragraph("P. UNITARIO", TABLE_HEADER),
        Paragraph("SUBTOTAL", TABLE_HEADER),
    ]]

    for item in items:
        line_subtotal = item["qty"] * item["unit_price"]

        desc_parts = [f"<b>{safe_text(item['name']).upper()}</b>"]
        if item["description"]:
            desc_parts.append(safe_text(item["description"]).replace("\n", "<br/>"))
        desc = "<br/>".join(desc_parts)

        technique = safe_text(item["technique"]).replace("\n", "<br/>") if item["technique"] else "—"
        color = safe_text(item["color"]) if item["color"] else "—"

        table_data.append([
            Paragraph(safe_text(item["no"]), TABLE_CELL_CENTER),
            Paragraph(desc, TABLE_CELL),
            Paragraph(technique, TABLE_CELL),
            Paragraph(color, TABLE_CELL),
            Paragraph(str(item["qty"]), TABLE_CELL_CENTER),
            Paragraph(money_q(item["unit_price"]), TABLE_CELL_CENTER),
            Paragraph(money_q(line_subtotal), TABLE_CELL_CENTER),
        ])

    products_table = Table(
        table_data,
        colWidths=[10 * mm, 43 * mm, 28 * mm, 24 * mm, 18 * mm, 24 * mm, 25 * mm],
        repeatRows=1,
    )
    products_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), GREEN),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.4, LIGHT_GRAY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [CREAM, colors.white]),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("ALIGN", (4, 1), (-1, -1), "CENTER"),
    ]))
    story.append(products_table)
    story.append(Spacer(1, 8 * mm))

    # -----------------------------------------------------
    # NOTAS Y RESUMEN FINANCIERO
    # -----------------------------------------------------
    #
    # Las notas explican condiciones generales de trabajo.
    # El resumen muestra subtotales, descuentos y total final.
    # -----------------------------------------------------

    notes_list = [
        "Tiempo de entrega: 10 a 15 días hábiles.",
        "50% de anticipo para iniciar producción.",
        "Precios sujetos a disponibilidad y cambios de material.",
        "Esta cotización no incluye modificaciones posteriores a la aprobación.",
    ]

    notes_text = "<br/>".join([f"• {safe_text(n)}" for n in notes_list])
    if notes:
        notes_text += f"<br/>• {safe_text(notes)}"

    notes_box = [
        Paragraph("NOTAS", SECTION),
        Spacer(1, 2 * mm),
        Paragraph(notes_text, BODY),
    ]

    summary_rows = [
        [Paragraph("SUBTOTAL", TOTAL_LABEL), Paragraph(money_q(subtotal), TOTAL_VALUE)],
        [Paragraph("DESCUENTO", TOTAL_LABEL), Paragraph(f"-{money_q(discount_amount)} ({discount_percent:.0f}%)", TOTAL_VALUE)],
        [Paragraph("ENVÍO", TOTAL_LABEL), Paragraph(money_q(shipping), TOTAL_VALUE)],
    ]

    summary_table = Table(summary_rows, colWidths=[34 * mm, 38 * mm])
    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CREAM),
        ("BOX", (0, 0), (-1, -1), 0.7, LINE),
        ("LINEABOVE", (0, 0), (-1, 0), 0.5, LINE),
        ("LINEABOVE", (0, 1), (-1, 1), 0.5, LINE),
        ("LINEABOVE", (0, 2), (-1, 2), 0.5, LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))

    total_bar = Table([[Paragraph("TOTAL", TOTAL_LABEL), Paragraph(money_q(total), TOTAL_VALUE)]],
                      colWidths=[34 * mm, 38 * mm])
    total_bar.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BEIGE),
        ("BOX", (0, 0), (-1, -1), 0.7, GOLD),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))

    summary_right = [summary_table, Spacer(1, 2 * mm), total_bar]

    bottom_table = Table([[notes_box, summary_right]], colWidths=[87 * mm, 68 * mm])
    bottom_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(bottom_table)
    story.append(Spacer(1, 10 * mm))

    # -----------------------------------------------------
    # FIRMA Y PIE DE PÁGINA
    # -----------------------------------------------------
    #
    # Esta parte cierra el documento con un estilo formal.
    # También incluye los datos de contacto de la empresa.
    # -----------------------------------------------------

    sig_data = [
        Paragraph("Atentamente,", BODY_GREEN),
        Spacer(1, 2 * mm),
        Paragraph(f"<font face='Times-Italic' size='16'>{safe_text(company_name)}</font>", BODY_GREEN),
        Spacer(1, 2 * mm),
        Table([[""]], colWidths=[52 * mm], rowHeights=[1.2 * mm], style=TableStyle([
            ("LINEABOVE", (0, 0), (-1, -1), 0.8, LIGHT_GOLD),
        ]))
    ]

    footer_left = Paragraph(
        f"{safe_text(website)} &nbsp;&nbsp;&nbsp; {safe_text(email)} &nbsp;&nbsp;&nbsp; {safe_text(phone)}",
        SMALL
    )
    footer_right = Paragraph(
        safe_text(instagram),
        SMALL
    )

    footer_table = Table([[footer_left, footer_right]], colWidths=[120 * mm, 35 * mm])
    footer_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LINEABOVE", (0, 0), (-1, -1), 0.7, LINE),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]))

    sig_table = Table([[sig_data, footer_table]], colWidths=[78 * mm, 77 * mm])
    sig_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(sig_table)

    def on_page(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(CREAM)
        canvas.rect(0, 0, A4[0], A4[1], stroke=0, fill=1)

        # curvas suaves decorativas
        canvas.setStrokeColor(LIGHT_GRAY)
        canvas.setLineWidth(14)
        try:
            canvas.setStrokeAlpha(0.20)
        except Exception:
            pass
        canvas.circle(A4[0] * 0.77, A4[1] * 1.01, 95, stroke=1, fill=0)
        canvas.circle(A4[0] * 0.80, A4[1] * 0.95, 120, stroke=1, fill=0)
        try:
            canvas.setStrokeAlpha(1)
        except Exception:
            pass

        # línea inferior
        canvas.setStrokeColor(LINE)
        canvas.setLineWidth(0.7)
        canvas.line(15 * mm, 12 * mm, A4[0] - 15 * mm, 12 * mm)

        canvas.setFillColor(GREEN)
        canvas.setFont("Helvetica", 8)
        canvas.drawString(15 * mm, 8 * mm, website)
        canvas.drawCentredString(A4[0] / 2, 8 * mm, email)
        canvas.drawRightString(A4[0] - 15 * mm, 8 * mm, phone)
        canvas.restoreState()

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)


# =========================================================
# GENERAR EL ARCHIVO FINAL
# =========================================================
#
# El nombre del PDF se limpia para evitar caracteres raros.
# Después se llama a build_pdf() para crear la cotización.
# =========================================================

filename = f"cotizacion_{sanitize_filename(quote_no)}.pdf"
build_pdf(filename)

print(f"\nPDF generado correctamente: {filename}")

# =========================================================
# GUÍA DE USO PARA EL PROFESOR / AL EJECUTAR EL ARCHIVO
# =========================================================
#
# 1. Instalar dependencias:
#    pip install reportlab
#
# 2. Ejecutar el script:
#    python nombre_del_archivo.py
#
# 3. El programa pedirá datos por la terminal:
#    - Datos de la empresa
#    - Datos del cliente
#    - Productos
#    - Cantidades
#    - Precios
#    - Descuento
#    - Envío
#    - Notas
#
# 4. Cuando el usuario termine de responder,
#    el programa calculará automáticamente:
#    - Subtotal
#    - Descuento
#    - Total final
#
# 5. Después generará un PDF llamado:
#    cotizacion_"numero".pdf
#
# 6. El archivo quedará guardado en la misma carpeta
#    donde se ejecutó el script.
#
# 7. Si el usuario desea personalizar el PDF:
#    - Puede cambiar el logo
#    - Puede modificar colores
#    - Puede agregar más productos
#    - Puede cambiar notas y datos de la empresa
#
# 8. Este flujo demuestra cómo el programa trabaja:
#    entrada de datos -> cálculos -> creación del PDF.
#
# =========================================================
