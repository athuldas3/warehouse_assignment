from app.models.seller import SellerMeta
from app.serializers.seller_serializer import SellerMetaSchema, UpdateSellerMetaSchema
from datetime import datetime
from app import db
from sqlalchemy import update
from sqlalchemy import cast, Integer


class SellerUtils:

    @staticmethod
    def create_seller(request):
        seller_data = request.get_json().get('seller_details')
        # # validate using serializer
        SellerMetaSchema().load(seller_data)
        # seller_data['sellerID'] = uuid.uuid4()
        seller_data['registrationDate'] = datetime.now()
        seller_entry = SellerMeta(**seller_data)
        db.session.add(seller_entry)
        db.session.commit()
        return {"sellerID": seller_entry.sellerID, "sellerName": seller_data.get('sellerName')}

    @staticmethod
    def update_seller(request):
        # Extract and validate seller data from the request JSON
        updated_seller_data = request.get_json().get('seller_details')
        seller_id = updated_seller_data.get('id')

        # validation
        UpdateSellerMetaSchema().load(updated_seller_data)

        # Retrieve the seller to update from the database
        seller = SellerMeta.query.filter_by(sellerID=cast(updated_seller_data.get('id'), Integer)).first()
        if not seller:
            raise Exception("Seller not found")

        # Define the update query
        updated_seller_data.pop('id')
        update_query = (
            update(SellerMeta)
            .where(SellerMeta.sellerID == seller_id)  # Pass the sellerID as a string
            .values(updated_seller_data)  # Pass the dictionary containing the new values
        )
        # Execute the update query
        db.session.execute(update_query)
        db.session.commit()
        return {"id": seller.sellerID, "sellerName": seller.sellerName, "sellerGST": seller.sellerGST}



