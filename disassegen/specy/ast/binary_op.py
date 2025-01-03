# generated by datamodel-codegen:
#   filename:  BinaryOp.json
#   timestamp: 2025-01-03T06:52:08+00:00

from __future__ import annotations

from enum import Enum
from typing import Any, List, Optional, Union

from pydantic import BaseModel, Extra, Field, conint, constr


class FieldType(Enum):
    AST_BinaryOp = 'AST.BinaryOp'


class Op(Enum):
    field___ = '-->'
    field____1 = '<->'


class Op1(Enum):
    field__ = '||'
    field___1 = '&&'
    field___2 = '<='
    field___3 = '>='
    field___4 = '=='
    field___5 = '!='
    field_ = '<'
    field__1 = '>'
    field___6 = '<<'
    field___7 = '>>'
    field__2 = '+'
    field__3 = '-'
    OR = 'OR'
    XOR = 'XOR'
    AND = 'AND'
    field__4 = '*'
    field__5 = '/'
    field__6 = '^'
    field___8 = '++'
    IN = 'IN'
    MOD = 'MOD'
    DIV = 'DIV'
    DIVRM = 'DIVRM'


class Meta(BaseModel):
    pass


class FieldType2(Enum):
    Types_String = 'Types.String'


class String(BaseModel):
    class Config:
        extra = Extra.forbid

    field_meta: Optional[Meta] = Field(None, alias='_meta')
    field_type: Optional[FieldType2] = Field(None, alias='_type')
    value: str = Field(..., examples=['A simple value.'])


class FieldType3(Enum):
    Types_Field = 'Types.Field'


class State(Enum):
    AArch32 = 'AArch32'
    AArch64 = 'AArch64'
    ext = 'ext'


class Name(BaseModel):
    __root__: constr(regex=r'^[A-Za-z][A-Za-z0-9_\s]*(?:<[^>]+>)?[A-Za-z0-9_]*$') = (
        Field(..., examples=['REG0', 'REG<n>_EL1'])
    )


class Instance(BaseModel):
    __root__: Optional[
        constr(regex=r'^[A-Za-z][A-Za-z0-9_]*(?:<[^>]+>)?[A-Za-z0-9_]*$')
    ] = Field(..., examples=['REG0', 'REG<n>_EL1', None])


class FieldType4(Enum):
    Range = 'Range'


class Range(BaseModel):
    class Config:
        extra = Extra.forbid

    field_meta: Optional[Meta] = Field(None, alias='_meta')
    field_type: Optional[FieldType4] = Field(None, alias='_type')
    start: conint(ge=0)
    width: conint(ge=1)


class FieldType5(Enum):
    ExpressionRange = 'ExpressionRange'


class ExpressionRange(BaseModel):
    class Config:
        extra = Extra.forbid

    field_meta: Optional[Meta] = Field(None, alias='_meta')
    field_type: Optional[FieldType5] = Field(None, alias='_type')
    expression: str


class FieldType6(Enum):
    Types_PstateField = 'Types.PstateField'


class FieldType7(Enum):
    Types_RegisterType = 'Types.RegisterType'


class FieldType8(Enum):
    Types_RegisterMultiFields = 'Types.RegisterMultiFields'


class Field1(BaseModel):
    __root__: constr(regex=r'^[A-Za-z][A-Za-z0-9_]*$')


class FieldType9(Enum):
    Values_Value = 'Values.Value'


class Text(BaseModel):
    __root__: Optional[Union[List[Union[List[str], str]], str]] = Field(
        ..., title='Text'
    )


class Value5(BaseModel):
    __root__: constr(regex=r'^(0(b[01x]+|x[0-9A-Fa-f]+)|\'[01x]+\')$')


class FieldType10(Enum):
    AST_Bool = 'AST.Bool'


class Bool(BaseModel):
    class Config:
        extra = Extra.forbid

    field_meta: Optional[Meta] = Field(None, alias='_meta')
    field_type: Optional[FieldType10] = Field(None, alias='_type')
    value: bool


class FieldType11(Enum):
    AST_Real = 'AST.Real'


class Real(BaseModel):
    class Config:
        extra = Extra.forbid

    field_meta: Optional[Meta] = Field(None, alias='_meta')
    field_type: Optional[FieldType11] = Field(None, alias='_type')
    value: float


class FieldType12(Enum):
    AST_Integer = 'AST.Integer'


class Integer(BaseModel):
    class Config:
        extra = Extra.forbid

    field_meta: Optional[Meta] = Field(None, alias='_meta')
    field_type: Optional[FieldType12] = Field(None, alias='_type')
    value: int


class FieldType13(Enum):
    AST_Set = 'AST.Set'


class FieldType14(Enum):
    AST_Function = 'AST.Function'


