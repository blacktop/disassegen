from typing import Optional

import click

from .spec import ArmSpec


@click.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option("--output", "-o", type=click.Path(), help="Optional output file path")
def main(input_file: str, output: Optional[str]) -> None:
    """
    Generate a disassembler from the input JSON ARM64 spec.

    Args:
        input_file: Path to the input JSON file
        output: Optional path to save the generated disassembler source code
    """
    try:
        # Parse the input using the spec
        parsed_result = ArmSpec(input_file)

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
