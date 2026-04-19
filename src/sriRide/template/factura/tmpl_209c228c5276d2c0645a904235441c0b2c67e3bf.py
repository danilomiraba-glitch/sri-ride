from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'factura.html'

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
    l_0_producto = resolve('producto')
    l_0_pago = resolve('pago')
    l_0_anexos = resolve('anexos')
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
    yield '</h1>\n        <span class="tipo-doc">FACTURA</span>\n        <span class="ambiente-badge">N° '
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
    yield '</td></tr>\n        <tr><td>Dirección</td><td>'
    yield escape(environment.getattr((undefined(name='cliente') if l_0_cliente is missing else l_0_cliente), 'direccion'))
    yield '</td></tr>\n        <tr><td>Placa</td><td>'
    yield escape((environment.getattr((undefined(name='cliente') if l_0_cliente is missing else l_0_cliente), 'placa') or ''))
    yield '</td></tr>\n        <tr><td>Fecha Emision</td><td>'
    yield escape(environment.getattr((undefined(name='cliente') if l_0_cliente is missing else l_0_cliente), 'fecha_emision'))
    yield '</td></tr>\n        <!-- Si hay guía de remisión sustitutiva, referenciar número -->\n        <tr class="'
    yield escape(('oculto' if (not environment.getattr((undefined(name='cliente') if l_0_cliente is missing else l_0_cliente), 'guia_remision')) else ''))
    yield '"><td>Guía Remisión</td><td>'
    yield escape((environment.getattr((undefined(name='cliente') if l_0_cliente is missing else l_0_cliente), 'guia_remision') or ''))
    yield '</td></tr>\n      </table>\n    </div>\n  </div>\n  <div class="seccion detalle-seccion">\n    <div class="seccion-header">\n      <h2>Detalle de Productos / Servicios</h2>\n    </div>\n    <div class="seccion-body">\n      <table class="detalle">\n        <thead>\n          <tr>\n            <th style="width:38pt" class="c">Cód.</th>\n            <th>Descripción / Detalle</th>\n            <th class="c" style="width:38pt">U.Med</th>\n            <th class="r" style="width:58pt">Cant</th>\n            <th class="r" style="width:44pt">P.Unit</th>\n            <th class="r" style="width:44pt">Desc</th>\n            <th class="r" style="width:58pt">Total</th>\n          </tr>\n        </thead>\n        <tbody>\n          '
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
        yield '\n            </td>\n            <td class="c">'
        yield escape(environment.getattr(l_1_item, 'unidad_medida'))
        yield '</td>\n            <td class="r">'
        yield escape(environment.getattr(l_1_item, 'cantidad'))
        yield '</td>\n            <td class="r">$'
        yield escape(environment.getattr(l_1_item, 'precio_unitario'))
        yield '</td>\n            <td class="r">$'
        yield escape(environment.getattr(l_1_item, 'descuento'))
        yield '</td>\n            <td class="r">$'
        yield escape(environment.getattr(l_1_item, 'precio_total'))
        yield '</td>\n          </tr>\n          '
    l_1_item = missing
    yield '\n        </tbody>\n      </table>\n    </div>\n  </div>\n  <div class="grupo-final">\n  <div class="bottom-zone">\n    <div class="clave-panel">\n      '
    if environment.getattr((undefined(name='pago') if l_0_pago is missing else l_0_pago), 'formas'):
        pass
        yield '\n      <div class="bloque-formas-pago">\n  <div class="fp-header">\n    <div>Forma de pago</div>\n    <div>Valor</div>\n    <div>Plazo</div>\n    <div>Tiempo</div>\n  </div>\n  '
        for l_1_forma in environment.getattr((undefined(name='pago') if l_0_pago is missing else l_0_pago), 'formas'):
            _loop_vars = {}
            pass
            yield '\n  <div class="fp-row">\n    <div class="fp-col forma">'
            yield escape(environment.getattr(l_1_forma, 'forma_pago'))
            yield '</div>\n    <div class="fp-col valor">'
            yield escape(environment.getattr(l_1_forma, 'valor_pago'))
            yield '</div>\n    <div class="fp-col plazo">'
            yield escape(environment.getattr(l_1_forma, 'plazo'))
            yield '</div>\n    <div class="fp-col dias">'
            yield escape(environment.getattr(l_1_forma, 'unidad_tiempo'))
            yield '</div>\n  </div>\n  '
        l_1_forma = missing
        yield '\n</div>\n      '
    yield '\n      <div>\n        <div class="meta-label" style="margin-bottom:2pt;">Verifique en</div>\n        <div style="font-size:var(--sz-value1);font-weight:600;color:var(--dark);">\n          srienlinea.sri.gob.ec\n        </div>\n      </div>\n      '
    if environment.getattr((undefined(name='anexos') if l_0_anexos is missing else l_0_anexos), 'info'):
        pass
        yield '\n      <div>\n        <div class="meta-label" style="margin-bottom:2pt;">Anexos</div>\n        <div style="font-size:var(--sz-value1);font-weight:600;color:var(--dark);">\n          '
        yield escape(environment.getattr((undefined(name='anexos') if l_0_anexos is missing else l_0_anexos), 'info'))
        yield '\n        </div>\n      </div>\n      '
    yield '\n      <div class="clave-subpanel bloque-opcional" id="bloque-info-adicional">\n        <span class="clave-titulo">Información Adicional</span>\n        <div class="info-adicional-grid">\n          '
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
    yield '</span>\n      </div>\n      <div class="totales-row">\n        <span>Descuento</span>\n        <span>-$'
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
    yield '</span>\n      </div>\n      <div class="totales-row '
    yield escape(('oculto' if (not environment.getattr((undefined(name='totales') if l_0_totales is missing else l_0_totales), 'propina')) else ''))
    yield '">\n        <span>Propina</span>\n        <span>$'
    yield escape((environment.getattr((undefined(name='totales') if l_0_totales is missing else l_0_totales), 'propina') or ''))
    yield '</span>\n      </div>\n      <!-- Gastos de exportación: se muestra el total, el detalle está en Anexo 2 -->\n      <div class="totales-row '
    yield escape(('oculto' if (not environment.getattr((undefined(name='totales') if l_0_totales is missing else l_0_totales), 'gastos_exportacion')) else ''))
    yield '">\n        <span>Gastos Exportación<span class="ref-anexo">*</span></span>\n        <span>$'
    yield escape((environment.getattr((undefined(name='totales') if l_0_totales is missing else l_0_totales), 'gastos_exportacion') or ''))
    yield '</span>\n      </div>\n      <div class="totales-row total-final">\n        <span>Valor Total</span>\n        <span>$'
    yield escape(environment.getattr((undefined(name='totales') if l_0_totales is missing else l_0_totales), 'total'))
    yield '</span>\n      </div>\n    </div>\n  </div>\n  '
    if environment.getattr((undefined(name='anexos') if l_0_anexos is missing else l_0_anexos), 'has_anexos'):
        pass
        yield '\n  <div class="nota-anexos">\n    <span class="nota-icon">★</span>\n    <p>\n      <strong>(*) Detalles en los Anexos adjuntos:</strong>\n      Cada anexo identifica este comprobante por su Clave de Acceso:\n      <strong>'
        yield escape(environment.getattr((undefined(name='doc') if l_0_doc is missing else l_0_doc), 'clave_acceso'))
        yield '</strong>.\n    </p>\n  </div>\n  '
    yield '\n  <div class="aviso-legal">\n    DOCUMENTO AUTORIZADO – \n    Este documento es una representación gráfica de un comprobante electrónico. \n    La validez de este comprobante puede ser consultada en el portal oficial del SRI, \n    mediante la clave de acceso detallada en este documento.</div>\n</div>\n</div>'

blocks = {}
debug_info = '7=21&8=24&16=30&18=32&23=34&27=36&31=38&38=42&42=44&43=47&45=50&46=53&55=56&56=58&57=60&58=62&59=64&65=66&66=68&67=70&68=72&69=74&71=76&93=80&96=84&99=86&100=88&101=91&104=94&105=96&106=98&107=100&108=102&118=106&126=109&128=113&129=115&130=117&131=119&142=124&146=127&153=130&155=134&164=138&168=140&170=142&172=144&176=146&180=148&184=150&186=152&188=154&190=156&192=158&194=160&196=162&198=164&200=166&203=168&205=170&209=172&213=174&219=177'