import streamlit as st
import pandas as pd

@st.cache_data
def load_data(gid):
    sheet_ID = "133p_AZdXgB3YUstAlOrn25tOJuplWbuGkx9KYwW9O7M"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_ID}/export?format=csv&gid={gid}"

    data = pd.read_csv(url)
    return data

def create_standings(data, pdata):
    standings = data.groupby(['PlayerID', 'Outcome']).size().unstack(fill_value=0)
    standings = standings.reset_index()

    col = ['PlayerID', 'w', 'l', 't']
    for c in col:
        if c not in standings.columns:
            col.remove(c)
    standings = standings[col].reset_index()

    standings = standings.merge(pdata[['PlayerID', 'Name']], on='PlayerID', how='left')
    standings['Player'] = standings['Name']

    col.remove('PlayerID')
    standings['GP'] = standings[col].sum(axis=1)
    standings['Win %'] = (standings['w'] / standings['GP']).round(3)

    forder = []
    if 'w' in col:
        standings = standings.rename(columns={'w': 'Wins'})
        forder = forder + ['Wins']
    if 'l' in col:
        standings = standings.rename(columns={'l': 'Losses'})
        forder = forder + ['Losses']
    if 't' in col:
        standings = standings.rename(columns={'t': 'Draws'})
        forder = forder + ['Draws']

    forder = ['Player', 'GP', 'Win %'] + forder + ['PlayerID']
    standings = standings[forder].sort_values(by='Wins', ascending=False)
    standings.insert(0, 'Seed', range(1, len(standings) + 1))

    base_url = 'https://7mj8sspzd6qkm2qloaxshl.streamlit.app'
    standings['Profile_Link'] = "/?player_id=" + standings['PlayerID'].astype(str) + "&name=" + standings['Player']
    forder = ['Seed', 'Profile_Link'] + forder

    standings = standings[forder].reset_index(drop=True)

    st.dataframe(
        standings,
        column_config={
            "PlayerID": None,
            "Player": None,
            "Profile_Link": st.column_config.LinkColumn("Player Name", display_text=r"&name=(.+)" ),
            "Win %": st.column_config.NumberColumn(format="%.3f")
        },
        hide_index=True,
    )


def player_profile(data, pdata):
    pid = st.query_params["player_id"]

    player_row = pdata[pdata['PlayerID'].astype(str) == str(pid)]

    if not player_row.empty:
        player_name = player_row.iloc[0]['Name']
        st.title(f"👤 {player_name}")
        
        st.subheader("Game History")
    else:
        st.error("Player not found.")

def show_lookup(pdata):
    #with st.sidebar:
    st.title("🔍 Player Lookup")
        
        # 1. Create a clean list of names for the dropdown
        # We add a "placeholder" so it doesn't automatically select the first player
    names_list = ["--- Select a Player ---"] + [f"{row['Name']} {row['PlayerID']}" for _, row in pdata.iterrows()]

    selected_name = st.selectbox("Search for a player:", names_list)

        # 2. If they actually picked a name (and not the placeholder)
    if selected_name != "--- Select a Player ---":
            # 3. Find the ID associated with that name
            # We filter the dataframe where the name matches and grab the 'PlayerID'
        selected_id = pdata[pdata['Name'] == selected_name.split()[0]]['PlayerID'].values[0]
            
            # 4. Teleport!
        st.query_params["player_id"] = selected_id
        st.rerun()

games = load_data(0)
players = load_data(1430924563)


if "player_id" in st.query_params:
    player_profile(games, players)
else:
    show_lookup(players)
    st.title("Chess Tournament Leaderboard")

    standings = create_standings(games, players)

    for index, row in players.iterrows():
    # 1. Create a layout for the row
    # [Seed1, Player1, "VS", Player2, Seed2]
        col1, col2, col3, col4, col5 = st.columns([1, 3, 1, 3, 1])
    
    with col1:
        st.markdown(f"**#{row['Seed']}**")
        
    with col2:
        # Button for Player 1
        if st.button(row['Player'], key=f"p1_{index}"):
            st.query_params["player_id"] = row['P1_ID']
            st.rerun()
            
    with col3:
        st.write("vs")
        
    with col4:
        # Button for Player 2
        if st.button(row['Player'], key=f"p2_{index}"):
            st.query_params["player_id"] = row['P2_IDl']
            st.rerun()
            
    with col5:
        st.markdown(f"**#{row['Seed']}**")
    
    st.divider() # Draw a line between matches
    
    

    
