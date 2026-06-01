import re
import json
from typing import Dict, List, Optional, Tuple
from collections import Counter, defaultdict

PATRON_HTTP = re.compile(r'''
    ^
    (?P<ip>\d{1,3}(?:\.\d{1,3}){3})    # Dirección IP
    \s+-\s+-\s+                          # "- -" (usuario/ident)
    \[(?P<timestamp>[^\]]+)\]            # Timestamp entre corchetes
    \s+
    "(?P<method>[A-Z]+)                  # Método HTTP (GET, POST, etc.)
    \s+(?P<path>[^\s]+)                  # Ruta solicitada
    \s+(?P<protocol>[^"]+)"              # Protocolo HTTP/1.x
    \s+(?P<status>\d{3})                 # Código de estado
    \s+(?P<bytes>\d+)                    # Bytes transferidos
    \s+"(?P<referer>[^"]*)"              # Referer (puede ser "-")
    \s+"(?P<user_agent>[^"]*)"           # User-Agent
    $
''', re.VERBOSE)

def parse_http_log(linea: str) -> Optional[Dict]:
    m = PATRON_HTTP.match(linea.strip())
    if not m:
        return None
    return {
        "ip":         m.group("ip"),
        "timestamp":  m.group("timestamp"),
        "method":     m.group("method"),
        "path":       m.group("path"),
        "status":     int(m.group("status")),
        "bytes":      int(m.group("bytes")),
        "referer":    m.group("referer"),
        "user_agent": m.group("user_agent"),
    }


PATRON_ERROR = re.compile(r'''
    ^
    \[(?P<timestamp>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\]   # Timestamp [YYYY-MM-DD HH:MM:SS]
    \s+
    (?P<level>ERROR|WARNING|INFO|DEBUG|CRITICAL)                  # Nivel de log
    \s+
    (?P<module>[\w.]+)                                            # Módulo (ej. app.database)
    \s+-\s+
    (?P<error_type>[\w]+):                                        # Tipo de error seguido de ":"
    \s*
    (?P<message>.+)                                               # Mensaje descriptivo
    $
''', re.VERBOSE)

def parse_error_log(linea: str) -> Optional[Dict]:
    m = PATRON_ERROR.match(linea.strip())
    if not m:
        return None
    return {
        "timestamp":  m.group("timestamp"),
        "level":      m.group("level"),
        "module":     m.group("module"),
        "error_type": m.group("error_type"),
        "message":    m.group("message").strip(),
    }


PATRON_AUTH = re.compile(r'''
    ^\[AUTH\]\s+                                               # Prefijo [AUTH]
    (?P<timestamp>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})      # Timestamp
    \s*\|.*                                                    # Resto de la línea
''', re.VERBOSE)

PATRON_KV = re.compile(r'(?<=\|)\s*(?P<key>\w+)=(?P<value>[^\|]+)')

def parse_auth_log(linea: str) -> Optional[Dict]:
    if not linea.strip().startswith("[AUTH]"):
        return None

    m_ts = re.search(r'\[AUTH\]\s+(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})', linea)
    if not m_ts:
        return None
    timestamp = m_ts.group(1)

    pares = {m.group("key"): m.group("value").strip()
             for m in PATRON_KV.finditer(linea)}

    campos_principales = {"user", "action", "status", "ip"}
    extra = {k: v for k, v in pares.items() if k not in campos_principales}

    return {
        "timestamp": timestamp,
        "user":      pares.get("user", ""),
        "action":    pares.get("action", ""),
        "status":    pares.get("status", ""),
        "ip":        pares.get("ip", ""),
        "extra":     extra,
    }

PATRON_DB = re.compile(r'''
    ^
    \[DB-(?P<timestamp>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\]  # Timestamp [DB-YYYY-MM-DD HH:MM:SS]
    \s+
    (?:
        (?P<slow>SLOW_QUERY)\s+\((?P<slow_time>[\d.]+)s\)          # SLOW_QUERY (Xs)
        |
        (?P<normal>QUERY)\s+executed\s+in\s+(?P<normal_time>[\d.]+)s  # QUERY executed in Xs
    )
    :\s+
    (?P<query>.+)                                                   # La query SQL
    $
''', re.VERBOSE)

