import streamlit as st
import pandas as pd
import boto3, os
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

try:
    os.mkdir('downloads')
except OSError as error:
    print(error)

s3_client = boto3.client('s3',aws_access_key_id = st.secrets["aws"]["aws_access_key_id"],
                    aws_secret_access_key = st.secrets["aws"]["aws_secret_access_key"])

s3_bucket = "music48"

st.set_page_config(page_title="S3 Manage Playlist",page_icon="🎵")
st.title("S3 Manage Playlist 🎵")

f = [key['Key'] for key in s3_client.list_objects(Bucket='music48',Prefix="Playlists/")['Contents']]

m = st.selectbox("Select Music",f,
            format_func = lambda x : x.replace("Playlists/","").replace(".csv",""))

if m != "Playlists/":
    object_name = m
    file_name = "downloads/"+m.replace("Playlists/","")

    s3_client.download_file(s3_bucket, object_name,file_name)

    data = pd.read_csv(file_name,index_col=0)

    gb = GridOptionsBuilder.from_dataframe(data)
    gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
    # gb.configure_side_bar() #Add a sidebar
    gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
    gridOptions = gb.build()

    grid_response = AgGrid(
        data,
        gridOptions=gridOptions,
        data_return_mode='AS_INPUT', 
        update_mode='MODEL_CHANGED', 
        fit_columns_on_grid_load=False,
        # theme='material', #Add theme color to the table
        enable_enterprise_modules=True,
        height=350, 
        width='100%'
    )

    data = grid_response['data']
    selected = grid_response['selected_rows'] 
    # st.write(selected)
    df = pd.DataFrame(selected) #Pass the selected rows to a new dataframe df
    # st.dataframe(df.drop(columns=['_selectedRowNodeInfo']))

    dropped = [i['_selectedRowNodeInfo']['nodeRowIndex'] for i in selected]
    # st.write(dropped)
    df2 = data.drop(dropped)
    if st.checkbox('view mod playlist'):
        st.dataframe(df2)
    mod = st.text_input("Playlist name",m.replace("Playlists/","").replace(".csv","")+"-mod")
    if st.button("Save playlist"):
        mod_file = "downloads/"+mod+".csv"
        df2.to_csv(mod_file)
        mod_object = "Playlists/"+mod+".csv"
        s3_client.upload_file(mod_file, s3_bucket, mod_object)