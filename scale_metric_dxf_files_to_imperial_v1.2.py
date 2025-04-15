import ezdxf
import os
from datetime import datetime

# Logging function — logs to file and prints
def log(message, log_file="scaling_log.txt"):
    print(message)
    with open(log_file, "a") as f:
        f.write(f"{datetime.now()} - {message}\n")

def scale_dxf(input_path, output_path, scale_factor):
    try:
        doc = ezdxf.readfile(input_path)
    except Exception as e:
        log(f"Failed to load {input_path}: {e}")
        return

    for entity in doc.modelspace().query('LINE CIRCLE ARC LWPOLYLINE POLYLINE TEXT MTEXT'):
        try:
            if entity.dxftype() == 'LINE':
                entity.dxf.start = (
                    entity.dxf.start.x * scale_factor,
                    entity.dxf.start.y * scale_factor,
                    entity.dxf.start.z * scale_factor,
                )
                entity.dxf.end = (
                    entity.dxf.end.x * scale_factor,
                    entity.dxf.end.y * scale_factor,
                    entity.dxf.end.z * scale_factor,
                )

            elif entity.dxftype() in ['CIRCLE', 'ARC']:
                entity.dxf.center = (
                    entity.dxf.center.x * scale_factor,
                    entity.dxf.center.y * scale_factor,
                    entity.dxf.center.z * scale_factor,
                )
                entity.dxf.radius *= scale_factor

            elif entity.dxftype() in ['TEXT', 'MTEXT']:
                entity.dxf.insert = (
                    entity.dxf.insert.x * scale_factor,
                    entity.dxf.insert.y * scale_factor,
                    entity.dxf.insert.z * scale_factor,
                )

            elif entity.dxftype() == 'LWPOLYLINE':
                elevation = entity.dxf.elevation if entity.dxf.hasattr("elevation") else 0
                for i, (x, y, *rest) in enumerate(entity):
                    entity[i] = (x * scale_factor, y * scale_factor, *rest)
                entity.dxf.elevation = elevation * scale_factor

            elif entity.dxftype() == 'POLYLINE':
                for vertex in entity.vertices:
                    loc = vertex.dxf.location
                    vertex.dxf.location = (
                        loc.x * scale_factor,
                        loc.y * scale_factor,
                        loc.z * scale_factor,
                    )

        except Exception as e:
            log(f"Error scaling entity {entity.dxftype()}: {e}")

    try:
        doc.saveas(output_path)
        log(f"Scaled {os.path.basename(input_path)} and saved as {output_path}")
    except Exception as e:
        log(f"Failed to save {output_path}: {e}")

def batch_scale_dxf(scale_factor):
    directory = os.path.dirname(os.path.realpath(__file__))

    # Clear log file at start
    with open("scaling_log.txt", "w") as f:
        f.write("DXF Scaling Log\n====================\n")

    for filename in os.listdir(directory):
        if filename.lower().endswith(".dxf"):
            input_path = os.path.join(directory, filename)
            log(f"Processing file: {input_path}")
            output_path = os.path.join(directory, "imperial_" + filename)
            scale_dxf(input_path, output_path, scale_factor)

# Example usage
scale_factor = 0.03937  # Scale from mm to inches
batch_scale_dxf(scale_factor)