def parse_db_log(linea: str) -> Optional[Dict]:
    m = PATRON_DB.match(linea.strip())
    if not m:
        return None

    if m.group("slow"):
        query_type = "SLOW_QUERY"
        exec_time  = float(m.group("slow_time"))
    else:
        query_type = "QUERY"
        exec_time  = float(m.group("normal_time"))

    return {
        "timestamp":      m.group("timestamp"),
        "query_type":     query_type,
        "execution_time": exec_time,
        "query":          m.group("query").strip(),
    }


def detectar_ataques_fuerza_bruta(logs_auth: List[Dict]) -> List[Dict]:
    fallos_por_ip: Dict[str, int] = defaultdict(int)

    for log in logs_auth:
        if log.get("action") == "LOGIN" and log.get("status") == "FAILED":
            fallos_por_ip[log["ip"]] += 1

    return [
        {"ip": ip, "intentos": intentos}
        for ip, intentos in sorted(fallos_por_ip.items(), key=lambda x: -x[1])
        if intentos > 3
    ]

PATRONES_SQL_INJECTION = [
    re.compile(r"(?i)\bOR\b\s+['\"]?\d+['\"]?\s*=\s*['\"]?\d+"),   # OR 1=1
    re.compile(r"(?i)\bUNION\b.*?\bSELECT\b"),                      # UNION SELECT
    re.compile(r"--"),                                               # Comentario SQL
    re.compile(r"(?i)\bDROP\b\s+\bTABLE\b"),                        # DROP TABLE
    re.compile(r"(?i)\bDELETE\b\s+\bFROM\b.*?\bWHERE\b\s+1\s*=\s*1"),  # DELETE WHERE 1=1
]

def detectar_sql_injection(logs_db: List[Dict]) -> List[Dict]:
    sospechosos = []
    for log in logs_db:
        query = log.get("query", "")
        for patron in PATRONES_SQL_INJECTION:
            if patron.search(query):
                entrada = dict(log)
                entrada["patron_detectado"] = patron.pattern
                sospechosos.append(entrada)
                break  
    return sospechosos


PATRON_PATH_TRAVERSAL = re.compile(
    r'(?:'
    r'\.\.[\\/]'             # ../ o ..\
    r'|%2e%2e%2f'            # URL-encoded ../
    r'|%2e%2e/'              # Mixto
    r'|\.\.%2f'              # Mixto
    r')',
    re.IGNORECASE
)

def detectar_path_traversal(logs_http: List[Dict]) -> List[Dict]:
    return [
        log for log in logs_http
        if PATRON_PATH_TRAVERSAL.search(log.get("path", ""))
    ]


def detectar_errores_criticos(logs_error: List[Dict]) -> List[Dict]:
    criticos = [
        log for log in logs_error
        if log.get("level") in ("ERROR", "CRITICAL")
    ]
    return sorted(criticos, key=lambda x: x.get("timestamp", ""))

_PREFIJO_AUTH   = re.compile(r'^\[AUTH\]')
_PREFIJO_DB     = re.compile(r'^\[DB-')
_PREFIJO_ERROR  = re.compile(r'^\[\d{4}-\d{2}-\d{2}')
_PREFIJO_HTTP   = re.compile(r'^\d{1,3}(?:\.\d{1,3}){3}\s')

def clasificar_linea(linea: str) -> str:
    linea = linea.strip()
    if not linea:
        return "desconocido"
    if _PREFIJO_AUTH.match(linea):
        return "auth"
    if _PREFIJO_DB.match(linea):
        return "db"
    if _PREFIJO_ERROR.match(linea):
        return "error"
    if _PREFIJO_HTTP.match(linea):
        return "http"
    return "desconocido"


