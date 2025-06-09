from flask import Blueprint, jsonify, request
from db import get_connection

pedidos_bp = Blueprint("pedidos", __name__)