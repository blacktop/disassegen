from dataclasses import dataclass, field, asdict
from typing import List, Optional, Union, Dict, Any
import json
from pathlib import Path


@dataclass
class Range:
    _type: str = "Range"
    start: int = 0
    width: int = 0


@dataclass
class ValuesValue:
    _type: str = "Values.Value"
    value: str = ""
    meaning: Optional[str] = None


@dataclass
class EncodingField:
    _type: str = "Instruction.Encodeset.Field"
    range: Range = field(default_factory=Range)
    name: str = ""
    value: ValuesValue = field(default_factory=ValuesValue)
    should_be_mask: ValuesValue = field(default_factory=ValuesValue)


@dataclass
class EncodingBits:
    _type: str = "Instruction.Encodeset.Bits"
    range: Range = field(default_factory=Range)
    value: ValuesValue = field(default_factory=ValuesValue)
    should_be_mask: ValuesValue = field(default_factory=ValuesValue)


@dataclass
class Encodeset:
    _type: str = "Instruction.Encodeset.Encodeset"
    width: int = 32
    values: List[Union[EncodingField, EncodingBits]] = field(default_factory=list)

    def __str__(self) -> str:
        """
        Provide a human-readable string representation of the Encodeset.

        Returns:
            str: A formatted string with key information about the encoding
        """
        output = []

        # Basic encoding information
        if self.width != 32:
            output.append(f"Encoding Width: {self.width} bits")

        for value in self.values:
            if value["_type"] == "Instruction.Encodeset.Field":
                line = f"- \033[1m\033[94m{value['name']}\033[0m"
                if value["range"]["start"] != 0 or value["range"]["width"] != 32:
                    line += f" range={value['range']['start']+value['range']['width']-1}:{value['range']['start']}"
                if value["value"]["value"]:
                    line += f" value={value['value']['value']}"
                    if value["value"]["meaning"]:
                        line += f" (meaning={value['value']['meaning']})"
                if value["should_be_mask"]["value"] and "1" in value["should_be_mask"]["value"]:
                    line += f" should_be_mask={value['should_be_mask']['value']}"
                    if value["should_be_mask"]["meaning"]:
                        line += f" (meaning={value['should_be_mask']['meaning']})"
                output.append(line)

            elif value["_type"] == "Instruction.Encodeset.Bits":
                line = f"- \033[1;32mBITS:\033[0m"
                if value["range"]["start"] != 0 or value["range"]["width"] != 32:
                    line += f" range={value['range']['start']+value['range']['width']-1}:{value['range']['start']}"
                if value["value"]["value"]:
                    line += f" value={value['value']['value']}"
                    if value["value"]["meaning"]:
                        line += f" (meaning={value['value']['meaning']})"
                if value["should_be_mask"]["value"] and "1" in value["should_be_mask"]["value"]:
                    line += f" should_be_mask={value['should_be_mask']['value']}"
                    if value["should_be_mask"]["meaning"]:
                        line += f"(meaning={value['should_be_mask']['meaning']})"
                output.append(line)

        return "\n".join(output)

    def __repr__(self) -> str:
        """
        Provide a detailed representation of the Encodeset object.

        Returns:
            str: A string representation suitable for debugging
        """
        return f"Encodeset(width={self.width}, " f"value_count={len(self.values)})"


# AST Schemas
@dataclass
class ASTIdentifier:
    _type: str = "AST.Identifier"
    value: str = ""


@dataclass
class ASTDotAtom:
    _type: str = "AST.DotAtom"
    values: List[Union[ASTIdentifier, Dict[str, Any]]] = field(default_factory=list)


@dataclass
class ASTBinaryOp:
    _type: str = "AST.BinaryOp"
    left: Union[ASTIdentifier, ASTDotAtom, Dict[str, Any]] = field(default_factory=dict)
    op: str = ""
    right: Union[ASTIdentifier, Dict[str, Any]] = field(default_factory=dict)


@dataclass
class ASTAssignment:
    _type: str = "AST.Assignment"
    var: Union[ASTIdentifier, ASTDotAtom, Dict[str, Any]] = field(default_factory=dict)
    val: Union[ASTIdentifier, ASTDotAtom, Dict[str, Any]] = field(default_factory=dict)


@dataclass
class ASTFunction:
    _type: str = "AST.Function"
    name: str = ""
    arguments: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class ASTBool:
    _type: str = "AST.Bool"
    value: bool = True


