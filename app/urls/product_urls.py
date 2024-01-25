from flask import request
from app import app
from app.views.product_view import get_weekly_products, create_seller_product_inv_log, update_seller_product_inv_log
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.custom_decorators.check_required_fields import check_required_fields
from app.custom_decorators.role_required import roles_required


@app.route('/products/weekly', methods=['GET'])
@jwt_required()
@roles_required(['PM', 'RM'])
def products():
    return get_weekly_products(request)


@app.route('/create/sellers/products/inv-log', methods=['POST'])
@check_required_fields(['seller_details', 'product_details', 'inv_log_details'])
@jwt_required()
@roles_required(['PM', 'RM'])
def add_seller_products_inv_log():
    return create_seller_product_inv_log(request)


@app.route('/update/sellers/products/inv-log', methods=['PUT'])
@check_required_fields(['seller_details', 'product_details', 'inv_log_details'])
@jwt_required()
@roles_required(['PM', 'RM'])
def put_seller_products_inv_log():
    return update_seller_product_inv_log(request)
