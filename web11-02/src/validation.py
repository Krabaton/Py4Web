from marshmallow import Schema, fields, ValidationError, validate


class RegistrationSchema(Schema):
    nick = fields.Str(validate=validate.Length(min=3), required=True)
    email = fields.Email()
    password = fields.Str(validate=validate.Length(min=6), required=True)


class LoginSchema(Schema):
    email = fields.Email()
    password = fields.Str(validate=validate.Length(min=6), required=True)
    remember = fields.Str()