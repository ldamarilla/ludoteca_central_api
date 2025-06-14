from base64 import b64decode, b64encode
from flask import Flask, jsonify, request, Blueprint, render_template
from sqlalchemy import create_engine, text
import re

vista_admin_1_bp = Blueprint("crear_usuario", __name__)

engine = create_engine(DATABASE_URI)

@vista_admin_1_bp.route("/", methods=["GET"])
def mostrar_nombre():
    if request.method == "GET""
        try:
            


        