Un arranque de navegador totalmente en frio puede tardar hasta 10 segundos.

el archivo test_render.py simula un pool (arranca el navegador antes de llamar a la librería) te dan métricas de cuanto tarda el arranque del navegador y cuanto tarda en procesar un documento ya con el navegador activo.

el archivo sin_pdf.py mide lo mismo en la librería pero sin navegador ya que solo se procesa HTML. sirve para medir cuanto es el tiempo desde la entrada de datos hasta HTML y cuanto es el tiempo desde el flujo del HTML hacia pdf.

con la librería y el navegador instalado abre consola desde esta carpeta y ejecuta Python test_render.py o Python sin_pdf.py