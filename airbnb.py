import streamlit as st
from streamlit_option_menu import option_menu
import pymongo
import pandas as pd
pd.set_option("display.max_columns", None)
import warnings
warnings.filterwarnings("ignore")
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image
from powerbiclient import QuickVisualize, get_dataset_config
from powerbiclient.authentication import DeviceCodeLoginAuthentication
import os

#Streamlit part
st.set_page_config(layout= "wide")


def dataframe():
    df= pd.read_csv(r"C:\Users\Santhosh\Desktop\CapstoneProject\Capstone\Airbnb\Airbnb.csv")
    return df

df= dataframe()

select= option_menu(menu_title=None, options=["Home", "About", "Data Exploration"],icons=["house","columns-gap","reception-4"],orientation= "horizontal",
                    default_index=0,
                styles={"container":{"padding": "0!important", "background-color": "green", "size": "cover"},
                        "icons":{"color": "white", "font-size": "20px"},
                        "nav-link":{"font-size": "20px", "text-align":"center", "margin": "-2px", "--hover-color": "blue"},
                        "nav-link-selected": {"background-color": "black"}})

if select == "Home":

    col1,col2= st.columns(2)
    with col1:
        st.title("AIRBNB")

        st.write("Airbnb, Inc. is an American company operating an online marketplace for short- and long-term homestays and experiences. The company acts as a broker and charges a commission from each booking. The company was founded in 2008 by Brian Chesky, Nathan Blecharczyk, and Joe Gebbia. Airbnb is a shortened version of its original name, AirBedandBreakfast.com. Airbnb is the most well-known company for short-term housing rentals.")
        st.write(" ")
        st.write("Founded :  August 2008; 15 years ago in San Francisco, California, U.S.")
        st.write(" ")
        st.write("Founders :  Brian Chesky,Joe Gebbia,Nathan Blecharczyk")
        st.write(" ")
        st.write("Headquarters : San Francisco, California, U.S.")
        st.write(" ")
        st.write("Services : Lodging, Hospitality, Homestay ")

    with col2:
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.image(r"C:\Users\Santhosh\Desktop\CapstoneProject\Capstone\Airbnb\airbnb-2-logo-png-transparent.png", width= 500)

if select == "About":

    st.header("ABOUT THIS PROJECT")

    st.subheader(":green[1. Data Collection:]")

    st.write('''***Gather data from Airbnb's public API or other available sources.
        Collect information on listings, hosts, reviews, pricing, and location data.***''')
    
    st.subheader(":green[2. Data Cleaning and Preprocessing:]")

    st.write('''***Clean and preprocess the data to handle missing values, outliers, and ensure data quality.
        Convert data types, handle duplicates, and standardize formats.***''')
    
    st.subheader(":green[3. Exploratory Data Analysis (EDA):]")

    st.write('''***Conduct exploratory data analysis to understand the distribution and patterns in the data.
        Explore relationships between variables and identify potential insights.***''')
    
    st.subheader(":green[4. Visualization:]")

    st.write('''***Create visualizations to represent key metrics and trends.
        Use charts, graphs, and maps to convey information effectively.
        Consider using tools like Matplotlib, Seaborn, or Plotly for visualizations.***''')
    
    st.subheader(":green[5. Geospatial Analysis:]")

    st.write('''***Utilize geospatial analysis to understand the geographical distribution of listings.
        Map out popular areas, analyze neighborhood characteristics, and visualize pricing variations.***''')

