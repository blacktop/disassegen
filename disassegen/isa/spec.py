import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Union


@dataclass
class Box:
    """Represents a bit field box in the instruction encoding."""

    name: Optional[str]
    high_bit: int
    width: int
    settings: Optional[str]
    use_name: bool
    ps_bits: Optional[str]
    constants: List[str]


@dataclass
class RegDiagram:
    """Represents the register diagram of an instruction encoding."""

    form: str
    ps_name: str
    boxes: List[Box]

    def __str__(self) -> str:
        """Format a register diagram as a visual ASCII representation."""
        if not self:
            return ""

        # Sort boxes by high bit in descending order
        boxes = sorted(self.boxes, key=lambda x: x.high_bit, reverse=True)

        # Find the highest bit for diagram width
        max_bit = max(box.high_bit for box in boxes)

        # Create the diagram lines
        bit_numbers = ""
        field_names = ""
        field_values = ""
        separator = ""

        current_bit = max_bit
        while current_bit >= 0:
            matching_box = None
            for box in boxes:
                if box.high_bit >= current_bit and (box.high_bit - box.width + 1) <= current_bit:
                    matching_box = box
                    break

            if matching_box:
                width = matching_box.width
                # Add bit numbers
                if width > 1:
                    bit_numbers += f"{matching_box.high_bit:<{width}}"
                else:
                    bit_numbers += str(matching_box.high_bit)

                # Add field names
                name = matching_box.name if matching_box.name else ""
                field_names += f"{name:^{width}}"

                # Add field values/constants
                if matching_box.constants:
                    const_str = "".join(matching_box.constants)
                    field_values += f"{const_str:^{width}}"
                else:
                    field_values += " " * width

                # Add separators
                separator += "+" + "-" * (width - 1)

                current_bit -= width
            else:
                bit_numbers += " "
                field_names += " "
                field_values += " "
                separator += "+"
                current_bit -= 1

        # Combine all lines
        diagram = (
            "Register Diagram:\n"
            f"{bit_numbers}\n"
            f"{separator}+\n"
            f"{field_names}\n"
            f"{field_values}\n"
            f"{separator}+"
        )
        return diagram


@dataclass
class Explanation:
    """Represents an explanation of instruction fields."""

    symbol: str
    description: str
    encoded_in: Optional[str]


@dataclass
class PseudoCode:
    """Represents pseudocode sections."""

    name: str
    section_type: str
    code: str


@dataclass
class ArchitectureVariant:
    """Represents an architecture variant."""

    name: str
    feature: str


@dataclass
class Encoding:
    """Represents an instruction encoding."""

    name: str
    label: str
    mnemonic: str
    instruction_class: str
    bit_diffs: str
    assembly_template: str
    reg_diagram: Optional[RegDiagram]


@dataclass
class InstructionClass:
    """Represents an instruction class."""

    name: str
    id: str
    no_encodings: int
    architecture_variants: List[ArchitectureVariant]
    encodings: List[Encoding]
    pseudocode: List[PseudoCode]


@dataclass
class Instruction:
    """Represents a complete instruction."""

    id: str
    title: str
    brief_description: str
    detailed_description: str
    instruction_classes: List[InstructionClass]
    explanations: List[Explanation]
    docvars: Dict[str, str]

    def __str__(self) -> str:
        """
        Create a string representation of the Instruction.

        Returns:
            str: A formatted string representation of the instruction
        """
        output = []

        output.append(f"Instruction: {self.id}")
        output.append(f"Title: {self.title}")
        output.append(f"Brief Description: {self.brief_description}")

        output.append("\nDocvars:")
        for key, value in self.docvars.items():
            output.append(f"  {key}: {value}")

        output.append("\nInstruction Classes:")
        for iclass in self.instruction_classes:
            output.append(f"\n- Class: {iclass.name} ({iclass.id})")
            output.append(f"  Number of encodings: {iclass.no_encodings}")

            output.append(f"  Architecture Variants:")
            for variant in iclass.architecture_variants:
                output.append(f"    * {variant.name} ({variant.feature})")

            output.append("  Encodings:")
            for encoding in iclass.encodings:
                output.append(f"\n    * {encoding.mnemonic}: {encoding.assembly_template}")
                if encoding.reg_diagram:
                    output.append("\n" + "\n".join(f"      {line}" for line in str(encoding.reg_diagram).split("\n")))
                    output.append("\n      Bit fields details:")
                    for box in encoding.reg_diagram.boxes:
                        if box.name:
                            output.append(f"        - {box.name} [bit {box.high_bit}, width {box.width}]")
                            if box.constants:
                                output.append(f"          Constants: {', '.join(box.constants)}")

            output.append("\n  Pseudocode:")
            for ps in iclass.pseudocode:
                output.append(f"    Section: {ps.section_type}")
                output.append("    Code:")
                for line in ps.code.split("\n"):
                    output.append(f"      {line}")

        output.append("\nExplanations:")
        for exp in self.explanations:
            output.append(f"  {exp.symbol}:")
            output.append(f"    Description: {exp.description}")
            if exp.encoded_in:
                output.append(f"    Encoded in: {exp.encoded_in}")

        return "\n".join(output)


