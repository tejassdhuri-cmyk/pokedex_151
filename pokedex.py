import streamlit as st
import pokebase as pb
import pandas as pd
import plotly.express as px
import re
import math
import requests
import os
# from functools import reduce

st.image("https://upload.wikimedia.org/wikipedia/commons/e/e5/Pokemon_logo.png?utm_source=commons.wikimedia.org&utm_campaign=index&utm_content=original",width=400)
st.title("Pokedex For The Original 151 Pokemons")

with open ("style.css") as file:
    st.html(f"<style>{file.read()}</style>")

#key of streamlit component: class .st-key-keyname
# sprite=pb.SpriteResource("pokemon",25)
# st.image(sprite.url,width='stretch')
#abilities,against_bug,against_dark,against_dragon,against_electric,against_fairy,against_fight,against_fire,against_flying,against_ghost,against_grass,against_ground,against_ice,against_normal,against_poison,against_psychic,against_rock,against_steel,against_water
main_details=pd.read_csv("Gen1_Pokemon.csv")
entries=pd.read_csv("entries.csv")
add_details=pd.read_csv("FirstGenPokemon.csv")
height_weight=pd.read_csv("pokemon_data.csv")
abilities_df=pd.read_csv("pokemon_complete.csv",nrows=151)

main_details["Number"]=[x for x in range(1,152)]
main_details=main_details.drop(columns=["Name"])
entries=entries.rename(columns={"ID":"Number"})
entries=entries.drop(columns=["Name"])

height_weight=height_weight[["Number","Name","Height","Weight"]]
add_details.columns=add_details.columns.str.strip()
new_df=add_details[["Number","Male_Pct","Female_Pct","Capt_Rate","Exp_Points","Exp_Speed","Base_Total"]]

abilities_df=abilities_df[[
    "abilities",
    "base_happiness",
    "japanese_name",
    "classfication",
    "base_egg_steps",
    "against_bug",
    "against_dark",
    "against_dragon",
    "against_electric",
    "against_fairy",
    "against_fight",
    "against_fire",
    "against_flying",
    "against_ghost",
    "against_grass",
    "against_ground",
    "against_ice",
    "against_normal",
    "against_poison",
    "against_psychic",
    "against_rock",
    "against_steel",
    "against_water"
]]
abilities_df["Number"]=[x for x in range(1,152)]
# dfs=[main_details,entries,new_df,height_weight]
pokemon_df=pd.merge(main_details,entries,on="Number",how="inner")
pokemon_df["Type 2"]=pokemon_df["Type 2"].fillna("No Secondary Type")
pokemon_df=pd.merge(pokemon_df,new_df,on="Number",how="inner")
pokemon_df=pd.merge(pokemon_df,height_weight,on="Number",how="inner")
pokemon_df=pd.merge(pokemon_df,abilities_df,on="Number",how="inner")
pokemon_df.set_index("Number",inplace=True)
# pokemon_df=pokemon_df.sort_values(by="ID")
# pokemon_df=reduce(lambda left,right: pd.merge(left,right,on="Number",how="inner"),dfs)
# st.write(pokemon_df)

pokemons=pokemon_df["Name"].to_list()
pokemon_id=pokemon_df.index.tolist()