def generar_reporte(logs: str) -> Dict:
    lineas = [l for l in logs.splitlines() if l.strip()]

    logs_http  = []
    logs_error = []
    logs_auth  = []
    logs_db    = []
    conteo     = {"http": 0, "error": 0, "auth": 0, "db": 0, "desconocido": 0}

    for linea in lineas:
        tipo = clasificar_linea(linea)
        conteo[tipo] = conteo.get(tipo, 0) + 1

        if tipo == "http":
            parsed = parse_http_log(linea)
            if parsed:
                logs_http.append(parsed)
        elif tipo == "error":
            parsed = parse_error_log(linea)
            if parsed:
                logs_error.append(parsed)
        elif tipo == "auth":
            parsed = parse_auth_log(linea)
            if parsed:
                logs_auth.append(parsed)
        elif tipo == "db":
            parsed = parse_db_log(linea)
            if parsed:
                logs_db.append(parsed)

    por_status: Dict[str, int] = {"2xx": 0, "3xx": 0, "4xx": 0, "5xx": 0}
    for log in logs_http:
        bucket = f"{log['status'] // 100}xx"
        if bucket in por_status:
            por_status[bucket] += 1

    counter_rutas = Counter(log["path"] for log in logs_http)
    counter_ips   = Counter(log["ip"]   for log in logs_http)

    seccion_http = {
        "total_requests": len(logs_http),
        "por_status":     por_status,
        "top_rutas":      counter_rutas.most_common(5),
        "top_ips":        counter_ips.most_common(5),
    }

    por_nivel  = Counter(log["level"]  for log in logs_error)
    por_modulo = Counter(log["module"] for log in logs_error)

    seccion_errores = {
        "total":     len(logs_error),
        "por_nivel": dict(por_nivel),
        "por_modulo": dict(por_modulo),
    }

    # --- Seguridad ---
    seccion_seguridad = {
        "alertas_fuerza_bruta":   detectar_ataques_fuerza_bruta(logs_auth),
        "alertas_sql_injection":  detectar_sql_injection(logs_db),
        "alertas_path_traversal": detectar_path_traversal(logs_http),
        "errores_criticos":       detectar_errores_criticos(logs_error),
    }

    # --- Rendimiento ---
    queries_lentos = [log for log in logs_db if log["query_type"] == "SLOW_QUERY"]
    tiempos = [log["execution_time"] for log in logs_db]
    tiempo_promedio = sum(tiempos) / len(tiempos) if tiempos else 0.0

    seccion_rendimiento = {
        "queries_lentos":         queries_lentos,
        "tiempo_promedio_queries": tiempo_promedio,
    }

    return {
        "resumen": {
            "total_lineas": len(lineas),
            "por_tipo": {
                "http":  conteo.get("http", 0),
                "error": conteo.get("error", 0),
                "auth":  conteo.get("auth", 0),
                "db":    conteo.get("db", 0),
            },
        },
        "http":        seccion_http,
        "errores":     seccion_errores,
        "seguridad":   seccion_seguridad,
        "rendimiento": seccion_rendimiento,
    }

def exportar_reporte_json(reporte: Dict, archivo: str) -> None:
    def serializable(obj):
        if isinstance(obj, (Counter, defaultdict)):
            return dict(obj)
        if isinstance(obj, tuple):
            return list(obj)
        raise TypeError(f"Tipo no serializable: {type(obj)}")

    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(reporte, f, ensure_ascii=False, indent=2, default=serializable)
    print(f"Reporte exportado a '{archivo}'")


def analisis_temporal(logs_http: List[Dict]) -> Dict[str, int]:
    patron_hora = re.compile(r'\d{2}/\w+/\d{4}:(\d{2}):\d{2}:\d{2}')
    conteo: Dict[str, int] = defaultdict(int)

    for log in logs_http:
        m = patron_hora.search(log.get("timestamp", ""))
        if m:
            conteo[m.group(1)] += 1

    return dict(sorted(conteo.items()))

PATRON_BOTS = re.compile(
    r'(?i)'
    r'\b(?:curl|wget|python-requests|python-urllib|scrapy|httpie|'
    r'go-http-client|java/|libwww-perl|lwp-trivial|'
    r'sqlmap|nikto|nmap|masscan|zgrab|dirbuster|'
    r'fuzz|scanner|bot|crawl|spider|slurp|bingbot|googlebot)\b'
)

def detectar_bots(logs_http: List[Dict]) -> List[Dict]:
    bots = []
    for log in logs_http:
        ua = log.get("user_agent", "")
        m = PATRON_BOTS.search(ua)
        if m:
            entrada = dict(log)
            entrada["bot_detectado"] = m.group(0).lower()
            bots.append(entrada)
    return bots


