Load Data from Backend
========================

There are multiple ways that we can get data from backend.

- First, make sure your backend has already started.
    - You can simply test your backend if is started on broswer via `http://127.0.0.1:8000`.
    - If the backend runs well, you will see `{"message": "Hello World"}` on the broswer.

- Then, let's connect backend from frontend, in Model.vue file (acturelly, you can connect the backend in any file, the code is same).
    - There are two ways (fetch, axios) that we can use to connect the backend.
    - Via `fetch`:
        You may notice there is a `async fetch()` function in Model.vue file, we can write the fetch function in it. 

        The benefit for us to make a request in the fetch function is the nuxt will run `async fetch()` before render the html, so we can get the data more fast.

        .. code-block:: javascript
            :linenos:

            async fetch() {
                 this.helloworld = await fetch(
                     'http://127.0.0.1:8000/hello/model'
                   ).then(res => res.json())
                   console.log(this.helloworld);
                
                   this.model = await fetch(
                     'http://127.0.0.1:8000/api/model'
                   ).then(res => res.blob())

                   console.log(this.model);
            },
        

        Also, we can write the fetch function in other area, e.g, in `created` or `method`:

        - created:

        .. code-block:: javascript
            :linenos:

            created: async function (){
                this.model = await fetch(
                    'http://127.0.0.1:8000/api/model'
                ).then(res => res.blob())
            },

        - method:

        .. code-block:: javascript
            :linenos:

            mounted() {
                this.start();
            },

            methods: {
                async start(){
                    this.model = await fetch(
                        'http://127.0.0.1:8000/api/model'
                    ).then(res => res.blob())

                    console.log(this.model);
                }
            },

    - Expect `fetch`, we also can use `axios` to make a request to backend.
        - if we want use `axios`, we need to import it. Here is the `Axios documentation <https://axios-http.com/docs/intro>`_

        .. code-block:: html
            :linenos:

            <script>
                import axios from "axios";
            </script>
        
        - Then we can do the same things as `fetch` function.
            - Under `async fetch()`:

             .. code-block:: javascript
                :linenos:

                async fetch() {
                    await axios.get('http://127.0.0.1:8000/hello/model').then((res)=>{
                        console.log(res.data);
                    })
                    await axios.get('http://127.0.0.1:8000/api/model',{ responseType: "blob" }).then((res)=>{
                        this.model = res.data;
                    })

                    console.log(this.model);
                },

            - In created:


                .. code-block:: javascript
                    :linenos:

                    created: async function (){
                         await axios.get('http://127.0.0.1:8000/api/model',{ responseType: "blob" }).then((res)=>{
                            this.model = res.data;
                        })
                    },

            - In method:

                .. code-block:: javascript
                    :linenos:

                    mounted() {
                        this.start();
                    },

                    methods: {
                        async start(){
                            await axios.get('http://127.0.0.1:8000/api/model',{ responseType: "blob" }).then((res)=>{
                                this.model = res.data;
                             })

                            console.log(this.model);
                        }
                    },