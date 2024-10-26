
import collections
import csv
from vendor.single import Single
from vendor.enums import CSVField
from vendor.exceptions import CSVProcessingError


def _process(dict_reader):
    for row in dict_reader:
        processed_row = {}
        for key, value in row.items():
            if value == "":
                continue
            try:
                field = CSVField(key)
            except ValueError:
                continue

            if field.is_string:
                processed_value = value
            elif field.is_integer:
                try:
                    processed_value = int(value)
                except ValueError:
                    csv_error = CSVProcessingError(
                        f"invalid value '{value}' for field '{field}'; "
                        f"must be integer or empty",
                    )
                    raise csv_error from None
            elif field.is_boolean:
                if value.lower() == "yes":
                    processed_value = True
                elif value.lower() == "no":
                    processed_value = False
                else:
                    csv_error = CSVProcessingError(
                        f"invalid value '{value}' for field '{field}'; "
                        f"must be 'yes', 'no', or empty",
                    )
                    raise csv_error from None
            processed_row[field.as_arg()] = processed_value

        if processed_row:
            yield processed_row


def _validate(iterable):
    for item in iterable:
        if isinstance(item, Single):
            yield item
        else:
            raise TypeError(
                "direct instantiation of Binder requires "
                "iterable of Single objects"
            )


class Binder(collections.abc.MutableSequence):
    def __init__(self, singles):
        self.singles = list(_validate(singles))

    def __getitem__(self, index):
        if isinstance(index, slice):
            return type(self)(self.singles[index])
        return self.singles[index]

    def __setitem__(self, index, value):
        self.singles[index] = value

    def __delitem__(self, index):
        del self.singles[index]

    def __len__(self):
        return len(self.singles)

    def insert(self, index, value):
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
        if size >= 6:
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

    @classmethod
    def create_csv_template(cls, filepath):
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(cls._CSV_TEMPLATE)

    @classmethod
    def from_csv(cls, filepath):
        with open(filepath, "r", newline="") as file:
            return cls(Single(**row) for row in _process(csv.DictReader(file)))

    def to_csv(self, filepath):
        """Save singles in binder to CSV, account for articles."""

    _CSV_TEMPLATE = (
        'Name,Set,Language,Condition,First Edition,Signed,Altered,Version,Rarity,Rare Color,Language Code,Article Page,Comment\n'
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
