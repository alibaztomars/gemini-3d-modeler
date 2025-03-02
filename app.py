import os
import json
import streamlit as st
import google.generativeai as genai
import numpy as np
import plotly.graph_objects as go

# Dil desteği
languages = {
    "Türkçe": {
        "app_title": "Gemini API ile 3D Nesne Oluşturucu",
        "api_key_label": "Gemini API Key",
        "model_version_label": "Gemini Model Versiyonu",
        "api_success": "API key başarıyla ayarlandı!",
        "api_error": "API key ayarlanırken hata oluştu:",
        "object_creation_header": "3D Nesne Oluşturma",
        "object_desc_label": "Oluşturmak istediğiniz 3D nesnenin açıklamasını yazın:",
        "object_desc_placeholder": "Örnek: Kırmızı bir küp, üzerinde mavi çizgiler olan",
        "object_type_label": "Nesne tipi:",
        "color_label": "Ana renk:",
        "create_button": "3D Nesne Oluştur",
        "data_format_title": "Veri Formatı Örneği",
        "creating_message": "Gemini API ile 3D nesne verisi oluşturuluyor...",
        "json_error": "API yanıtından geçerli JSON verisi çıkarılamadı.",
        "default_showing": "Varsayılan 3D nesne gösteriliyor...",
        "error_message": "3D nesne verisi oluşturulurken bir hata oluştu:",
        "default_object_header": "Varsayılan 3D Nesne",
        "json_data_header": "Oluşturulan 3D Nesne Verisi",
        "visualization_header": "3D Görselleştirme",
        "download_json": "JSON Verisini İndir",
        "how_to_use_title": "Nasıl Kullanılır?",
        "how_to_use": """
        1. Sidebar'dan Gemini API anahtarınızı ve model versiyonunu seçin
        2. Oluşturmak istediğiniz 3D nesnenin açıklamasını yazın
        3. Nesnenin tipini ve rengini seçin
        4. "3D Nesne Oluştur" butonuna tıklayın
        5. Gemini API, verdiğiniz açıklamaya göre 3D nesne verisi oluşturacak
        6. Oluşturulan veri 3D olarak görselleştirilecek
        7. JSON verisini indirebilirsiniz
        
        **Not:** Gemini API anahtarı almanız gerekiyor. Google AI Studio'dan bir API anahtarı edinebilirsiniz.
        """,
        "api_key_how_to_title": "Gemini API Key Nasıl Alınır?",
        "api_key_how_to": """
        1. [Google AI Studio](https://makersuite.google.com/app/apikey) adresine gidin
        2. Google hesabınızla giriş yapın
        3. "Get API key" butonuna tıklayın
        4. Yeni bir API anahtarı oluşturun
        5. Oluşturulan API anahtarını kopyalayın ve bu uygulamada kullanın
        """,
        "object_types": [
            "Basit Küp", 
            "Küre", 
            "Silindir", 
            "Piramit", 
            "Koni", 
            "Torus (Simit)", 
            "Özel Şekil"
        ],
        "color_palette": [
            "Kırmızı", 
            "Mavi", 
            "Yeşil", 
            "Sarı", 
            "Mor", 
            "Turuncu", 
            "Pembe", 
            "Beyaz",
            "Siyah", 
            "Gri", 
            "Turkuaz"
        ],
        "prompts": {
            "intro": "Bana aşağıdaki açıklamaya göre bir 3D nesne için JSON formatında veri oluştur:",
            "description": "Açıklama:",
            "type": "Tip:",
            "color": "Renk:",
            "format_request": "Lütfen aşağıdaki formatta JSON verisi döndür:",
            "only_json": "Sadece JSON verisini döndür, ekstra açıklama ekleme."
        }
    },
    "English": {
        "app_title": "3D Object Generator with Gemini API",
        "api_key_label": "Gemini API Key",
        "model_version_label": "Gemini Model Version",
        "api_success": "API key set successfully!",
        "api_error": "Error setting API key:",
        "object_creation_header": "Create 3D Object",
        "object_desc_label": "Enter description of the 3D object you want to create:",
        "object_desc_placeholder": "Example: A red cube with blue lines on it",
        "object_type_label": "Object type:",
        "color_label": "Main color:",
        "create_button": "Create 3D Object",
        "data_format_title": "Data Format Example",
        "creating_message": "Creating 3D object data with Gemini API...",
        "json_error": "Could not extract valid JSON data from API response.",
        "default_showing": "Showing default 3D object...",
        "error_message": "An error occurred while creating 3D object data:",
        "default_object_header": "Default 3D Object",
        "json_data_header": "Generated 3D Object Data",
        "visualization_header": "3D Visualization",
        "download_json": "Download JSON Data",
        "how_to_use_title": "How to Use",
        "how_to_use": """
        1. Enter your Gemini API key and select model version in the sidebar
        2. Write a description of the 3D object you want to create
        3. Select object type and color
        4. Click the "Create 3D Object" button
        5. Gemini API will generate 3D object data based on your description
        6. The generated data will be visualized in 3D
        7. You can download the JSON data
        
        **Note:** You need to obtain a Gemini API key from Google AI Studio.
        """,
        "api_key_how_to_title": "How to Get a Gemini API Key",
        "api_key_how_to": """
        1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
        2. Sign in with your Google account
        3. Click "Get API key"
        4. Create a new API key
        5. Copy the generated API key and use it in this application
        """,
        "object_types": [
            "Simple Cube", 
            "Sphere", 
            "Cylinder", 
            "Pyramid", 
            "Cone", 
            "Torus (Donut)", 
            "Custom Shape"
        ],
        "color_palette": [
            "Red", 
            "Blue", 
            "Green", 
            "Yellow", 
            "Purple", 
            "Orange", 
            "Pink", 
            "White",
            "Black", 
            "Gray", 
            "Turquoise"
        ],
        "prompts": {
            "intro": "Create JSON format data for a 3D object based on the following description:",
            "description": "Description:",
            "type": "Type:",
            "color": "Color:",
            "format_request": "Please return JSON data in the following format:",
            "only_json": "Return only the JSON data, do not add extra explanation."
        }
    }
}

