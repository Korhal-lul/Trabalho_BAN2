from flask import Blueprint, render_template, request, redirect

from services.cliente_service import ClienteService

cliente_bp = Blueprint(
    "cliente",
    __name__,
    url_prefix="/clientes"
)

@cliente_bp.route("/")
def listar():

    clientes = ClienteService.listar()

    return render_template(
        "cliente/listar.html",
        clientes=clientes
    )

@cliente_bp.route("/novo", methods=["GET", "POST"])
def novo():

    if request.method == "POST":

        ClienteService.cadastrar(
            request.form
        )

        return redirect("/clientes")

    return render_template(
        "cliente/cadastrar.html"
    )