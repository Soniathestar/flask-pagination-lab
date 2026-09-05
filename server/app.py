#!/usr/bin/env python3

from flask import request, session, jsonify, make_response
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

import os
from config import create_app, db, api
from models import Book, BookSchema

env = os.getenv("FLASK_ENV", "dev")
app = create_app(env)

class Books(Resource):
    def get(self):
        # Parse and sanitize query params, falling back to sensible defaults
        try:
            page = int(request.args.get('page', 1))
        except (TypeError, ValueError):
            page = 1

        try:
            per_page = int(request.args.get('per_page', 5))
        except (TypeError, ValueError):
            per_page = 5

        # Guard against nonsensical or abusive values
        page = max(page, 1)
        per_page = max(min(per_page, 100), 1)

        

        pagination = Book.query.paginate(
            page=page, per_page=per_page, error_out=False
        )

        books = [BookSchema().dump(b) for b in pagination.items]

        return {
            "page": page,
            "per_page": per_page,
            "total": pagination.total,
            "total_pages": pagination.pages,