@dataclass
class ASTInteger:
    _type: str = "AST.Integer"
    value: int = 0


@dataclass
class ASTSet:
    _type: str = "AST.Set"
    values: List[Union[ASTIdentifier, ASTInteger, Dict[str, Any]]] = field(default_factory=list)


@dataclass
class ASTStatementBlock:
    _type: str = "AST.StatementBlock"
    statements: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class Instruction:
    _type: str = "Instruction.Instruction"
    name: str = ""
    encoding: Encodeset = field(default_factory=Encodeset)
    condition: Optional[Union[ASTFunction, ASTBool]] = None
    operation_id: Optional[str] = None
    assembly: Optional[Dict[str, Any]] = None
    assemble: Optional[Dict[str, Any]] = None
    disassemble: Optional[Dict[str, Any]] = None
    assertions: Optional[Dict[str, Any]] = None


@dataclass
class InstructionGroup:
    _type: str = "Instruction.InstructionGroup"
    name: str = ""
    title: Optional[str] = None
    encoding: Encodeset = field(default_factory=Encodeset)
    condition: Optional[Union[ASTFunction, ASTBool]] = None
    children: List[Union["InstructionGroup", Instruction]] = field(default_factory=list)
    operation_id: Optional[str] = None


@dataclass
class InstructionSet:
    _type: str = "Instruction.InstructionSet"
    name: str = ""
    read_width: int = 32
    encoding: Encodeset = field(default_factory=Encodeset)
    condition: Optional[Union[ASTFunction, ASTBool]] = None
    operation_id: Optional[str] = None
    children: List[Union[InstructionGroup, Instruction]] = field(default_factory=list)


@dataclass
class AssemblySymbol:
    _type: str = "Instruction.Symbols.Literal"
    value: str = ""


@dataclass
class AssemblyRuleReference:
    _type: str = "Instruction.Symbols.RuleReference"
    rule_id: str = ""


@dataclass
class Assembly:
    _type: str = "Instruction.Assembly"
    symbols: List[Union[AssemblySymbol, AssemblyRuleReference]] = field(default_factory=list)


@dataclass
class AssemblyRuleChoice:
    _type: str = "Instruction.Rules.Choice"
    choices: List[Union[Assembly, None]] = field(default_factory=list)
    display: Optional[str] = None
    description: Optional[Dict[str, Any]] = None


@dataclass
class AssemblyRuleRule:
    _type: str = "Instruction.Rules.Rule"
    assemble: Optional[ASTStatementBlock] = None
    disassemble: Optional[ASTStatementBlock] = None
    symbols: Optional[Union[Assembly, None]] = None
    display: Optional[str] = None
    description: Optional[Dict[str, Any]] = None
    condition: Optional[Dict[str, Any]] = None


@dataclass
class AssemblyRuleToken:
    _type: str = "Instruction.Rules.Token"
    pattern: str = ""
    default: Optional[str] = None


@dataclass
class Operation:
    _type: str = "Instruction.Operation"
    operation: List[List[str]] = field(default_factory=list)
    decode: Optional[List[List[str]]] = None
    description: str = ""
    brief: str = ""
    title: str = ""


@dataclass
class OperationAlias:
    _type: str = "Instruction.OperationAlias"
    operation_id: str = ""
    description: str = ""
    brief: str = ""
    title: str = ""


@dataclass
class LicenseInfo:
    _type: str = "Meta.License"
    copyright: str = ""
    info: str = ""


@dataclass
class VersionInfo:
    _type: str = "Meta.Version"
    architecture: str = ""
    build: str = ""
    ref: str = ""
    schema: str = ""
    timestamp: str = ""


@dataclass
class MetaSchema:
    _type: str = "Meta"
    license: LicenseInfo = field(default_factory=LicenseInfo)
    version: VersionInfo = field(default_factory=VersionInfo)


@dataclass
class Instructions:
    _type: str = "Instruction.Instructions"
    meta: MetaSchema = field(default_factory=MetaSchema)
    assembly_rules: Union[str, AssemblyRuleChoice, AssemblyRuleRule, AssemblyRuleToken] = field(default_factory=dict)
    instructions: List[InstructionSet] = field(default_factory=list)
    operations: Dict[str, Union[Operation, OperationAlias]] = field(default_factory=dict)


