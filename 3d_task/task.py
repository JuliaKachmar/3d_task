import vtk
import pydicom

# Load DICOM data
filename = "3d_task/file.dcm"
dcm = pydicom.dcmread(filename)

# Create VTK image data
data = vtk.vtkImageData()
data.SetDimensions(dcm.Rows, dcm.Columns, len(dcm.pixel_array))
data.SetSpacing((dcm.PixelSpacing[0], dcm.PixelSpacing[1], dcm.SliceThickness))
data.SetOrigin(dcm.ImagePositionPatient)

# Convert pixel data to VTK format
pixel_data = dcm.pixel_array.astype(float)
pixel_data = (pixel_data - pixel_data.min()) / (pixel_data.max() - pixel_data.min())
vtk_data = vtk.util.numpy_support.numpy_to_vtk(pixel_data.ravel(), deep=True, array_type=vtk.VTK_FLOAT)
vtk_data.SetNumberOfComponents(1)
data.GetPointData().SetScalars(vtk_data)

# Create VTK renderer and window
renderer = vtk.vtkRenderer()
renderer.SetBackground(0.2, 0.3, 0.4)
renderer.ResetCamera()
window = vtk.vtkRenderWindow()
window.AddRenderer(renderer)

# Create VTK volume from image data
volume_mapper = vtk.vtkFixedPointVolumeRayCastMapper()
volume_mapper.SetInputData(data)
volume = vtk.vtkVolume()
volume.SetMapper(volume_mapper)
renderer.AddVolume(volume)

# Display the window
window.Render()
