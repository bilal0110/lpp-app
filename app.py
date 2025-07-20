import streamlit as st
import pickle
import numpy as np
import pandas as pd

# importing the model
pipe = pickle.load(open('pipe.pkl','rb'))
df = pickle.load(open('df.pkl','rb'))

st.title("Laptop Price Predictor")

# brand
company =st.selectbox('Brand',df['Company'].unique())

# Type of laptop
Type = st.selectbox('Type', df['TypeName'].unique())

# RAM
RAM = st.selectbox("RAM In GB",[2,4,6,8,12,16,24,32,64])

# Weight
Weight = st.number_input('Weight of the laptop')

# Touch Screen
TouchScreen = st.selectbox('Touch Screen',['No','Yes'])

# IPS Display
IPS = st.selectbox('IPS Display',['No','Yes'])

# Screen Size
Screen_size = st.number_input('Screen Size')

# Resolution
resolution = st.selectbox('Screen Resolution',['1920x1080','1366x768','1600x900','3840x2160','3200x1800',
                                               '2880x1800','2560x1600','2560x1440','2304x1440'])

# CPU
cpu = st.selectbox('CPU',df['Cpu Brand'].unique()) 

# HDD
hdd = st.selectbox('HDD(in GB)',[0,128,256,512,1024,2048])

sdd = st.selectbox('SDD(in GB)',[0,8,128,256,512,1024])

# GPU
gpu = st.selectbox('GPU',df['Gpu brand'].unique()) 

# OS
os = st.selectbox('OS',df['OS'].unique())

if st.button('Predict Price'):
    # query point
    ppi = None

    if TouchScreen=='Yes':
        TouchScreen=1
    else:
        TouchScreen = 0
    
    if IPS =='Yes':
        IPS = 1
    else:
        IPS = 0

    try:
        X_res = int(resolution.split('x')[0])
        Y_res = int(resolution.split('x')[1])
        if Screen_size == 0:
            st.error('Screen size cannot be zero.')
        else:
            ppi = ((X_res**2) + (Y_res**2))**0.5/Screen_size
            # ✅ Create a DataFrame with columns in the original order
            query_df = pd.DataFrame([[company, Type, RAM, Weight, TouchScreen, IPS, ppi, cpu, hdd, sdd, gpu, os]], 
                                    columns=['Company', 'TypeName', 'Ram', 'Weight', 'TouchScreen', 'IPS', 'ppi', 'Cpu Brand', 'HDD', 'SSD', 'Gpu brand', 'OS'])
            
            # Predict using the DataFrame
            price = int(np.exp(pipe.predict(query_df)[0]))
            st.success(f"The predicted price of this configuration is ₹{price:,}")

    except Exception as e:
        st.error(f"An error occurred: {e}")







