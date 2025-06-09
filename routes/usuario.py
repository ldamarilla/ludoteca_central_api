from flask import Blueprint, jsonify, request
from db import get_connection

usuario_bp = Blueprint("usuario", __name__)

@usuario