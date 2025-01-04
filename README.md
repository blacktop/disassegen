# disassegen

> Generate arbitrary language AARCH64 disassemblers from ARMARM spec

## Goal 🤔

My hope is to create a tool that I wanted to exist for a long time and that is a tool to take the ARM spec and generate a disassembler, assembler and emulator from it.

The 'move' is probably to create C code from the spec and let other languages create bindings via FFI, but having had the pain of CGO I'd prefer to generate native source per language.

My dream is to convert the spec into an AST that I could then convert into any language's source code, but I might start with some simple templating to get something that works out the door as a MVP.

## Current Progress 📈

Just trying to understand the MRS BSD format and see if it's usable in it's current state or if we still need the XML.

## Getting Started 🚀

Clone repo

```bash
git clone https://github.com/blacktop/disassegen.git
```

Download the SPEC

```bash
make aarchmrs
```

Run

```bash
make run
```

## Spec 📖

- <https://developer.arm.com/Architectures/A-Profile%20Architecture#Downloads>

## Notes 📓

- <https://github.com/alastairreid/asl-interpreter>

## License 

MIT Copyright (c) 2025 blacktop