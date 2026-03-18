# Aranti — catalogo.aranti.mx
## Guía de despliegue y actualización trimestral

---

## ESTRUCTURA DE ARCHIVOS

```
aranti-catalogo/
├── index.html          ← Visor público del catálogo (clientes)
├── catalogo.pdf        ← ⬅ REEMPLAZAR cada temporada
├── admin/
│   └── index.html      ← Herramienta interna (equipo)
└── INSTRUCCIONES.md
```

---

## PRIMERA VEZ — CONFIGURAR catalogo.aranti.mx

### Paso 1 — Crear cuenta en Netlify (gratis)
1. Ve a https://netlify.com
2. Crea cuenta con tu email (Google o email directo)
3. Ya en el dashboard, haz clic en **"Add new site" → "Deploy manually"**

### Paso 2 — Subir la carpeta
1. Coloca el PDF del catálogo dentro de la carpeta como `catalogo.pdf`
2. Arrastra la carpeta `aranti-catalogo` completa al área de deploy de Netlify
3. Netlify te da una URL tipo: `random-name.netlify.app` — ya está live

### Paso 3 — Conectar tu dominio
1. En Netlify: **Site configuration → Domain management → Add custom domain**
2. Escribe: `catalogo.aranti.mx` → confirmar
3. Netlify te indica que agregues un registro DNS

### Paso 4 — Agregar el registro DNS
En el panel donde administras tu dominio (Shopify Domains, GoDaddy, etc.):
- Tipo: `CNAME`
- Nombre / Host: `catalogo`
- Valor / Points to: `[tu-sitio].netlify.app`
- TTL: 3600 (o default)

Espera 5–30 minutos y listo. Netlify activa SSL automáticamente.

---

## CADA TEMPORADA — Actualizar el catálogo

### Paso 1 — Reemplazar el PDF
- Nombra el nuevo PDF exactamente: `catalogo.pdf`
- Reemplaza el archivo en la carpeta

### Paso 2 — Actualizar la base de datos del admin
Abre `admin/index.html` en un editor de texto y actualiza:
- El array `RAW` con los nuevos productos
- El objeto `SKU_DB` con los SKUs conocidos
- El título de la temporada (busca "Primavera 26'" y cambia a la nueva)

> Si prefieres que Claude haga esto automáticamente, comparte el PDF o
> Google Doc del nuevo catálogo y pide: "Actualiza el admin para [temporada]"

### Paso 3 — Redesplegar en Netlify
1. Ve a tu sitio en Netlify
2. **Deploys → drag & drop** la carpeta actualizada
3. En 30 segundos el sitio está actualizado

---

## USO DEL ADMIN

**URL:** `catalogo.aranti.mx/admin`
**Contraseña:** `aranti2026`

### Flujo de revisión
1. Selecciona una sección en el panel izquierdo
2. Verifica cada producto:
   - Si tiene SKU correcto → **Aprobar**
   - Si el SKU está en blanco → escríbelo y luego **Aprobar**
   - Si el producto no aplica esta temporada → **Omitir**
3. Usa el filtro **"Sin SKU"** para ir directo a los productos que faltan
4. Al terminar, descarga los CSVs

### Exportar
- **CSV para Google Sheets** → pega en la hoja "Base" de BD_Claude.xlsx
- **CSV para Shopify** → importa en Shopify Admin → Products → Import

### Nota sobre los datos guardados
El admin guarda el progreso en el navegador (localStorage).
Cada persona del equipo ve su propio progreso en su dispositivo.
Para sincronizar: una persona hace la revisión completa y exporta los CSVs.

---

## CONTACTO Y SOPORTE

- WhatsApp Aranti: +52 56 2484 5101
- Email: ventas@aranti.mx
- Tienda: aranti.mx

---
*Generado por Claude para Aranti · Primavera 26'*
