import pickle
import streamlit as st
import requests
import os

# TMDB API anahtarı
API_KEY = "8265bd1679663a7ea12ac168da84d2e8"

# Fonksiyonlar
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    data = requests.get(url).json()
    if "poster_path" in data:
        poster_path = data["poster_path"]
        return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    else:
        return None

def fetch_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    data = requests.get(url).json()
    return data

def recommend(movie, max_results=5):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_info = []
    count = 0
    for i in distances[1:]:
        movie_id = movies.iloc[i[0]].movie_id
        movie_details = fetch_movie_details(movie_id)
        if movie_details:
            recommended_movie_info.append({
                "title": movie_details["title"],
                "poster": fetch_poster(movie_id),
                "overview": movie_details["overview"],
                "rating": movie_details["vote_average"],
                "release_date": movie_details["release_date"],
                "genres": [genre["name"] for genre in movie_details["genres"]],
                "cast": fetch_movie_cast(movie_id),
                "director": fetch_movie_crew(movie_id, "Director"),
                "writer": fetch_movie_crew(movie_id, "Writer")
            })
            count += 1
            if count >= max_results:
                break

    return recommended_movie_info

def fetch_movie_cast(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={API_KEY}"
    data = requests.get(url).json()
    cast = [actor["name"] for actor in data["cast"][:5]]  # İlk 5 oyuncuyu al
    return cast

def fetch_movie_crew(movie_id, job):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={API_KEY}"
    data = requests.get(url).json()
    crew = [member["name"] for member in data["crew"] if member["job"] == job]
    return crew

# Streamlit arayüzü
st.set_page_config(layout="wide")
st.title('🎬 Film Öneri Sistemi 🎥')


# Sidebar
st.sidebar.title("🎬 Bilgi")

# Metin
st.sidebar.write("""
Bu uygulama, [TMDB Movie Metadata](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata) veri seti üzerinde analiz yapılarak oluşturulmuştur.
Veri seti, filmlerin başlık, özet, oyuncu kadrosu, yönetmen, yayın tarihi gibi bilgilerini içermektedir.
Analiz aşamasında veri seti üzerinde keşifsel veri analizi (EDA) yapılmış ve benzerlik tabanlı bir öneri sistemi için gerekli hazırlık işlemleri gerçekleştirilmiştir.
Sonrasında ise cosine similarity kullanılarak bir film seçildiğinde benzer filmlerin önerilmesi için bir model kurulmuştur.
""")

# Metinler
st.write("✨ **Film Seçin:** Aşağıdaki listeden favori filminizi seçin. Hangi türde film izlemek istediğinizi seçmek için bir adım daha yakınsınız!")

st.write('🎉 **Önerileri Görüntüleyin:** Seçtiğiniz film hakkında en iyi önerileri almak için "Önerileri Görüntüleyin" düğmesine tıklayın. Sürprizlere hazır olun!')

st.write("🌟 **Eğlenceli Detaylar:** Film önerileriyle birlikte oyuncu kadrosu, yönetmen, yayın tarihi ve daha fazlası hakkında eğlenceli bilgileri keşfedin.")

st.write("🔍 **Keşfetmeye Hazır mısınız?:** Hadi başlayalım! Sevdiğiniz filmleri keşfetmek ve yeni favoriler keşfetmek için şimdi başlayın!")
# Filmleri yükle
file_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(file_dir, 'movie_list.pkl')
movies = pickle.load(open(file_path, 'rb'))

file_path_similarity = os.path.join(file_dir, 'similarity.pkl')
similarity = pickle.load(open(file_path_similarity, 'rb'))

# Film seçme kutusu
selected_movie = st.selectbox("Lütfen Film Seçiniz.", movies['title'].values)

# Öneri sayısını belirleme
max_results = st.slider("Kaç Adet Öneri İstiyorsunuz ?", 1, 10, 5)

if st.button('Önerileri Göster'):
    recommended_movies = recommend(selected_movie, max_results)
    cols = st.columns(3)  # 3 sütun oluştur
    for i, movie in enumerate(recommended_movies):
        with cols[i % 3]:  # Sütunları döngüyle dolaş
            st.subheader(movie["title"])
            st.image(movie["poster"], caption=movie["overview"], width=500)
            st.write(f"**Rating:** {movie['rating']}")
            st.write(f"**Release Date:** {movie['release_date']}")
            st.write(f"**Genres:** {', '.join(movie['genres'])}")
            st.write(f"**Director:** {', '.join(movie['director'])}")
            st.write(f"**Cast:** {', '.join(movie['cast'])}")

if st.button("Hazırlayan"):
        st.write("Deniz ÜNLÜ")
        st.write("İletişim: denizstatistics@gmail.com")
        st.write("Linkedin: www.linkedin.com/in/deniz-ünlü-5a5036244")
        st.write("Github: https://github.com/denizzunlu")
