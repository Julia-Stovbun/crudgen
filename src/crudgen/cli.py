import typer
from pydantic import ValidationError

from crudgen.core.loader import load_config

app = typer.Typer(no_args_is_help=True)


@app.command()
def main(config_path: str = typer.Argument(..., help="Path to YAML/JSON config")) -> None:
    try:
        cfg = load_config(config_path)
    except FileNotFoundError as e:
        raise typer.Exit(code=2) from e
    except ValueError as e:
        typer.echo(f"Error: {e}")
        raise typer.Exit(code=2) from e
    except ValidationError as e:
        typer.echo("Config validation error:")
        typer.echo(str(e))
        raise typer.Exit(code=2) from e

    typer.echo("Config OK ✅")
    typer.echo(f"Entity: {cfg.entity} -> table '{cfg.table}'")
    typer.echo(f"Fields: {', '.join(cfg.fields.keys())}")


if __name__ == "__main__":
    app()