# abilities_df["Name"]=pokemons
# pokemon_df=pd.merge(pokemon_df,abilities_df,on="Name",how="inner")
tabs=st.tabs(["Pokemon Info","Filter by type","Region"])
with tabs[0]:
    pokemon_input=st.selectbox("Enter Pokemon:",key="pokinput",options=pokemons)  
            
    pokemon_input=pokemon_input.capitalize()
    submit_btn=st.button("See Details",key="chkbtn")

    def pokemon_no(pok_input):
        for i in range(len(pokemons)):
            if pokemons[i]==pok_input:
                return pokemon_id[i]

    number=pokemon_no(pokemon_input)

    if submit_btn:
        if pokemon_input in pokemons:    
            cols=st.columns([2,4])
            with cols[0]:
                st.subheader(f"{pokemon_input}/{pokemon_df.loc[number,"japanese_name"]}:")
                st.subheader(f"Pokedex No. {number}")
                sprite=pb.SpriteResource("pokemon",number)
                st.image(sprite.url,width='stretch')
                st.write(f"{pokemon_df.loc[number,"classfication"]}")
                type_dict={
                    'Normal': '#A8A77A',
	                'Fire': '#EE8130',
	                'Water': '#6390F0',
	                'Electric': '#F7D02C',
	                'Grass': '#7AC74C',
	                'Ice': '#96D9D6',
	                'Fighting': '#C22E28',
	                'Poison': '#A33EA1',
	                'Ground': '#E2BF65',
	                'Flying': '#A98FF3',
	                'Psychic': '#F95587',
	                'Bug': '#A6B91A',
	                'Rock': '#B6A136',
	                'Ghost': '#735797',
	                'Dragon': '#6F35FC',
	                'Dark': '#705746',
	                'Steel': '#B7B7CE',
	                'Fairy': '#D685AD',
                }
                st.subheader("Type(s)")
                if pokemon_df.loc[number,"Type 2"]!="No Secondary Type":
                    type1=pokemon_df.loc[number,"Type 1"]
                    type2=pokemon_df.loc[number,"Type 2"]
                    with st.container(key="types"):           
                        type1_color=type_dict[type1]
                        type2_color=type_dict[type2]
                        st.markdown(f"""
                                <div style="display:flex; flex-direction:row; justify-content:center;">
                                    <div style="
                                      background-color:{type1_color};gap:6px;border-radius:8px;">
                                      <h5 style="text-align:center;padding-left:15px">{type1}</h5> 
                                    </div>
                                    <div style="
                                        background-color:{type2_color};border-radius:8px;">
                                        <h5 style="text-align:center;padding-left:15px">{type2}</h5> 
                                    </div>
                                <div>                              
                                """,unsafe_allow_html=True)
                else:
                    type1=pokemon_df.loc[number,"Type 1"]
                    with st.container(key="type1"):           
                        type1_color=type_dict[type1]
                        st.markdown(f"""
                                <div style="
                                background-color:{type1_color};border-radius:8px;">
                                <h5 style="text-align:center">{type1}</h5>
                            </div>                          
                            """,unsafe_allow_html=True,width='stretch') 
                               
                st.subheader("Abilities")
                with st.container(border=True,key="p_ability"):
                    abilities=pokemon_df.loc[number,"abilities"]
                    result = re.sub(r"[\[\]']", "", abilities)
                    st.write(result)        
                st.subheader("Height and Weight")    
                with st.container(border=True,key="h_w_contain"):
                    st.write(f"Height: {pokemon_df.loc[number,"Height"]}m") 
                    st.write(f"Weight: {pokemon_df.loc[number,"Weight"]}Kg")  
                st.subheader("Gender Distribution")
                with st.container(border=True,key="gender_contain"):
                    if pokemon_df.loc[number,"Male_Pct"]==0 and pokemon_df.loc[number,"Female_Pct"]==0:
                        st.write("Genderless")
                    else:    
                        st.write(f"{pokemon_df.loc[number,"Male_Pct"]}% ♂️, {pokemon_df.loc[number,"Female_Pct"]}% ♀️")
                
            with cols[1]:
                st.subheader("Pokedex Entry:")
                with st.container(border=True,key="entry_contain"):
                    st.write(pokemon_df.loc[number,"Pokedex_Entry"])
                st.subheader("Catch Rate:")    
                with st.container(border=True,key="catch"):
                    catch_rate=(pokemon_df.loc[number,"Capt_Rate"]*100)/(3*255)
                    st.write(f"{round(catch_rate,1)}% with a pokeball on full HP.")
                st.subheader("Growth and Experience:")    
                with st.container(border=True,key="grow"):
                    st.write(f"{pokemon_input} takes {pokemon_df.loc[number,"Exp_Points"]} experience points to level up to Lv. 100")
                    st.write(f"Growth Rate: {pokemon_df.loc[number,"Exp_Speed"]}")
                sub_cols=st.columns(2)
                with sub_cols[0]:
                    with st.container(border=True,key="egg_cycle"):
                        st.write(f"Base Egg Cycle: {pokemon_df.loc[number,"base_egg_steps"]}")
                with sub_cols[1]:        
                    with st.container(border=True,key="base_happ"):
                        st.write(f"Base Happiness Value: {pokemon_df.loc[number,"base_happiness"]}")    
                st.subheader(f"{pokemon_input} stats:")    
                with st.container(border=True,key="stats"):
                    stats={
                        "p_stats":[
                            pokemon_df.loc[number,"Speed"],
                            pokemon_df.loc[number,"Sp. Def"],
                            pokemon_df.loc[number,"Sp. Atk"],
                            pokemon_df.loc[number,"Defense"],
                            pokemon_df.loc[number,"Attack"],
                            pokemon_df.loc[number,"HP"]    
                        ],
                        "stats_name":["Speed","Sp.Def","Sp.Atk","Defense","Attack","HP"]
                    }
                    stats_df=pd.DataFrame(stats)
                    total=stats_df["p_stats"].sum()
                    stats_graph=px.bar(
                        data_frame=stats_df,
                        x="p_stats",
                        y="stats_name",
                        labels={"p_stats":f"Total:{total}"},
                        text_auto=".2s"
                    ) 
                    stats_graph.update_traces(textfont_size=14, textangle=0, textposition="outside", cliponaxis=False)
                    st.plotly_chart(stats_graph,width='stretch')        
        elif pokemon_input=="":
                st.warning("Please enter a pokemon")            
        else:
            st.error("Pokemon not found!")
