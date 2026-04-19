from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'nota-credito.html'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_assets = resolve('assets')
    l_0_doc = resolve('doc')
    l_0_emisor = resolve('emisor')
    l_0_cliente = resolve('cliente')
    l_0_comprobante = resolve('comprobante')
    l_0_producto = resolve('producto')
    l_0_info_adicional = resolve('info_adicional')
    l_0_totales = resolve('totales')
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
    yield '</h1>\n        <span class="tipo-doc">Nota de Crédito</span>\n        <span class="ambiente-badge">N° '
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
    yield '\n      </div>\n    </div>\n  </div>\n  <div class="partes">\n    <div class="parte">\n      <span class="parte-label">Emisor</span>\n      <table>\n        <tr><td>Razón Social</td><td>'
    yield escape(environment.getattr((undefined(name='emisor') if l_0_emisor is missing else l_0_emisor), 'razon_social'))
    yield '</td></tr>\n        <tr><td>Dir. Matriz</td><td>'
    yield escape(environment.getattr((undefined(name='emisor') if l_0_emisor is missing else l_0_emisor), 'direccion'))
    yield '</td></tr>\n        <tr><td>Dir. Establecimiento</td><td>'
    yield escape(environment.getattr((undefined(name='emisor') if l_0_emisor is missing else l_0_emisor), 'direccion_estab'))
    yield '</td></tr>\n        <tr><td>Regimén</td><td>'
    yield escape(environment.getattr((undefined(name='emisor') if l_0_emisor is missing else l_0_emisor), 'regimen'))
    yield '</td></tr>\n        <tr><td>Obligado a contabilidad</td><td>'
    yield escape(environment.getattr((undefined(name='emisor') if l_0_emisor is missing else l_0_emisor), 'obligado_contabilidad'))
    yield '</td></tr>\n      </table>\n    </div>\n    <div class="parte">\n      <span class="parte-label">Cliente</span>\n      <table>\n        <tr><td>Razón Social/Nombre</td><td>'
    yield escape(environment.getattr((undefined(name='cliente') if l_0_cliente is missing else l_0_cliente), 'razon_social'))
    yield '</td></tr>\n        <tr><td>RUC / Cédula</td><td>'
    yield escape(environment.getattr((undefined(name='cliente') if l_0_cliente is missing else l_0_cliente), 'identificacion'))
    yield '</td></tr>\n        <tr><td>Fecha Emision</td><td>'
    yield escape(environment.getattr((undefined(name='cliente') if l_0_cliente is missing else l_0_cliente), 'fecha_emision'))
    yield '</td></tr>\n      </table>\n    </div>\n  </div>\n  <div class="anx-referencia-banda">\n    <div class="anx-ref-item">\n      <span class="anx-ref-label">Comprobante que se Modifica</span>\n      <span class="anx-ref-value">'
    yield escape(environment.getattr((undefined(name='comprobante') if l_0_comprobante is missing else l_0_comprobante), 'tipo_comprobante'))
    yield ' N° '
    yield escape(environment.getattr((undefined(name='comprobante') if l_0_comprobante is missing else l_0_comprobante), 'numero_comprobante'))
    yield '</span>\n    </div>\n    <div class="anx-ref-item">\n      <span class="anx-ref-label">Fecha Emisión (comprobante a modificar)</span>\n      <span class="anx-ref-value">'
    yield escape(environment.getattr((undefined(name='comprobante') if l_0_comprobante is missing else l_0_comprobante), 'fecha_comprobante'))
    yield '</span>\n    </div>\n    <div class="anx-ref-item">\n      <span class="anx-ref-label">Razon modificacion</span>\n      <span class="anx-ref-value">'
    yield escape(environment.getattr((undefined(name='comprobante') if l_0_comprobante is missing else l_0_comprobante), 'motivo'))
    yield '</span>\n    </div>\n  </div>\n  <div class="seccion detalle-seccion">\n    <div class="seccion-header">\n      <h2>Detalle de Productos / Servicios</h2>\n    </div>\n    <div class="seccion-body">\n      <table class="detalle">\n        <thead>\n          <tr>\n            <th style="width:38pt" class="c">Cód.</th>\n            <th>Descripción / Detalle</th>\n            <th class="r" style="width:58pt">Cant</th>\n            <th class="r" style="width:44pt">P.Unit</th>\n            <th class="r" style="width:44pt">Desc</th>\n            <th class="r" style="width:58pt">Total</th>\n          </tr>\n        </thead>\n        <tbody>\n          '
    for l_1_item in environment.getitem((undefined(name='producto') if l_0_producto is missing else l_0_producto), 'items'):
        _loop_vars = {}
        pass
        yield '\n          <tr>\n            <td class="c">\n              <div style="font-size:7.5pt;">'
        yield escape(environment.getattr(l_1_item, 'codigo'))
        yield '</div>\n            </td>\n            <td>\n              <div class="item-name">'
        yield escape(environment.getattr(l_1_item, 'descripcion'))
        yield '</div>\n              '
        if environment.getattr(l_1_item, 'detalle_adicional'):
            pass
            yield '\n              <div class="item-desc">'
            yield escape(environment.getattr(l_1_item, 'detalle_adicional'))
            yield '</div>\n              '
        yield '\n            </td>\n            <td class="r">'
        yield escape(environment.getattr(l_1_item, 'cantidad'))
        yield '</td>\n            <td class="r">$'
        yield escape(environment.getattr(l_1_item, 'precio_unitario'))
        yield '</td>\n            <td class="r">$'
        yield escape(environment.getattr(l_1_item, 'descuento'))
        yield '</td>\n            <td class="r">$'
        yield escape(environment.getattr(l_1_item, 'precio_total'))
        yield '</td>\n          </tr>\n          '
    l_1_item = missing
    yield '\n        </tbody>\n      </table>\n    </div>\n  </div>\n  <div class="bottom-zone">\n    <div class="clave-panel">\n      <div>\n        <div class="meta-label" style="margin-bottom:2pt;">Verifique en</div>\n        <div style="font-size:var(--sz-value1);font-weight:600;color:var(--dark);">\n          srienlinea.sri.gob.ec\n        </div>\n      </div>\n      <div class="clave-subpanel bloque-opcional" id="bloque-info-adicional">\n        <span class="clave-titulo">Información Adicional</span>\n        <div class="info-adicional-grid">\n          '
    for l_1_campo in environment.getattr((undefined(name='info_adicional') if l_0_info_adicional is missing else l_0_info_adicional), 'campos'):
        _loop_vars = {}
        pass
        yield '\n          <div class="info-adic-item">\n            <span class="info-adic-value">'
        yield escape(environment.getattr(l_1_campo, 'campo_adicional'))
        yield '</span>\n          </div>\n          '
    l_1_campo = missing
    yield '\n        </div>\n      </div>\n    </div>\n    <div class="totales-panel">\n      <div class="totales-row">\n        <span>Subtotal IVA 0%</span>\n        <span>$'
    yield escape(environment.getattr((undefined(name='totales') if l_0_totales is missing else l_0_totales), 'subtotal_iva_0'))
    yield '</span>\n      </div>\n      <div class="totales-row">\n        <span>Subtotal IVA 15%</span>\n        <span>$'
    yield escape(environment.getattr((undefined(name='totales') if l_0_totales is missing else l_0_totales), 'subtotal_iva_15'))
    yield '</span>\n      </div>\n      <div class="totales-row '
    yield escape(('oculto' if (not environment.getattr((undefined(name='totales') if l_0_totales is missing else l_0_totales), 'subtotal_iva_5')) else ''))
    yield '">\n        <span>Subtotal IVA 5%</span>\n        <span>$'
    yield escape((environment.getattr((undefined(name='totales') if l_0_totales is missing else l_0_totales), 'subtotal_iva_5') or ''))
    yield '</span>\n      </div>\n      <div class="totales-row">\n        <span>Subtotal No Obj / Exento IVA</span>\n        <span>$'
    yield escape(environment.getattr((undefined(name='totales') if l_0_totales is missing else l_0_totales), 'subtotal_objeto_exento'))
    yield '</span>\n      </div>\n      <div class="totales-row '
    yield escape(('oculto' if (not environment.getattr((undefined(name='totales') if l_0_totales is missing else l_0_totales), 'total_descuento')) else ''))
    yield '">\n        <span>Descuento</span>\n        <span>-$'
    yield escape(environment.getattr((undefined(name='totales') if l_0_totales is missing else l_0_totales), 'total_descuento'))
    yield '</span>\n      </div>\n      <div class="totales-row">\n        <span>Subtotal</span>\n        <span>$'
    yield escape(environment.getattr((undefined(name='totales') if l_0_totales is missing else l_0_totales), 'subtotal_general'))
    yield '</span>\n      </div>\n      <div class="totales-row '
    yield escape(('oculto' if (not environment.getattr((undefined(name='totales') if l_0_totales is missing else l_0_totales), 'total_iva_15')) else ''))
    yield '">\n        <span>IVA 15%</span>\n        <span>$'
    yield escape((environment.getattr((undefined(name='totales') if l_0_totales is missing else l_0_totales), 'total_iva_15') or ''))
    yield '</span>\n      </div>\n      <div class="totales-row '
    yield escape(('oculto' if (not environment.getattr((undefined(name='totales') if l_0_totales is missing else l_0_totales), 'total_iva_5')) else ''))
    yield '">\n        <span>Total IVA 5%</span>\n        <span>$'
    yield escape((environment.getattr((undefined(name='totales') if l_0_totales is missing else l_0_totales), 'total_iva_5') or ''))
    yield '</span>\n      </div>\n      <div class="totales-row '
    yield escape(('oculto' if (not environment.getattr((undefined(name='totales') if l_0_totales is missing else l_0_totales), 'total_ice')) else ''))
    yield '">\n        <span>Total ICE</span>\n        <span>'
    yield escape((environment.getattr((undefined(name='totales') if l_0_totales is missing else l_0_totales), 'total_ice') or ''))
    yield '</span>\n      </div>\n      <div class="totales-row total-final">\n        <span>Valor Total</span>\n        <span>$'
    yield escape(environment.getattr((undefined(name='totales') if l_0_totales is missing else l_0_totales), 'total'))
    yield '</span>\n      </div>\n    </div>\n  </div>\n  <div class="aviso-legal">\n    DOCUMENTO AUTORIZADO – \n    Este documento es una representación gráfica de un comprobante electrónico. \n    La validez de este comprobante puede ser consultada en el portal oficial del SRI, \n    mediante la clave de acceso detallada en este documento.</div>\n</div>'

blocks = {}
debug_info = '7=20&8=23&16=29&18=31&23=33&27=35&31=37&38=41&42=43&43=46&45=49&46=52&55=55&56=57&57=59&58=61&59=63&65=65&66=67&67=69&74=71&78=75&82=77&102=79&105=83&108=85&109=87&110=90&113=93&114=95&115=97&116=99&134=103&136=107&145=111&149=113&151=115&153=117&157=119&159=121&161=123&165=125&167=127&169=129&171=131&173=133&175=135&177=137&181=139'