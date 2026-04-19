from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'anexo_reembolso.html'

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
    l_0_reembolso = resolve('reembolso')
    pass
    if (environment.getattr((undefined(name='anexos') if l_0_anexos is missing else l_0_anexos), 'reembolsos') and environment.getitem(environment.getattr((undefined(name='anexos') if l_0_anexos is missing else l_0_anexos), 'reembolsos'), 'items')):
        pass
        yield '\n<div class="ride-page new-page" id="anexo-3">\n  <div class="corner-tr"></div>\n  <div class="corner-br"></div>\n  <div class="cabecera-mini">\n    <div class="mini-logo">\n      <div class="logo-box">\n        '
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
        yield '</div>\n    <div class="anx-info">\n      <div class="anx-titulo">Detalle de Reembolsos</div>\n      <div class="anx-subtitulo">\n        El intermediario actúa como mandatario; los valores reembolsados no integran su base imponible de IVA\n      </div>\n    </div>\n  </div>\n  <div class="anx-referencia-banda">\n    <div class="anx-ref-item">\n      <span class="anx-ref-label">Comprobante Origen</span>\n      <span class="anx-ref-value">Factura N° '
        yield escape(environment.getattr((undefined(name='doc') if l_0_doc is missing else l_0_doc), 'numero'))
        yield '</span>\n    </div>\n    <div class="anx-ref-item">\n      <span class="anx-ref-label">Fecha Emisión</span>\n      <span class="anx-ref-value">'
        yield escape(environment.getattr((undefined(name='cliente') if l_0_cliente is missing else l_0_cliente), 'fecha_emision'))
        yield '</span>\n    </div>\n    <div class="anx-ref-item">\n      <span class="anx-ref-label">Intermediario</span>\n      <span class="anx-ref-value">'
        yield escape(environment.getattr((undefined(name='emisor') if l_0_emisor is missing else l_0_emisor), 'razon_social'))
        yield ' · RUC '
        yield escape(environment.getattr((undefined(name='doc') if l_0_doc is missing else l_0_doc), 'ruc'))
        yield '</span>\n    </div>\n    <div class="anx-ref-item">\n      <span class="anx-ref-label">Clave de Acceso</span>\n      <span class="anx-ref-value" style="font-size:7pt;letter-spacing:0.2pt;">'
        yield escape(environment.getattr((undefined(name='doc') if l_0_doc is missing else l_0_doc), 'clave_acceso'))
        yield '</span>\n    </div>\n  </div>\n  <div class="reembolsos-wrap">\n    <table class="t-reembolso">\n      <thead>\n        <tr>\n          <th>RUC Proveedor</th>\n          <th>No. Documento</th>\n          <th>F. Emisión</th>\n          <th>Clave de Acceso</th>\n          <th class="r">Sub. T</th>\n          <th class="r">Impuestos</th>\n          <th class="r">Total</th>\n        </tr>\n      </thead>\n      <tbody>\n        '
        for l_1_item in environment.getitem(environment.getattr((undefined(name='anexos') if l_0_anexos is missing else l_0_anexos), 'reembolsos'), 'items'):
            _loop_vars = {}
            pass
            yield '\n        <tr>\n          <td>'
            yield escape(environment.getattr(l_1_item, 'ruc_reembolso'))
            yield '</td>\n          <td>'
            yield escape(environment.getattr(l_1_item, 'numero_comprobante'))
            yield '</td>\n          <td>'
            yield escape(environment.getattr(l_1_item, 'fecha_emision'))
            yield '</td>\n          <td style="font-family:var(--font-cond);font-size:7.5pt;">'
            yield escape(environment.getattr(l_1_item, 'numero_autorizacion'))
            yield '</td>\n          <td class="r">$'
            yield escape(environment.getattr(l_1_item, 'subtotal_reembolso'))
            yield '</td>\n          <td class="r">'
            yield escape(environment.getattr(l_1_item, 'total_impuestos'))
            yield '</td>\n          <td class="r">$'
            yield escape(environment.getattr(l_1_item, 'total_reembolso'))
            yield '</td>\n        </tr>\n        '
        l_1_item = missing
        yield '\n      </tbody>\n    </table>\n    <div class="reembolso-totales">\n      <div class="remb-total-item">\n        <span class="remb-total-label">Total Comprobantes</span>\n        <span class="remb-total-val">'
        yield escape(environment.getattr((undefined(name='reembolso') if l_0_reembolso is missing else l_0_reembolso), 'total_comprobantes'))
        yield '</span>\n      </div>\n      <div class="remb-total-item">\n        <span class="remb-total-label">Total Base Imponible</span>\n        <span class="remb-total-val">$'
        yield escape(environment.getattr((undefined(name='reembolso') if l_0_reembolso is missing else l_0_reembolso), 'total_base_reembolsos'))
        yield '</span>\n      </div>\n      <div class="remb-total-item">\n        <span class="remb-total-label">Total IVA Reembolsado</span>\n        <span class="remb-total-val">$'
        yield escape(environment.getattr((undefined(name='reembolso') if l_0_reembolso is missing else l_0_reembolso), 'total_impuestos_reembolsos'))
        yield '</span>\n      </div>\n      <div class="remb-total-item">\n        <span class="remb-total-label">Total Reembolso</span>\n        <span class="remb-total-val">$'
        yield escape(environment.getattr((undefined(name='reembolso') if l_0_reembolso is missing else l_0_reembolso), 'total_todos_reembolsos'))
        yield '</span>\n      </div>\n    </div>\n  </div>\n  <div class="nota-anexos" style="margin: 0; border-top: 1pt solid var(--gray-mid); border-bottom: none;">\n    <span class="nota-icon">§</span>\n    <p>\n      Los valores de este anexo corresponden a gastos incurridos por cuenta del mandante y reembolsados al intermediario.\n      Dichos montos <strong>no forman parte de los ingresos gravables ni de la base imponible de IVA</strong> del intermediario.\n      El IVA pagado en dichos comprobantes es crédito tributario del mandante, no del intermediario.\n    </p>\n  </div>\n  <div class="anx-footer">\n    <span><strong>'
        yield escape(environment.getattr((undefined(name='anexo') if l_0_anexo is missing else l_0_anexo), 'index'))
        yield ' de '
        yield escape(environment.getattr((undefined(name='anexo') if l_0_anexo is missing else l_0_anexo), 'total'))
        yield '</strong> · Factura N° '
        yield escape(environment.getattr((undefined(name='doc') if l_0_doc is missing else l_0_doc), 'numero'))
        yield '</span>\n  </div>\n</div>\n'

blocks = {}
debug_info = '1=18&8=21&9=24&16=30&18=32&22=36&29=38&40=40&44=42&48=44&52=48&69=50&71=54&72=56&73=58&74=60&75=62&76=64&77=66&85=70&89=72&93=74&97=76&110=78'