# Dil seçimi için durum kontrolü
if 'language' not in st.session_state:
    st.session_state.language = "English"

# Sayfa düzeni
st.set_page_config(layout="wide")

# Sağ üst köşe dil seçimi için sütunlar
col1, col2, col3 = st.columns([1, 6, 1])

with col3:
    selected_language = st.selectbox(
        "",
        options=list(languages.keys()),
        index=list(languages.keys()).index(st.session_state.language),
        key="language_selector"
    )
    st.session_state.language = selected_language

# Geçerli dildeki metinler
texts = languages[st.session_state.language]

# Streamlit uygulaması
st.title(texts["app_title"])

# API Key ayarları
api_key = st.sidebar.text_input(texts["api_key_label"], type="password")
model_version = st.sidebar.selectbox(
    texts["model_version_label"], 
    ["gemini-2.0-flash-exp", "gemini-1.5-pro", "gemini-1.5-flash"]
)

if api_key:
    os.environ["GOOGLE_API_KEY"] = api_key
    try:
        genai.configure(api_key=api_key)
        st.sidebar.success(texts["api_success"])
    except Exception as e:
        st.sidebar.error(f"{texts['api_error']} {str(e)}")

# 3D nesne isteme bölümü
st.header(texts["object_creation_header"])
nesne_aciklamasi = st.text_area(texts["object_desc_label"], 
                              placeholder=texts["object_desc_placeholder"])

nesne_tipleri = texts["object_types"]
secilen_tip = st.selectbox(texts["object_type_label"], nesne_tipleri)

renk_paleti = texts["color_palette"]
secilen_renk = st.selectbox(texts["color_label"], renk_paleti)

