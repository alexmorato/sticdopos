GENERAR manifest de los apuntes.
PS D:\GIT\alex\sticdopos> python .\apunts_new\generate_manifest.py .\apunts_new\
Manifest generado correctamente: apunts_new/manifest.json

Paser word a Markdown
URL: https://word2md.com/

Corregir header, para que los headers sean secuenciales.
PS D:\GIT\alex\sticdopos> python .\assets\python\retocar_md.py .\apunts_new\T12\T12-Apunts-Xavi.md --corregirHeaders

Poner numeros a los headers. Se pone el primer numero del word origen.
PS D:\GIT\alex\sticdopos> python .\assets\python\retocar_md.py .\apunts_new\T12\T12-Apunts-Xavi.md 12.1

Añadir el TOC table of content
PS D:\GIT\alex\sticdopos> python .\assets\python\retocar_md.py .\apunts_new\T12\T12-Apunts-Xavi.md --toc
Fichero actualizado: D:\GIT\alex\sticdopos\apunts_new\T12\T12-Apunts-Xavi.md


--------------------------------------
Convertir JPG a webp
Si es JPG tiene el fondo no transparente.
https://cloudconvert.com/webp-converter

Copia la URL del preview y te vas a:
https://base64.guru/converter/encode/image/webp

Con este validas: https://base64.guru/converter/decode/image

esto en el .md
![grafic1](data:image/webp;base64,xxxxxxxxxxxx)