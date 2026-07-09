from flask import Blueprint, jsonify, request

orders_bp = Blueprint("orders", __name__, url_prefix="/api/orders")

# In-memory fixture data — HTTP handlers only read JSON-safe structures.
_ORDERS = [
    {"id": "ORD-1001", "sku": "GLaDOS-core", "quantity": 2, "status": "shipped"},
    {"id": "ORD-1002", "sku": "companion-cube", "quantity": 1, "status": "pending"},
]


@orders_bp.get("")
def list_orders():
    return jsonify({"orders": _ORDERS})


@orders_bp.get("/<order_id>")
def get_order(order_id: str):
    for order in _ORDERS:
        if order["id"] == order_id:
            return jsonify(order)
    return jsonify({"error": "not found"}), 404


@orders_bp.post("/search")
def search_orders():
    """Accepts JSON filters only — no binary or serialized payloads."""
    filters = request.get_json(silent=True) or {}
    status = filters.get("status")
    results = _ORDERS if status is None else [o for o in _ORDERS if o["status"] == status]
    return jsonify({"orders": results})
