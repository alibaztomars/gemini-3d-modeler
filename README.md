# Gemini 3D Object Generator

![Gemini 3D Object Generator](https://raw.githubusercontent.com/alibaztomars/gemini-3d-modeler/main/app_screenshot.png)

A Streamlit web application that uses Google's Gemini API to generate and visualize 3D objects based on text descriptions. The app supports both English and Turkish languages.

## 🌟 Features

- Create 3D objects from text descriptions using Gemini API
- Visualize 3D objects in real-time with interactive controls
- Support for multiple object types (cube, sphere, cylinder, pyramid, cone, torus, custom)
- Color customization options
- Bilingual interface (English and Turkish)
- Download generated 3D object data as JSON
- Fallback to default 3D objects when no description is provided

## 🛠️ Installation

### Prerequisites

- Python 3.7+
- Google Gemini API key

### Step 1: Clone the repository

```bash
git clone https://github.com/alibaztomars/gemini-3d-modeler.git
cd gemini-3d-modeler
```

### Step 2: Create a virtual environment (optional but recommended)

```bash
python -m venv venv
```

Activate the virtual environment:

- On Windows:
```bash
venv\Scripts\activate
```

- On macOS/Linux:
```bash
source venv/bin/activate
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

If you don't have a requirements.txt file, install the required packages manually:

```bash
pip install streamlit google-generativeai numpy plotly
```

## 🚀 Usage

### Step 1: Get a Google Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Get API key"
4. Create a new API key
5. Copy the generated API key

### Step 2: Run the application

```bash
streamlit run app.py
```

The application will start and open in your default web browser.

### Step 3: Using the application

1. Enter your Gemini API key in the sidebar
2. Select a Gemini model version (gemini-2.0-flash-exp, gemini-1.5-pro, or gemini-1.5-flash)
3. Enter a description of the 3D object you want to create
4. Select an object type and main color
5. Click the "Create 3D Object" button
6. The application will generate 3D object data using the Gemini API
7. The 3D object will be visualized in the application
8. You can download the generated JSON data for future use

## 📦 Data Format

The application generates and works with 3D object data in the following JSON format:

```json
{
  "type": "cube",  // cube, sphere, cylinder, pyramid, cone, torus, custom
  "vertices": [[x1,y1,z1], [x2,y2,z2], ...],  // 3D coordinates
  "faces": [[v1,v2,v3], [v2,v3,v4], ...],  // indices in vertices array
  "colors": ["#FF0000", "#00FF00", ...],  // color codes for each face
  "name": "Red Cube"  // object name
}
```

## 🌐 Language Support

The application supports both English and Turkish languages. You can switch between languages using the dropdown menu in the top-right corner of the application.

## 🔄 Default Objects

If you don't provide a description or if the API fails to generate a valid 3D object, the application will display a default 3D object based on your selected object type and color.

## 🤖 How Gemini API is Used

The application constructs a prompt that includes:
- Your object description
- Selected object type
- Selected color preference
- Required data format

The Gemini API then generates JSON data that defines the 3D object, which is subsequently visualized in the application.

## 🖼️ Screenshots

![Main Interface](https://raw.githubusercontent.com/alibaztomars/gemini-3d-modeler/main/screenshots/main_interface.png)

![3D Visualization](https://raw.githubusercontent.com/alibaztomars/gemini-3d-modeler/main/screenshots/3d_visualization.png)

## 📝 License

[MIT](LICENSE)

## 🙏 Acknowledgments

- [Google Gemini API](https://ai.google.dev/gemini-api)
- [Streamlit](https://streamlit.io/)
- [Plotly](https://plotly.com/)

## 📞 Contact

Ali Baz Tomars - [@alibaztomars](https://github.com/alibaztomars)

Project Link: [https://github.com/alibaztomars/gemini-3d-modeler](https://github.com/alibaztomars/gemini-3d-modeler)
