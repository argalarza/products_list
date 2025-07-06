from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ariadne import load_schema_from_path, make_executable_schema
from ariadne.asgi import GraphQL
from .resolvers import query

# Cargar el esquema y los resolvers
type_defs = load_schema_from_path("app/schema.graphql")
schema = make_executable_schema(type_defs, query)

# Crear la app FastAPI
app = FastAPI()

# Agregar CORS para permitir cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes cambiar "*" por ["http://tudominio.com"] en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar el endpoint GraphQL
graphql_app = GraphQL(schema, context_value=lambda request: {"request": request})
app.mount("/", graphql_app)
