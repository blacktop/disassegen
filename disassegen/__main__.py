from typing import Optional

import click

from .spec import MRSSpec
from .isa.spec import ISASpec


@click.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option("--output", "-o", type=click.Path(), help="Optional path to save the generated disassembler source code")
def main(input_file: str, output: Optional[str]) -> None:
    """
    Generate a disassembler from the input JSON ARM64 spec.

    Args:
        input_file: Path to the input JSON file
    """
    try:
        if input_file.endswith(".xml"):
            parsed_result = ISASpec(input_file)
        else:
            parsed_result = MRSSpec(input_file)

        if output:
            with open(output, "w") as f:
                f.write(parsed_result)
        else:
            # Print to console if no output file specified
            print(parsed_result)

    except Exception as e:
        click.echo(f"Error processing file: {e}", err=True)
        exit(1)


if __name__ == "__main__":
    main()
