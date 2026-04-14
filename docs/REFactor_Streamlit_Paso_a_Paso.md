# Plan de refactorización total de Streamlit (sin perder comportamiento)

## Objetivo
Mantener **todas** las consultas, formularios, cálculos y pantallas tal como funcionan hoy, pero rediseñar la estructura para:

- reducir duplicación,
- centralizar conexiones a base de datos,
- endurecer seguridad SQL,
- facilitar mantenimiento y pruebas,
- mejorar rendimiento de carga.

---

## Hallazgos del estado actual (resumen técnico)

Levantamiento rápido del repositorio (29 módulos Python) muestra alta repetición de patrones de UI y datos:

- 183 llamadas a `pd.read_sql(...)` distribuidas en múltiples pantallas.
- 22 inserciones SQL construidas con `f"..."` (riesgo de inyección y errores por comillas).
- 195 usos de `st.sidebar.empty()` con lógica repetitiva de limpieza de placeholders.
- Flujo principal con estado manual y navegación por botones, muy acoplado entre módulos.

Comando de auditoría usado:

```bash
python - <<'PY'
import glob,re
files=glob.glob('*.py')
metrics=[]
for f in files:
    t=open(f,encoding='utf-8').read()
    metrics.append((f,t.count('pd.read_sql('),t.count('cursor'),len(re.findall(r'execute\(f"',t)),t.count('st.sidebar.empty()')))
print('files',len(files))
print('total read_sql',sum(m[1] for m in metrics))
print('total execute f"',sum(m[3] for m in metrics))
print('total sidebar.empty',sum(m[4] for m in metrics))
PY
```

---

## Arquitectura objetivo (propuesta)

```text
app/
  main.py                   # entrypoint Streamlit
  config/
    settings.py             # secretos, constantes, zonas horarias
  core/
    session.py              # estado y navegación
    routing.py              # registro de pantallas/procesos
  db/
    connection.py           # pool + helpers transaccionales
    queries.py              # consultas parametrizadas reutilizables
    repositories/
      usuarios_repo.py
      registro_repo.py
      historial_repo.py
  services/
    auth_service.py
    reporte_service.py
    historial_service.py
  ui/
    layout.py               # sidebar común, footer, estilos
    components.py           # inputs reutilizables
    pages/
      ingreso.py
      procesos.py
      precampo.py
      ...
  tests/
    test_repositories.py
    test_services.py
    test_regression_smoke.py
```

---

## Paso a paso recomendado (orden seguro)

### Fase 0 — Congelamiento funcional (baseline)
1. Documentar flujos críticos por perfil (1, 2 y 3), empezando desde `Ingreso.py` y `Procesos.py`.
2. Definir “escenarios de no regresión” para cada formulario (campos, validaciones, inserción esperada).
3. Tomar muestra de datos de salida de tablas clave (`registro`, `capacitaciones`, `otros_registros`, `correcciones`) para comparar antes/después.

### Fase 1 — Capa de base de datos única
1. Crear `db/connection.py` con una sola factoría de conexión cacheada (`st.cache_resource`) y API única para lectura/escritura.
2. Extraer credenciales y parsing de URI fuera de pantallas (hoy está disperso; base en `Autenticacion.py`).
3. Definir helpers:
   - `fetch_df(sql, params)`
   - `fetch_one(sql, params)`
   - `execute(sql, params)`
   - `execute_many(sql, rows)`

### Fase 2 — Parametrizar SQL (sin tocar negocio)
1. Reemplazar TODO `execute(f"INSERT ... {valor} ...")` por placeholders `%s`.
2. Reemplazar `read_sql(f"SELECT ... '{usuario}'")` por consultas parametrizadas.
3. Mantener exactamente mismas columnas y reglas de mapeo para no afectar BI.

### Fase 3 — Repositorios por dominio
1. Crear repositorios por tabla/proceso:
   - `usuarios_repo` (credenciales, perfil, supervisor, nombre),
   - `registro_repo` (insert de reportes),
   - `correcciones_repo`, `capacitaciones_repo`, etc.
2. Cada pantalla deja de conocer SQL crudo; solo llama métodos del repositorio.
3. Agregar tipado básico con `dataclass` para payloads de inserción.

### Fase 4 — Servicios de negocio
1. Crear `auth_service` para login, validación y carga de contexto de usuario.
2. Crear `reporte_service` para reglas transversales repetidas: `marca`, `semana`, `año`, `horas_bi`, defaults (`N/A`, `0`).
3. Centralizar transformaciones que se repiten en múltiples pantallas.

### Fase 5 — Navegación y estado
1. Sustituir inicialización manual de decenas de banderas `st.session_state.X = False` por una estructura única:
   - `session_state.current_page`
   - `session_state.user_context`
2. Implementar un router (`routing.py`) con mapa `page_id -> handler`.
3. Reducir limpieza manual de placeholders con layout reutilizable.

### Fase 6 — Componentes UI reutilizables
1. Extraer sidebar común (Procesos/Historial/Capacitaciones/Otros/Bonos/Salir).
2. Crear componentes de formulario repetidos (fecha, distrito, sector, tipo, estado, observaciones, horas).
3. Estandarizar mensajes de éxito/error y validaciones mínimas de campos.

### Fase 7 — Optimización de rendimiento
1. Cachear catálogos estáticos (`distrito`, `sector`, `manzana`, listas fijas).
2. Evitar lecturas repetidas de usuario (`nombre`, `perfil`, `supervisor`) dentro de una misma sesión.
3. Consolidar consultas del historial cuando sea posible (menos roundtrips).

### Fase 8 — Pruebas y no regresión
1. Pruebas unitarias a repositorios (query + parámetros).
2. Pruebas de servicios (reglas de negocio, defaults y cálculos).
3. Smoke tests de cada módulo principal con dataset de prueba.
4. Checklist UAT con usuarios clave antes de desplegar.

### Fase 9 — Despliegue por oleadas
1. Migración módulo por módulo (no big bang).
2. Feature flag por página (nueva versión activable por proceso).
3. Monitoreo de errores + rollback rápido por módulo.

---

## Priorización sugerida (impacto alto primero)

1. **Autenticación + contexto usuario** (`Ingreso.py`, `Autenticacion.py`).
2. **Módulos de captura de mayor volumen** (`Precampo.py`, `Postcampo.py`, `FMI.py`, `CC_*`).
3. **Historial y reportes** (`Historial.py`, `Bonos_Extras.py`).
4. **Módulos secundarios** (`Capacitacion.py`, `Otros_Registros.py`, `Correcciones.py`).

---

## Riesgos a controlar

- Cambios en nombres/orden de columnas de inserción.
- Diferencias de timezone (`America/Guatemala`) en `marca` y fechas.
- Dependencia implícita de defaults tipo `N/A`, `0`, `P0`.
- Acoplamiento entre navegación y estados globales.

Mitigación: refactor por capas, pruebas de snapshot SQL y validación funcional por proceso.

---

## ¿Es posible hacerlo sin perder lo actual?

Sí, **es totalmente posible**, siempre que se haga incrementalmente y con estrategia de no-regresión. La clave es:

1. primero encapsular datos,
2. luego mover SQL,
3. luego mover UI/estado,
4. y recién al final optimizar fuerte.

Con este orden, los módulos pueden seguir operando como hoy mientras modernizas internamente.
