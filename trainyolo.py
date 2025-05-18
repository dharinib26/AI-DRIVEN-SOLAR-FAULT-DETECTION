from ultralytics import YOLO


model = YOLO('yolo11n.pt')  # Load a pre-trained model (YOLO11n nano)

# Set up training parameters
model.train(
    data='datasets/data.yaml',  # Path to the dataset YAML file
    epochs=10,                  # Number of epochs
    imgsz=440,                  # Image size (640x640 in this case)
    batch=2                    # Batch size
    #device=1                    # Use GPU 0 (set device=-1 for CPU)
)