class FieldType15(Enum):
    AST_SquareOp = 'AST.SquareOp'


class FieldType16(Enum):
    AST_Slice = 'AST.Slice'


class FieldType17(Enum):
    AST_Concat = 'AST.Concat'


class FieldType18(Enum):
    AST_Tuple = 'AST.Tuple'


class FieldType19(Enum):
    AST_DotAtom = 'AST.DotAtom'


class FieldType20(Enum):
    AST_Identifier = 'AST.Identifier'


class Regex(BaseModel):
    __root__: constr(regex=r'^([a-zA-Z_][a-zA-Z0-9_]*(<[^>]+>)?[a-zA-Z0-9_]*$)')


class CIdentifierRegex(BaseModel):
    __root__: constr(regex=r'^[a-zA-Z_][a-zA-Z0-9_]*$')


class FieldType21(Enum):
    AST_TypeAnnotation = 'AST.TypeAnnotation'


class FieldType22(Enum):
    AST_Type = 'AST.Type'


class FieldType23(Enum):
    AST_UnaryOp = 'AST.UnaryOp'


class Op2(Enum):
    field_ = '!'
    field__1 = '-'
    NOT = 'NOT'


class Rangeset(BaseModel):
    __root__: List[Union[Range, ExpressionRange]] = Field(
        ...,
        examples=[
            [
                {'_type': 'Range', 'start': 6, 'width': 1},
                {'_type': 'Range', 'start': 2, 'width': 3},
            ]
        ],
        title='Rangeset',
    )


class Value2(BaseModel):
    class Config:
        extra = Extra.forbid

    name: constr(regex=r'^PSTATE\.[A-Za-z][A-Za-z0-9_]*$')
    slices: Optional[Rangeset] = None


class PstateField(BaseModel):
    class Config:
        extra = Extra.forbid

    field_meta: Optional[Meta] = Field(None, alias='_meta')
    field_type: Optional[FieldType6] = Field(None, alias='_type')
    value: Value2


class Value3(BaseModel):
    name: Name
    instance: Optional[Instance] = None
    state: State
    slices: Optional[Rangeset] = None


class RegisterType(BaseModel):
    class Config:
        extra = Extra.forbid

    field_meta: Optional[Meta] = Field(None, alias='_meta')
    field_type: Optional[FieldType7] = Field(None, alias='_type')
    value: Value3 = Field(
        ...,
        examples=[
            {'state': 'AArch64', 'name': 'REG0'},
            {
                'state': 'AArch32',
                'name': 'REG0',
                'instance': 'REG0_S',
                'slices': [{'_type': 'Range', 'start': 4, 'width': 1}],
            },
        ],
    )


class Value4(BaseModel):
    fields: List[Field1] = Field(..., min_items=2, unique_items=True)
    register_: Optional[Name] = Field(None, alias='register')
    name: Name
    state: State
    slices: Optional[Rangeset] = None


class RegisterMultiFields(BaseModel):
    class Config:
        extra = Extra.forbid

    field_meta: Optional[Meta] = Field(None, alias='_meta')
    field_type: Optional[FieldType8] = Field(None, alias='_type')
    value: Value4


class Value(BaseModel):
    class Config:
        extra = Extra.forbid

    field_meta: Optional[Meta] = Field(None, alias='_meta')
    field_type: Optional[FieldType9] = Field(None, alias='_type')
    meaning: Optional[Text] = None
    value: constr(regex=r'^\'[01x]+\'$') = Field(..., examples=["'10'", "'1x'"])


class Identifier(BaseModel):
    class Config:
        extra = Extra.forbid

    field_meta: Optional[Meta] = Field(None, alias='_meta')
    field_type: Optional[FieldType20] = Field(None, alias='_type')
    value: Regex


class Value1(BaseModel):
    state: State
    name: Name
    field: str
    slices: Optional[Rangeset] = None


class FieldModel(BaseModel):
    class Config:
        extra = Extra.forbid

    field_meta: Optional[Meta] = Field(None, alias='_meta')
    field_type: Optional[FieldType3] = Field(None, alias='_type')
    value: Value1 = Field(
        ...,
        examples=[
            {'state': 'AArch64', 'name': 'REG0', 'field': 'F1'},
            {
                'state': 'AArch32',
                'name': 'REG0',
                'field': 'F1',
                'rangeset': '5:4',
                'instance': 'REG0_S',
            },
        ],
    )


class BinaryOp1(BaseModel):
    class Config:
        extra = Extra.forbid

    field_meta: Optional[Meta] = Field(None, alias='_meta')
    field_type: Optional[FieldType] = Field(None, alias='_type')
    left: Expression
    op: Op
    right: Expression


