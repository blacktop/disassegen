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
class Instruction:
    _type: str = "Instruction.Instruction"
    name: str = ""
    encoding: Encodeset = field(default_factory=Encodeset)
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
class ASTStatementBlock:
    _type: str = "AST.StatementBlock"
    statements: List[Dict[str, Any]] = field(default_factory=list)


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
                    output.append(f"{indent_str}- {item.name}")

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