class ISASpec:
    """Parser for ARM instruction XML format."""

    def __init__(self, file_path: Union[str, Path]):
        """Initialize parser with XML file."""
        self.file_path = file_path
        xml_content = open(self.file_path, "r").read()
        self.root = ET.fromstring(xml_content)
        self.instruction = self.parse()

    def parse_box(self, box_elem: ET.Element) -> Box:
        """Parse a bit field box element."""
        # Get constants (c elements)
        constants = []
        for c in box_elem.findall("./c"):
            if c.text:
                constants.append(c.text)
            elif "colspan" in c.attrib:
                # Handle colspan placeholders
                constants.append("_" * int(c.get("colspan", "1")))

        return Box(
            name=box_elem.get("name"),
            high_bit=int(box_elem.get("hibit", 0)),
            width=int(box_elem.get("width", 1)),
            settings=box_elem.get("settings"),
            use_name=box_elem.get("usename") == "1",
            ps_bits=box_elem.get("psbits"),
            constants=constants,
        )

    def parse_reg_diagram(self, diagram_elem: ET.Element) -> RegDiagram:
        """Parse a register diagram element."""
        if diagram_elem is None:
            return None

        boxes = []
        for box_elem in diagram_elem.findall("./box"):
            boxes.append(self.parse_box(box_elem))

        return RegDiagram(form=diagram_elem.get("form", ""), ps_name=diagram_elem.get("psname", ""), boxes=boxes)

    def parse_pseudocode(self, ps_elem: ET.Element) -> List[PseudoCode]:
        """Parse pseudocode sections."""
        if ps_elem is None:
            return []

        sections = []
        for pstext in ps_elem.findall(".//pstext"):
            sections.append(
                PseudoCode(
                    name=ps_elem.get("name", ""),
                    section_type=pstext.get("section", ""),
                    code="".join(pstext.itertext()).strip(),
                )
            )
        return sections

    def parse_explanation(self, exp_elem: ET.Element) -> Explanation:
        """Parse an explanation element."""
        symbol_elem = exp_elem.find(".//symbol")
        account_elem = exp_elem.find(".//account")

        return Explanation(
            symbol=symbol_elem.text if symbol_elem is not None else "",
            description="".join(account_elem.find(".//para").itertext()).strip() if account_elem is not None else "",
            encoded_in=account_elem.get("encodedin") if account_elem is not None else None,
        )

    def parse_docvars(self) -> Dict[str, str]:
        """Parse document variables."""
        docvars = {}
        for docvar in self.root.findall(".//docvar"):
            docvars[docvar.get("key", "")] = docvar.get("value", "")
        return docvars

    def parse_arch_variants(self, iclass_elem: ET.Element) -> List[ArchitectureVariant]:
        """Parse architecture variants."""
        variants = []
        for variant in iclass_elem.findall(".//arch_variant"):
            variants.append(ArchitectureVariant(name=variant.get("name", ""), feature=variant.get("feature", "")))
        return variants

    def parse_encoding(self, encoding_elem: ET.Element, parent_reg_diagram: Optional[RegDiagram] = None) -> Encoding:
        """Parse an individual encoding element."""
        # Extract docvars
        docvars = encoding_elem.findall(".//docvar")
        docvar_dict = {var.get("key"): var.get("value") for var in docvars}

        # Get assembly template
        asm_template = encoding_elem.find(".//asmtemplate")
        template_text = "".join(asm_template.itertext()) if asm_template is not None else ""

        return Encoding(
            name=encoding_elem.get("name", ""),
            label=encoding_elem.get("label", ""),
            mnemonic=docvar_dict.get("mnemonic", ""),
            instruction_class=docvar_dict.get("instr-class", ""),
            bit_diffs=encoding_elem.get("bitdiffs", ""),
            assembly_template=template_text,
            reg_diagram=parent_reg_diagram,
        )

    def parse_instruction_class(self, iclass_elem: ET.Element) -> InstructionClass:
        """Parse an instruction class element."""
        # Parse architecture variants
        arch_variants = self.parse_arch_variants(iclass_elem)

        # Parse register diagram first (it's shared across encodings)
        reg_diagram = self.parse_reg_diagram(iclass_elem.find("./regdiagram"))

        # Parse encodings
        encodings = []
        for encoding_elem in iclass_elem.findall(".//encoding"):
            encodings.append(self.parse_encoding(encoding_elem, reg_diagram))

        # Parse pseudocode
        pseudocode = []
        for ps_section in iclass_elem.findall(".//ps_section/ps"):
            pseudocode.extend(self.parse_pseudocode(ps_section))

        return InstructionClass(
            name=iclass_elem.get("name", ""),
            id=iclass_elem.get("id", ""),
            no_encodings=int(iclass_elem.get("no_encodings", 0)),
            architecture_variants=arch_variants,
            encodings=encodings,
            pseudocode=pseudocode,
        )

    def parse(self) -> Instruction:
        """Parse the complete instruction XML."""
        # Get basic instruction information
        instruction_id = self.root.get("id", "")
        title = self.root.get("title", "")

        # Get descriptions
        brief_desc, detailed_desc = self.parse_description()

        # Parse instruction classes
        instruction_classes = []
        for iclass_elem in self.root.findall(".//iclass"):
            instruction_classes.append(self.parse_instruction_class(iclass_elem))

        # Parse explanations
        explanations = []
        for exp_elem in self.root.findall(".//explanations/explanation"):
            explanations.append(self.parse_explanation(exp_elem))

        # Parse docvars
        docvars = self.parse_docvars()

        return Instruction(
            id=instruction_id,
            title=title,
            brief_description=brief_desc,
            detailed_description=detailed_desc,
            instruction_classes=instruction_classes,
            explanations=explanations,
            docvars=docvars,
        )

    def parse_description(self) -> tuple[str, str]:
        """Extract brief and detailed descriptions."""
        desc_elem = self.root.find(".//desc")
        if desc_elem is None:
            return "", ""

        brief = desc_elem.find(".//brief/para")
        brief_text = brief.text if brief is not None else ""

        detailed = []
        for para in desc_elem.findall(".//authored/para"):
            detailed.append(para.text.strip())

        return brief_text, "\n".join(detailed)
    
    def __str__(self) -> str:
        return str(self.instruction)
