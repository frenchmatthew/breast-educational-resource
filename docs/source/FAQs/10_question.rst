Why the route is  `model-heart`?
======================================

- Let's look at the `topics.json` file under ./frontend/assets/data/topics.json

    .. code-block:: json
        :linenos:

        {
            "model": {
                "title": "Template",
                "heading": "Te Manawa",
                "icon": "mdi-home",
                "subTopics": {
                    "heart": {
                    "title": "Home",
                    "heading": "Heading",
                    "icon": "mdi-home-heart",
                    "dataFile": "heart-main",
                    "category": "success",
                    "subTitle": "subSuccess",
                    "model": { "name": "NoInfarct" }
                    }
                }
        },

In here, you can see the first key of the root dictionary is `model` and the first subTopics key is `heart`, thus the first routes is `model-heart`.

You can modify those key in json file to change to your own routes.

Notice, after you change the first route, you still need to change the route in `middleware`, under `./frontend/pages/index.vue` line 6.