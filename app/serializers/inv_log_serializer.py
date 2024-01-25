from marshmallow import fields, Schema


class InventoryLogSchema(Schema):
    quantity = fields.Integer(required=True)
    category = fields.String(required=True)


class UpdateInventoryLogSchema(Schema):
    id = fields.Integer(required=True)
    quantity = fields.Integer(required=True)
    category = fields.String(required=True)