@dataclass
class InstructionAlias:
    _type: str = "Instruction.InstructionAlias"
    name: str = ""
    operation_id: str = ""
    assembly: Optional[Assembly] = field(default_factory=Assembly)
    preferred: Optional[Union[ASTFunction, ASTBool]] = field(default_factory=lambda: ASTBool(value=False))
    condition: Optional[Union[ASTFunction, ASTBool]] = None


@dataclass
class InstructionInstance:
    _type: str = "Instruction.InstructionInstance"
    name: str = ""
    properties: Optional[Dict[str, Any]] = field(default_factory=dict)
    condition: Optional[Union[ASTFunction, ASTBool]] = None
    children: Optional[List["InstructionInstance"]] = field(default_factory=list)


# Traits Schemas
@dataclass
class HasCondition:
    condition: Optional[Union[ASTFunction, ASTBool, ASTBinaryOp, Dict[str, Any]]] = None


class ArmSpec(object):

    def __init__(self, file_path: Union[str, Path]):
        self.file_path = file_path
        self.instructions = self.load_instruction_schema_from_json(file_path)

    def load_instruction_schema_from_json(self, file_path: Union[str, Path]) -> Instructions:
        """
        Load an Instructions object from a JSON file.

        Args:
            file_path (Union[str, Path]): Path to the JSON file to load

        Returns:
            Instructions: Parsed Instructions object
        """
        # Convert to Path object if it's a string
        path = Path(file_path)

        # Read and parse the JSON file
        with path.open("r") as f:
            data = json.load(f)

        # Convert JSON data to Instructions object
        return self.parse_instructions(data)

    def parse_instructions(self, data: Dict[str, Any]) -> Instructions:
        """
        Parse a dictionary into an Instructions object.

        Args:
            data (Dict[str, Any]): Dictionary representation of Instructions

        Returns:
            Instructions: Parsed Instructions object
        """
        # Parse meta
        meta = MetaSchema(**data.get("_meta", {}))

        # Parse assembly rules
        assembly_rules = {
            k: (
                AssemblyRuleToken(**v)
                if v.get("_type") == "Instruction.Rules.Token"
                else (
                    AssemblyRuleChoice(**v)
                    if v.get("_type") == "Instruction.Rules.Choice"
                    else AssemblyRuleRule(**v) if v.get("_type") == "Instruction.Rules.Rule" else v
                )
            )
            for k, v in data.get("assembly_rules", {}).items()
        }

        # Parse instructions
        instructions = [self.parse_instruction_set(inst_data) for inst_data in data.get("instructions", [])]

        # Parse operations
        operations = {
            k: (
                Operation(**v)
                if v.get("_type") == "Instruction.Operation"
                else OperationAlias(**v) if v.get("_type") == "Instruction.OperationAlias" else v
            )
            for k, v in data.get("operations", {}).items()
        }

        return Instructions(meta=meta, assembly_rules=assembly_rules, instructions=instructions, operations=operations)

    def parse_instruction_set(self, data: Dict[str, Any]) -> InstructionSet:
        """
        Parse a dictionary into an InstructionSet object.

        Args:
            data (Dict[str, Any]): Dictionary representation of InstructionSet

        Returns:
            InstructionSet: Parsed InstructionSet object
        """
        # Parse encoding
        encoding = Encodeset(**data.get("encoding", {}))

        # Parse children
        children = []
        for child_data in data.get("children", []):
            if child_data.get("_type") == "Instruction.InstructionGroup":
                children.append(self.parse_instruction_group(child_data))
            elif child_data.get("_type") == "Instruction.Instruction":
                children.append(self.parse_instruction(child_data))

        # Parse condition
        condition = None
        if "condition" in data:
            condition_data = data["condition"]
            if condition_data.get("_type") == "AST.Function":
                condition = ASTFunction(**condition_data)
            elif condition_data.get("_type") == "AST.Bool":
                condition = ASTBool(**condition_data)

        return InstructionSet(
            name=data.get("name", ""),
            read_width=data.get("read_width", 32),
            encoding=encoding,
            condition=condition,
            operation_id=data.get("operation_id"),
            children=children,
        )

    def parse_instruction_group(self, data: Dict[str, Any]) -> InstructionGroup:
        """
        Parse a dictionary into an InstructionGroup object.

        Args:
            data (Dict[str, Any]): Dictionary representation of InstructionGroup

        Returns:
            InstructionGroup: Parsed InstructionGroup object
        """
        # Parse encoding
        encoding = Encodeset(**data.get("encoding", {}))

        # Parse children
        children = []
        for child_data in data.get("children", []):
            if child_data.get("_type") == "Instruction.InstructionGroup":
                children.append(self.parse_instruction_group(child_data))
            elif child_data.get("_type") == "Instruction.Instruction":
                children.append(self.parse_instruction(child_data))

        # Parse condition
        condition = None
        if "condition" in data:
            condition_data = data["condition"]
            if condition_data.get("_type") == "AST.Function":
                condition = ASTFunction(**condition_data)
            elif condition_data.get("_type") == "AST.Bool":
                condition = ASTBool(**condition_data)

        return InstructionGroup(
            name=data.get("name", ""),
            title=data.get("title"),
            encoding=encoding,
            condition=condition,
            children=children,
            operation_id=data.get("operation_id"),
        )

    def parse_instruction(self, data: Dict[str, Any]) -> Instruction:
        """
        Parse a dictionary into an Instruction object.

        Args:
            data (Dict[str, Any]): Dictionary representation of Instruction

        Returns:
            Instruction: Parsed Instruction object
        """
        # Parse encoding
        encoding = Encodeset(**data.get("encoding", {}))

        return Instruction(
            name=data.get("name", ""),
            encoding=encoding,
            operation_id=data.get("operation_id"),
            assembly=data.get("assembly"),
            assemble=data.get("assemble"),
            disassemble=data.get("disassemble"),
            assertions=data.get("assertions"),
        )

    def save_instructions_to_json(self, instructions: Instructions, file_path: Union[str, Path]) -> None:
        """
        Save an Instructions object to a JSON file.

        Args:
            instructions (Instructions): Instructions object to save
            file_path (Union[str, Path]): Path to save the JSON file
        """
        # Convert Instructions object to a dictionary
        data = asdict(instructions)

        # Write to file
        with Path(file_path).open("w") as f:
            json.dump(data, f, indent=2)

    def __str__(self) -> str:
        """
        Provide a human-readable string representation of the ArmSpec.

        Returns:
            str: A formatted string with key information about the loaded instructions
        """
        output = []

        output.append(f"ArmSpec: {self.file_path}")

        output.append(" - Version:")
        output.append(f"   - Architecture: {self.instructions.meta.version['architecture']}")
        output.append(f"   - Build: {self.instructions.meta.version['build']}")
        output.append(f"   - Ref: {self.instructions.meta.version['ref']}")
        output.append(f"   - Schema: {self.instructions.meta.version['schema']}")
        output.append(f"   - Timestamp: {self.instructions.meta.version['timestamp']}")

        # Detailed breakdown of instruction groups and individual instructions
        output.append("\nInstruction Breakdown:")
        for instruction_set in self.instructions.instructions:
            output.append(f"- {instruction_set.name}")

            # Recursively add instruction groups and instructions
            def add_instruction_details(item, indent=1):
                indent_str = "  " * indent
                if hasattr(item, "name"):
                    asm = ""
                    if hasattr(item, "assembly"):
                        asm = ""
                        for symbol in item.assembly["symbols"]:
                            if symbol["_type"] == "Instruction.Symbols.Literal":
                                asm += symbol["value"]
                            elif symbol["_type"] == "Instruction.Symbols.RuleReference":
                                if self.instructions.assembly_rules.get(symbol["rule_id"]):
                                    if hasattr(self.instructions.assembly_rules[symbol["rule_id"]], "default"):
                                        asm += self.instructions.assembly_rules[symbol["rule_id"]].default
                                    elif hasattr(self.instructions.assembly_rules[symbol["rule_id"]], "display") and self.instructions.assembly_rules[symbol["rule_id"]].display is not None:
                                        asm += self.instructions.assembly_rules[symbol["rule_id"]].display                                    
                                    else:
                                        asm += f"({symbol['rule_id']})" 
                    output.append(f"{indent_str}- \033[1;35m{item.name}\033[0m \033[1;36m{asm}\033[0m")
                    output.append(f"{item.encoding}")

                if hasattr(item, "children"):
                    for child in item.children:
                        add_instruction_details(child, indent + 1)

            for child in instruction_set.children:
                add_instruction_details(child)

        # Operation details
        # output.append("\nOperation IDs:")
        # for op_id, operation in self.instructions.operations.items():
        #     output.append(f"- {op_id}: {operation.title or operation.brief}")

        return "\n".join(output)
