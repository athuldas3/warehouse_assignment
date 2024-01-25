from marshmallow import Schema, fields, validate


class ProductMetaSchema(Schema):
    productName = fields.String(required=True, validate=validate.Length(max=255))


class UpdateProductMetaSchema(Schema):
    id = fields.Integer(required=True)
    productName = fields.String(required=True, validate=validate.Length(max=255))
