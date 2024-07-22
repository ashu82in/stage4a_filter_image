#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 13:03:34 2024

@author: ashutoshgoenka
"""

import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image
# from exif import Image as Image2
from PIL.ExifTags import TAGS
import PIL
import os
import zipfile
from zipfile import ZipFile, ZIP_DEFLATED
import pathlib
import shutil
import docx
import docxtpl
from docx import Document
from docx.shared import Inches
from docx.enum.section import WD_ORIENT
from docx.shared import Cm, Inches
import random
from random import randint
from streamlit import session_state



state = session_state
if "key" not in state:
    state["key"] = str(randint(1000, 100000000))
    
if 'counter' not in state: 
    state["counter"]= 0
    
if "loaded" not in state:
    state["loaded"] = False

st.set_page_config(layout="wide")


if state["loaded"] == False:
    try:
        shutil.rmtree("images_comp")
    except:
        pass

if state["loaded"] == False:

    try:
        os.mkdir("images_comp")
    except:
        pass


def update_folder_with_filtered_images():
    pass


st.title("Stage 4A - Filter Image")
up_files = st.file_uploader("Upload Image Files", type = ["png", "jpeg", "jpg"] ,accept_multiple_files=True, key=state["key"])
obs_img_list = []
st.write("Upload Observation (Optional)", 4)
obs_file = st.file_uploader("Upload Observation Excel File With Image List Updated", type=['csv','xlsx'],accept_multiple_files=False,key="fileUploader")
if obs_file is not None:
    df = pd.read_excel(obs_file)
    df = df.dropna(thresh=5)
    df = df.astype({"Image Number": str})
    # st.write(df)
    obs_img = list(df["Image Number"])
    
    for i in obs_img:
        img_list =  i.split(",")
        for j in img_list:
            temp_j = j.strip()
            obs_img_list.append(temp_j)
    st.write(obs_img_list)
    st.write(len(set(obs_img_list)))
    temp_file_list = []
    image_not_used = []
    image_used = []
    repeated_val = []
    vals_added = []
    obs_img_list_to_check_missed_file = [j for j in obs_img_list]
    for file in up_files:
        temp_file_name  = file.name
        used_bool = False
        for i in obs_img_list:

            if i in temp_file_name:
                obs_img_list_to_check_missed_file.remove(i)
                temp_file_list.append(file)
                image_used.append(temp_file_name)
                used_bool = True
                if i not in vals_added:
                    vals_added.append(i)
                else:
                    repeated_val.append(i)
                
            
        if used_bool == False:
            image_not_used.append(temp_file_name)
    st.write("Missing Files", obs_img_list_to_check_missed_file)
    st.write("Images not displayed: ", image_not_used)
    st.write("Images used", image_used)
    up_files = temp_file_list
    total_no_files = len(up_files)
    if state["loaded"] == False:
        for file in up_files:
            # st.write(file.name)
            im = Image.open(file)
            
            
            im.save("images_comp/"+file.name)
            pos = up_files.index(file)
            if pos>= total_no_files-1:
                state["loaded"] = True
    
    st.write("repeated Files: " + str(repeated_val))
    st.write("Total Files: " + str(len(up_files)))
    
    if len(up_files) >0:
        zip_path = "images_compressed.zip"
        directory_to_zip = "images_comp"
        folder = pathlib.Path(directory_to_zip)
        
        
        with ZipFile(zip_path, 'w', ZIP_DEFLATED) as zip:
            for file in folder.iterdir():
                zip.write(file, arcname=file.name)
        
        with open("images_compressed.zip", "rb") as fp:
            btn = st.download_button(
                label="Download ZIP",
                data=fp,
                on_click=update_folder_with_filtered_images,
                file_name="images_compressed.zip",
                mime="application/zip"
        )
    

    
    
