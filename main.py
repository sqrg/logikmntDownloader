import csv
import os

import bs4
import requests

from urllib.parse import urlparse

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen        import canvas

ALTO, ANCHO = A4

CANT_TEMAS = 12

URL_TEMPLATE = 'https://www.logikamente.com.ar/cache.php?url=_temas_b/b_{}_{}.jpg'

def downloadImage(folder_name, file_name, image_content):

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    full_path = '{}/{}.jpg'.format(folder_name, file_name)

    with open(full_path, 'wb') as image:
        image.write(image_content)

    print('Imagen descargada con exito: {}'.format(full_path))

for nro in range(1, CANT_TEMAS + 1):

    nro_tema = '{:02}'.format(nro)

    error = False

    nro_pagina = 1

    c = canvas.Canvas(nro_tema + '.pdf', pagesize=A4)

    while not error:

        nro_pagina_text = '{:02}'.format(nro_pagina)

        r = requests.get(URL_TEMPLATE.format(nro_tema, nro_pagina_text))

        if r.content == b'':

            c.save()

            error = True

        else:

            downloadImage(nro_tema, nro_pagina_text, r.content)

            c.drawImage('{}/{}.jpg'.format(nro_tema, nro_pagina_text), 0, 0, ALTO, ANCHO)
            c.showPage()

            nro_pagina += 1
