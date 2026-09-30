from sqlalchemy.orm import Session
from app.models import Ingrediente, Reserva

class StockService:

    @staticmethod
    def get_ingredientes(db: Session, search_text: str = ""):
        query = db.query(Ingrediente)
        if search_text.strip():
            pattern = f"%{search_text.strip()}%"
            query = query.filter(Ingrediente.nombre.ilike(pattern))
        return query.order_by(Ingrediente.nombre.asc()).all()

    @staticmethod
    def reabastecer_stock(db: Session, id_ingrediente: int, cantidad: float) -> bool:
        ingrediente = db.query(Ingrediente).filter(Ingrediente.id_ingrediente == id_ingrediente).first()
        if ingrediente and cantidad > 0:
            ingrediente.stock_actual = float(ingrediente.stock_actual or 0) + cantidad
            db.commit()
            return True
        return False

    @staticmethod
    def descontar_stock_por_reserva(db: Session, id_reserva: int) -> bool:
        """Al entregar una comanda, busca los ingredientes con nombres coincidentes a los platos y descuenta stock."""
        reserva = db.query(Reserva).filter(Reserva.id_reserva == id_reserva).first()
        if not reserva or not reserva.menu:
            return False

        for plato in reserva.menu.platos:
            # Buscar si existe un ingrediente clave registrado con el nombre del plato
            pattern = f"%{plato.nombre.strip()}%"
            ingrediente = db.query(Ingrediente).filter(Ingrediente.nombre.ilike(pattern)).first()
            
            if ingrediente:
                actual = float(ingrediente.stock_actual or 0)
                ingrediente.stock_actual = max(0.0, actual - 1.0)

        db.commit()
        return True

    @staticmethod
    def guardar_ingrediente(db: Session, datos: dict) -> bool:
        if datos.get("id_ingrediente"):
            ing = db.query(Ingrediente).filter(Ingrediente.id_ingrediente == datos["id_ingrediente"]).first()
            if ing:
                ing.nombre = datos.get("nombre", ing.nombre)
                ing.unidad_medida = datos.get("unidad_medida", ing.unidad_medida)
                ing.stock_actual = datos.get("stock_actual", ing.stock_actual)
                ing.stock_minimo = datos.get("stock_minimo", ing.stock_minimo)
                ing.alergeno = datos.get("alergeno", ing.alergeno)
                ing.tipo_alergeno = datos.get("tipo_alergeno", ing.tipo_alergeno)
        else:
            nuevo_ing = Ingrediente(**datos)
            db.add(nuevo_ing)
        db.commit()
        return True
    
    @staticmethod
    def crear_ingrediente(db, nombre, unidad_medida, stock_actual, stock_minimo, alergeno=False, tipo_alergeno="Ninguno"):
        nuevo = Ingrediente(
            nombre=nombre,
            unidad_medida=unidad_medida,
            stock_actual=stock_actual,
            stock_minimo=stock_minimo,
            alergeno=alergeno,
            tipo_alergeno=tipo_alergeno
        )
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        return nuevo
