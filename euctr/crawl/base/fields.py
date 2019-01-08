# -*- coding: utf-8 -*-
import sqlalchemy as sa
from scrapy import Field
from six import add_metaclass
from abc import ABCMeta, abstractmethod
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from . import helpers


@add_metaclass(ABCMeta)
class Base(Field):

    # Public

    def __init__(self, primary_key=False):
        self.__primary_key = primary_key

    def __repr__(self):
        return type(self).__name__

    @property
    @abstractmethod
    def column_type(self):
        pass  # pragma: no cover

    @property
    def primary_key(self):
        return self.__primary_key

    def parse(self, value):
        return value


class Text(Base):

    # Public

    column_type = sa.Text


class Integer(Base):

    # Public

    column_type = sa.Integer

    def parse(self, value):
        if value is None:
            return None
        return int(value)


class Boolean(Base):

    # Public

    column_type = sa.Boolean

    def __init__(self, true_value=None, **params):
        super(Boolean, self).__init__(**params)
        self.__true_value = true_value

    def parse(self, value):
        if value is None:
            return None
        if self.__true_value is not None:
            value = (value.lower() == self.__true_value.lower())
        return value



class Date(Base):

    # Public

    column_type = sa.Date

    def __init__(self, formats, **params):
        super(Date, self).__init__(**params)
        if not isinstance(formats, (list, tuple)):
            formats = [formats]
        self.__formats = formats

    def parse(self, value):
        if value is None:
            return None
        for i, fmt in enumerate(self.__formats):
            try:
                return helpers.parse_date(value, format=fmt)
            except ValueError:
                pass
        msg = "time data '{value}' doesn't match any of the formats: {formats}"
        raise ValueError(msg.format(value=value, formats=self.__formats))


class Datetime(Base):

    # Public

    column_type = sa.DateTime(timezone=True)

    def __init__(self, format=None, **params):
        super(Datetime, self).__init__(**params)
        self.__format = format

    def parse(self, value):
        if value is None:
            return None
        if self.__format is not None:
            value = helpers.parse_datetime(value, format=self.__format)
        return value


class Json(Base):

    # Public

    column_type = JSONB


class Array(Base):

    # Public

    def __init__(self, field=None, **params):
        super(Array, self).__init__(**params)
        if field is None:
            field = Text()
        self.__field = field
        self.__column_type = ARRAY(field.column_type)

    @property
    def column_type(self):
        return self.__column_type

    def parse(self, value):
        if value is None:
            return None
        result = []
        for item in value:
            result.append(self._field.parse(item))
        return result
