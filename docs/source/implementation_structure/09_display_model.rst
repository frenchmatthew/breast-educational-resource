Display model on pages
==========================

There two ways we can display a `.obj` 3D model in pages - `copper3d <https://github.com/LinkunGao/copper3d_visualisation>`_ or `threejs <https://threejs.org/docs/#manual/en/introduction/Creating-a-scene>`_

Let's look at the `Model.vue` file.

- copper3d
    - setup copper3d, have a look at `/plugins/copper.js`
    - let's config copper3d in `Model.vue`, mounted function.

    .. code-block:: javascript
            :linenos:

             mounted() {
                this.Copper = this.$Copper();
                this.baseRenderer = this.$baseRenderer();
                const baseContainer = this.$baseContainer();
                this.container = this.$refs.baseDomObject;
                setTimeout(() => {
                    this.mdAndUp
                        ? (baseContainer.style.height = "100vh")
                        : (baseContainer.style.height = "100vw");
                    this.container.appendChild(baseContainer);
                    this.start();
                }, 100);

                // when window resize, we need to resize the scene
                window.addEventListener("resize", () => {
                setTimeout(() => {
                    this.mdAndUp
                    ? (baseContainer.style.height = "100vh")
                    : (baseContainer.style.height = "100vw");
                    this.scene.onWindowResize();
                }, 500);
                });
            },
        

    - Then let's write the start function in `methods`

        .. code-block:: javascript
            :linenos:

            async start(){
                console.log("load model functions.");
                
                // get model from backend
                this.model = await fetch(
                    'http://127.0.0.1:8000/api/model'
                ).then(res => res.blob())

                const model_url = URL.createObjectURL(this.model) 

                this.loadModel(model_url,"test");
            },

    - After we get model from backend, let's load the model

         .. code-block:: javascript
            :linenos:

            loadModel(model_url, model_name) {

            const viewURL = 'modelView/noInfarct_view.json';

            this.scene = this.baseRenderer.getSceneByName(model_name);
            if (this.scene === undefined) {
                this.scene = this.baseRenderer.createScene(model_name);
                // this.scene.controls.staticMoving = true;
                // this.scene.controls.rotateSpeed = 3.0;
                // this.scene.controls.panSpeed = 3.0;
                this.baseRenderer.setCurrentScene(this.scene);
                this.scene.loadOBJ(model_url, (content) => {
                // this.scene.setModelPosition(content, { x: 5, y: 2 });
                console.log(content);
                });
                this.scene.loadViewUrl(viewURL);
            }
            this.scene.onWindowResize();
            },

    - Notice, if we found the model not in a correct position, we need to modify the its camera views.
        - In this case you can found the views in `/static/modelView/noInfarct_view.json`

        .. code-block:: javascript
            :linenos:
            
            {
                "farPlane": 1000,
                "targetPosition": [0, 0, 0],
                "nearPlane": 0.01,
                "upVector": [0, -1, 0],
                "eyePosition": [0, 0, -600]
            }

- threejs

    Let's look at the threejs documentation - `create a scene <https://threejs.org/docs/#manual/en/introduction/Creating-a-scene>`_