def mostrar_reporte(reporte: Dict) -> None:
    """Muestra el reporte de forma legible en consola."""
    print("=" * 70)
    print("                    REPORTE DE ANÁLISIS DE LOGS")
    print("=" * 70)

    print("\RESUMEN GENERAL")
    print("-" * 40)
    print(f"Total de líneas procesadas: {reporte['resumen']['total_lineas']}")
    print("Por tipo:")
    for tipo, count in reporte['resumen']['por_tipo'].items():
        print(f"  • {tipo.upper()}: {count}")

    if 'http' in reporte:
        print("LOGS HTTP")
        print("-" * 40)
        print(f"Total requests: {reporte['http']['total_requests']}")
        print("Por código de estado:")
        for status, count in reporte['http']['por_status'].items():
            print(f"  • {status}: {count}")
        print("Top 5 rutas más solicitadas:")
        for ruta, count in reporte['http'].get('top_rutas', [])[:5]:
            print(f"  • {ruta}: {count} requests")

    if 'errores' in reporte:
        print("ERRORES")
        print("-" * 40)
        print(f"Total errores: {reporte['errores']['total']}")
        print("Por nivel:")
        for nivel, count in reporte['errores']['por_nivel'].items():
            print(f"  • {nivel}: {count}")

    if 'seguridad' in reporte:
        print("ALERTAS DE SEGURIDAD")
        print("-" * 40)

        fb = reporte['seguridad'].get('alertas_fuerza_bruta', [])
        if fb:
            print(f"  Posibles ataques de fuerza bruta: {len(fb)}")
            for alerta in fb:
                print(f"     IP: {alerta['ip']} - {alerta['intentos']} intentos fallidos")

        sql = reporte['seguridad'].get('alertas_sql_injection', [])
        if sql:
            print(f"  Posibles SQL Injection: {len(sql)}")
            for alerta in sql[:3]:
                print(f"     Query: {alerta['query'][:60]}...")

        pt = reporte['seguridad'].get('alertas_path_traversal', [])
        if pt:
            print(f"  Posibles Path Traversal: {len(pt)}")
            for alerta in pt[:3]:
                print(f"     Ruta: {alerta['path']}")

    if 'rendimiento' in reporte:
        print("\RENDIMIENTO")
        print("-" * 40)
        print(f"Queries lentos detectados: {len(reporte['rendimiento'].get('queries_lentos', []))}")
        if 'tiempo_promedio_queries' in reporte['rendimiento']:
            print(f"Tiempo promedio de queries: {reporte['rendimiento']['tiempo_promedio_queries']:.3f}s")

    print("\n" + "=" * 70)

LOGS_PRUEBA = """
192.168.1.100 - - [15/Mar/2024:10:23:45 -0600] "GET /api/users HTTP/1.1" 200 1234 "https://ejemplo.com" "Mozilla/5.0 (Windows NT 10.0)"
192.168.1.101 - - [15/Mar/2024:10:23:46 -0600] "POST /api/login HTTP/1.1" 200 89 "-" "curl/7.68.0"
192.168.1.102 - - [15/Mar/2024:10:23:47 -0600] "GET /admin/../../../etc/passwd HTTP/1.1" 403 0 "-" "sqlmap/1.0"
[2024-03-15 10:24:00] INFO app.startup - Application: started successfully on port 8080
[2024-03-15 10:25:12] ERROR app.database - DatabaseConnectionError: Connection refused to host db.server.com:5432
[2024-03-15 10:25:15] WARNING app.cache - CacheWarning: Redis connection timeout, using fallback
[2024-03-15 10:26:00] ERROR app.auth - AuthenticationError: Invalid token for user admin@empresa.com
[AUTH] 2024-03-15 10:30:00 | user=admin@empresa.com | action=LOGIN | status=SUCCESS | ip=10.0.0.5 | session=abc123xyz
[AUTH] 2024-03-15 10:31:00 | user=hacker@mail.com | action=LOGIN | status=FAILED | ip=192.168.1.50 | attempts=1
[AUTH] 2024-03-15 10:31:30 | user=hacker@mail.com | action=LOGIN | status=FAILED | ip=192.168.1.50 | attempts=2
[AUTH] 2024-03-15 10:32:00 | user=hacker@mail.com | action=LOGIN | status=FAILED | ip=192.168.1.50 | attempts=3
[AUTH] 2024-03-15 10:32:30 | user=hacker@mail.com | action=LOGIN | status=FAILED | ip=192.168.1.50 | attempts=4
[AUTH] 2024-03-15 10:33:00 | user=otro@empresa.com | action=LOGOUT | status=SUCCESS | ip=10.0.0.10 | session=def456uvw
[DB-2024-03-15 10:35:22] QUERY executed in 0.045s: SELECT * FROM users WHERE email = 'admin@empresa.com'
[DB-2024-03-15 10:35:25] QUERY executed in 0.012s: SELECT id, name FROM products WHERE active = 1
[DB-2024-03-15 10:36:00] SLOW_QUERY (2.5s): SELECT * FROM orders o JOIN products p ON o.product_id = p.id JOIN users u ON o.user_id = u.id
[DB-2024-03-15 10:37:00] QUERY executed in 0.001s: SELECT * FROM users WHERE username = 'admin' OR 1=1--'
[DB-2024-03-15 10:38:00] QUERY executed in 0.002s: SELECT * FROM users UNION SELECT * FROM passwords
192.168.1.200 - - [15/Mar/2024:10:40:00 -0600] "GET /products?id=1 HTTP/1.1" 200 5678 "https://tienda.com" "Mozilla/5.0"
192.168.1.200 - - [15/Mar/2024:10:40:05 -0600] "GET /products?id=2 HTTP/1.1" 200 4321 "https://tienda.com" "Mozilla/5.0"
192.168.1.201 - - [15/Mar/2024:10:41:00 -0600] "GET /api/users HTTP/1.1" 401 123 "-" "PostmanRuntime/7.26.8"
192.168.1.201 - - [15/Mar/2024:10:41:05 -0600] "GET /api/users HTTP/1.1" 500 0 "-" "PostmanRuntime/7.26.8"
[2024-03-15 10:42:00] ERROR app.api - NullPointerException: Cannot read property 'id' of undefined
[DB-2024-03-15 10:45:00] SLOW_QUERY (5.2s): SELECT COUNT(*) FROM logs WHERE date > '2024-01-01'
""".strip()


