from app.serializers.product_serializer import ProductMetaSchema, UpdateProductMetaSchema
from app.models.inventory_log import InventoryLog
from app.models.product import ProductMeta
from app.models.seller import SellerMeta
from datetime import datetime
from sqlalchemy import func
from collections import defaultdict
from app import db
from sqlalchemy import update
from sqlalchemy import cast, Integer


class ProductUtils:

    @staticmethod
    def create_product(request, seller_id):
        product_data = request.get_json().get('product_details')
        # validate using serializer
        ProductMetaSchema().load(product_data)
        product_data['sellerID'] = seller_id
        product_data['onboardInventoryDate'] = datetime.now()
        # validation using serializer
        product_entry = ProductMeta(**product_data)
        db.session.add(product_entry)
        db.session.commit()
        return {"productID": product_entry.productID, "productName": product_data.get('productName')}

    @staticmethod
    def update_product(request):
        product_data = request.get_json().get('product_details')
        product_id = product_data.get('id')

        # validate using serializer
        UpdateProductMetaSchema().load(product_data)

        # check product exists
        product = ProductMeta.query.filter_by(productID=cast(product_data.get('id'), Integer)).first()
        if not product:
            raise Exception("Product not found")

        # Define the update query
        product_data.pop('id')
        update_query = (
            update(ProductMeta)
            .where(ProductMeta.productID == product_id)  # Pass the productID
            .values(product_data)  # Pass the dictionary containing the new values
        )
        # Execute the update query
        db.session.execute(update_query)
        db.session.commit()
        return {"productID": product.productID, "productName": product.productName}

    @staticmethod
    def get_weekly_products_count(request):
        from datetime import datetime, timedelta
        # Parse input parameters from the request
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        seller_name = request.args.get('seller_name')

        # Convert date strings to datetime objects
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d') if start_date_str else None
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d') if end_date_str else None

        # Initialize the base query
        base_query = db.session.query(
            func.date_trunc('week', InventoryLog.addInventoryDate).label('week_start'),
            func.sum(InventoryLog.quantity).label('total_quantity')
        ).join(ProductMeta)

        # Add filters based on the presence of parameters
        if seller_name:
            seller = SellerMeta.query.filter_by(sellerName=seller_name).first()
            if seller:
                base_query = base_query.filter(
                    func.cast(ProductMeta.sellerID, db.String()) == str(seller.sellerID)
                )

        if start_date:
            base_query = base_query.filter(func.date_trunc('week', InventoryLog.addInventoryDate) >= start_date)

        if end_date:
            base_query = base_query.filter(func.date_trunc('week', InventoryLog.addInventoryDate) <= end_date)

        # Execute the query and retrieve the results
        query_result = base_query.group_by(func.date_trunc('week', InventoryLog.addInventoryDate)).all()

        # Process the query result to create the response
        response = defaultdict(int)
        current_week_start = start_date - timedelta(days=start_date.weekday())
        while current_week_start <= end_date:
            current_week_end = current_week_start + timedelta(days=6)
            week_label = f"Week({current_week_start.strftime('%Y-%m-%d')} - {current_week_end.strftime('%Y-%m-%d')})"
            response[week_label] = 0  # Initialize count to 0
            for result in query_result:
                week_start = result.week_start
                if current_week_start <= week_start <= current_week_end:
                    response[week_label] = result.total_quantity
                    break
            current_week_start += timedelta(days=7)

        return response