# Örnek verileri gösterme
with st.expander(texts["data_format_title"]):
    st.code("""
{
  "type": "cube",  // cube, sphere, cylinder, pyramid, cone, torus, custom
  "vertices": [[x1,y1,z1], [x2,y2,z2], ...],  // 3D coordinates
  "faces": [[v1,v2,v3], [v2,v3,v4], ...],  // indices in vertices array
  "colors": ["#FF0000", "#00FF00", ...],  // color codes for each face
  "name": "Red Cube"  // object name
}
    """)

def parse_json_from_text(text):
    """Metin içinden JSON verilerini çıkarır"""
    try:
        # JSON bloğunu metinden çıkarma
        start_idx = text.find('{')
        end_idx = text.rfind('}') + 1
        
        if start_idx == -1 or end_idx == 0:
            return None
        
        json_str = text[start_idx:end_idx]
        return json.loads(json_str)
    except Exception as e:
        st.error(f"JSON ayrıştırma hatası: {str(e)}")
        st.text("Ham metin çıktısı:")
        st.text(text)
        return None

def create_3d_visualization(data):
    """JSON verisinden 3D görselleştirme oluşturur"""
    fig = go.Figure()
    
    if data["type"] == "cube":
        # Küp için
        vertices = np.array(data["vertices"])
        faces = data["faces"]
        colors = data["colors"]
        
        for i, face in enumerate(faces):
            color = colors[i % len(colors)]
            face_vertices = vertices[face]
            
            # Yüzün köşelerini ve ilk köşeyi ekleyerek kapalı bir şekil oluştur
            x = list(face_vertices[:, 0]) + [face_vertices[0, 0]]
            y = list(face_vertices[:, 1]) + [face_vertices[0, 1]]
            z = list(face_vertices[:, 2]) + [face_vertices[0, 2]]
            
            fig.add_trace(go.Mesh3d(
                x=face_vertices[:, 0],
                y=face_vertices[:, 1],
                z=face_vertices[:, 2],
                i=[0],
                j=[1],
                k=[2],
                color=color,
                opacity=0.8,
                name=f"Face {i+1}"
            ))
            
            # Yüzeyin kenarlarını çizgi olarak ekle
            fig.add_trace(go.Scatter3d(
                x=x, y=y, z=z,
                mode='lines',
                line=dict(color='black', width=2),
                showlegend=False
            ))
    
    elif data["type"] == "sphere":
        # Küre için
        center = data.get("center", [0, 0, 0])
        radius = data.get("radius", 1)
        color = data.get("colors", ["#FF0000"])[0]
        
        # Küre yüzeyi oluştur
        u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
        x = center[0] + radius * np.cos(u) * np.sin(v)
        y = center[1] + radius * np.sin(u) * np.sin(v)
        z = center[2] + radius * np.cos(v)
        
        fig.add_trace(go.Surface(
            x=x, y=y, z=z,
            colorscale=[[0, color], [1, color]],
            showscale=False,
            opacity=0.8
        ))
    
    elif data["type"] == "cylinder":
        # Silindir için
        base_center = data.get("base_center", [0, 0, 0])
        top_center = data.get("top_center", [0, 0, 1])
        radius = data.get("radius", 1)
        color = data.get("colors", ["#0000FF"])[0]
        
        # Silindir yanlarını oluştur
        theta = np.linspace(0, 2*np.pi, 36)
        base_x = base_center[0] + radius * np.cos(theta)
        base_y = base_center[1] + radius * np.sin(theta)
        base_z = np.full_like(theta, base_center[2])
        
        top_x = top_center[0] + radius * np.cos(theta)
        top_y = top_center[1] + radius * np.sin(theta)
        top_z = np.full_like(theta, top_center[2])
        
        fig.add_trace(go.Surface(
            x=np.vstack([base_x, top_x]),
            y=np.vstack([base_y, top_y]),
            z=np.vstack([base_z, top_z]),
            colorscale=[[0, color], [1, color]],
            showscale=False,
            opacity=0.8
        ))
        
        # Alt ve üst tabanlar
        fig.add_trace(go.Mesh3d(
            x=base_x, y=base_y, z=base_z,
            i=list(range(0, 34, 3)),
            j=list(range(1, 35, 3)),
            k=list(range(2, 36, 3)),
            color=color,
            opacity=0.8
        ))
        
        fig.add_trace(go.Mesh3d(
            x=top_x, y=top_y, z=top_z,
            i=list(range(0, 34, 3)),
            j=list(range(1, 35, 3)),
            k=list(range(2, 36, 3)),
            color=color,
            opacity=0.8
        ))
    
    elif data["type"] in ["torus", "cone", "pyramid", "custom"]:
        # Diğer şekiller için doğrudan verteks ve yüzleri kullan
        vertices = np.array(data["vertices"])
        faces = data["faces"]
        colors = data["colors"]
        
        # Tüm şekli tek bir mesh olarak göster
        fig.add_trace(go.Mesh3d(
            x=vertices[:, 0],
            y=vertices[:, 1],
            z=vertices[:, 2],
            i=[face[0] for face in faces],
            j=[face[1] for face in faces],
            k=[face[2] for face in faces],
            facecolor=[colors[i % len(colors)] for i in range(len(faces))],
            opacity=0.8
        ))
    
    # Görünüm ayarları
    fig.update_layout(
        title=data.get("name", "3D Object"),
        scene=dict(
            xaxis=dict(showbackground=True, showticklabels=False, title=''),
            yaxis=dict(showbackground=True, showticklabels=False, title=''),
            zaxis=dict(showbackground=True, showticklabels=False, title=''),
            aspectmode='data'
        ),
        margin=dict(l=0, r=0, b=0, t=30),
        scene_camera=dict(
            eye=dict(x=1.5, y=1.5, z=1.5)
        )
    )
    
    return fig

