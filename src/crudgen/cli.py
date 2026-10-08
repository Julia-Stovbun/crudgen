from pathlib import Path

import typer
import yaml
from pydantic import ValidationError

from crudgen.core.generator import render_fastapi
from crudgen.core.loader import load_config

app = typer.Typer(no_args_is_help=True)


@app.command()
def main(
    config_path: Path = typer.Argument(..., help="YAML or JSON config"),
    out: Path = typer.Option(Path("out"), "--out", "-o", help="Output directory"),
    overwrite: bool = typer.Option(False, "--overwrite", help="Overwrite generated files"),
) -> None:
    try:
        outputs = render_fastapi(load_config(str(config_path)), out, overwrite)
    except (FileNotFoundError, FileExistsError, ValueError, ValidationError, yaml.YAMLError) as exc:
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(code=2) from exc
    for path in outputs:
        typer.echo(str(path))


if __name__ == "__main__":
    app()
