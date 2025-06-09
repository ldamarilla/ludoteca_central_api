from flask import Blueprint, jsonify, request
from db import get_connection

productos_bp = Blueprint("productos", __name__)