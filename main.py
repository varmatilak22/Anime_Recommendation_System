import streamlit as st
import streamlit.components.v1 as components
import base64, os

# Page config
st.set_page_config(page_title="Welcome to Aniflix 🎥", page_icon="🎥", layout="wide")

st.markdown("""
    <style>
        .centered {
            position: relative;
            z-index: 1;  /* Ensures the content stays above the overlay */
            background-image: url('https://m.media-amazon.com/images/I/81AK6YSEfQL.jpg');
            background-size: cover;
            background-position: center;
            height: 80vh;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
        }
        .centered::after {
            content: ""; /* Create a blank content element */
            position: absolute; /* Position it over the background */
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: rgba(0, 0, 0, 0.7); /* Black overlay with reduced opacity */
            z-index: -1;
        }

        .title {
            font-size: 5.4rem;
            color: #ff0000;
            font-weight: bold;
            display: flex;
            justify-content: center;
            margin-top: 50px;
            text-shadow: 3px 3px 10px rgba(0, 0, 0, 0.7);
            align-content: center;
            align-items: center;
        }

        .subtitle {
            font-size: 2rem;
            color: white;
            margin-top: 1rem;
            margin-bottom: 2rem;
            text-shadow: 2px 2px 6px rgba(0, 0, 0, 0.6);
            display: flex;
            align-content: center;
            justify-content: center;
            align-items: center;  /* Subtle shadow for subtitle */
        }

        /* Button styling */
        .stButton.st-emotion-cache-8atqhb.e1mlolmg0 {
            position: absolute; /* Absolute positioning to place it below title/subtitle */
            bottom: 180px; /* Position it slightly above the bottom of the container */
            right:30px;
            display: flex;
            align-content: center;
            justify-content: center;
            align-items: center;
            z-index: 2; /* Ensure button is above the overlay */
        }

        .stButton > button {
            background-color: #E50914;
            color: white;
            font-size: 1.2rem;
            padding: 0.75rem 2rem;
            border-radius: 8px;
            border: none;
            cursor: pointer;
            transition: background-color 0.3s;
            margin-top: 20px;
        }

        .stButton > button:hover {
            background-color: #b20710;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class='centered'>
        <div class='title'>ANIFLIX 🎥</div>
        <div class='subtitle'>Unleash your next anime obsession powered by AI.</div>
    </div>
""", unsafe_allow_html=True)

# Start Recommendation Button - Positioned below the title and subtitle
if st.button("Start Recommending"):
    st.switch_page("pages/Login.py")


# Top 10 Anime Carousel - Ranking with Background Image Cards
st.markdown("<h2 style='text-align: center; color: #E50914; margin-top: 50px;font-size:3rem;'>Trending Anime All Time 🚀</h2>", unsafe_allow_html=True)

top_anime = [
    {"title": "Attack on Titan", "image": "https://upload.wikimedia.org/wikipedia/en/d/df/Humanity_in_Chains.png", "rank": 1, "desc": "A thrilling anime about humanity's fight against Titans."},
    {"title": "Naruto", "image": "https://videos.openai.com/vg-assets/assets%2Ftask_01jsw6sqb6ewa90h76gywkanyq%2F1745777204_img_0.webp?st=2025-04-27T16%3A20%3A44Z&se=2025-05-03T17%3A20%3A44Z&sks=b&skt=2025-04-27T16%3A20%3A44Z&ske=2025-05-03T17%3A20%3A44Z&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skoid=aa5ddad1-c91a-4f0a-9aca-e20682cc8969&skv=2019-02-02&sv=2018-11-09&sr=b&sp=r&spr=https%2Chttp&sig=tKs5XddkhIOBcHpYMQB6TLVYNuCfgqvZ%2FwDZv1bMN1w%3D&az=oaivgprodscus", "rank": 2, "desc": "Follow Naruto's journey to becoming the strongest ninja."},
    {"title": "One Piece", "image": "https://upload.wikimedia.org/wikipedia/en/9/90/One_Piece%2C_Volume_61_Cover_%28Japanese%29.jpg", "rank": 3, "desc": "A pirate adventure searching for the ultimate treasure."},
    {"title": "Demon Slayer", "image": "https://upload.wikimedia.org/wikipedia/en/2/21/Kimetsu_no_Yaiba_Mugen_Ressha_Hen_Poster.jpg", "rank": 4, "desc": "A tale of a boy seeking revenge against demons."},
    {
        "title": "Solo Leveling",
        "image": "https://upload.wikimedia.org/wikipedia/en/thumb/9/93/Solo_Leveling_season_2_key_visual.jpg/250px-Solo_Leveling_season_2_key_visual.jpg",
        "rank": 5,
        "desc": "Follow Sung Jin-Woo as he evolves from the weakest hunter to the strongest being in a world full of dungeons and monsters."
    },
    {
        "title": "Bleach",
        "image": "https://upload.wikimedia.org/wikipedia/en/thumb/7/72/Bleachanime.png/250px-Bleachanime.png",
        "rank": 6,
        "desc": "Ichigo Kurosaki gains the powers of a Soul Reaper and must protect the living and the spirits from evil forces."
    },
    {
        "title": "Jujutsu Kaisen",
        "image": "https://upload.wikimedia.org/wikipedia/en/0/07/JujutsuKaisenkeyvisual.jpg",
        "rank": 7,
        "desc": "Yuji Itadori joins a secret organization to fight curses after consuming a powerful cursed object."
    },
    {
        "title": "Black Clover",
        "image": "https://upload.wikimedia.org/wikipedia/en/6/69/Black_Clover%2C_volume_1.jpg",
        "rank": 8,
        "desc": "Asta, a boy born without magic, dreams of becoming the Wizard King in a world where magic is everything."
    },
    {
        "title": "Death Note",
        "image": "https://upload.wikimedia.org/wikipedia/en/thumb/7/72/Death_Note_Characters.jpg/250px-Death_Note_Characters.jpg",
        "rank": 9,
        "desc": "Light Yagami discovers a mysterious notebook that lets him kill anyone whose name he writes in it, leading to a high-stakes battle of wits."
    },
    {
        "title": "Classroom of the Elite",
        "image": "https://myanimelist.net/images/anime/1010/124180.jpg",
        "rank": 10,
        "desc": "At an elite high school, students must fight, manipulate, and strategize to survive and thrive in a cutthroat academic world."
    }

]