def generate_default_3d_object(type_name, color_name):
    """Seçilen nesne tipine göre varsayılan 3D nesne verileri oluşturur"""
    # Renk isimlerini ingilizce/türkçe için birleştir
    color_map = {
        "Kırmızı": "#FF0000", "Red": "#FF0000", 
        "Mavi": "#0000FF", "Blue": "#0000FF", 
        "Yeşil": "#00FF00", "Green": "#00FF00", 
        "Sarı": "#FFFF00", "Yellow": "#FFFF00", 
        "Mor": "#800080", "Purple": "#800080", 
        "Turuncu": "#FFA500", "Orange": "#FFA500", 
        "Pembe": "#FFC0CB", "Pink": "#FFC0CB", 
        "Beyaz": "#FFFFFF", "White": "#FFFFFF",
        "Siyah": "#000000", "Black": "#000000", 
        "Gri": "#808080", "Gray": "#808080", 
        "Turkuaz": "#40E0D0", "Turquoise": "#40E0D0"
    }
    
    color_hex = color_map.get(color_name, "#FF0000")
    
    # İki dil için nesne tipleri eşleştirme
    type_map = {
        "Basit Küp": "cube", "Simple Cube": "cube",
        "Küre": "sphere", "Sphere": "sphere",
        "Silindir": "cylinder", "Cylinder": "cylinder",
        "Piramit": "pyramid", "Pyramid": "pyramid",
        "Koni": "cone", "Cone": "cone",
        "Torus (Simit)": "torus", "Torus (Donut)": "torus", 
        "Özel Şekil": "custom", "Custom Shape": "custom"
    }
    
    object_type = type_map.get(type_name, "cube")
    
    if object_type == "cube":
        return {
            "type": "cube",
            "vertices": [
                [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],
                [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]
            ],
            "faces": [
                [0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4],
                [1, 2, 6, 5], [2, 3, 7, 6], [3, 0, 4, 7]
            ],
            "colors": [color_hex] * 6,
            "name": f"{color_name} Cube/Küp"
        }
    elif object_type == "sphere":
        return {
            "type": "sphere",
            "center": [0, 0, 0],
            "radius": 1,
            "colors": [color_hex],
            "name": f"{color_name} Sphere/Küre"
        }
    elif object_type == "cylinder":
        return {
            "type": "cylinder",
            "base_center": [0, 0, 0],
            "top_center": [0, 0, 1],
            "radius": 0.5,
            "colors": [color_hex],
            "name": f"{color_name} Cylinder/Silindir"
        }
    # Diğer şekiller için de ön tanımlı veriler eklenebilir
    
    # Varsayılan: Küp
    return {
        "type": "cube",
        "vertices": [
            [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],
            [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]
        ],
        "faces": [
            [0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4],
            [1, 2, 6, 5], [2, 3, 7, 6], [3, 0, 4, 7]
        ],
        "colors": [color_hex] * 6,
        "name": f"{color_name} Object/Nesne"
    }

