import streamlit as st


st.set_page_config(layout='wide')


MODEL_LIST = {
    'None'     : 'None',
    'Yolov5-s' : 'Yolov5-s',
    'Yolov5-n' : 'Yolov5-n',
    'Yolov6-s' : 'Yolov6-s'
}

VIDEO_LIST = {
    'None' : None,
    'frist_video': '/opt/ml/input/database/videos/input2/example_video1.mp4',
    'second_video' : '/opt/ml/input/database/videos/input2/example_video2.mp4'
}

# test video (임시)
TEST_VIDEO = '/opt/ml/input/database/videos/output2/test_video.mp4'


def main():
    st.title("Sixth Sense Streamlit Demo Page")
    if 'bt_inference' not in st.session_state:
        st.session_state['bt_inference'] = False
    
    with st.sidebar.container():
        st.selectbox('Model List', [i for i in MODEL_LIST.keys()])
        video_path = st.selectbox('Video List', [i for i in VIDEO_LIST.keys()], key='select_video')
        
        
    with st.sidebar.container():
        video_path = VIDEO_LIST[video_path]
        if video_path is not None:
            example_video1 = open(video_path, 'rb')
            example_video1_bytes = example_video1.read()
            st.video(example_video1_bytes)
            
        if st.button("inference"):
            st.session_state['bt_inference'] = True
        
    
    if st.session_state['bt_inference']:
        example_video2 = open(TEST_VIDEO, 'rb')
        example_video2_bytes = example_video2.read()
        st.video(example_video2_bytes)
        
    
        
        
    
    
    




if __name__ == '__main__':
    main()