# Custom CSS for carousel
st.markdown("""
    <style>
        .scrolling-wrapper {
            overflow-x: auto;
            display: flex;
            flex-wrap: nowrap;
            gap: 20px;
            padding: 20px;
        }
        
        .anime-card {
            flex: 0 0 auto;
            background-color: #141414;
            width: 300px;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.6);
            position: relative;
            transition: transform 0.3s ease;
        }

        .anime-card:hover {
            transform: scale(1.05);
        }

        .anime-image {
            position: relative;
            height: 400px;
            background-size: cover;
            background-position: center;
        }

        .rank-badge {
            position: absolute;
            top: 10px;
            left: 10px;
            background-color: #E50914;
            color: white;
            font-weight: bold;
            padding: 5px 12px;
            border-radius: 8px;
            font-size: 1.2rem;
        }

        .anime-details {
            padding: 15px;
            color: white;
            text-align: center;
        }

        .anime-title {
            font-size: 1.5rem;
            font-weight: bold;
            margin-bottom: 10px;
        }

        .anime-desc {
            font-size: 0.9rem;
            color: #ccc;
        }

        /* Hide Scrollbar */
        .scrolling-wrapper::-webkit-scrollbar {
            display: none;
        }
        @media (max-width: 768px) {
    .scrolling-wrapper {
        gap: 10px;
        padding: 10px;
    }

    .anime-card {
        width: 250px !important;
        height: 450px !important;
    }

    .anime-image {
        height: 300px !important;
    }

    .card-title {
        font-size: 1.2rem !important;
    }

    .card-desc {
        font-size: 0.8rem !important;
        max-height: 80px !important;
    }

    .rank-badge {
        font-size: 1rem !important;
        padding: 4px 10px !important;
    }
}

@media (max-width: 480px) {
    .anime-card {
        width: 200px !important;
        height: 400px !important;
    }

    .anime-image {
        height: 250px !important;
    }

    .card-title {
        font-size: 1rem !important;
    }

    .card-desc {
        font-size: 0.75rem !important;
        max-height: 60px !important;
    }

    .rank-badge {
        font-size: 0.9rem !important;
        padding: 3px 8px !important;
    }
}
    </style>
""", unsafe_allow_html=True)

# Custom CSS to hide Streamlit's scrollbars completely
hide_streamlit_style = """
    <style>
    /* Hide Streamlit's default scrollbars */
    section.main > div { overflow: hidden; }
    </style>
"""

