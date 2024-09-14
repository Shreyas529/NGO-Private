import streamlit as st

def about_us():
    st.markdown("""
    <style>
    body {
        background-color: #0F2027;
        background-image: linear-gradient(315deg, #0F2027 0%, #203A43 74%, #2C5364 100%);
        color: white;
    }
    
    
    
    p{
        font-size: 20px;
    }
    
    li{
        font-size: 20px;
    }    
    
    .stButton > button {
            background-color: #FF4B4B; /* Consistent color with app.py */
            color: white;
            border-radius: 30px;
            padding: 10px 24px;
            border: none;
            font-size: 16px;
            font-weight: 600;
            transition: all 0.3s ease;
            margin: 0 10px;
            width: 200px;
        }
        .stButton > button:hover {
            background-color: #FFFFFF; /* Hover effect */
            color: #FF4B4B;
            transform: scale(1.05);
            font-weight: bold;
        }
    
    hr.solid {
        border-top: 3px solid #bbb;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <hr class="solid">
    <h1  color: #FF4B4B;>About NexusNGO</h1>
    
    <p >At NexusNGO, we are driven by a mission to revolutionize the way individuals and organizations contribute to social causes. In a world where generosity and the desire to make a difference are abundant, many still face challenges in identifying trustworthy organizations and ensuring that their donations are used effectively. NexusNGO aims to bridge this gap by providing a seamless, transparent, and impactful donation experience.</p>
    <hr class="solid">
    
    <h2  color: #FF4B4B;>Our Vision</h2>
    
    <p >We envision a world where every act of generosity reaches its true potential. By simplifying the donation process and ensuring transparency through cutting-edge technologies, we aim to foster trust and encourage more individuals to contribute to worthy causes.</p>
    <hr class="solid">
    
    <h2  color: #FF4B4B;'>Our Solution</h2>
    
    <p >NexusNGO Offers a two fold solution to existing donation challenges:</p>
    <li>AI-Driven Item Matching: Donors can easily list or take a photo of an item, and our AI matches it with relevant NGOs that are in need of the specific donation.</li>
    <li>Blockchain-Powered Transparency: Every monetary donation is recorded on a tamper-proof, decentralized ledger, ensuring accountability and building trust between donors and NGOs.</li>
    <hr class="solid">
    
    <h2  color: #FF4B4B;>Why Choose NexusNGO</h2>
    
    <li>Ease of Use: Whether you're donating goods or money, our platform makes the process easy and intuitive.</li>
    <li>Increased Trust: By utilizing blockchain, we ensure that all funds are tracked, giving you peace of mind that your donations are used responsibly</li>
    <li>Impactful Giving: Our AI-driven matching system connects you with NGOs that are in need of your specific donations, maximizing the impact of your contribution.</li>
    <hr class="solid">
    
    <h2  color: #FF4B4B;>Join us on our mission</h2>
    
    <p >Together, we can create a world where every act of generosity makes a lasting impact. Join NexusNGO today and be a part of the change you wish to see in the world.</p>
    <hr class="solid">
    """, unsafe_allow_html=True)
    
    if st.button("Back to Home"):
        st.session_state['role'] = None
        st.rerun()
    
if __name__ == "__main__":
    about_us()