# Oluşturma butonu
if st.button(texts["create_button"]) and api_key:
    
    # API'den veri oluşturma seçeneği
    if nesne_aciklamasi:
        with st.spinner(texts["creating_message"]):
            try:
                # Gemini modeli ayarları
                model = genai.GenerativeModel(model_version)
                
                # İstek metni oluşturma - Seçilen dile göre
                prompts = texts["prompts"]
                istek_metni = f"""
                {prompts["intro"]}
                
                {prompts["description"]} {nesne_aciklamasi}
                {prompts["type"]} {secilen_tip}
                {prompts["color"]} {secilen_renk}
                
                {prompts["format_request"]}
                
                ```json
                {{
                  "type": "cube", // cube, sphere, cylinder, pyramid, cone, torus, custom
                  "vertices": [[x1,y1,z1], [x2,y2,z2], ...], // Vertices / Köşe noktaları
                  "faces": [[v1,v2,v3], [v2,v3,v4], ...], // Faces / Yüzeyler
                  "colors": ["#FF0000", "#00FF00", ...], // Colors / Renkler
                  "name": "Red Cube" // Name / İsim
                }}
                ```
                
                {prompts["only_json"]}
                """
                
                # Gemini API'ye istek gönderme
                response = model.generate_content(istek_metni)
                
                # Yanıttan JSON verisi çıkarma
                json_data = parse_json_from_text(response.text)
                
                if json_data:
                    # JSON verisi gösterme
                    st.subheader(texts["json_data_header"])
                    st.json(json_data)
                    
                    # 3D görselleştirme
                    st.subheader(texts["visualization_header"])
                    fig = create_3d_visualization(json_data)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # JSON verisini indirme
                    st.download_button(
                        label=texts["download_json"],
                        data=json.dumps(json_data, indent=2),
                        file_name=f"{json_data.get('name', '3d_object')}.json",
                        mime="application/json"
                    )
                else:
                    st.error(texts["json_error"])
                    # Varsayılan 3D nesne gösterme
                    st.info(texts["default_showing"])
                    default_data = generate_default_3d_object(secilen_tip, secilen_renk)
                    fig = create_3d_visualization(default_data)
                    st.plotly_chart(fig, use_container_width=True)
            
            except Exception as e:
                st.error(f"{texts['error_message']} {str(e)}")
                # Varsayılan 3D nesne gösterme
                st.info(texts["default_showing"])
                default_data = generate_default_3d_object(secilen_tip, secilen_renk)
                fig = create_3d_visualization(default_data)
                st.plotly_chart(fig, use_container_width=True)
    else:
        # API kullanmadan direkt varsayılan 3D nesne gösterme
        default_data = generate_default_3d_object(secilen_tip, secilen_renk)
        st.subheader(texts["default_object_header"])
        st.json(default_data)
        
        fig = create_3d_visualization(default_data)
        st.plotly_chart(fig, use_container_width=True)

# Kullanım kılavuzu
with st.expander(texts["how_to_use_title"]):
    st.markdown(texts["how_to_use"])

# API Key edinme hakkında bilgi
with st.expander(texts["api_key_how_to_title"]):
    st.markdown(texts["api_key_how_to"])