class BinaryOp2(BaseModel):
    class Config:
        extra = Extra.forbid

    field_meta: Optional[Meta] = Field(None, alias='_meta')
    field_type: Optional[FieldType] = Field(None, alias='_type')
    left: Expression
    op: Op1
    right: Expression


class BinaryOp(BaseModel):
    __root__: Union[BinaryOp1, BinaryOp2] = Field(..., title='BinaryOp')


class Expression(BaseModel):
    __root__: Union[
        String,
        FieldModel,
        PstateField,
        RegisterType,
        RegisterMultiFields,
        Value,
        Bool,
        Real,
        Integer,
        Set,
        Function,
        SquareOp,
        Concat,
        Tuple,
        DotAtom,
        Identifier,
        TypeAnnotation,
        UnaryOp,
        BinaryOp,
    ]


class Set(BaseModel):
    class Config:
        extra = Extra.forbid

    field_meta: Optional[Meta] = Field(None, alias='_meta')
    field_type: Optional[FieldType13] = Field(None, alias='_type')
    values: Optional[List[Expression]] = []


class Function(BaseModel):
    class Config:
        extra = Extra.forbid

    field_meta: Optional[Meta] = Field(None, alias='_meta')
    field_type: Optional[FieldType14] = Field(None, alias='_type')
    name: Any
    arguments: Optional[List[Expression]] = []


class SquareOp(BaseModel):
    class Config:
        extra = Extra.forbid

    field_meta: Optional[Meta] = Field(None, alias='_meta')
    field_type: Optional[FieldType15] = Field(None, alias='_type')
    var: Expression
    arguments: Optional[List[Union[Expression, Slice]]] = []


class Slice(BaseModel):
    class Config:
        extra = Extra.forbid

    field_meta: Optional[Meta] = Field(None, alias='_meta')
    field_type: Optional[FieldType16] = Field(None, alias='_type')
    left: Expression
    right: Expression


class Concat(BaseModel):
    class Config:
        extra = Extra.forbid

    field_meta: Optional[Meta] = Field(None, alias='_meta')
    field_type: Optional[FieldType17] = Field(None, alias='_type')
    values: List[Expression] = Field(..., min_items=2)


class Tuple(BaseModel):
    class Config:
        extra = Extra.forbid

    field_meta: Optional[Meta] = Field(None, alias='_meta')
    field_type: Optional[FieldType18] = Field(None, alias='_type')
    values: List[Expression] = Field(..., min_items=2)


class DotAtom(BaseModel):
    class Config:
        extra = Extra.forbid

    field_meta: Optional[Meta] = Field(None, alias='_meta')
    field_type: Optional[FieldType19] = Field(None, alias='_type')
    values: List[Expression] = Field(..., min_items=2)


class TypeAnnotation1(BaseModel):
    class Config:
        extra = Extra.forbid

    field_meta: Optional[Meta] = Field(None, alias='_meta')
    field_type: Optional[FieldType21] = Field(None, alias='_type')
    var: Union[Identifier, DotAtom]
    type: Type


class TypeAnnotation(BaseModel):
    __root__: Union[TypeAnnotation1, constr(regex=r'.+::.+')] = Field(
        ...,
        examples=[
            {
                '_type': 'AST.TypeAnnotation',
                'var': {'_type': 'AST.Identifier', 'value': 'UNKNOWN'},
                'type': {
                    '_type': 'AST.Type',
                    'name': {
                        '_type': 'AST.Function',
                        'name': 'bits',
                        'arguments': [{'_type': 'AST.Integer', 'value': 32}],
                    },
                },
            }
        ],
        title='TypeAnnotation',
    )


class Type1(BaseModel):
    class Config:
        extra = Extra.forbid

    field_meta: Optional[Meta] = Field(None, alias='_meta')
    field_type: Optional[FieldType22] = Field(None, alias='_type')
    name: Union[Identifier, Function]


class Type(BaseModel):
    __root__: Union[Type1, str] = Field(
        ...,
        examples=[
            {
                '_type': 'AST.Type',
                'name': {
                    '_type': 'AST.Function',
                    'name': 'bits',
                    'arguments': [{'_type': 'AST.Integer', 'value': 32}],
                },
            },
            {
                '_type': 'AST.Type',
                'name': {'_type': 'AST.Identifier', 'value': 'integer'},
            },
        ],
        title='Type',
    )


class UnaryOp(BaseModel):
    class Config:
        extra = Extra.forbid

    field_meta: Optional[Meta] = Field(None, alias='_meta')
    field_type: Optional[FieldType23] = Field(None, alias='_type')
    op: Op2
    expr: Expression


BinaryOp1.update_forward_refs()
BinaryOp2.update_forward_refs()
Expression.update_forward_refs()
SquareOp.update_forward_refs()
TypeAnnotation1.update_forward_refs()