# HTML + CSS for smooth horizontal scrolling inside only, plus Netflix fonts + hover effects
html_code = """
<div style="overflow-x: auto; overflow-y: hidden; white-space: nowrap; padding: 20px; -ms-overflow-style: none; scrollbar-width: none; font-family: 'Netflix Sans', 'Helvetica Neue', 'Arial', sans-serif;">
    <style>
        /* Hide scrollbar for webkit browsers */
        div::-webkit-scrollbar {
            display: flex;
        }
        /* Hover Effects */
        .card-title:hover {
            color: #E50914; /* Netflix Red */
            transition: color 0.3s ease;
            cursor: pointer;
        }
        .card-desc:hover {
            color: #E50914; /* Netflix Red */
            transition: color 0.3s ease;
            cursor: pointer;
        }
        /* Card Hover Animation - Moves card upwards and increases size */
        .anime-card:hover {
            transform: translateY(-15px) scale(1.05); /* Moves the card up and scales it */
            box-shadow: 0 16px 50px rgba(0,0,0,0.8); /* Adds a larger shadow for the lifted effect */
            transition: transform 0.3s ease, box-shadow 0.3s ease; /* Smooth transition */
        }
        .card-desc{
        font-size: 0.9rem;
            color: #ccc;
            overflow: hidden;
            text-wrap:auto;
            text-overflow: ellipsis;
            max-height:100px;
            width:100%;
        </style>
"""

for anime in top_anime:
    img_url = anime['image']
    print(img_url)

    html_code += f"""
    <div class="anime-card" style="display: inline-block; background-color: #141414; color: white;height:520px; width: 300px; margin-right: 20px; border-radius: 15px; overflow: hidden; box-shadow: 0 8px 24px rgba(0,0,0,0.6); font-family: 'Netflix Sans', 'Helvetica Neue', 'Arial', sans-serif;">
        <div style="position: relative; height: 400px; background-image: url('{img_url}'); background-size: cover; background-position: center;">
            <div style="position: absolute; top: 10px; left: 10px; background-color: #E50914; color: white; font-weight: bold; padding: 5px 12px; border-radius: 8px; font-size: 1.2rem;">
                #{anime['rank']}
            </div>
        </div>
        <div style="padding: 15px; text-align: center;">
            <div class="card-title" style="font-size: 1.5rem; font-weight: bold; margin-bottom: 10px;">{anime['title']}</div>
            <div class="card-desc">{anime['desc']}</div>
        </div>
    </div>
    """

html_code += "</div>"

# Inject CSS and Render HTML
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
components.html(html_code, height=550)

#Genre Section
st.markdown("<h2 style='text-align: center; color: #E50914;font-size:3rem;'>Anime Genres 🎭</h2>", unsafe_allow_html=True)

st.markdown("""
<style>
    /* Genre cards */
    .background {
        text-align: center;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.6);
        transition: transform 0.3s ease;
        color: white;
        position: relative;
        overflow: hidden;
        margin:10px;
        height:400px;
        background-color: rgba(0, 0, 0, 0.6); /* Default background overlay */
    }
    .background:hover {
        transform: scale(1.05);
    }
    .background img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        position: absolute;
        top: 0;
        left: 0;
        z-index: -1; /* Ensure image stays behind the text */
        opacity: 0.4; /* Less opacity on the background image */
    }
    .genre-card h3 {
        margin-top: 15px;
        z-index: 1; /* Ensure text stays above the background */
        position: relative;
    }

    
</style>
""", unsafe_allow_html=True)

