
import collections
import csv
from vendor.single import Single
from vendor.descriptors import IterableOf
from vendor.enums import Field
from vendor.exceptions import (
    CSVFormatError,
    DictFormatError,
    ProcessingError,
    CSVProcessingError,
    DictProcessingError,
)


_CSV_TEMPLATE = (
    'name,set,language,condition,first_edition,signed,altered,version,rarity,rare_color,language_code,article_page,comment\n'
    'Tatsunoko,CORE,English,NM,no,no,no,,,,,,"This field is completely IGNORED, because only fields in the CSVField enum are used when reading CSVs."\n'
    'Tatsunoko,CORE,English,NM,no,no,no,,,,,,"If you have more copies of the same card, add a ROW FOR EACH. This is a second Tatsunoko, see?"\n'
    'TATSUNOKO,core,english,nm,NO,NO,No,,,,,,"All field values are CASE-INSENSITIVE, so this third Tatsunoko is the same as the previous two."\n'
    'Krebons,TDGS,,,,,,,,,,,"If a field is left empty, the Single object will use the DEFAULT value for the corresponding attribute."\n'
    'Scapeghost,TDIL,,,,,,,,,,,"However, Name and Set MUST ALWAYS be given, lest an error be raised."\n'
    ',,,,,,,,,,,,Although COMPLETELY EMPTY rows are allowed and will be skipped.\n'
    ',,,,,,,,,,,,"That is, rows with no values in the relevant fields. Remember, this field is ignored."\n'
    ',,,,,,,,,,,,\n'
    'Megalosmasher X,SR04,German,,,,,,,,,,LANGUAGE may be specified with the full word.\n'
    'Zombino,EXFO,de,,,,,,,,,,"Or with ISO language codes. Like the Set 1 code, here."\n'
    'Mad Dog of Darkness,DR2,deu,,,,,,,,,,"Or the Set 2/T code, here."\n'
    'Archfiend Soldier,DR1,ger,,,,,,,,,,"Or the Set 2/B code, here."\n'
    'Luster Dragon,DR1,deu,,,,,,,,,,"Finally, the Set 3 codes happen to coincide with one of the previous ones for all valid card languages."\n'
    'Gemini Elf,IOC,English,,,,,,,,,,The default language is English.\n'
    ',,,,,,,,,,,,\n'
    'Mirror Force,LDK2,,LP,,,,,,,,,CONDITION may be specified with the abbreviation.\n'
    'Dimensional Prison,SDCR,,Light Played,,,,,,,,,Or the full description.\n'
    'Dimensional Prison,SDCR,,good,,,,,,,,,Another example.\n'
    'Sakuretsu Armor,OP13,,NM,,,,,,,,,The default condition is Near Mint.\n'
    ',,,,,,,,,,,,\n'
    'Graceful Charity,SDP,,,no,yes,no,,,,,,The BOOLEAN fields may be either yes or no.\n'
    'Pot of Duality,DREV,,,Yes,No,No,,,,,,Another example.\n'
    'Pot of Duality,DREV,,,YES,,,,,,,,"No is the default value for all boolean fields, so this Pot of Duality is the same as the one above."\n'
)


def _process(iter_of_dicts):
    for dictionary in iter_of_dicts:
        processed_dict = {}
        for key, value in dictionary.items():
            if value in ["", None]:
                continue
            try:
                field = Field(key)
            except ValueError:
                continue

            if field.is_string:
                if isinstance(value, str):
                    processed_value = value
                else:
                    raise ProcessingError.for_field_type(str, field, value)

            elif field.is_integer:
                if isinstance(value, int):
                    processed_value = value
                elif isinstance(value, float):
                    if not value.is_integer():
                        raise ProcessingError.for_field_type(int, field, value)
                    processed_value = int(value)
                elif isinstance(value, str):
                    if not value.isdigit():
                        raise ProcessingError.for_field_type(int, field, value)
                    processed_value = int(value)
                else:
                    raise ProcessingError.for_field_type(int, field, value)

            elif field.is_boolean:
                if isinstance(value, bool):
                    processed_value = value
                elif isinstance(value, str):
                    if value.lower() in ["true", "yes"]:
                        processed_value = True
                    elif value.lower() in ["false", "no"]:
                        processed_value = False
                    else:
                        raise ProcessingError.for_field_type(bool, field, value)
                else:
                    raise ProcessingError.for_field_type(bool, field, value)

            processed_dict[field] = processed_value

        if processed_dict:
            yield processed_dict


