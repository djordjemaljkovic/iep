from functools import wraps

from flask import Response, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt


def roleCheck(role):
    def innerRole(func):
        @wraps(func)
        def decorator(*arguments, **keywordArguments):
            verify_jwt_in_request();
            claims = get_jwt();
            if (("role" in claims) and (role in claims["role"])):
                return func(*arguments, **keywordArguments);
            return jsonify(message="Missing Authorization Header"), 401;
        return decorator;
    return innerRole;

def customerCheck(isCustomer):
    def innerCustomer(func):
        @wraps(func)
        def decorator(*arguments, **keywordArguments):
            verify_jwt_in_request();
            claims = get_jwt();
            if (("isCustomer" in claims) and (claims["isCustomer"] == isCustomer)):
                return func(*arguments, **keywordArguments);
            else:
                return jsonify(msg="Missing Authorization Header"), 401;
        return decorator;
    return innerCustomer;

