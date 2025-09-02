CREATE TABLE "categorias_reciclaje" (
  "id_categoria" INTEGER PRIMARY KEY,
  "nombre_categoria" VARCHAR,
  "descripcion" varchar,
  "created_at" TIMESTAMP
);

CREATE TABLE "tipos_material" (
  "id_material" INTEGER PRIMARY KEY,
  "id_categoria" INTEGER,
  "nombre_material" VARCHAR,
  "descripcion" VARCHAR,
  "tiempo_descomposicion" varchar,
  "created_at" TIMESTAMP
);

CREATE TABLE "instrucciones_reciclaje" (
  "id_instruccion" INTEGER PRIMARY KEY,
  "id_material" INTEGER,
  "paso_numero" INTEGER,
  "instruccion" TEXT,
  "imagen_url" VARCHAR,
  "created_at" TIMESTAMP
);

CREATE TABLE "centros_reciclaje" (
  "id_centro" INTEGER PRIMARY KEY,
  "nombre_centro" VARCHAR,
  "direccion" VARCHAR,
  "telefono" VARCHAR,
  "horario_atencion" VARCHAR,
  "latitud" DECIMAL,
  "longitud" DECIMAL,
  "created_at" TIMESTAMP
);

CREATE TABLE "centros_materiales" (
  "id_centro_material" INTEGER PRIMARY KEY,
  "id_centro" INTEGER,
  "id_material" INTEGER,
  "created_at" TIMESTAMP
);

CREATE TABLE "usuarios" (
  "id_usuario" INTEGER PRIMARY KEY,
  "nombre" VARCHAR,
  "email" VARCHAR,
  "password_hash" VARCHAR,
  "localidad" VARCHAR,
  "created_at" TIMESTAMP
);

CREATE TABLE "user_logros" (
  "id_logro" INTEGER PRIMARY KEY,
  "id_usuario" INTEGER,
  "tipo_logro" VARCHAR,
  "fecha_obtencion" TIMESTAMP
);

CREATE TABLE "preguntas_frecuentes" (
  "id_pregunta" INTEGER PRIMARY KEY,
  "pregunta" VARCHAR,
  "respuesta" VARCHAR,
  "created_at" TIMESTAMP
);

CREATE TABLE "consejos_ecologicos" (
  "id_consejo" INTEGER PRIMARY KEY,
  "titulo" VARCHAR,
  "contenido" VARCHAR,
  "imagen_url" VARCHAR,
  "created_at" TIMESTAMP
);

ALTER TABLE "user_logros" ADD FOREIGN KEY ("id_usuario") REFERENCES "usuarios" ("id_usuario");

ALTER TABLE "centros_materiales" ADD FOREIGN KEY ("id_centro") REFERENCES "centros_reciclaje" ("id_centro");

ALTER TABLE "centros_materiales" ADD FOREIGN KEY ("id_material") REFERENCES "tipos_material" ("id_material");

ALTER TABLE "tipos_material" ADD FOREIGN KEY ("id_categoria") REFERENCES "categorias_reciclaje" ("id_categoria");

ALTER TABLE "instrucciones_reciclaje" ADD FOREIGN KEY ("id_material") REFERENCES "tipos_material" ("id_material");
