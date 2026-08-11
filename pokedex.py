import streamlit as st
import pokebase as pb
import pandas as pd
import plotly.express as px
import re
# from functools import reduce

st.image("https://upload.wikimedia.org/wikipedia/commons/e/e5/Pokemon_logo.png?utm_source=commons.wikimedia.org&utm_campaign=index&utm_content=original",width=400)
st.title("Pokedex For The Original 150 Pokemons")

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
pokemon_input=st.text_input("Enter Pokemon:",key="pokinput")
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
            st.subheader("Type")
            if pokemon_df.loc[number,"Type 2"]=="No Secondary Type":
                with st.container(border=True,key="primary"):
                    st.write(f"{pokemon_df.loc[number,"Type 1"]}")
            else:
                with st.container(border=True,key="secondary"):
                    st.write(f"{pokemon_df.loc[number,"Type 1"]}/{pokemon_df.loc[number,"Type 2"]}")
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
                stats_graph=px.bar(
                    data_frame=stats_df,
                    x="p_stats",
                    y="stats_name",
                    labels={"p_stats":"stats"}
                ) 
                st.plotly_chart(stats_graph,width='stretch')        
    elif pokemon_input=="":
            st.warning("Please enter a pokemon")            
    else:
        st.error("Pokemon not found!")






