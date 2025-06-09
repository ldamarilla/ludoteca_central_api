from flask import Blueprint, jsonify, request
from db import get_connection

carrito_bp = Blueprint("carrito", __name__)