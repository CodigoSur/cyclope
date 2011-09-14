# -*- coding: utf-8 -*-
gettext("""Es aquí donde utilizaremos las vistas asociadas que describimos en el punto anterior. Podemos decidir, por ejemplo, que en la región lateral izquierda se muestre una lista jerarquizada de las categorías pertenecientes a una colección, en la región superior se muestre un menú de navegación y en la barra lateral izquierda un listado de resúmenes de los contenidos de la categoría “Destacados”.""")
# -*- coding: utf-8 -*-
gettext("""!(left)/media/uploads/manual_cyclope_3/logica/5-elements.png(alt_text)!""")
# -*- coding: utf-8 -*-
gettext("""!(left)/media/uploads/manual_cyclope_3/logica/water-left.png(alt_text)!""")
# -*- coding: utf-8 -*-
gettext("""En Cyclope podemos utilizar diferentes esquemas para las diferentes secciones de nuestro sitio web, aunque el caso más común, que viene pre-configurado, es tener un esquema para la portada (o página de inicio) y otro para el resto del sitio web.""")
# -*- coding: utf-8 -*-
gettext("""h3. Qué son las Regiones""")
# -*- coding: utf-8 -*-
gettext("""Las Regiones están configuradas en un archivo llamado __init__.py de la carpeta donde se guardan los HTML de nuestro sitio. Nos permiten definir la cantidad de regiones que podrá tener nuestro sitio web. Cada Región se invoca dentro de los archivos HTML de nuestro Tema. En el caso de Neutrona Theme, la configuración de las regiones se ve así:""")
# -*- coding: utf-8 -*-
gettext("""bc. # *-- coding:utf-8 --*@""")
# -*- coding: utf-8 -*-
gettext("""\"\"Configuration for the Neutrona theme templates and regions.""")
# -*- coding: utf-8 -*-
gettext("""Attributes:""")
# -*- coding: utf-8 -*-
gettext("""verbose_name: name of theme to be displayed in the admin interface""")
# -*- coding: utf-8 -*-
gettext("""layout_templates: dictionary defining regions for the available templates""")
# -*- coding: utf-8 -*-
gettext("""\"\"\"""")
# -*- coding: utf-8 -*-
gettext("""from django.utils.translation import ugettext_lazy as _""")
# -*- coding: utf-8 -*-
gettext("""verbose_name = _('Neutrona')""")
# -*- coding: utf-8 -*-
gettext("""layout_templates = {""")
# -*- coding: utf-8 -*-
gettext("""'4_elements.html':""")
# -*- coding: utf-8 -*-
gettext("""{""")
# -*- coding: utf-8 -*-
gettext("""'verbose_name': _('4 Elements'),""")
# -*- coding: utf-8 -*-
gettext("""'regions' : {""")
# -*- coding: utf-8 -*-
gettext("""'air': _('air'),""")
# -*- coding: utf-8 -*-
gettext("""'water': _('water'),""")
# -*- coding: utf-8 -*-
gettext("""'before_fire': _('before fire'),""")
# -*- coding: utf-8 -*-
gettext("""'after_fire': _('after fire'),""")
# -*- coding: utf-8 -*-
gettext("""'earth': _('earth'),""")
# -*- coding: utf-8 -*-
gettext("""}""")
# -*- coding: utf-8 -*-
gettext("""},""")
# -*- coding: utf-8 -*-
gettext("""'5_elements.html':""")
# -*- coding: utf-8 -*-
gettext("""{""")
# -*- coding: utf-8 -*-
gettext("""'verbose_name': _('5 Elements'),""")
# -*- coding: utf-8 -*-
gettext("""'regions' : {""")
# -*- coding: utf-8 -*-
gettext("""'air': _('air'),""")
# -*- coding: utf-8 -*-
gettext("""'water': _('water'),""")
# -*- coding: utf-8 -*-
gettext("""'love': _('love'),""")
# -*- coding: utf-8 -*-
gettext("""'before_fire': _('before fire'),""")
# -*- coding: utf-8 -*-
gettext("""'after_fire': _('after fire'),""")
# -*- coding: utf-8 -*-
gettext("""'earth': _('earth'),""")
# -*- coding: utf-8 -*-
gettext("""}""")
# -*- coding: utf-8 -*-
gettext("""},""")
# -*- coding: utf-8 -*-
gettext("""'empty.html':""")
# -*- coding: utf-8 -*-
gettext("""{'verbose_name': _('Empty'),""")
# -*- coding: utf-8 -*-
gettext("""'regions': {}""")
# -*- coding: utf-8 -*-
gettext("""},""")
# -*- coding: utf-8 -*-
gettext("""'newsletter.html':""")
# -*- coding: utf-8 -*-
gettext("""{'verbose_name': _('Newsletter'),""")
# -*- coding: utf-8 -*-
gettext("""'regions' : {""")
# -*- coding: utf-8 -*-
gettext("""'header': _('header'),""")
# -*- coding: utf-8 -*-
gettext("""'before_content': _('before content'),""")
# -*- coding: utf-8 -*-
gettext("""'after_content': _('after content'),""")
# -*- coding: utf-8 -*-
gettext("""}""")
# -*- coding: utf-8 -*-
gettext("""},""")
# -*- coding: utf-8 -*-
gettext("""}""")
# -*- coding: utf-8 -*-
gettext("""Definir las Regiones de nuestro sitio en el documento de configuración __init_.py, nos permite poder definir por medio de la opción Esquemas, las vistas que queremos que se vean en cada región del sitio. Neutrona Theme, viene con regiones creadas por defecto que cubrirán la mayor cantidad de usos. Es por eso que te recomendamos no cambiar esta información salvo que realmente sepas lo que estás haciendo.""")
# -*- coding: utf-8 -*-
gettext("""h3. Qué son los Esquemas""")
# -*- coding: utf-8 -*-
gettext("""Los esquemas nos permiten generar “vistas” dentro de las regiones de nuestro sitio web, para cada tipo contenido creado, sean artículos, páginas, Bloques HTML, Colecciones, Categorías, Menús, Contactos, audios, videos, etc., etc.""")
# -*- coding: utf-8 -*-
gettext("""Por ejemplo podemos crear un Esquema que en la región “Agua” (Water) se muestre una lista jerarquizada de las categorías pertenecientes a una colección, en la región “Aire” (Air) se muestre un menú de navegación y en la región “Amor” (Love) se visualice un listado de resúmenes de los contenidos de la categoría “Destacados”.""")
# -*- coding: utf-8 -*-
gettext("""Por defecto, Neutrona Theme usa dos Esquemas preconfigurados: 5-Elements y 4-Elements. 5-Elements es el esquema para la portada del sitio, mientras que 4-Elements, está utilizado como Esquema interior, o sea, Esquema por defecto en \"Configuración Global(Cyclope 3: Configuración Global)\":/configuracion-global.""")
# -*- coding: utf-8 -*-
gettext("""En Neutrona Theme existen una base de datos en /demo/db/sandbox.db que podrás renombrar a site.db para tener todas las vistas posibles las regiones de cada Esquema: 4-Elements-SandBox y 5-Elements-SandBox.""")
# -*- coding: utf-8 -*-
gettext("""Diviértete mirando todas las posibilidades actuales y aprender a configurar tus propios Esquemas.""")
