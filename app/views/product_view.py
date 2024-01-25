from app import db
from flask import jsonify
from app.views.utilities.inv_log_utils import InvLogUtils
from app.views.utilities.product_utils import ProductUtils
from app.views.utilities.seller_utils import SellerUtils


def get_weekly_products(request):
    try:
        return ProductUtils().get_weekly_products_count(request)
    except Exception as e:
        return {'error': str(e)}, 500


def create_seller_product_inv_log(request):
    try:
        # Add seller data
        seller_data = SellerUtils().create_seller(request)
        # Add product data
        product_data = ProductUtils().create_product(request, seller_data.get('sellerID'))
        # Create inventory log
        inv_log_data = InvLogUtils().create_inv_log(request, product_data.get('productID'))

        return jsonify({"seller_details": seller_data, "product_details": product_data,
                        "inv_log_details": inv_log_data}), 200

    except Exception as e:
        # If any exception occurs, roll back the transaction
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


def update_seller_product_inv_log(request):

    try:
        seller_data = SellerUtils().update_seller(request)
        product_data = ProductUtils().update_product(request)
        inv_log_data = InvLogUtils().update_inventory_log(request)

        return jsonify({"seller_details": seller_data, "product_details": product_data,
                        "inv_log_details": inv_log_data}), 200

    except Exception as e:
        # If any exception occurs, roll back the transaction
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
