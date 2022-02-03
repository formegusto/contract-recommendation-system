import requests as req


def update_process(type):
    def decorator(func):
        def wrap(*args, **kwargs):
            api_server = "http://localhost:8080"
            update_path = "/process"

            # try:
            #     result = func(*args, **kwargs)

            #     req.patch(api_server + update_path, json={
            #         "type": type,
            #         "status": True
            #     })

            #     return result
            # except:
            #     req.patch(api_server + update_path, json={
            #         "type": type,
            #         "status": False
            #     })
            #     return
            result = func(*args, **kwargs)

            req.patch(api_server + update_path, json={
                "type": type,
                "status": True
            })

            return result
        return wrap
    return decorator
