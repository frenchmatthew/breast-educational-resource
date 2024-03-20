Backend
=========

The backend is using Fastapi, and the python version is 3.9+.

- Design API
    - Send json object to frontend

    .. code-block:: python
            :linenos:

            @app.get("/hello/{name}")
            async def say_hello(name: str):
                return {"message": f"Hello {name}"}
    
    - In frontend we can use :red:`fetch` to make a request to backend

    .. code-block:: JavaScript
            :linenos:

             async fetch() {
                const helloworld = await fetch(
                    'http://127.0.0.1:8000/hello/model'
                ).then(res => res.json())
                console.log(helloworld);
            },

    - Send mesh file to frontend

    .. code-block:: python
            :linenos:

            @app.get("/api/model")
            async def get_display_model():
                model_path = "./data/mask.obj"
                file_res = FileResponse(model_path, media_type="application/octet-stream", filename="mask.obj")
                return file_res

    - Receive mesh in frontend via blob

    .. code-block:: JavaScript
            :linenos:

            async fetch() {
                const model = await fetch(
                    'http://127.0.0.1:8000/api/model'
                ).then(res => res.blob())
                console.log(model);
            },