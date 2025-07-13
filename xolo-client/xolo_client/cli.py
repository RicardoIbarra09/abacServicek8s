import typer
import json
from xolo_client.client import XoloPolicyClient

app = typer.Typer()
client = XoloPolicyClient()


@app.command(name="list")
def list_policies():
    """Listar todas las políticas"""
    typer.echo(json.dumps(client.list_policies(), indent=2))


@app.command()
def get(policy_id: str):
    """Obtener una política específica"""
    typer.echo(json.dumps(client.get_policy(policy_id), indent=2))


@app.command()
def create(file_path: str):
    """
    Crear un conjunto de políticas desde un archivo JSON.

    El archivo debe contener una lista de políticas como JSON.
    """
    with open(file_path, 'r') as f:
        policy_list = json.load(f)
    if not isinstance(policy_list, list):
        typer.echo("El archivo debe contener una lista de políticas (JSON array).")
        raise typer.Exit(1)

    result = client.create_policies(policy_list)
    typer.echo(json.dumps(result, indent=2))


@app.command()
def inject(file_path: str):
    """
    Inyectar una sola política al evaluador en memoria.

    El archivo debe contener una política individual.
    """
    with open(file_path, 'r') as f:
        policy = json.load(f)
    result = client.inject_policy(policy)
    typer.echo(json.dumps(result, indent=2))


@app.command()
def delete(policy_id: str):
    """Eliminar una política"""
    typer.echo(json.dumps(client.delete_policy(policy_id), indent=2))


@app.command()
def update(policy_id: str, file_path: str):
    """Actualizar una política desde un archivo JSON"""
    with open(file_path, 'r') as f:
        updated_policy = json.load(f)
    typer.echo(json.dumps(client.update_policy(policy_id, updated_policy), indent=2))


@app.command()
def prepare():
    """Preparar comunidades"""
    typer.echo(json.dumps(client.prepare_communities(), indent=2))


@app.command()
def evaluate(file_path: str):
    """Evaluar una solicitud de acceso"""
    with open(file_path, 'r') as f:
        request = json.load(f)
    typer.echo(json.dumps(client.evaluate_request(request), indent=2))


@app.command("evaluate-batch")
def evaluate_batch(file_path: str):
    """Evaluar lote de solicitudes de acceso"""
    with open(file_path, 'r') as f:
        request_list = json.load(f)
    if not isinstance(request_list, list):
        typer.echo("El archivo debe contener una lista de solicitudes (JSON array).")
        raise typer.Exit(1)

    typer.echo(json.dumps(client.evaluate_batch_requests(request_list), indent=2))


if __name__ == "__main__":
    app()