if __name__ == "__main__":
    print("PRUEBA DE PARSERS")
    print("=" * 50)

    linea_http = '192.168.1.100 - - [15/Mar/2024:10:23:45 -0600] "GET /api/users HTTP/1.1" 200 1234 "https://ejemplo.com" "Mozilla/5.0"'
    print("\n-- Parser HTTP --")
    print(f"Entrada: {linea_http[:60]}...")
    print(f"Resultado: {parse_http_log(linea_http)}")

    linea_error = "[2024-03-15 10:25:12] ERROR app.database - DatabaseConnectionError: Connection refused"
    print("\n-- Parser Error --")
    print(f"Entrada: {linea_error}")
    print(f"Resultado: {parse_error_log(linea_error)}")

    linea_auth = "[AUTH] 2024-03-15 10:30:00 | user=admin@empresa.com | action=LOGIN | status=SUCCESS | ip=10.0.0.5 | session=abc123xyz"
    print("\n-- Parser Auth --")
    print(f"Entrada: {linea_auth}")
    print(f"Resultado: {parse_auth_log(linea_auth)}")

    linea_db = "[DB-2024-03-15 10:35:22] QUERY executed in 0.045s: SELECT * FROM users"
    print("\n-- Parser DB --")
    print(f"Entrada: {linea_db}")
    print(f"Resultado: {parse_db_log(linea_db)}")

    linea_db_slow = "[DB-2024-03-15 10:36:00] SLOW_QUERY (2.5s): SELECT * FROM orders JOIN products"
    print("\n-- Parser DB (SLOW_QUERY) --")
    print(f"Entrada: {linea_db_slow}")
    print(f"Resultado: {parse_db_log(linea_db_slow)}")

    print("\nGENERANDO REPORTE COMPLETO...\n")
    reporte = generar_reporte(LOGS_PRUEBA)
    mostrar_reporte(reporte)

    print("\n BONUS: Exportando reporte a JSON...")
    exportar_reporte_json(reporte, "/home/claude/reporte_logs.json")

    print("\n BONUS: Análisis temporal de requests HTTP...")
    logs_http_parsed = [parse_http_log(l) for l in LOGS_PRUEBA.splitlines()
                        if clasificar_linea(l) == "http" and parse_http_log(l)]
    distribucion = analisis_temporal(logs_http_parsed)
    print(f"  Distribución por hora: {distribucion}")

    print("\n BONUS: Detección de bots...")
    bots = detectar_bots(logs_http_parsed)
    for bot in bots:
        print(f"  Bot '{bot['bot_detectado']}' desde IP {bot['ip']} → {bot['path']}")