def _validate(iterable, *, type_):
    list_len = None
    for item in iterable:
        if not isinstance(item, type_):
            raise DictFormatError(
                "all dictionary values must be of the same type "
                "(supported: dict, list)"
            )
        if type_ is list:
            length = len(item)
            list_len = list_len or length
            if list_len != length:
                raise DictFormatError(
                    "for a dict of lists, all lists must have equal length"
                )
        yield item


class Binder(collections.abc.MutableSequence):
    singles = IterableOf(Single)

    def __init__(self, singles):
        self.singles = singles

    def __getitem__(self, index):
        if isinstance(index, slice):
            return type(self)(self.singles[index])
        return self.singles[index]

    def __setitem__(self, index, value):
        if not isinstance(value, Single):
            raise TypeError
        self.singles[index] = value

    def __delitem__(self, index):
        del self.singles[index]

    def __len__(self):
        return len(self.singles)

    def insert(self, index, value):
        if not isinstance(value, Single):
            raise TypeError
        self.singles.insert(index, value)

    def __eq__(self, other):
        if not isinstance(other, Binder):
            return NotImplemented
        return self.singles == other.singles

    def __add__(self, other):
        if not isinstance(other, Binder):
            return NotImplemented
        return type(self)(self.singles + other.singles)

    def __repr__(self):
        cls = self.__class__.__name__
        size = len(self)
        indent = 4 * " "
        if size < 2:
            repr_string = f"{cls}({self.singles})"
        elif 2 <= size < 6:
            singles_string = f",\n{indent}".join(map(repr, self.singles))
            repr_string = f"{cls}([\n{indent}{singles_string},\n])"
        elif size >= 6:
            keep = 2
            omitted = size - 2*keep
            assert omitted > 1
            start_chunk = (
                f"{indent}{self.singles[0]!r},\n"
                f"{indent}{self.singles[1]!r},\n"
            )
            omitted_chunk = f"{indent}# ... omitted {omitted} items ...\n"
            end_chunk = (
                f"{indent}{self.singles[-2]!r},\n"
                f"{indent}{self.singles[-1]!r},\n"
            )
            singles_string = start_chunk + omitted_chunk + end_chunk
            repr_string = f"{cls}([\n{singles_string}])"
        return repr_string

    @staticmethod
    def create_csv_template(filepath):
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(_CSV_TEMPLATE)

    @classmethod
    def from_csv(cls, filepath):
        with open(filepath, "r", newline="") as file:
            reader = csv.DictReader(file)

            field_count = collections.Counter(reader.fieldnames)
            duplicate_fields = [
                field for field, count in field_count.items() if count > 1
            ]
            if duplicate_fields:
                raise CSVFormatError.for_duplicate_fields(
                    reader.fieldnames, duplicate_fields
                )

            missing_required_fields = [
                field for field in Field.get_required()
                if field not in reader.fieldnames
            ]
            if missing_required_fields:
                raise CSVFormatError.for_missing_required_fields(
                    reader.fieldnames, missing_required_fields
                )

            try:
                binder = cls(Single(**row) for row in _process(reader))
            except ProcessingError as pe:
                raise CSVProcessingError.from_processing_error(pe) from None

        return binder

    def to_csv(self, filepath):
        with open(filepath, "w", encoding="utf-8") as file:
            csv_writer = csv.DictWriter(file, fieldnames=Field)
            csv_writer.writeheader()
            csv_writer.writerows(single.to_dict() for single in self)

    @classmethod
    def from_dict(cls, dictionary):
        first_value = next(iter(dictionary.values()))
        if isinstance(first_value, dict):
            print("TODO: dict of dict")
            return cls([])

        elif isinstance(first_value, list):
            attributes = list(dictionary.keys())
            validated_values = _validate(dictionary.values(), type_=list)
            values_collection = zip(*(values for values in validated_values))
            kwargs_collection = (
                dict(zip(attributes, values)) for values in values_collection
            )
            try:
                binder = cls(
                    Single(**kwargs) for kwargs in _process(kwargs_collection)
                )
            except ProcessingError as pe:
                raise DictProcessingError.from_processing_error(pe) from None
            return binder

    def to_dict(self):
        binder_default_dict = collections.defaultdict(dict)
        for i, single in enumerate(self):
            for attribute, value in single.to_dict().items():
                binder_default_dict[attribute][i] = value
        return dict(binder_default_dict)
