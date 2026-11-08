-- Habilitar modo WAL y configuraciones de rendimiento
PRAGMA journal_mode=WAL;
PRAGMA synchronous=NORMAL;
PRAGMA busy_timeout=5000;

-- 1. Tabla de Bodegas
CREATE TABLE IF NOT EXISTS warehouses (
    warehouse_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    location TEXT
);

-- 2. Tabla Principal de Inventario (Con precio unitario para análisis financiero)
CREATE TABLE IF NOT EXISTS inventory (
    product_id TEXT NOT NULL,
    warehouse_id TEXT NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity >= 0),
    min_stock INTEGER DEFAULT 10,
    unit_cost REAL DEFAULT 100.0,
    PRIMARY KEY (product_id, warehouse_id),
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id)
);

-- 3. Tabla de Auditoría (Kardex Histórico)
CREATE TABLE IF NOT EXISTS audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id TEXT NOT NULL,
    warehouse_id TEXT NOT NULL,
    delta INTEGER NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 4. Tabla de Excepciones / Pérdida de Venta (Dead Letter Log)
CREATE TABLE IF NOT EXISTS rejected_movements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id TEXT NOT NULL,
    warehouse_id TEXT NOT NULL,
    attempted_delta INTEGER NOT NULL,
    reason TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 5. Trigger para Kardex Automático
CREATE TRIGGER IF NOT EXISTS log_inventory_changes
AFTER UPDATE ON inventory
BEGIN
    INSERT INTO audit_log (product_id, warehouse_id, delta)
    VALUES (NEW.product_id, NEW.warehouse_id, NEW.quantity - OLD.quantity);
END;