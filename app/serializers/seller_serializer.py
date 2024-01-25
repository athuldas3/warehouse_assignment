from marshmallow import Schema, fields, validate


class SellerMetaSchema(Schema):
    sellerName = fields.String(required=True, validate=validate.Length(max=255))
    sellerGST = fields.String(required=True, validate=validate.Length(max=15))


class UpdateSellerMetaSchema(Schema):
    id = fields.Integer(required=True)
    sellerName = fields.String(required=True, validate=validate.Length(max=255))
    sellerGST = fields.String(required=True, validate=validate.Length(max=15))
