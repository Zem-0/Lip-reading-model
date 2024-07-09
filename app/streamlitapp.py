import streamlit as st
import tensorflow as tf
import os
import imageio
from utils import load_data, num_to_char
from modelutil import load_model


st.title('LipReader')
st.info('This application is originally developed from the LipNet deep learning model.')

st.title('LipNet Full Stack App')

# Define the data directory path
data_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 's1')

# Check if the data directory exists
if not os.path.exists(data_dir):
    st.error(f"The data directory {data_dir} does not exist.")
else:
    # Generating a list of options or videos 
    options = os.listdir(data_dir)
    
    if options:
        selected_video = st.selectbox('Choose video', options)

        # Generate two columns 
        col1, col2 = st.columns(2)

        file_path = os.path.join(data_dir, selected_video)

        # Rendering the video 
        with col1:
            st.info('The video below displays the converted video in mp4 format')
            os.system(f'ffmpeg -i {file_path} -vcodec libx264 test_video.mp4 -y')

            # Rendering inside of the app
            with open('test_video.mp4', 'rb') as video:
                video_bytes = video.read()
            st.video(video_bytes)

        with col2:
            st.info('This is all the machine learning model sees when making a prediction')
            video, annotations = load_data(tf.convert_to_tensor(file_path))
            #imageio.mimsave('animation.gif', video, fps=10)
            st.image('app/animation.gif', width=400)

            st.info('This is the output of the machine learning model as tokens')
            model = load_model()
            yhat = model.predict(tf.expand_dims(video, axis=0))
            decoder = tf.keras.backend.ctc_decode(yhat, [75], greedy=True)[0][0].numpy()
            st.text(decoder)

            # Convert prediction to text
            st.info('Decode the raw tokens into words')
            converted_prediction = tf.strings.reduce_join(num_to_char(decoder)).numpy().decode('utf-8')
            st.text(converted_prediction)
    else:
        st.warning("No video files found in the data directory.")
