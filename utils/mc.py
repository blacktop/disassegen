import os
import re
import subprocess
import sys

import click


class MC:

    def __init__(self):
        super().__init__()

    def assemble(self, str) -> int:
        try:
            process = subprocess.Popen(
                ["/opt/homebrew/opt/llvm/bin/llvm-mc", "-arch=arm64", "-mattr=v9.5a", "-show-encoding"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            stdout, stderr = process.communicate(input=str)
            if process.returncode != 0:
                raise Exception(f"Failed to assemble: {stderr}")
            #  .section\t__TEXT,__text,regular,pure_instructions
            #     hint    #24                             ; encoding: [0x1f,0x23,0x03,0xd5]
            hex_numbers = re.findall(r"0x[0-9a-fA-F]+", stdout)
            result = 0
            for i, hex_number in enumerate(hex_numbers):
                result |= int(hex_number, 16) << (i * 8)
            return result
        except Exception as e:
            raise e

    def disassemble(self, int) -> str:
        try:
            process = subprocess.Popen(
                ["/opt/homebrew/opt/llvm/bin/llvm-mc", "-arch=arm64", "-mattr=v9.5a", "-disassemble"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            hex_bytes = [f"{(int >> (8 * i)) & 0xFF:02x}" for i in range(4)]
            stdout, stderr = process.communicate(input="0x" + " 0x".join(hex_bytes))
            if process.returncode != 0:
                raise Exception(f"Failed to disassemble: {stderr}")
            # Skip the first line of stdout
            lines = stdout.splitlines()
            if lines:
                return "\n".join([line.strip() for line in lines[1:]])
            else:
                return ""
        except Exception as e:
            raise e


@click.group()
def cli():
    """LLVM Machine Code Playground"""
    if not os.path.exists("/opt/homebrew/opt/llvm/bin/llvm-mc"):
        print("'llvm-mc' tool not found. Please run `brew install llvm` to install it.")
        sys.exit()


@cli.command()
@click.argument("instructions", type=str)
def assemble(instructions: str):
    """Assemble ARM64 instructions"""
    print(hex(MC().assemble(instructions)))


@cli.command()
@click.argument("uint32", type=str)
def disassemble(uint32: str):
    """Disassemble ARM64 instructions"""
    if uint32.startswith("0x"):
        uint32 = int(uint32, 16)
    else:
        uint32 = int(uint32)
    print(MC().disassemble(uint32))


if __name__ == "__main__":
    cli()
