import typer
from pydantic import ValidationError

from crudgen.core.loader import load_config
from crudgen.core.generator import render_fastapi

app = typer.Typer(no_args_is_help=True)


@app.command()
def main(
    config_path: str = typer.Argument(..., help="Path to YAML/JSON config"),
    out: str = typer.Option("out", "--out", "-o", help="Output directory"),
    overwrite: bool = typer.Option(False, "--overwrite", help="Overwrite output files if they exist"),
) -> None:
    try:
        cfg = load_config(config_path)
    except FileNotFoundError as e:
        typer.echo(str(e))
        raise typer.Exit(code=2) from e
    except ValueError as e:
        typer.echo(f"Error: {e}")
        raise typer.Exit(code=2) from e
    except ValidationError as e:
        typer.echo("Config validation error:")
        typer.echo(str(e))
        raise typer.Exit(code=2) from e

    outputs = render_fastapi(cfg, out_dir=out, overwrite=overwrite)
    typer.echo("Generated ✅")
    for p in outputs:
        typer.echo(f"- {p}")


if __name__ == "__main__":
    app()
