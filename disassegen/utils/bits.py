# CREDIT: https://github.com/jonpalmisc/workbench/blob/master/bitfield_visualizer/bitviz.py

UNICODE_ARROW = "\u25B2"
UNICODE_VLINE = "\u2502"
UNICODE_HLINE = "\u2500"
UNICODE_JOINT = "\u2518"


class Field(object):
    """Singular field inside of a bitfield."""

    name: str
    start: int
    end: int

    def __init__(self, name: str, end: int, start: int = -1):
        self.name = name
        self.end = end
        self.start = start if start >= 0 else end

    def __lt__(self, other):
        return self.end < other.end

    def extract(self, value: int) -> int:
        """Extract this field's value from the given input value."""

        return (value >> self.start) & (2 ** (self.end + 1 - self.start) - 1)

    def bits(self, value: int) -> str:
        """Like 'extract', but returns a binary-representation string."""

        return "{n:0{w}b}".format(n=self.extract(value), w=self.width)

    @property
    def width(self) -> int:
        """Field width (in bits)."""

        return self.end + 1 - self.start

    @property
    def range(self) -> str:
        """Field range formatted as an '[end:start]' string."""

        if self.end == self.start:
            return f"[{self.start}]"
        else:
            return f"[{self.end}:{self.start}]"


class Bitfield:
    """Numerous, optionally-contiguous fields."""

    fields: list[Field]

    def __init__(self, fields):
        self.fields = fields

    def dump(self, value: int):
        """Dump bitfield contents."""

        for s in self.fields:
            bits = "{n:0{w}b}".format(n=s.extract(value), w=s.width)
            print(f"{s.name:<16}{s.range:<12}{bits}")

    def diagram(self, value: int = 4294967295) -> str:
        """Generate a bitfield diagram as a string."""
        # Must sort so that fields are listed in left-to-right order.
        fields = sorted(self.fields, reverse=True)

        max_name_width = max([len(s.name) for s in fields]) + 2

        # Build the diagram line by line
        lines = []

        # Print the bits in each field.
        bits_line = f"{'':>{max_name_width}}   "
        bits_line += " ".join(t.bits(value) for t in fields)
        lines.append(bits_line)

        # Print the arrow below each field.
        arrow_line = f"{'':>{max_name_width}}   "
        arrow_line += " ".join(" " * (t.width - 1) + UNICODE_ARROW for t in fields)
        lines.append(arrow_line)

        # Print the lines connecting each label to each field.
        for i, r in enumerate(fields):
            # Start with the field name right-aligned
            connect_line = f"{r.name:>{max_name_width}} " + UNICODE_HLINE * 2

            for j, s in enumerate(fields):
                leading = UNICODE_HLINE * (s.width - 1)

                if j == i:
                    connect_line += f"{leading}{UNICODE_JOINT} "
                elif j < i:
                    connect_line += f"{leading}{UNICODE_HLINE * 2}"
                else:
                    connect_line += f"{'':{s.width-1}}{UNICODE_VLINE} "

            lines.append(connect_line)

        # Add an extra newline at the end
        lines.append("")

        # Join the lines and return as a string
        return "\n".join(lines)


if __name__ == "__main__":
    paciaz = Bitfield(
        [
            Field("hints_0", 4, 0),
            Field("ID", 11, 5),
            Field("hints_1", 25, 12),
            Field("control_0", 28, 26),
            Field("hints_2", 31, 29),
        ]
    )

    print("\n[PACIAZ]")
    print(paciaz.diagram(0xD503231F))

# [PACIAZ]
#               110 101 01000000110010 0011000 11111
#                 ▲   ▲              ▲       ▲     ▲
#     hints_2 ────┘   │              │       │     │
#   control_0 ────────┘              │       │     │
#     hints_1 ───────────────────────┘       │     │
#          ID ───────────────────────────────┘     │
#     hints_0 ─────────────────────────────────────┘
