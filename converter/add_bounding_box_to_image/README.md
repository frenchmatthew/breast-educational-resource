# Installation   

Install python dependencies:   

``` 
pip install -r requirements.txt 
``` 

Install the breast-metadata package:

```  
git clone https://github.com/abi-breast-biomechanics-group/breast-metadata
cd breast-metadata 
pip install -e . 
```  

# Usage   

``` 
cd add_bounding_box_to_image  
python add_bounding_box_to_image.py --config <path to configuration file> 
```

See the template configuration file (template_config_file.json) for an example of how to set up the configuration file.  
