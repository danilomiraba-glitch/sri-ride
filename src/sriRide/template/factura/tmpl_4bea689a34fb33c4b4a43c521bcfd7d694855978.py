from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'anexo_remision.html'

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
    l_0_remision = resolve('remision')
    pass
    if environment.getattr((undefined(name='anexos') if l_0_anexos is missing else l_0_anexos), 'guiaRemision'):
        pass
        yield '\n<div class="ride-page new-page" id="anexo-1">\n  <div class="corner-tr"></div>\n  <div class="corner-br"></div>\n  <div class="cabecera-mini">\n    <div class="mini-logo">\n      <div class="logo-box">\n        '
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
        yield '</span>\n      <span class="mini-ref-label" style="margin-top:3pt;">Clave de Acceso</span>\n      <div class="barcode-section">\n        <img src="data:image/svg+xml;base64,__BARCODE__" alt="Código de Barras SRI" class="barcode-svg">\n      </div>\n    </div>\n  </div>\n  <div class="anexo-seccion-header">\n    <div class="anx-numero">A'
        yield escape(environment.getattr((undefined(name='anexo') if l_0_anexo is missing else l_0_anexo), 'index'))
        yield '</div>\n    <div class="anx-info">\n      <div class="anx-titulo">Información Sustitutiva Guía de Remisión</div>\n      <div class="anx-subtitulo">\n       Reglamento Comprobantes SRI · Documento complementario que acredita el traslado lícito de mercadería.\n      </div>\n    </div>\n  </div>\n  <div class="anx-referencia-banda">\n    <div class="anx-ref-item">\n      <span class="anx-ref-label">Comprobante Origen</span>\n      <span class="anx-ref-value">Factura N° '
        yield escape(environment.getattr((undefined(name='doc') if l_0_doc is missing else l_0_doc), 'numero'))
        yield '</span>\n    </div>\n    <div class="anx-ref-item">\n      <span class="anx-ref-label">Fecha Emisión</span>\n      <span class="anx-ref-value">'
        yield escape(environment.getattr((undefined(name='cliente') if l_0_cliente is missing else l_0_cliente), 'fecha_emision'))
        yield '</span>\n    </div>\n    <div class="anx-ref-item">\n      <span class="anx-ref-label">Emisor</span>\n      <span class="anx-ref-value">'
        yield escape(environment.getattr((undefined(name='emisor') if l_0_emisor is missing else l_0_emisor), 'razon_social'))
        yield ' · RUC '
        yield escape(environment.getattr((undefined(name='doc') if l_0_doc is missing else l_0_doc), 'ruc'))
        yield '</span>\n    </div>\n    <div class="anx-ref-item">\n      <span class="anx-ref-label">Clave de Acceso</span>\n      <span class="anx-ref-value" style="font-size:7pt;letter-spacing:0.2pt;">'
        yield escape(environment.getattr((undefined(name='doc') if l_0_doc is missing else l_0_doc), 'clave_acceso'))
        yield '</span>\n    </div>\n  </div>\n  <div class="guia-grid">\n    <div class="guia-item">\n      <div class="guia-label">Dirección de Partida</div>\n      <div class="guia-value">'
        yield escape(environment.getattr((undefined(name='remision') if l_0_remision is missing else l_0_remision), 'partida'))
        yield '</div>\n    </div>\n    <div class="guia-item">\n      <div class="guia-label">Dirección Destinatario</div>\n      <div class="guia-value">'
        yield escape(environment.getattr((undefined(name='remision') if l_0_remision is missing else l_0_remision), 'destinatario'))
        yield '</div>\n    </div>\n    <div class="guia-item">\n      <div class="guia-label">Placa Vehículo</div>\n      <div class="guia-value">'
        yield escape(environment.getattr((undefined(name='remision') if l_0_remision is missing else l_0_remision), 'placa'))
        yield '</div>\n    </div>\n    <div class="guia-item">\n      <div class="guia-label">Transportista</div>\n      <div class="guia-value">'
        yield escape(environment.getattr((undefined(name='remision') if l_0_remision is missing else l_0_remision), 'transportista'))
        yield '</div>\n    </div>\n    <div class="guia-item">\n      <div class="guia-label">RUC Transportista</div>\n      <div class="guia-value">'
        yield escape(environment.getattr((undefined(name='remision') if l_0_remision is missing else l_0_remision), 'ruc_transportista'))
        yield '</div>\n    </div>\n    <div class="guia-item">\n      <div class="guia-label">Período de Transporte</div>\n      <div class="guia-value">'
        yield escape(environment.getattr((undefined(name='remision') if l_0_remision is missing else l_0_remision), 'inicio_transporte'))
        yield ' → '
        yield escape(environment.getattr((undefined(name='remision') if l_0_remision is missing else l_0_remision), 'fin_transporte'))
        yield '</div>\n    </div>\n  </div>\n  <div class="anx-subseccion">\n    <div class="anx-subseccion-header">Detalle de Destinos / Tramos</div>\n    <div class="guia-destinos">\n      <table class="t-destinos">\n        <thead>\n          <tr>\n            <th>#</th>\n            <th>Motivo de Traslado</th>\n            <th>Doc. Aduanero Único</th>\n            <th>Cód. Estab. Destino</th>\n            <th>Ruta</th>\n          </tr>\n        </thead>\n        <tbody>\n          '
        for l_1_destino_item in environment.getattr(environment.getattr((undefined(name='anexos') if l_0_anexos is missing else l_0_anexos), 'guiaRemision'), 'destinos'):
            _loop_vars = {}
            pass
            yield '\n          <tr>\n            <td class="c">'
            yield escape(environment.getattr(l_1_destino_item, 'numero'))
            yield '</td>\n            <td>'
            yield escape(environment.getattr(l_1_destino_item, 'motivo_traslado'))
            yield '</td>\n            <td>'
            yield escape(environment.getattr(l_1_destino_item, 'doc_aduanero'))
            yield '</td>\n            <td class="c">'
            yield escape(environment.getattr(l_1_destino_item, 'cod_establecimiento_destino'))
            yield '</td>\n            <td>'
            yield escape(environment.getattr(l_1_destino_item, 'ruta_destino'))
            yield '</td>\n          </tr>\n          '
        l_1_destino_item = missing
        yield '\n        </tbody>\n      </table>\n    </div>\n  </div>\n  <div class="anx-footer">\n    <span>Base legal: Art. 27–37 Reglamento Comprobantes de Venta, Retención y Docs. Complementarios (SRI) · Vigencia: desde fecha de emisión hasta entrega final</span>\n    <span><strong>Anexo '
        yield escape(environment.getattr((undefined(name='anexo') if l_0_anexo is missing else l_0_anexo), 'index'))
        yield ' de '
        yield escape(environment.getattr((undefined(name='anexo') if l_0_anexo is missing else l_0_anexo), 'total'))
        yield '</strong> · Factura N° '
        yield escape(environment.getattr((undefined(name='doc') if l_0_doc is missing else l_0_doc), 'numero'))
        yield '</span>\n  </div>\n</div>\n'

blocks = {}
debug_info = '1=18&8=21&9=24&16=30&18=32&22=36&30=38&41=40&45=42&49=44&53=48&59=50&63=52&67=54&71=56&75=58&79=60&96=64&98=68&99=70&100=72&101=74&102=76&111=80'