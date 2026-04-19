from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'anexo_exportador.html'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_anexos = resolve('anexos')
    l_0_assets = resolve('assets')
    l_0_anexo = resolve('anexo')
    l_0_emisor = resolve('emisor')
    l_0_doc = resolve('doc')
    l_0_cliente = resolve('cliente')
    l_0_exportador = resolve('exportador')
    pass
    if environment.getattr((undefined(name='anexos') if l_0_anexos is missing else l_0_anexos), 'exportacion'):
        pass
        yield '\n<div class="ride-page new-page" id="anexo-2">\n  <div class="corner-tr"></div>\n  <div class="corner-br"></div>\n  <!-- Cabecera mini -->\n  <div class="cabecera-mini">\n    <div class="mini-logo">\n      <div class="logo-box">\n        '
        if ((undefined(name='assets') if l_0_assets is missing else l_0_assets) and environment.getattr((undefined(name='assets') if l_0_assets is missing else l_0_assets), 'logo_png_b64')):
            pass
            yield '\n        <img src="data:image/png;base64,'
            yield escape(environment.getattr((undefined(name='assets') if l_0_assets is missing else l_0_assets), 'logo_png_b64'))
            yield '" alt="Logo Emisor" class="logo-img">\n        '
        else:
            pass
            yield '\n        <span class="logo-placeholder">Logo<br>Emisor</span>\n        '
        yield '\n      </div>\n    </div>\n    <div class="mini-doc">\n      <span class="anexo-tag">Anexo '
        yield escape(environment.getattr((undefined(name='anexo') if l_0_anexo is missing else l_0_anexo), 'index'))
        yield '</span>\n      <span class="mini-title">Factura</span>\n      <span class="mini-subtitle">'
        yield escape(environment.getattr((undefined(name='emisor') if l_0_emisor is missing else l_0_emisor), 'razon_social'))
        yield ' · RUC '
        yield escape(environment.getattr((undefined(name='doc') if l_0_doc is missing else l_0_doc), 'ruc'))
        yield '</span>\n    </div>\n    <div class="mini-ref">\n      <span class="mini-ref-label">Factura N°</span>\n      <span class="mini-ref-value">'
        yield escape(environment.getattr((undefined(name='doc') if l_0_doc is missing else l_0_doc), 'numero'))
        yield '</span>\n      <div class="barcode-section">\n    <img src="data:image/svg+xml;base64,__BARCODE__" alt="Código de Barras SRI" class="barcode-svg">\n        </div>\n    </div>\n  </div>\n  <div class="anexo-seccion-header">\n    <div class="anx-numero">A'
        yield escape(environment.getattr((undefined(name='anexo') if l_0_anexo is missing else l_0_anexo), 'index'))
        yield '</div>\n    <div class="anx-info">\n      <div class="anx-titulo">Datos de Exportación / Comercio Exterior</div>\n      <div class="anx-subtitulo">\n        Tarifa 0% IVA en exportaciones · El valor de gastos de exportación referenciados en la factura corresponden a este anexo\n      </div>\n    </div>\n  </div>\n  <div class="anx-referencia-banda">\n    <div class="anx-ref-item">\n      <span class="anx-ref-label">Comprobante Origen</span>\n      <span class="anx-ref-value">Factura N° '
        yield escape(environment.getattr((undefined(name='doc') if l_0_doc is missing else l_0_doc), 'numero'))
        yield '</span>\n    </div>\n    <div class="anx-ref-item">\n      <span class="anx-ref-label">Fecha Emisión</span>\n      <span class="anx-ref-value">'
        yield escape(environment.getattr((undefined(name='cliente') if l_0_cliente is missing else l_0_cliente), 'fecha_emision'))
        yield '</span>\n    </div>\n    <div class="anx-ref-item">\n      <span class="anx-ref-label">Emisor (Exportador)</span>\n      <span class="anx-ref-value">'
        yield escape(environment.getattr((undefined(name='emisor') if l_0_emisor is missing else l_0_emisor), 'razon_social'))
        yield ' · RUC '
        yield escape(environment.getattr((undefined(name='doc') if l_0_doc is missing else l_0_doc), 'ruc'))
        yield '</span>\n    </div>\n    <div class="anx-ref-item">\n      <span class="anx-ref-label">Clave de Acceso</span>\n      <span class="anx-ref-value" style="font-size:7pt;letter-spacing:0.2pt;">'
        yield escape(environment.getattr((undefined(name='doc') if l_0_doc is missing else l_0_doc), 'clave_acceso'))
        yield '</span>\n    </div>\n  </div>\n  <div class="exportacion-grid">\n    <div class="exp-item">\n      <div class="exp-label">Tipo Comercio Exterior</div>\n      <div class="exp-value">EXPORTADOR</div>\n    </div>\n    <div class="exp-item">\n      <div class="exp-label">IncoTerm Factura</div>\n      <div class="exp-value">'
        yield escape(environment.getattr((undefined(name='exportador') if l_0_exportador is missing else l_0_exportador), 'icoterm'))
        yield '</div>\n    </div>\n    <div class="exp-item">\n      <div class="exp-label">Lugar IncoTerm</div>\n      <div class="exp-value">'
        yield escape(environment.getattr((undefined(name='exportador') if l_0_exportador is missing else l_0_exportador), 'lugar_icoterm'))
        yield '</div>\n    </div>\n    <div class="exp-item">\n      <div class="exp-label">País de Origen</div>\n      <div class="exp-value">'
        yield escape(environment.getattr((undefined(name='exportador') if l_0_exportador is missing else l_0_exportador), 'pais_origen'))
        yield '</div>\n    </div>\n    <div class="exp-item">\n      <div class="exp-label">Puerto de Embarque</div>\n      <div class="exp-value">'
        yield escape(environment.getattr((undefined(name='exportador') if l_0_exportador is missing else l_0_exportador), 'puerto_embarque'))
        yield '</div>\n    </div>\n    <div class="exp-item">\n      <div class="exp-label">Puerto de Destino</div>\n      <div class="exp-value">'
        yield escape(environment.getattr((undefined(name='exportador') if l_0_exportador is missing else l_0_exportador), 'puerto_destino'))
        yield '</div>\n    </div>\n    <div class="exp-item">\n      <div class="exp-label">País Destino</div>\n      <div class="exp-value">'
        yield escape(environment.getattr((undefined(name='exportador') if l_0_exportador is missing else l_0_exportador), 'pais_destino'))
        yield '</div>\n    </div>\n    <div class="exp-item">\n      <div class="exp-label">País Adquisición</div>\n      <div class="exp-value">'
        yield escape(environment.getattr((undefined(name='exportador') if l_0_exportador is missing else l_0_exportador), 'pais_adquisicion'))
        yield '</div>\n    </div>\n    <div class="exp-item">\n      <div class="exp-label">IncoTerm Total s/Imp.</div>\n      <div class="exp-value">'
        yield escape(environment.getattr((undefined(name='exportador') if l_0_exportador is missing else l_0_exportador), 'incoterm_total'))
        yield '</div>\n    </div>\n  </div>\n  <div class="anx-subseccion">\n    <div class="anx-subseccion-header">Desglose de Gastos de Exportación (referenciados en la Factura)</div>\n    <div class="anx-gastos-exportacion">\n      '
        for l_1_gasto in environment.getattr(environment.getattr((undefined(name='anexos') if l_0_anexos is missing else l_0_anexos), 'exportacion'), 'gastos'):
            _loop_vars = {}
            pass
            yield '\n      <div class="anx-gasto-item">\n        <div class="anx-gasto-label">'
            yield escape(environment.getattr(l_1_gasto, 'etiqueta'))
            yield '</div>\n        <div class="anx-gasto-value">$'
            yield escape(environment.getattr(l_1_gasto, 'valor'))
            yield '</div>\n      </div>\n      '
        l_1_gasto = missing
        yield '\n    </div>\n  </div>\n  <div class="anx-footer">\n    <span><strong>'
        yield escape(environment.getattr((undefined(name='anexo') if l_0_anexo is missing else l_0_anexo), 'index'))
        yield ' de '
        yield escape(environment.getattr((undefined(name='anexo') if l_0_anexo is missing else l_0_anexo), 'total'))
        yield '</strong> · Factura N° '
        yield escape(environment.getattr((undefined(name='doc') if l_0_doc is missing else l_0_doc), 'numero'))
        yield '</span>\n  </div>\n</div>\n'

blocks = {}
debug_info = '1=18&9=21&10=24&17=30&19=32&23=36&30=38&41=40&45=42&49=44&53=48&63=50&67=52&71=54&75=56&79=58&83=60&87=62&91=64&97=66&99=70&100=72&106=76'