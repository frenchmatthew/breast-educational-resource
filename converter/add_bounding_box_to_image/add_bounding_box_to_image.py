import argparse 
import json 
import os
import numpy as np
import breast_metadata
import SimpleITK as sitk
import pyvista as pv 

def find_boundary_voxels(voxel, feature_radius): 
    # find the boundary voxels of the feature 
    boundary_voxels = [] 

    # find the boundary voxels in the x direction 
    for i in range(-feature_radius, feature_radius+1): 
        boundary_voxels.append((voxel[0] + i, voxel[1] - feature_radius, voxel[2])) 
        boundary_voxels.append((voxel[0] + i, voxel[1] + feature_radius, voxel[2])) 

    # find the boundary voxels in the y direction 
    for i in range(-feature_radius, feature_radius+1): 
        boundary_voxels.append((voxel[0] - feature_radius, voxel[1] + i, voxel[2])) 
        boundary_voxels.append((voxel[0] + feature_radius, voxel[1] + i, voxel[2]))  

    return boundary_voxels

def add_bounding_box(input_image, feature_centroid, feature_radius, line_thickness, box_colour, output_image):  

    # Load the medical_img image 
    medical_img = breast_metadata.Scan(input_image)       
    print(medical_img.spacing) 
    
    # ------------------------------------------------------- 
    # Work around for **DUCTAL** carcinoma MRI image for which the origin seems to be incorrect when compared to slicer and snapitk
    # medical_img.origin = (-168.6891, -172.5950, -95.2903)     
    # # also the anterior posterior axis is flipped 
    # medical_img.values = np.flip(medical_img.values, axis=1) 
    # # left and right axis is also been flipped 
    # medical_img.values = np.flip(medical_img.values, axis=0)  
    # ------------------------------------------------------- 

    # ------------------------------------------------------- 
    # # Work around for **Lobular** carcinoma MRI image for which the origin seems to be incorrect when compared to slicer and snapitk
    # medical_img.origin = (-153.5000, -190.6240, -113.6380)     
    # # also the anterior posterior axis is flipped 
    # medical_img.values = np.flip(medical_img.values, axis=1) 
    # # left and right axis is also been flipped 
    # medical_img.values = np.flip(medical_img.values, axis=0)  
    # -------------------------------------------------------

    # ------------------------------------------------------- 
    # Work around for tomography images which do not seem to like the Scan class (update Scan class later)

    # if the medical image values are empty, 
    # load the image from the path using SimpleITK (it will be a single dicom file)
    if medical_img.values.shape == (1, 1, 1):     
        print('Issue: Medical image values are empty')
        print('Defaulting to loading image using SimpleITK')
        # find file ending in .dcm  
        for file in os.listdir(input_image): 
            if file.endswith('.dcm'): 
                medical_img_sitk = sitk.ReadImage(os.path.join(input_image, file)) 
                break 
        # convert the SimpleITK image to scan class  
        # get the pixel array from the SimpleITK image 
        # get the origin and spacing from the SimpleITK image  
        medical_img.values = sitk.GetArrayFromImage(medical_img_sitk) 
        medical_img.origin = medical_img_sitk.GetOrigin() 
        medical_img.spacing = medical_img_sitk.GetSpacing() 
        medical_img.values = np.swapaxes(medical_img.values, 0, 2)     
        medical_img.values = np.flip(medical_img.values, axis=0) 
        medical_img.values = np.flip(medical_img.values, axis=1)  
        
        # get the bit length of the image 
        print(f'Loaded image bit length: {medical_img_sitk.GetPixelIDTypeAsString()}') 
        print(f'Loaded image shape: {medical_img.values.shape}') 
        print(f'Loaded image origin: {medical_img.origin}') 
        print(f'Loaded image spacing: {medical_img.spacing}')     

        print('Setting numpy array to correct bit length') 
        print(f'Original bit length: {medical_img.values.dtype}') 

        # set numpy array (ie medical_img.values) to the correct bit length 
        # convert GetPixelIDTypeAsString to numpy dtype 
        if medical_img_sitk.GetPixelIDTypeAsString() == '16-bit unsigned integer': 
            medical_img.values = medical_img.values.astype(np.uint16) 
        elif medical_img_sitk.GetPixelIDTypeAsString() == '16-bit signed integer': 
            medical_img.values = medical_img.values.astype(np.int16)  
            
    # -------------------------------------------------------
    print(medical_img.values.shape)
    img_grid = breast_metadata.SCANToPyvistaImageGrid(medical_img, "RAI")     
 

    # calculate voxel coordinate of the feature centroid 
    voxel_feature_centroid = np.round((np.array(feature_centroid) - img_grid.origin) / img_grid.spacing).astype(int)     
    print(voxel_feature_centroid)    

    box_colour_val = 2.0**10 - 1.0 if box_colour == 'white' else 0.0 
    assert box_colour in ['white', 'black'], 'Invalid box colour'

    for d_radius in range(line_thickness+1):  
        voxels = find_boundary_voxels(voxel_feature_centroid, feature_radius + d_radius) 
        for voxel in voxels:   
            medical_img.values[voxel[0], voxel[1], voxel[2]] = box_colour_val
            for z_radius in range(feature_radius):  
                medical_img.values[voxel[0], voxel[1], voxel[2] + z_radius] = box_colour_val
                medical_img.values[voxel[0], voxel[1], voxel[2] - z_radius] = box_colour_val

    # ------------------------------------------------------- 
    # Work around to visualize the image inside app 
    if modality == 'MRI': 
        # reduce the size of the image to make it easier to visualize  
        center_voxel = np.array(medical_img.values.shape) // 2

        # remove all slices above or below the center slice (in x- / right-left- axis), depending on which side the feature is located 
        if voxel_feature_centroid[0] > center_voxel[0]:   
            print('Removing slices above the center slice')
            medical_img.values = medical_img.values[center_voxel[0]:, :, :]  
            medical_img.origin = (medical_img.origin[0] + (center_voxel[0] * medical_img.spacing[0]), medical_img.origin[1], medical_img.origin[2])
        else:  
            print('Removing slices below the center slice')
            medical_img.values = medical_img.values[:center_voxel[0], :, :]  
            medical_img.origin = (medical_img.origin[0], medical_img.origin[1], medical_img.origin[2]) 

    else:  
        assert modality == 'Tomo', 'Invalid modality'
    # -------------------------------------------------------  

    print(medical_img.origin)
    # save the image with the bounding box drawn on it  
    img_grid = breast_metadata.SCANToPyvistaImageGrid(medical_img, "RAI")
    img_grid.save(output_image + '.vti')   
    
    # Create sitk image  
    if modality == 'MRI':
        sitk_image = sitk.GetImageFromArray(np.swapaxes(medical_img.values.astype(np.float32), 2, 0))  
    else: 
        assert modality == 'Tomo', 'Invalid modality'
        sitk_image = sitk.GetImageFromArray(np.swapaxes(medical_img.values.astype(np.uint16), 2, 0))  

    sitk_image.SetSpacing(medical_img.spacing) 
    sitk_image.SetOrigin(medical_img.origin)  
    sitk.WriteImage(sitk_image, output_image + '.nrrd')      

    # save txt file with bounding box z-coordinate / transverse plane index  
    with open(output_image + '_slice_index.txt', 'w') as file: 
        file.write(str(voxel_feature_centroid[2]))  


    # ------------------------------------------------------- 
    # Downsampling the image for easier visualization in the app

    if modality == 'Tomo':
        # Save downsampled version by a factor of 2 
        downsampled_values = medical_img.values[::2, ::2, ::2] 
        downsampled_spacing = np.array(medical_img.spacing) * 2 
        downsampled_origin = list(medical_img.origin)
        downsampled_origin[0] += medical_img.spacing[0] 
        downsampled_origin[1] += medical_img.spacing[1] 
        downsampled_origin[2] += medical_img.spacing[2]  
        downsampled_img = sitk.GetImageFromArray(np.swapaxes(downsampled_values.astype(np.uint16), 2, 0)) 
        downsampled_img.SetSpacing(downsampled_spacing) 
        downsampled_img.SetOrigin(downsampled_origin) 
        sitk.WriteImage(downsampled_img, output_image + '_downsampled_2x2x2.nrrd')    

        with open(output_image + '_downsampled_slice_index.txt', 'w') as file: 
            file.write(str(voxel_feature_centroid[2] // 2)) 

        # save downsampled version by a factor of 2  
        # save without header information
        downsampled_values = medical_img.values[::2, ::2, ::2] 
        downsampled_img = sitk.GetImageFromArray(np.swapaxes(downsampled_values.astype(np.uint16), 2, 0))   
        sitk.WriteImage(downsampled_img, output_image + '_downsampled_2x2x2_empty_header.nrrd')

        # save downsampled image with a factor of 2x2x1   
        downsampled_values = medical_img.values[::2, ::2, :] 
        downsampled_spacing = np.array(medical_img.spacing) * np.array([2, 2, 1]) 
        downsampled_origin = list(medical_img.origin) 
        downsampled_origin[0] += medical_img.spacing[0] 
        downsampled_origin[1] += medical_img.spacing[1] 
        downsampled_img = sitk.GetImageFromArray(np.swapaxes(downsampled_values.astype(np.uint16), 2, 0)) 
        downsampled_img.SetSpacing(downsampled_spacing) 
        downsampled_img.SetOrigin(downsampled_origin) 
        sitk.WriteImage(downsampled_img, output_image + '_downsampled_2x2x1.nrrd')   

        with open(output_image + '_downsampled_slice_index_2x2x1.txt', 'w') as file: 
            file.write(str(voxel_feature_centroid[2]))

    # -------------------------------------------------------

    
        

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        prog='Add Bounding Box')

    parser.add_argument('-c',
                        '--config_file', 
                        type=str, 
                        help='Path to the medical_img image', 
                        required=True) 

    args = parser.parse_args()    

    config_file = args.config_file

    with open(config_file, 'r') as file: 
        config = json.load(file) 

    input_image = config['input_image'] 
    output_image = config['output_image']
    feature_centroid = config['feature_centroid (world coordinates)'] 
    feature_radius = config['feature_radius (voxels)'] 
    line_thickness = config['line_thickness (voxels)']   
    box_color = config['box_colour'] 
    modality = config['modality']

    add_bounding_box(input_image, feature_centroid, feature_radius, line_thickness, box_color, output_image)