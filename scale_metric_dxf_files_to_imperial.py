import ezdxf
import os
import numpy as np  # Import NumPy to handle the arrays

def scale_dxf(input_path, output_path, scale_factor):
    # Load DXF file
    try:
        doc = ezdxf.readfile(input_path)
    except Exception as e:
        print(f"Failed to load {input_path}: {e}")
        return

    # Loop through all entities in the model space and apply scaling
    for entity in doc.modelspace().query('LINE CIRCLE ARC LWPOLYLINE POLYLINE TEXT MTEXT'):
        if entity.dxftype() == 'LINE':
            entity.dxf.start = (entity.dxf.start.x * scale_factor, entity.dxf.start.y * scale_factor)
            entity.dxf.end = (entity.dxf.end.x * scale_factor, entity.dxf.end.y * scale_factor)
        elif entity.dxftype() in ['CIRCLE', 'ARC']:
            entity.dxf.center = (entity.dxf.center.x * scale_factor, entity.dxf.center.y * scale_factor)
            entity.dxf.radius = entity.dxf.radius * scale_factor
        elif entity.dxftype() == 'TEXT' or entity.dxftype() == 'MTEXT':
            entity.dxf.insert = (entity.dxf.insert.x * scale_factor, entity.dxf.insert.y * scale_factor)
        elif entity.dxftype() == 'LWPOLYLINE':
            for vertex in entity:
                if isinstance(vertex, np.ndarray):
                    vertex[0] *= scale_factor
                    vertex[1] *= scale_factor
                else:
                    vertex.x *= scale_factor
                    vertex.y *= scale_factor
        elif entity.dxftype() == 'POLYLINE':
            for vertex in entity.vertices():
                if isinstance(vertex, np.ndarray):
                    vertex[0] *= scale_factor
                    vertex[1] *= scale_factor
                else:
                    vertex.x *= scale_factor
                    vertex.y *= scale_factor

    # Save the modified DXF file
    doc.saveas(output_path)

def batch_scale_dxf(scale_factor):
    # Get the current folder where the script is located
    directory = os.path.dirname(os.path.realpath(__file__))
    
    # List all DXF files in the directory
    for filename in os.listdir(directory):
        if filename.lower().endswith(".dxf"):
            input_path = os.path.join(directory, filename)
            
            # Debug: Print the input path
            print(f"Processing file: {input_path}")
            
            # Add "imperial_" before the original file name
            output_path = os.path.join(directory, "imperial_" + filename)
            scale_dxf(input_path, output_path, scale_factor)
            print(f"Scaled {filename} and saved as {output_path}")

# Example usage
scale_factor = 0.03937  # Set the scale factor to 0.03937
batch_scale_dxf(scale_factor)
