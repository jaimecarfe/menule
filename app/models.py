from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Date,
    DateTime,
    Enum,
    Numeric,
    ForeignKey,
    Text,
    Table,
)
from sqlalchemy.orm import relationship
from app.database import Base


# Tabla intermedia M:N entre Menus y Platos
menu_platos = Table(
    "MenuPlatos",
    Base.metadata,
    Column(
        "id_menu",
        Integer,
        ForeignKey("Menus.id_menu", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "id_plato",
        Integer,
        ForeignKey("Platos.id_plato", ondelete="CASCADE"),
        primary_key=True,
    ),
)

# 🛠️ NUEVA: Tabla intermedia M:N entre Reservas y Platos elegidos
reserva_platos = Table(
    "ReservaPlatos",
    Base.metadata,
    Column(
        "id_reserva",
        Integer,
        ForeignKey("Reservas.id_reserva", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "id_plato",
        Integer,
        ForeignKey("Platos.id_plato", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Usuario(Base):
    __tablename__ = "Usuarios"

    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    dni = Column(String(20), unique=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    contrasena_hash = Column(String(255), nullable=False)
    telefono = Column(String(20))
    fecha_alta = Column(Date)
    credencial_activa = Column(Boolean, default=True)
    tipo = Column(
        Enum(
            "estudiante",
            "profesor",
            "administrador",
            "personal_comedor",
            "visitante",
            name="tipo_usuario",
        ),
        nullable=False,
    )

    reservas = relationship("Reserva", back_populates="usuario")
    pagos = relationship("Pago", back_populates="usuario")
    incidencias = relationship(
        "Incidencia",
        foreign_keys="Incidencia.id_usuario",
        back_populates="usuario",
    )
    incidencias_asignadas = relationship(
        "Incidencia",
        foreign_keys="Incidencia.id_responsable",
        back_populates="responsable",
    )

    estudiante_info = relationship("Estudiante", uselist=False, back_populates="usuario")
    profesor_info = relationship("Profesor", uselist=False, back_populates="usuario")


class Estudiante(Base):
    __tablename__ = "Estudiantes"

    id_usuario = Column(
        Integer,
        ForeignKey("Usuarios.id_usuario", ondelete="CASCADE"),
        primary_key=True,
    )
    grado_academico = Column(String(50))
    tui_numero = Column(String(20), unique=True)
    saldo = Column(Numeric(10, 2), default=0.00)

    usuario = relationship("Usuario", back_populates="estudiante_info")


class Profesor(Base):
    __tablename__ = "Profesores"

    id_usuario = Column(
        Integer,
        ForeignKey("Usuarios.id_usuario", ondelete="CASCADE"),
        primary_key=True,
    )
    grado_academico = Column(String(50))
    tui_numero = Column(String(20), unique=True)
    saldo = Column(Numeric(10, 2), default=0.00)

    usuario = relationship("Usuario", back_populates="profesor_info")


class Ingrediente(Base):
    __tablename__ = "Ingredientes"

    id_ingrediente = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    unidad_medida = Column(String(20), default="Kg")
    stock_actual = Column(Numeric(10, 2), default=0.0)
    stock_minimo = Column(Numeric(10, 2), default=0.0)
    alergeno = Column(Boolean, default=False)
    tipo_alergeno = Column(String(50))


class Plato(Base):
    __tablename__ = "Platos"

    id_plato = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    tipo = Column(String(50))
    alergenos = Column(String(255))
    activo = Column(Boolean, default=True)

    menus = relationship("Menu", secondary=menu_platos, back_populates="platos")


class Menu(Base):
    __tablename__ = "Menus"

    id_menu = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(Date, nullable=False)
    tipo = Column(
        Enum(
            "desayuno",
            "almuerzo",
            "cena",
            name="tipo_menu",
        ),
        nullable=False,
    )
    max_reservas = Column(Integer)
    disponible = Column(Boolean, default=True)

    reservas = relationship("Reserva", back_populates="menu")
    platos = relationship("Plato", secondary=menu_platos, back_populates="menus")


class Reserva(Base):
    __tablename__ = "Reservas"

    id_reserva = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(
        Integer,
        ForeignKey("Usuarios.id_usuario"),
        nullable=False,
    )
    id_menu = Column(
        Integer,
        ForeignKey("Menus.id_menu"),
        nullable=False,
    )
    fecha_reserva = Column(DateTime, nullable=False)
    estado = Column(
        Enum(
            "pendiente",
            "confirmada",
            "cancelada",
            "recogida",
            name="estado_reserva",
        ),
        default="pendiente",
    )
    estado_bit = Column(Boolean)

    usuario = relationship("Usuario", back_populates="reservas")
    menu = relationship("Menu", back_populates="reservas")
    pagos = relationship("Pago", back_populates="reserva")
    
    # 🛠️ RELACIÓN DIRECTA A LOS PLATOS ELEGIDOS EN ESTA RESERVA
    platos = relationship("Plato", secondary=reserva_platos)


class Pago(Base):
    __tablename__ = "Pagos"

    id_pago = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(
        Integer,
        ForeignKey("Usuarios.id_usuario"),
        nullable=False,
    )
    id_reserva = Column(
        Integer,
        ForeignKey("Reservas.id_reserva"),
    )
    monto = Column(Numeric(10, 2), nullable=False)
    metodo = Column(
        Enum(
            "tui",
            "bono",
            "tarjeta",
            "efectivo",
            name="metodo_pago",
        ),
        nullable=False,
    )
    fecha_pago = Column(DateTime, nullable=False)
    descuento = Column(Numeric(10, 2), default=0)
    estado = Column(
        Enum(
            "pendiente",
            "completado",
            "fallido",
            "reembolsado",
            name="estado_pago",
        ),
        default="pendiente",
    )
    correo = Column(String(150))

    usuario = relationship("Usuario", back_populates="pagos")
    reserva = relationship("Reserva", back_populates="pagos")


class Incidencia(Base):
    __tablename__ = "Incidencias"

    id_incidencia = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(
        Integer,
        ForeignKey("Usuarios.id_usuario"),
    )
    id_responsable = Column(
        Integer,
        ForeignKey("Usuarios.id_usuario"),
    )
    titulo = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=False)
    numero_seguimiento = Column(String(50))
    fecha_reporte = Column(DateTime, nullable=False)
    estado = Column(
        Enum(
            "abierta",
            "en_proceso",
            "resuelta",
            "cerrada",
            name="estado_incidencia",
        ),
        default="abierta",
    )
    prioridad = Column(
        Enum(
            "baja",
            "media",
            "alta",
            "critica",
            name="prioridad_incidencia",
        ),
        default="media",
    )
    destino = Column(
        Enum(
            "cocina",
            "administracion",
            name="destino_incidencia",
        ),
        default="cocina",
        nullable=False,
    )
    fecha_resolucion = Column(DateTime)
    solucion = Column(Text)

    usuario = relationship(
        "Usuario",
        foreign_keys=[id_usuario],
        back_populates="incidencias",
    )
    responsable = relationship(
        "Usuario",
        foreign_keys=[id_responsable],
        back_populates="incidencias_asignadas",
    )