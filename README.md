# 🤖 The Tech Alpha - AI Image Assistant

यह एक **Professional AI Image Assistant** वेब एप्लीकेशन है जिसे **Streamlit** और **TensorFlow** की मदद से बनाया गया है। 

> 🎯 **Internship Project:** यह प्रोजेक्ट **"The Tech Alpha"** में मेरी इंटर्नशिप का **दूसरा प्रोजेक्ट (Second Internship Task)** है। यह एक इंटेलिजेंट AI टूल है जो यूजर द्वारा अपलोड की गई इमेज या PDF की जांच करके सटीक जवाब देता है।

---

## ✨ Features (मुख्य खूबियां)

* **Multi-Model Support:** आप अपनी जरूरत के हिसाब से दो बेहतरीन AI मॉडल्स चुन सकते हैं:
  * `MobileNetV2` (तेज और हल्का काम करने के लिए)
  * `ResNet50` (अधिक सटीक रिजल्ट्स के लिए)
* **Dual Input Modes:** आप कंप्यूटर से इमेज/PDF फाइल अपलोड कर सकते हैं या फिर **Live Camera** का उपयोग करके तुरंत फोटो खींच सकते हैं।
* **PDF Analysis Support:** `PyMuPDF (fitz)` की मदद से यह एप्लीकेशन PDF फाइल के पहले पेज को इमेज में बदलकर उसकी भी जांच कर सकती है।
* **Persistent Chat Memory:** इसमें `SQLite3` डेटाबेस का उपयोग किया गया है, जिससे ऐप बंद होने या रीफ्रेश होने के बाद भी आपकी चैट हिस्ट्री सुरक्षित रहती है।
* **Clean UI/UX:** ब्लैक और व्हाइट थीम के साथ एक बहुत ही साफ और आसान इंटरफेस दिया गया है।

---

## 🛠️ Tech Stack (किन चीजों का इस्तेमाल हुआ है)

* **Frontend:** Streamlit
* **Deep Learning Framework:** TensorFlow / Keras
* **Image Processing:** Pillow (PIL), NumPy
* **PDF Processing:** PyMuPDF (fitz)
* **Database:** SQLite3

---

## 🚀 How to Run (इसे अपने कंप्यूटर पर कैसे चलाएं)

इस प्रोजेक्ट को अपने लोकल कंप्यूटर पर चलाने के लिए नीचे दिए गए स्टेप्स को फॉलो करें:

### 1. प्रोजेक्ट डाउनलोड करें (Clone the Repository)
सबसे पहले कोड को डाउनलोड करें और उस फोल्डर के अंदर जाएं:
```bash
git clone https://github.com
cd TheTechAlpha_AI_IMAGE_CLASSIFICATION_TOOL
```

### 2. जरूरी लाइब्रेरी इंस्टॉल करें (Install Requirements)
टर्मिनल या कमांड प्रॉम्प्ट (CMD) खोलें और नीचे दी गई कमांड चलाकर सभी जरूरी पैकेजेस इंस्टॉल करें:
```bash
pip install streamlit tensorflow numpy Pillow PyMuPDF
```

### 3. एप्लीकेशन को रन करें (Run the App)
अब प्रोजेक्ट फोल्डर के अंदर रहते हुए टर्मिनल पर यह कमांड टाइप करके **Enter** दबाएं:
```bash
streamlit run thetechalpha.py
```
*इसके बाद आपके ब्राउज़र में `http://localhost:8501` पर यह AI टूल खुल जाएगा।*

---

## 📂 Project Structure (प्रोजेक्ट की फाइलें)
* `thetechalpha.py` - मुख्य पायथन कोड फाइल।
* `chat_history.db` - चैट बैकअप रखने के लिए डेटाबेस फाइल (ऐप चलने के बाद खुद बनेगी)।
* `README.md` - प्रोजेक्ट की जानकारी।
