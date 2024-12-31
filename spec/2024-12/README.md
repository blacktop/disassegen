# AARCHMRS containing the JSON files for A-profile Architecture

## Introduction

This is the Arm Architecture Machine Readable Specification containing
JSON files representing the architecture as a machine readable format.

This package contains a subset of the information provided in the packages
with Arm proprietary licenses. Content that is not currently in a machine-readable
format, as well as all descriptive content, is omitted.

The [notice](docs/notice.html) gives details of the license terms and conditions
under which this package is provided.

## Package contents

 - `Features.json` contains the architecture feature constraints.
 - `Instructions.json` contains the A64 Instruction Set Architecture.
 - `Registers.json` contains the AArch32, AArch64, and MemoryMapped
   System Registers and System instructions.
 - [`schema`](schema/) contains JSON schema for the data.
 - [`docs`](docs/index.html) contains the rendered view of the schema
   as well as user guides to help understand the data above.

## Package quality

  - The architectural content contained within the data files has the same quality
    as the equivalent XML releases.
  - The schema and is still under development and is subject to change.