# List of anime genres with corresponding images
genres = [
    {"name": "Action", "image": "https://videos.openai.com/vg-assets/assets%2Ftask_01jsvf9ypff6ctewt8zqp8d7rt%2F1745752564_img_0.webp?st=2025-04-27T09%3A54%3A23Z&se=2025-05-03T10%3A54%3A23Z&sks=b&skt=2025-04-27T09%3A54%3A23Z&ske=2025-05-03T10%3A54%3A23Z&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skoid=aa5ddad1-c91a-4f0a-9aca-e20682cc8969&skv=2019-02-02&sv=2018-11-09&sr=b&sp=r&spr=https%2Chttp&sig=ROPaksc5B6aLBU2P2DcAA3sYiPAswV51oS4ytuxMkB4%3D&az=oaivgprodscus", "class": "action-card"},
    {"name": "Adventure", "image": "https://videos.openai.com/vg-assets/assets%2Ftask_01jsvfhpwheb2a7btsq2k6hg3g%2F1745752846_img_1.webp?st=2025-04-27T09%3A54%3A45Z&se=2025-05-03T10%3A54%3A45Z&sks=b&skt=2025-04-27T09%3A54%3A45Z&ske=2025-05-03T10%3A54%3A45Z&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skoid=aa5ddad1-c91a-4f0a-9aca-e20682cc8969&skv=2019-02-02&sv=2018-11-09&sr=b&sp=r&spr=https%2Chttp&sig=r%2BfJBvVGGFFPiRDLiInR%2BWw%2FvklDmyXvOPwPGRAT46o%3D&az=oaivgprodscus", "class": "adventure-card"},
    {"name": "Romance", "image": "https://videos.openai.com/vg-assets/assets%2Ftask_01jsvfp7t5ep992ndv359d9x9c%2F1745752993_img_0.webp?st=2025-04-27T09%3A55%3A51Z&se=2025-05-03T10%3A55%3A51Z&sks=b&skt=2025-04-27T09%3A55%3A51Z&ske=2025-05-03T10%3A55%3A51Z&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skoid=aa5ddad1-c91a-4f0a-9aca-e20682cc8969&skv=2019-02-02&sv=2018-11-09&sr=b&sp=r&spr=https%2Chttp&sig=n4Aq7DvST3SnFzeSHjK2Q6BdlXqVbHypBT5g%2FNZYBsg%3D&az=oaivgprodscus", "class": "romance-card"},
    {"name": "Comedy", "image": "https://videos.openai.com/vg-assets/assets%2Ftask_01jsvfv5nwf0mtkk3pjxbb1xyy%2F1745753159_img_0.webp?st=2025-04-27T09%3A55%3A12Z&se=2025-05-03T10%3A55%3A12Z&sks=b&skt=2025-04-27T09%3A55%3A12Z&ske=2025-05-03T10%3A55%3A12Z&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skoid=aa5ddad1-c91a-4f0a-9aca-e20682cc8969&skv=2019-02-02&sv=2018-11-09&sr=b&sp=r&spr=https%2Chttp&sig=0OezFU0BkVgRWKAbjnP9iGkwR4znNo7aTYOu6A01xS0%3D&az=oaivgprodscus", "class": "comedy-card"},
    {"name": "Fantasy", "image": "https://videos.openai.com/vg-assets/assets%2Ftask_01jsvgeq3efgrbz0z2agvr81ha%2F1745753770_img_1.webp?st=2025-04-27T09%3A54%3A23Z&se=2025-05-03T10%3A54%3A23Z&sks=b&skt=2025-04-27T09%3A54%3A23Z&ske=2025-05-03T10%3A54%3A23Z&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skoid=aa5ddad1-c91a-4f0a-9aca-e20682cc8969&skv=2019-02-02&sv=2018-11-09&sr=b&sp=r&spr=https%2Chttp&sig=etgbx4ycxJ0NSOfV8baMlrhA%2FbQR6Xi8t2Sxw031CLk%3D&az=oaivgprodscus", "class": "fantasy-card"},
    {"name": "Horror", "image": "https://videos.openai.com/vg-assets/assets%2Ftask_01jsvm4xd5f8e8cj8kvqhpyw09%2F1745757677_img_0.webp?st=2025-04-27T11%3A24%3A53Z&se=2025-05-03T12%3A24%3A53Z&sks=b&skt=2025-04-27T11%3A24%3A53Z&ske=2025-05-03T12%3A24%3A53Z&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skoid=aa5ddad1-c91a-4f0a-9aca-e20682cc8969&skv=2019-02-02&sv=2018-11-09&sr=b&sp=r&spr=https%2Chttp&sig=0twM8ketvI5xT6d6e7RLauqWhZ7ke%2BvW2EBu8hPe8Bo%3D&az=oaivgprodscus", "class": "horror-card"},
]

# Genre cards in rows
cols = st.columns(3)
for idx, genre in enumerate(genres):
    with cols[idx % 3]:
        st.markdown(f"""
            <div class="genre-card {genre['class']}" >
                <div class="background" style="position: relative;opacity:0.7; background-image: url('{genre['image']}'); background-size: cover; background-position: center; display: flex; align-items: center; justify-content: center;"></div>
                <h3 style="color: white;position:absolute;top:40%;left:40%; text-shadow: 2px 2px 6px rgba(0, 0, 0, 0.7); font-size: 2.5rem;">
                    {genre['name']}
                </h3>
            </div> 
        """, unsafe_allow_html=True)

# Footer or Additional Information
st.markdown("""
    <style>
        .footer {
            background-color: #141414;
            color: #757575;
            padding: 40px 20px;
            font-family: 'Helvetica Neue', Arial, sans-serif;
            text-align:center;
        }
        .footer h4 {
            color: #E50914;
            font-size: 2rem;
            margin-bottom: 10px;
        }
        .footer p {
            font-size: 1.3rem;
            margin-bottom: 20px;
        }
        .footer .links {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 30px;
        }
        .footer .links a {
            color: #757575;
            font-size: 0.8rem;
            text-decoration: none;
            transition: color 0.2s ease;
        }
        .footer .links a:hover {
            color: #ffffff;
            text-decoration: underline;
        }
    </style>

    <div class="footer">
        <h4>Welcome to Aniflix 🎥</h4>
        <p>Your one-stop platform to discover the best anime content recommended by AI.</p>
        <div class="links">
            <a href="#">About Us</a>
            <a href="#">Help Center</a>
            <a href="#">Terms of Use</a>
            <a href="#">Privacy Policy</a>
            <a href="#">Contact</a>
        </div>
    </div>
""", unsafe_allow_html=True)