if select == "Data Exploration":

    with st.sidebar:

        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        

        add_radio =st.radio("ANALYSIS", ["PRICE ANALYSIS","AVAILABILITY ANALYSIS","LOCATION ANALYSIS","GIOSPATIAL VISUALISATION", "CHARTS"])     

    if add_radio == "PRICE ANALYSIS":
        
        st.title("Price Difference")
        col1,col2= st.columns(2)

        with col1:

            country=st.selectbox("Select the country",df["country"].unique())

            df_1=df[df["country"]== country]
            df_1.reset_index(drop= True, inplace= True)

        

            room_type=st.selectbox("Select the roomtype",df_1["room_type"].unique())
        
            df_2=df_1[df_1["room_type"]== room_type]
            df_2.reset_index(drop=True, inplace= True)

            df_bar= pd.DataFrame(df_2.groupby("property_type")[["price","review_scores","number_of_reviews"]].sum())
            df_bar.reset_index(inplace= True) 
        with col2:
            fig_bar= px.bar(df_bar, x="property_type", y= "price", title="Price based on property type", hover_data=["review_scores","number_of_reviews"],color_discrete_sequence= px.colors.sequential.gray_r,width= 600, height= 450)
            st.plotly_chart(fig_bar)  

        col1,col2 = st.columns(2)

        with col1:

            property_type = st.selectbox("Select the property type", df_2["property_type"].unique())

            df_3=df_2[df_2["property_type"]== property_type]
            df_3.reset_index(drop= True, inplace= True)

            df_pie= pd.DataFrame(df_3.groupby("host_response_time")[["price","bedrooms"]].sum())
            df_pie.reset_index(inplace= True)

        with col2:

            pie_chart_1 = px.pie(df_pie, values="price", names= "host_response_time", hover_data=["bedrooms"],
                                 title="Price based on host response time",
                                 color_discrete_sequence= px.colors.sequential.Rainbow_r,width= 600, height= 450)
            st.plotly_chart(pie_chart_1)

        col1,col2 = st.columns(2)

        with col1:

            hostResponseTime= st.selectbox("Select the host_response_time", df_3["host_response_time"].unique())

            df_4=df_3[df_3["host_response_time"]== hostResponseTime]
            df_4.reset_index(drop= True, inplace= True)

            df_bar_1= pd.DataFrame(df_4.groupby("bed_type")[["minimum_nights","maximum_nights","price"]].sum())
            df_bar_1.reset_index(inplace=True)

            fig_bar_1= px.bar(df_bar_1, x="bed_type", y=["minimum_nights","maximum_nights"],
                              title="Price based on min & max nights", hover_data=["price"], barmode="group",
                              color_discrete_sequence= px.colors.sequential.Rainbow_r,width= 600, height= 450)
            st.plotly_chart(fig_bar_1)

        with col2:

            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.write(" ")
            

            df_bar_2 = pd.DataFrame(df_4.groupby("bed_type")[["bedrooms","beds","accommodates", "price"]].sum())
            df_bar_2.reset_index(inplace= True)
            
            fig_bar_2= px.bar(df_bar_2, x="bed_type", y=["bedrooms","beds","accommodates"], hover_data= "price",
                              title="Price based on bedrooms, beds & accommodates", barmode="group",
                              color_discrete_sequence= px.colors.sequential.Rainbow_r,width= 600, height= 450)
            st.plotly_chart(fig_bar_2)

    if add_radio == "AVAILABILITY ANALYSIS":

        def dataframe():
            df_A= pd.read_csv(r"C:\Users\Santhosh\Desktop\CapstoneProject\Capstone\Airbnb\Airbnb.csv")
            return df_A
        
        df_A= dataframe()
        
        st.title("Availabilities") 

        col1,col2 = st.columns(2)
        with col1:

            Country = st.selectbox("Select the Country",df_A["country"]. unique())

            df_A_1 = df_A[df_A["country"]== Country]
            df_A_1.reset_index(drop= True, inplace= True)

            property_type_A= st.selectbox("Select the Property type", df_A_1["property_type"].unique())

            df_A_2= df_A_1[df_A_1["property_type"]== property_type_A ]
            df_A_2.reset_index(drop= True, inplace= True)

        with col2:

            df_A_sun30 = px.sunburst(df_A_1, path=["room_type","bed_type","is_location_exact"], values="availability_30", width=600, height= 450,
                                     title="Availability 30",color_discrete_sequence= px.colors.sequential.Electric_r)
            st.plotly_chart(df_A_sun30)

        col1,col2 = st.columns(2)

        with col1:

            df_A_sun60 = px.sunburst(df_A_1, path=["room_type","bed_type","is_location_exact"], values="availability_60", width=600, height= 450,
                                     title="Availability 60",color_discrete_sequence= px.colors.sequential.Rainbow_r)
            st.plotly_chart(df_A_sun60)

        with col2:    

            df_A_sun90 = px.sunburst(df_A_1, path=["room_type","bed_type","is_location_exact"], values="availability_90", width=600, height= 450,
                                     title="Availability 90",color_discrete_sequence= px.colors.sequential.Hot_r)
            st.plotly_chart(df_A_sun90)

        col1,col2 = st.columns(2)

        with col1:

            df_A_sun365 = px.sunburst(df_A_1, path=["room_type","bed_type","is_location_exact"], values="availability_365", width=600, height= 450,
                                     title="Availability 365",color_discrete_sequence= px.colors.sequential.Rainbow_r)
            st.plotly_chart(df_A_sun365)

        with col2:

            room_type_A = st.selectbox("Select the room type", df_A_2["room_type"].unique())

            df_A_3= df_A_2[df_A_2["room_type"]== room_type_A]

            df_mul_bar_a = pd.DataFrame(df_A_3.groupby("host_response_time")[["availability_30","availability_60","availability_90","availability_365","price"]].sum())
            df_mul_bar_a.reset_index( inplace= True)
            

            fig_bar_3 = px.bar(df_mul_bar_a, x ="host_response_time", y=["availability_30","availability_60","availability_90","availability_365","price"], hover_data= "price",
                               title= "Availability based on host response time", barmode="group",color_discrete_sequence=px.colors.sequential.Electric_r, width=600, height= 450)
            
            st.plotly_chart(fig_bar_3)

    if add_radio == "LOCATION ANALYSIS":

        st.title("Location Analysis")

        def dataframe():
            df_l = pd.read_csv(r"C:\Users\Santhosh\Desktop\CapstoneProject\Capstone\Airbnb\Airbnb.csv")
            return df_l
        
        df_l= dataframe()
        col1,col2 = st.columns(2)

        with col1:

            country_l= st.selectbox("Select the Country_l",df_l["country"].unique())

            df1_l= df_l[df_l["country"] == country_l]
            df1_l.reset_index(drop= True, inplace= True)

        with col2:

            proper_ty_l= st.selectbox("Select the Property_type_l",df1_l["property_type"].unique())

            df2_l= df1_l[df1_l["property_type"] == proper_ty_l]
            df2_l.reset_index(drop= True, inplace= True)

        col1,col2 = st.columns(2)

        with col1:

            st.write("")

            def select_the_df(sel_val):
                if sel_val == str(df2_l['price'].min())+' '+str('to')+' '+str(differ_max_min*0.30 + df2_l['price'].min())+' '+str("(30% of the Value)"):

                    df_val_30= df2_l[df2_l["price"] <= differ_max_min*0.30 + df2_l['price'].min()]
                    df_val_30.reset_index(drop= True, inplace= True)
                    return df_val_30

                elif sel_val == str(differ_max_min*0.30 + df2_l['price'].min())+' '+str('to')+' '+str(differ_max_min*0.60 + df2_l['price'].min())+' '+str("(30% to 60% of the Value)"):
                
                    df_val_60= df2_l[df2_l["price"] >= differ_max_min*0.30 + df2_l['price'].min()]
                    df_val_60_1= df_val_60[df_val_60["price"] <= differ_max_min*0.60 + df2_l['price'].min()]
                    df_val_60_1.reset_index(drop= True, inplace= True)
                    return df_val_60_1
            
                elif sel_val == str(differ_max_min*0.60 + df2_l['price'].min())+' '+str('to')+' '+str(df2_l['price'].max())+' '+str("(60% to 100% of the Value)"):

                    df_val_100= df2_l[df2_l["price"] >= differ_max_min*0.60 + df2_l['price'].min()]
                    df_val_100.reset_index(drop= True, inplace= True)
                    return df_val_100
                
            differ_max_min= df2_l['price'].max()-df2_l['price'].min()
        
            val_sel= st.radio("Select the Price Range",[str(df2_l['price'].min())+' '+str('to')+' '+str(differ_max_min*0.30 + df2_l['price'].min())+' '+str("(30% of the Value)"),
                                                        
                                                        str(differ_max_min*0.30 + df2_l['price'].min())+' '+str('to')+' '+str(differ_max_min*0.60 + df2_l['price'].min())+' '+str("(30% to 60% of the Value)"),

                                                        str(differ_max_min*0.60 + df2_l['price'].min())+' '+str('to')+' '+str(df2_l['price'].max())+' '+str("(60% to 100% of the Value)")])
        col1, col2=st.columns(2)
        with col1:                                 
            df_val_sel= select_the_df(val_sel)

            
        with col2:

            # checking the correlation

            df_val_sel_corr= df_val_sel.drop(columns=["listing_url","name", "property_type",                 
                                                "room_type", "bed_type","cancellation_policy",
                                                "images","host_url","host_name", "host_location",                   
                                                "host_response_time", "host_thumbnail_url",            
                                                "host_response_rate","host_is_superhost","host_has_profile_pic" ,         
                                                "host_picture_url","host_neighbourhood",
                                                "host_identity_verified","host_verifications",
                                                "street", "suburb", "government_area", "market",                        
                                                "country", "country_code","location_type","is_location_exact",
                                                "amenities"]).corr()
            


        col1,col2 =st.columns(2)

        with col1:
            df_val_sel_gr= pd.DataFrame(df_val_sel.groupby("accommodates")[["cleaning_fee","bedrooms","beds","extra_people"]].sum())
            df_val_sel_gr.reset_index(inplace= True)

            fig_1= px.bar(df_val_sel_gr, x="accommodates", y= ["cleaning_fee","bedrooms","beds"], title="ACCOMMODATES",
                        hover_data= "extra_people", barmode='group', color_discrete_sequence=px.colors.sequential.Hot_r,width=600, height=450)
            st.plotly_chart(fig_1)
            
            
        with col2:    
            room_ty_l= st.selectbox("Select the Room type", df_val_sel["room_type"].unique())

            df_val_sel_rt= df_val_sel[df_val_sel["room_type"] == room_ty_l]

            fig_2= px.bar(df_val_sel_rt, x= ["street","host_location","host_neighbourhood"],y="market", title="MARKET",
                        hover_data= ["name","host_name","market"], barmode='group',orientation='h', color_discrete_sequence=px.colors.sequential.Hot_r,width=600, height=450)
            st.plotly_chart(fig_2)

        fig_3= px.bar(df_val_sel_rt, x="government_area", y= ["host_is_superhost","host_neighbourhood","cancellation_policy"], title="GOVERNMENT AREA",
                    hover_data= ["guests_included","location_type"], barmode='group', color_discrete_sequence=px.colors.sequential.Jet_r,width=1000)
        st.plotly_chart(fig_3)

    if add_radio == "GIOSPATIAL VISUALISATION":

        st.title("GEOSPATIAL VISUALIZATION")
        

        GeoMap = px.scatter_mapbox(df, lat='latitude', lon='longitute', color='price', size='accommodates',
                        color_continuous_scale= "rainbow",hover_name='name',range_color=(0,49000), mapbox_style="carto-positron",
                        zoom=1)
        GeoMap.update_layout(width=1150,height=800,title='Geospatial Distribution')
        st.plotly_chart(GeoMap) 

    if add_radio == "CHARTS":

        col1,col2 = st.columns(2)

        with col1:
        
            country_c = st.selectbox("Select The Country", df["country"].unique())

            df_con = df[df["country"]== country_c]

        with col2: 

            property_c = st.selectbox("Select The Property", df_con["property_type"].unique())

        df_pro = df_con[df_con["property_type"]== property_c]
        df_pro.reset_index(drop= True, inplace= True)

        df_pro_sorted = df_pro.sort_values(by="price")
        df_pro_sorted.reset_index(drop= True, inplace= True)

        df_price= pd.DataFrame(df_pro_sorted.groupby("host_neighbourhood")["price"].agg(["sum","mean"]))
        df_price.reset_index(inplace= True)
        df_price.columns= ["neighbourhood", "total_price", "average_price"]

        col1,col2 = st.columns(2)

        with col1:
            
            total_price = px.bar(df_price, x="total_price", y="neighbourhood", orientation="h",
                                    title="Price based on Neighbourhood", width=600, height= 450)
            
            st.plotly_chart(total_price)  

        with col2:
            
            Avg_price = px.bar(df_price, x= "average_price", y= "neighbourhood", orientation="h",
                                title="Average price based Neighbourhood", width=600, height= 450)
            st.plotly_chart(Avg_price)

        col1,col2 = st.columns(2)

        with col1:
            
            dfPrice1 = pd.DataFrame(df_pro_sorted.groupby("host_location")["price"].agg(["sum","mean"]))
            dfPrice1.reset_index(inplace= True)
            dfPrice1.columns= ["location","total_price","average_price"]

            total_price_cha= px.bar(dfPrice1, x="total_price", y="location", orientation="h",
                                    title="Price based on location", width=600, height=450,
                                    color_discrete_sequence=px.colors.sequential.gray_r)
            st.plotly_chart(total_price_cha)

        with col2: 

            Avg_price_cha= px.bar(dfPrice1, x="average_price", y="location", orientation="h",
                                    title="Average price based on location", width=600, height=450,
                                    color_discrete_sequence=px.colors.sequential.gray_r)
            st.plotly_chart(Avg_price_cha)

        roomType = st.selectbox("Select The RoomType", df_pro_sorted["room_type"].unique())
        dfRoomType= df_pro_sorted[df_pro_sorted["room_type"]==roomType]

        dfRoomTypeSortedPrice = dfRoomType.sort_values(by= "price")
        dfRoomTypeSortedPrice.reset_index(drop= True, inplace= True)

        dfRoomTypeSortedPrice100 = dfRoomTypeSortedPrice.head(100)

        fig_bar_4 = px.bar(dfRoomTypeSortedPrice100, x="name", y="price", color="price",
                            color_continuous_scale= "rainbow",range_color=(0,dfRoomTypeSortedPrice100["price"].max()),
                            title= "Min_night Max_night and Accommodates", width= 1000, height= 800,
                            hover_data=["minimum_nights", "maximum_nights", "accommodates"])
        
        st.plotly_chart(fig_bar_4)

        fig_bar_5 = px.bar(dfRoomTypeSortedPrice100, x="name", y="price", color="price",
                            color_continuous_scale= "blues",range_color=(0,dfRoomTypeSortedPrice100["price"].max()),
                            title= "Bedrooms,Beds, Bed_type and Accommodates", width= 1000, height= 800,
                            hover_data=["accommodates","bedrooms","beds","bed_type"])
        
        st.plotly_chart(fig_bar_5)  

        ##END###

