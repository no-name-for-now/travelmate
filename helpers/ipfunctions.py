from flask import request
def get_ip():
    if "X-Forwarded-For" in request.headers:
        return request.headers.getlist("X-Forwarded-For")[0].rpartition(' ')[-1]
    elif "X-Real-IP" in request.headers:
        return request.headers.getlist("X-Real-IP")[0]
    else:
        return request.remote_addr