with tabs[1]:
    st.subheader("Filter by type:")
    # st.dataframe(pokemon_df)
    type1_df=pokemon_df.groupby("Type 1")[["Speed","Sp. Def","Sp. Atk","Defense","Attack","HP"]].mean()
    type2_df=pokemon_df.groupby("Type 2")[["Speed","Sp. Def","Sp. Atk","Defense","Attack","HP"]].mean()
    # st.write(pd.DataFrame(type2_df))
    types=["Grass","Fire","Water","Electric","Bug","Poison","Normal","Flying","Rock","Ground","Steel","Psychic","Ghost","Dark","Fairy","Fighting","Ice","Dragon"]
    type_input=st.selectbox(label="Select a type:",options=types,key="typepok")
    filtered_df=pokemon_df[
        (pokemon_df["Type 1"]==type_input) | (pokemon_df["Type 2"]==type_input)
    ] 
    filter_button=st.button("Filter",key="filterbtn")
    if filter_button: 
        st.subheader(f"{type_input} Type Pokemons")
        two_cols=st.columns(3)
        for i,index in enumerate(filtered_df.index):
            target_col=two_cols[i%3]
            with target_col:
                sprites_types=pb.SpriteResource("pokemon",index)
                st.image(sprites_types.url,width='stretch')
                st.subheader(pokemons[index-1],text_alignment="center")

        def generate_graph(df,col1,col2,type_input):
            total=df[col2].sum()
            stats_graph=px.bar(
                data_frame=df,
                x=col2,
                y=col1,
                title=f"Average Stats for {type_input} type",
                labels={"stats":f"Total:{math.floor(total)}","stats_name":""},
                text_auto=".2s"
            ) 
            stats_graph.update_traces(textfont_size=13, textangle=0, textposition="outside", cliponaxis=False)
            st.plotly_chart(stats_graph,width='stretch')

        if type_input in type1_df.index:        
            type_stats={
                "stats_name":["Speed","Sp.Def","Sp.Atk","Defense","Attack","HP"],
                "stats":[
                    type1_df.loc[type_input,"Speed"],
                    type1_df.loc[type_input,"Sp. Def"],
                    type1_df.loc[type_input,"Sp. Atk"],
                    type1_df.loc[type_input,"Defense"],
                    type1_df.loc[type_input,"Attack"],
                    type1_df.loc[type_input,"HP"]
                ]
            }
            type_statsdf=pd.DataFrame(type_stats)
            generate_graph(type_statsdf,"stats_name","stats",type_input)  
        else:
            type_stats={
                "stats_name":["Speed","Sp.Def","Sp.Atk","Defense","Attack","HP"],
                "stats":[
                    type2_df.loc[type_input,"Speed"],
                    type2_df.loc[type_input,"Sp. Def"],
                    type2_df.loc[type_input,"Sp. Atk"],
                    type2_df.loc[type_input,"Defense"],
                    type2_df.loc[type_input,"Attack"],
                    type2_df.loc[type_input,"HP"]
                ]
            }  
            type_statsdf=pd.DataFrame(type_stats) 
            generate_graph(type_statsdf,"stats_name","stats",type_input)            

with tabs[2]:
    # id=1
    # url=f"https://pokeapi.co/api/v2/region/{id}/"
    # response=requests.get(url)
    # if response.status_code==200:
    #     response=response.json()
    #     st.write(response["name"])
    #     st.write(response["locations"][0]["url"])
    # else:
    #     st.error(f"Error fetching data {response.status_code}")
    st.header("Kanto Map")
    st.image(os.path.join(os.getcwd(),'static','kanto_map.png'),width='stretch')        





