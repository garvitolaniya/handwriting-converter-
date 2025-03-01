import streamlit as st
from streamlit_drawable_canvas import st_canvas
import os
import datetime
from PIL import Image
import pandas as pd
import numpy as np

def save_image(image_data, folder_path, sample_id):
    # Convert numpy array to Image
    image = Image.fromarray(image_data)
    
    # Save the image as JPG
    filename = f"{sample_id}.jpg"
    file_path = os.path.join(folder_path, filename)
    image.save(file_path, "JPEG")
    return file_path

def main():
    st.title("Handwriting Sample Collector")
    
    # Set canvas properties
    canvas_result = st_canvas(
        fill_color="rgba(255, 255, 255, 0.3)",
        stroke_width=3,
        stroke_color="#000000",
        background_color="#FFFFFF",
        width=400,
        height=200,
        drawing_mode="freedraw",
        key="canvas",
    )
    
    # Directory setup
    base_dir = "handwriting_samples"
    today = datetime.date.today().strftime("%Y-%m-%d")
    folder_path = os.path.join(base_dir, today)
    os.makedirs(folder_path, exist_ok=True)
    
    # Load or create metadata file
    metadata_file = os.path.join(base_dir, "samples.csv")
    if os.path.exists(metadata_file):
        df = pd.read_csv(metadata_file)
    else:
        df = pd.DataFrame(columns=["Sample ID", "Date", "File Path"])
    
    if st.button("Save Sample"):
        if canvas_result.image_data is not None:
            # Convert to uint8 and remove alpha channel
            image_data = (canvas_result.image_data[:, :, :3] * 255).astype(np.uint8)
            
            # Generate sample ID
            sample_id = len(df) + 1
            
            # Save image
            file_path = save_image(image_data, folder_path, sample_id)
            
            # Update metadata
            df = df.append({"Sample ID": sample_id, "Date": today, "File Path": file_path}, ignore_index=True)
            df.to_csv(metadata_file, index=False)
            
            st.success(f"Sample {sample_id} saved successfully!")
            st.image(file_path, caption=f"Sample {sample_id}")

if __name__ == "__main__":
    main()

