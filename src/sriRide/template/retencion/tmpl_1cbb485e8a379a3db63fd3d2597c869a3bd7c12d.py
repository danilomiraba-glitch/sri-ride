from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'retencion.html'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_assets = resolve('assets')
    l_0_doc = resolve('doc')
    l_0_emisor = resolve('emisor')
    l_0_sujeto_retenido = resolve('sujeto_retenido')
    l_0_deatalle_documentos = resolve('deatalle_documentos')
    l_0_info_adicional = resolve('info_adicional')
    pass
    yield '\ufeff<div class="ride-page" id="pagina-principal">\n  <div class="corner-tr"></div>\n  <div class="corner-br"></div>\n  <div class="cabecera">\n    <div class="cab-logo">\n      <div class="logo-box">\n        '
    if ((undefined(name='assets') if l_0_assets is missing else l_0_assets) and environment.getattr((undefined(name='assets') if l_0_assets is missing else l_0_assets), 'logo_png_b64')):
        pass
        yield '\n        <img src="data:image/png;base64,'
        yield escape(environment.getattr((undefined(name='assets') if l_0_assets is missing else l_0_assets), 'logo_png_b64'))
        yield '" alt="Logo Emisor" class="logo-img">\n        '
    else:
        pass
        yield '\n        <span class="logo-placeholder">Logo<br>Emisor</span>\n        '
    yield '\n      </div>\n    </div>\n    <div class="cab-doc">\n      <div class="cab-doc-top">\n        <h1>RUC: '
    yield escape(environment.getattr((undefined(name='doc') if l_0_doc is missing else l_0_doc), 'ruc'))
    yield '</h1>\n        <span class="tipo-doc">Comprobante de Retención</span>\n        <span class="ambiente-badge">N° '
    yield escape(environment.getattr((undefined(name='doc') if l_0_doc is missing else l_0_doc), 'numero'))
    yield '</span>\n      </div>\n      <div class="cab-doc-meta">\n        <div class="meta-item">\n          <span class="meta-label">Fecha y Hora de Autorización</span>\n          <span class="meta-value">'
    yield escape(environment.getattr((undefined(name='doc') if l_0_doc is missing else l_0_doc), 'fecha_autorizacion'))
    yield '</span>\n        </div>\n        <div class="meta-item">\n          <span class="meta-label">Clave de Acceso</span>\n          <span class="meta-value">'
    yield escape(environment.getattr((undefined(name='doc') if l_0_doc is missing else l_0_doc), 'clave_acceso'))
    yield '</span>\n        </div>\n        <div class="meta-item">\n          <span class="meta-label">Tipo de Emisión - Ambiente</span>\n          <span class="meta-value">'
    yield escape(environment.getattr((undefined(name='doc') if l_0_doc is missing else l_0_doc), 'tipo_emision'))
    yield ' - '
    yield escape(environment.getattr((undefined(name='doc') if l_0_doc is missing else l_0_doc), 'ambiente'))
    yield '</span>\n        </div>\n        <div class="barcode-section">\n    <img src="data:image/svg+xml;base64,__BARCODE__" alt="Código de Barras SRI" class="barcode-svg">\n        </div>\n        <div class="meta-item full-width">\n          <span class="meta-label">Número de autorización</span>\n          <span class="meta-value">'
    yield escape(environment.getattr((undefined(name='doc') if l_0_doc is missing else l_0_doc), 'numero_autorizacion'))
    yield '</span>\n        </div>\n      </div>\n      <div class="badges-tributarios">\n        '
    if environment.getattr((undefined(name='doc') if l_0_doc is missing else l_0_doc), 'cntrbynte_esp'):
        pass
        yield '\n        <span class="badge-trib destacado">Contribuyente Especial Nro. '
        yield escape(environment.getattr((undefined(name='doc') if l_0_doc is missing else l_0_doc), 'cntrbynte_esp'))
        yield '</span>\n        '
    yield '\n        '
    if environment.getattr((undefined(name='doc') if l_0_doc is missing else l_0_doc), 'agent_retencn'):
        pass
        yield '\n        <span class="badge-trib agente">Agente de Retención Nro. '
        yield escape(environment.getattr((undefined(name='doc') if l_0_doc is missing else l_0_doc), 'agent_retencn'))
        yield '</span>\n        '
    yield '\n      </div>\n    </div>\n  </div>\n  <div class="partes">\n    <div class="parte">\n      <span class="parte-label">'
    yield escape(environment.getattr((undefined(name='emisor') if l_0_emisor is missing else l_0_emisor), 'nombre_comercial'))
    yield '</span>\n      <table>\n        <tr><td>Razón Social</td><td>'
    yield escape(environment.getattr((undefined(name='emisor') if l_0_emisor is missing else l_0_emisor), 'razon_social'))
    yield '</td></tr>\n        <tr><td>Dir. Matriz</td><td>'
    yield escape(environment.getattr((undefined(name='emisor') if l_0_emisor is missing else l_0_emisor), 'direccion'))
    yield '</td></tr>\n        <tr><td>Dir. Establecimiento</td><td>'
    yield escape(environment.getattr((undefined(name='emisor') if l_0_emisor is missing else l_0_emisor), 'direccion_estab'))
    yield '</td></tr>\n        <tr><td>Regimén</td><td>'
    yield escape(environment.getattr((undefined(name='emisor') if l_0_emisor is missing else l_0_emisor), 'regimen'))
    yield '</td></tr>\n        <tr><td>Obligado a contabilidad</td><td>'
    yield escape(environment.getattr((undefined(name='emisor') if l_0_emisor is missing else l_0_emisor), 'obligado_contabilidad'))
    yield '</td></tr>\n      </table>\n    </div>\n    <div class="parte">\n      <span class="parte-label">Sujeto de Retención</span>\n      <table>\n        <tr><td>Identificación</td><td>'
    yield escape(environment.getattr((undefined(name='sujeto_retenido') if l_0_sujeto_retenido is missing else l_0_sujeto_retenido), 'identificacion'))
    yield '</td></tr>\n        <tr><td>Razón Social/Nombre y apellido</td><td>'
    yield escape(environment.getattr((undefined(name='sujeto_retenido') if l_0_sujeto_retenido is missing else l_0_sujeto_retenido), 'razon_social'))
    yield '</td></tr>\n        <tr><td>Fecha de Emisión</td><td>'
    yield escape(environment.getattr((undefined(name='sujeto_retenido') if l_0_sujeto_retenido is missing else l_0_sujeto_retenido), 'fecha_emision'))
    yield '</td></tr>\n      </table>\n    </div>\n  </div>\n    <div class="seccion-header">\n      <h2>Documentos</h2>\n    </div>\n    '
    for l_1_item in environment.getitem((undefined(name='deatalle_documentos') if l_0_deatalle_documentos is missing else l_0_deatalle_documentos), 'items'):
        _loop_vars = {}
        pass
        yield '\n    <div data-tpl-repeat="retencion.items">\n      <div class="anexo-seccion-header">\n       <div class="anx-info">\n        <div class="anx-titulo">Documento</div>\n       </div>\n      </div>\n      <div class="anx-referencia-banda">\n      <div class="anx-ref-item">\n        <span class="anx-ref-label">Comprobante</span>\n        <span class="anx-ref-value">'
        yield escape(environment.getattr(l_1_item, 'tipo_documento'))
        yield '</span>\n      </div>\n      <div class="anx-ref-item">\n        <span class="anx-ref-label">Fecha Emisión</span>\n        <span class="anx-ref-value">'
        yield escape(environment.getattr(l_1_item, 'fecha_emision_docsustento'))
        yield '</span>\n      </div>\n      <div class="anx-ref-item">\n        <span class="anx-ref-label">Numero de Autorización</span>\n        <span class="anx-ref-value">'
        yield escape(environment.getattr(l_1_item, 'numero_autorizacion'))
        yield '</span>\n      </div>\n    </div>\n    <div class="anx-subseccion">\n      <div class="anx-subseccion-header">Detalles</div>\n      <div class="guia-destinos">\n        <table class="t-destinos">\n          <thead>\n            <tr>\n              <th>Ejercicio Fiscal</th>\n              <th>Impuesto</th>\n              <th>base imponible para la retencion</th>\n              <th>Porcentaje Retencion</th>\n              <th>Valor Retenido</th>\n            </tr>\n          </thead>\n          <tbody>\n            '
        t_1 = 1
        for l_2_ret in environment.getattr(l_1_item, 'detalle_retencion'):
            _loop_vars = {}
            pass
            yield '\n              <tr>\n                <td class="c">'
            yield escape(environment.getattr(l_1_item, 'ejercicio_fiscal'))
            yield '</td>\n                <td>'
            yield escape(environment.getattr(l_2_ret, 'codigo'))
            yield '</td>\n                <td>'
            yield escape(environment.getattr(l_2_ret, 'base_imponible_retencion'))
            yield '</td>\n                <td>'
            yield escape(environment.getattr(l_2_ret, 'porcentaje_retencion'))
            yield '</td>\n                <td class="c">'
            yield escape(environment.getattr(l_2_ret, 'valor_retencion'))
            yield '</td>\n              </tr>\n            '
            t_1 = 0
        l_2_ret = missing
        if t_1:
            pass
            yield '\n              <tr>\n                <td class="c">---</td>\n                <td>Sin detalles</td>\n                <td>---</td>\n                <td class="c"></td>\n              </tr>\n            '
        yield '\n          </tbody>\n        </table>\n      </div>\n    </div>\n    </div>\n    '
    l_1_item = missing
    yield '  \n    <div class="clave-subpanel bloque-opcional" id="bloque-info-adicional">\n        <span class="clave-titulo">Información Adicional</span>\n        <div class="info-adicional-grid">\n          '
    for l_1_campo in environment.getattr((undefined(name='info_adicional') if l_0_info_adicional is missing else l_0_info_adicional), 'campos'):
        _loop_vars = {}
        pass
        yield '\n          <div class="info-adic-item">\n            <span class="info-adic-value">'
        yield escape(environment.getattr(l_1_campo, 'campo_adicional'))
        yield '</span>\n          </div>\n          '
    l_1_campo = missing
    yield '\n        </div>\n      </div>\n  <div class="aviso-legal">\n    DOCUMENTO AUTORIZADO – \n    Este documento es una representación gráfica de un comprobante electrónico. \n    La validez de este comprobante puede ser consultada en el portal oficial del SRI, \n    mediante la clave de acceso detallada en este documento.</div>\n</div>'

blocks = {}
debug_info = '7=18&8=21&16=27&18=29&23=31&27=33&31=35&38=39&42=41&43=44&45=47&46=50&53=53&55=55&56=57&57=59&58=61&59=63&65=65&66=67&67=69&74=71&84=75&88=77&92=79&109=82&111=86&112=88&113=90&114=92&115=94&134=104&136=108'