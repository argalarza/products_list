from ariadne import QueryType
from fastapi import Request
from .models import product_collection
from .jwt_utils import verify_token
from bson import ObjectId

query = QueryType()

@query.field("listProducts")
def resolve_list_products(_, info):
    request: Request = info.context["request"]
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise Exception("Falta el token")

    token = auth_header.split(" ")[1]
    user = verify_token(token)

    products = list(product_collection.find())
    for product in products:
        product["_id"] = str(product["_id"])
    return products
