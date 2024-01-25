from app.models.inventory_log import InventoryLog, get_category_by_key
from app.serializers.inv_log_serializer import InventoryLogSchema, UpdateInventoryLogSchema
import uuid
from datetime import datetime
from app import db
from sqlalchemy import update
from sqlalchemy import cast, Integer


class InvLogUtils:

    @staticmethod
    def create_inv_log(request, product_id):
        inv_log_data = request.get_json().get('inv_log_details')
        # validate using serializer
        InventoryLogSchema().load(inv_log_data)
        inv_log_data['warehouseID'] = uuid.uuid4()
        inv_log_data['productID'] = product_id
        inv_log_data['category'] = get_category_by_key(inv_log_data.get('category'))
        inv_log_data['addInventoryDate'] = datetime.now()
        inv_log_entry = InventoryLog(**inv_log_data)
        db.session.add(inv_log_entry)
        db.session.commit()
        return {"id": inv_log_entry.id, "quantity": inv_log_data.get('quantity')}

    @staticmethod
    def update_inventory_log(request):

        inv_log_data = request.get_json().get('inv_log_details')
        inv_log_id = inv_log_data.get('id')

        # validate using serializer
        UpdateInventoryLogSchema().load(inv_log_data)
        inv_log = InventoryLog.query.filter_by(id=cast(inv_log_data.get('id'), Integer)).first()
        if not inv_log:
            raise Exception("Inventory log not found")

        # Define the update query
        category_obj = get_category_by_key(inv_log_data.get('category'))
        if not category_obj:
            raise Exception("Inventory category not found")

        # op id from update data
        inv_log_data.pop('id')

        # set category object
        inv_log_data['category'] = category_obj
        update_query = (
            update(InventoryLog)
            .where(InventoryLog.id == inv_log_id)  # Pass the productID
            .values(inv_log_data)  # Pass the dictionary containing the new values
        )
        # Execute the update query
        db.session.execute(update_query)
        db.session.commit()
        return {"id": inv_log.id, "quantity": inv_log.quantity, "category": inv_log.category.value}
