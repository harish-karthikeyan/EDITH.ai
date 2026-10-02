import os
import time
import base64
import threading

import cv2
import streamlit as st
import streamlit.components.v1 as components

from ultralytics import YOLO

from ai.edith_controller import EDITHController


# ============================================================
# EDITH.ai
# Environmental Digital Intelligence for Threat & Habitat
# FINAL OPTIMIZED VERSION
# ============================================================


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="EDITH.ai",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

CAMERA_URL = "http://0.0.0.0:8080/"

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "edith_wildlife-3",
    "weights",
    "best.pt"
)

ALARM_PATH = r"E:\Projects\EDITH.ai\emergency_alarm_siren.mp3"


# ============================================================
# AI CONFIGURATION
# ============================================================

GENERAL_CONF = 0.35

# Deer gets a slightly lower threshold
DEER_CONF = 0.25

INFERENCE_SIZE = 512

# AI checks approximately twice per second
INFERENCE_INTERVAL = 0.50

HIGH_RISK = 60

CRITICAL_RISK = 80


# ============================================================
# SUPPORTED WILDLIFE
# ============================================================

SUPPORTED_WILDLIFE = {

    "bear": "Bear",

    "deer": "Deer",

    "elephant": "Elephant",

    "leopard": "Leopard",

    "monkey": "Monkey",

    "tiger": "Tiger",

    "wildboar": "Wild Boar",

    "wild_boar": "Wild Boar",

    "wild boar": "Wild Boar"
}


# ============================================================
# SESSION STATE
# ============================================================

DEFAULTS = {

    "monitoring": False,

    "analysis": None,

    "alert_active": False,

    "alert_suppressed": False,

    "authority_notified": False,

    "audio_armed": False,

    "last_inference": 0.0,

    "last_species": None,

    "last_confidence": 0.0,

    "last_risk": 0,

    "farmer_alert": False,

    "authority_alert": False,

    "deterrent_active": False
}


for key, value in DEFAULTS.items():

    if key not in st.session_state:

        st.session_state[key] = value


# ============================================================
# CAMERA WORKER
# ============================================================

class CameraWorker:

    def __init__(self, url):

        self.url = url

        self.cap = None

        self.frame = None

        self.lock = threading.Lock()

        self.running = False

        self.connected = False

        self.thread = None

    def start(self):

        if self.running:

            return

        self.running = True

        self.thread = threading.Thread(
            target=self._capture_loop,
            daemon=True
        )

        self.thread.start()

    def _connect(self):

        try:

            cap = cv2.VideoCapture(
                self.url
            )

            cap.set(
                cv2.CAP_PROP_BUFFERSIZE,
                1
            )

            if cap.isOpened():

                self.cap = cap

                self.connected = True

                return True

            cap.release()

        except Exception:

            pass

        self.connected = False

        return False

    def _capture_loop(self):

        while self.running:

            if self.cap is None:

                if not self._connect():

                    time.sleep(1)

                    continue

            try:

                ret, frame = self.cap.read()

                if ret and frame is not None:

                    with self.lock:

                        self.frame = frame

                    self.connected = True

                else:

                    self.connected = False

                    try:

                        self.cap.release()
                    except Exception:
                        pass

                    self.cap = None

                    time.sleep(0.3)

            except Exception:

                self.connected = False

                try:

                    self.cap.release()
                except Exception:
                    pass

                self.cap = None

                time.sleep(0.3)

    def get_frame(self):

        with self.lock:

            if self.frame is None:

                return None

            return self.frame.copy()

    def stop(self):

        self.running = False

        self.connected = False

        self.frame = None

        if self.cap is not None:

            try:

                self.cap.release()

            except Exception:

                pass

        self.cap = None


# ============================================================
# PERSISTENT CAMERA OBJECT
# ============================================================

@st.cache_resource
def get_camera():

    return CameraWorker(
        CAMERA_URL
    )


camera = get_camera()


# ============================================================
# LOAD AI MODEL
# ============================================================

@st.cache_resource
def load_ai():

    model = YOLO(
        MODEL_PATH
    )

    controller = EDITHController()

    return model, controller


try:

    if not os.path.exists(MODEL_PATH):

        raise FileNotFoundError(
            "Model not found:\n" + MODEL_PATH
        )

    model, controller = load_ai()

    AI_READY = True

    AI_ERROR = ""

except Exception as error:

    model = None

    controller = None

    AI_READY = False

    AI_ERROR = str(error)


# ============================================================
# LOAD MP3
# ============================================================

@st.cache_data
def load_alarm():

    if not os.path.exists(ALARM_PATH):

        return None

    try:

        with open(
            ALARM_PATH,
            "rb"
        ) as audio_file:

            audio_bytes = audio_file.read()

        return base64.b64encode(
            audio_bytes
        ).decode("utf-8")

    except Exception:

        return None


ALARM_BASE64 = load_alarm()


# ============================================================
# CSS
# ============================================================

st.html(
    """
    <style>

    @import url(
        'https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700&display=swap'
    );

    html,
    body,
    .stApp,
    [class*="css"],
    button,
    input,
    select,
    textarea {

        font-family:
            'Orbitron',
            monospace !important;
    }


    .stApp {

        background:
            radial-gradient(
                circle at 80% 0%,
                rgba(0,255,255,0.045),
                transparent 30%
            ),
            #020607;

        color: #eaffff;
    }


    header {

        visibility: hidden;
    }


    .block-container {

        max-width: 1180px;

        padding-top: 1rem;

        padding-bottom: 2rem;
    }


    .edith-title {

        color: #00ffff;

        font-size: 2rem;

        letter-spacing: 7px;

        font-weight: 600;
    }


    .edith-subtitle {

        color: #63858a;

        font-size: 0.60rem;

        letter-spacing: 3px;

        margin-bottom: 20px;
    }


    .section-title {

        border-left:
            3px solid #00ffff;

        padding-left: 12px;

        color: #00ffff;

        font-size: 0.75rem;

        letter-spacing: 4px;

        margin-top: 22px;

        margin-bottom: 13px;
    }


    .status-box {

        border:
            1px solid
            rgba(0,255,255,0.18);

        background:
            rgba(4,13,15,0.75);

        padding: 14px;

        text-align: center;
    }


    .status-value {

        color: #00ffff;

        font-size: 0.67rem;

        letter-spacing: 1px;
    }


    .status-label {

        color: #597276;

        font-size: 0.48rem;

        letter-spacing: 2px;

        margin-top: 5px;
    }


    .panel {

        background:
            rgba(13,18,23,0.95);

        border:
            1px solid
            rgba(0,255,255,0.10);

        border-radius: 8px;

        padding: 20px;

        min-height: 245px;
    }


    .label {

        color: #00ffff;

        font-size: 0.55rem;

        letter-spacing: 2px;

        margin-top: 8px;
    }


    .value {

        color: white;

        font-size: 0.92rem;

        letter-spacing: 1px;

        margin-top: 5px;
    }


    .risk-number {

        color: #00ffff;

        font-size: 3rem;

        letter-spacing: 3px;

        margin-top: 12px;
    }


    .risk-level {

        color: #ffcc00;

        font-size: 0.65rem;

        letter-spacing: 2px;
    }


    .small {

        color: #60797d;

        font-size: 0.52rem;

        line-height: 1.7;
    }


    .alert-box {

        border:
            2px solid #ff304f;

        background:
            rgba(80,0,15,0.35);

        padding: 20px;

        text-align: center;

        animation:
            pulse
            1s
            infinite;
    }


    .alert-title {

        color: #ff304f;

        font-size: 0.95rem;

        font-weight: 700;

        letter-spacing: 4px;
    }


    .alert-text {

        color: white;

        font-size: 0.58rem;

        letter-spacing: 1px;

        margin-top: 8px;
    }


    .audio-ready {

        border:
            1px solid
            rgba(0,255,255,0.20);

        background:
            rgba(0,255,255,0.03);

        padding: 10px;

        color: #6f8b8f;

        font-size: 0.52rem;

        letter-spacing: 1px;

        text-align: center;
    }


    @keyframes pulse {

        0% {

            box-shadow:
                0 0 4px
                rgba(255,48,79,0.15);
        }

        50% {

            box-shadow:
                0 0 25px
                rgba(255,48,79,0.70);
        }

        100% {

            box-shadow:
                0 0 4px
                rgba(255,48,79,0.15);
        }
    }


    div.stButton > button {

        background:
            #071418 !important;

        color:
            #00ffff !important;

        border:
            1px solid
            rgba(0,255,255,0.30) !important;

        border-radius:
            3px !important;

        font-family:
            'Orbitron',
            monospace !important;

        font-size:
            0.57rem !important;

        letter-spacing:
            1.2px !important;

        min-height:
            40px;
    }


    div.stButton > button:hover {

        border-color:
            #00ffff !important;

        color:
            white !important;
    }

    </style>
    """
)


# ============================================================
# HEADER
# ============================================================

st.html(
    """
    <div class="edith-title">
        EDITH.ai
    </div>

    <div class="edith-subtitle">
        ENVIRONMENTAL DIGITAL INTELLIGENCE FOR THREAT & HABITAT
    </div>
    """
)


# ============================================================
# SYSTEM STATUS
# ============================================================

st.html(
    """
    <div class="section-title">
        SYSTEM STATUS
    </div>
    """
)

s1, s2, s3, s4 = st.columns(4)


with s1:

    st.html(
        """
        <div class="status-box">

            <div class="status-value">
                ONLINE
            </div>

            <div class="status-label">
                EDITH CORE
            </div>

        </div>
        """
    )


with s2:

    camera_status = (
        "ONLINE"
        if camera.connected
        else "STANDBY"
    )

    st.html(
        f"""
        <div class="status-box">

            <div class="status-value">
                {camera_status}
            </div>

            <div class="status-label">
                CAMERA LINK
            </div>

        </div>
        """
    )


with s3:

    ai_status = (
        "READY"
        if AI_READY
        else "ERROR"
    )

    st.html(
        f"""
        <div class="status-box">

            <div class="status-value">
                {ai_status}
            </div>

            <div class="status-label">
                AI ENGINE
            </div>

        </div>
        """
    )


with s4:

    st.html(
        """
        <div class="status-box">

            <div class="status-value">
                CUSTOM
            </div>

            <div class="status-label">
                WILDLIFE MODEL
            </div>

        </div>
        """
    )


# ============================================================
# FARM CONFIGURATION
# ============================================================

st.html(
    """
    <div class="section-title">
        FARM CONFIGURATION
    </div>
    """
)

crop = st.selectbox(
    "CROP TYPE",
    [
        "other",
        "rice",
        "banana",
        "sugarcane",
        "maize",
        "groundnut",
        "vegetables",
        "coconut",
        "cotton",
        "millet"
    ]
)


# ============================================================
# MONITORING CONTROL
# ============================================================

st.html(
    """
    <div class="section-title">
        MONITORING CONTROL
    </div>
    """
)

control1, control2 = st.columns(2)


with control1:

    if not st.session_state.monitoring:

        if st.button(
            "◉ START EDITH MONITORING",
            use_container_width=True
        ):

            camera.start()

            st.session_state.monitoring = True

            st.rerun()

    else:

        if st.button(
            "◉ STOP EDITH MONITORING",
            use_container_width=True
        ):

            camera.stop()

            st.session_state.monitoring = False

            st.session_state.alert_active = False

            st.session_state.alert_suppressed = False

            st.session_state.authority_notified = False

            st.rerun()


with control2:

    if not st.session_state.audio_armed:

        if st.button(
            "🔊 ENABLE ALERT AUDIO",
            use_container_width=True
        ):

            st.session_state.audio_armed = True

            st.rerun()

    else:

        st.html(
            """
            <div class="audio-ready">

                🔊 ALERT AUDIO ARMED<br>
                SIREN READY

            </div>
            """
        )


# ============================================================
# WILDLIFE MONITORING
# ============================================================

st.html(
    """
    <div class="section-title">
        WILDLIFE MONITORING
    </div>
    """
)

camera_col, dynamic_col = st.columns(
    [1.15, 0.85]
)


# ============================================================
# CAMERA FEED
# ============================================================

with camera_col:

    camera_html = f"""
    <html>

    <body style="
        margin:0;
        padding:0;
        background:#020607;
        overflow:hidden;
    ">

        <img
            src="{CAMERA_URL}"
            style="
                width:100%;
                height:350px;
                object-fit:cover;
                display:block;
            "
        >

    </body>

    </html>
    """

    components.html(
        camera_html,
        height=355,
        scrolling=False
    )


# ============================================================
# CONTINUOUS EDITH ENGINE
# ============================================================

if st.session_state.monitoring:

    @st.fragment(
        run_every=0.5
    )
    def live_edith():

        # ====================================================
        # GET LATEST FRAME
        # ====================================================

        frame = camera.get_frame()

        if frame is None:

            with dynamic_col:

                st.html(
                    """
                    <div class="panel">

                        <div class="label">
                            CAMERA
                        </div>

                        <div class="value">
                            WAITING FOR FRAME
                        </div>

                    </div>
                    """
                )

            return


        # ====================================================
        # RESIZE
        # ====================================================

        height, width = frame.shape[:2]

        if width > 640:

            scale = 640 / width

            frame = cv2.resize(
                frame,
                (
                    640,
                    int(height * scale)
                )
            )


        # ====================================================
        # INFERENCE TIMER
        # ====================================================

        current_time = time.time()

        should_infer = (

            current_time -
            st.session_state.last_inference

            >= INFERENCE_INTERVAL

        )


        # ====================================================
        # YOLO
        # ====================================================

        if should_infer:

            st.session_state.last_inference = current_time

            try:

                results = model.predict(

                    source=frame,

                    conf=0.20,

                    imgsz=INFERENCE_SIZE,

                    device=0,

                    verbose=False,

                    max_det=5
                )

                result = results[0]

            except Exception as error:

                with dynamic_col:

                    st.error(
                        "YOLO ERROR: "
                        + str(error)
                    )

                return


            # =================================================
            # BEST WILDLIFE DETECTION
            # =================================================

            best_species = None

            best_confidence = 0.0


            if result.boxes is not None:

                for box in result.boxes:

                    class_id = int(
                        box.cls[0]
                    )

                    confidence = float(
                        box.conf[0]
                    )

                    detected_name = str(
                        result.names[class_id]
                    ).lower().strip()


                    if detected_name not in SUPPORTED_WILDLIFE:

                        continue


                    threshold = (

                        DEER_CONF

                        if detected_name == "deer"

                        else GENERAL_CONF

                    )


                    if confidence < threshold:

                        continue


                    if confidence > best_confidence:

                        best_confidence = confidence

                        best_species = (
                            SUPPORTED_WILDLIFE[
                                detected_name
                            ]
                        )


            # =================================================
            # NO WILDLIFE DETECTED
            # =================================================

            if best_species is None:

                st.session_state.analysis = None

                st.session_state.last_species = None

                st.session_state.last_confidence = 0.0

                st.session_state.last_risk = 0

                st.session_state.alert_active = False

                st.session_state.authority_notified = False

                st.session_state.alert_suppressed = False


            # =================================================
            # WILDLIFE DETECTED
            # =================================================

            else:

                species_key = (

                    best_species
                    .lower()
                    .replace(" ", "_")

                )


                try:

                    analysis = controller.analyze(

                        species=species_key,

                        confidence=best_confidence,

                        crop=crop,

                        # Current prototype baseline.
                        # Real sighting history can be
                        # connected later.

                        recent_sightings=1,

                        previous_sightings=1,

                        current_distance_km=5.0,

                        previous_distance_km=5.0,

                        direction="unknown",

                        hours_since_last_sighting=24,

                        night=False
                    )

                except Exception as error:

                    with dynamic_col:

                        st.error(
                            "EDITH ENGINE ERROR: "
                            + str(error)
                        )

                    return


                st.session_state.analysis = analysis

                st.session_state.last_species = (
                    best_species
                )

                st.session_state.last_confidence = (
                    best_confidence
                )


                # =============================================
                # RISK
                # =============================================

                risk = int(
                    analysis["risk"]["score"]
                )

                st.session_state.last_risk = risk


                # =============================================
                # ALERT
                # =============================================

                if risk >= HIGH_RISK:

                    if not st.session_state.alert_suppressed:

                        if not st.session_state.alert_active:

                            st.session_state.alert_active = True

                            st.session_state.authority_notified = True

                            # Full rerun is intentional.
                            # It makes the alarm component
                            # appear outside this fragment.

                            st.rerun()


                else:

                    if st.session_state.alert_active:

                        st.session_state.alert_active = False

                        st.session_state.authority_notified = False

                        st.rerun()


        # ====================================================
        # CURRENT ANALYSIS
        # ====================================================

        analysis = (
            st.session_state.analysis
        )


        # ====================================================
        # AI PANEL
        # ====================================================

        with dynamic_col:

            if analysis is None:

                species = "NO WILDLIFE"

                confidence = "--"

                damage = "NONE"

                movement = "MONITORING"

                risk = "--"

                risk_level = "LOW"

            else:

                species = (
                    analysis["detection"]["species"]
                )

                confidence = (
                    f'{analysis["detection"]["confidence"]:.1f}%'
                )

                damage = (
                    analysis["damage"]["severity"]
                )

                movement = (
                    analysis["movement"]["status"]
                )

                risk = str(
                    analysis["risk"]["score"]
                )

                risk_level = (
                    analysis["risk"]["level"]
                )


            st.html(
                f"""
                <div class="panel">

                    <div class="label">
                        DETECTED SPECIES
                    </div>

                    <div class="value">
                        {species}
                    </div>

                    <div class="label">
                        CONFIDENCE
                    </div>

                    <div class="value">
                        {confidence}
                    </div>

                    <div class="label">
                        DAMAGE SEVERITY
                    </div>

                    <div class="value">
                        {damage}
                    </div>

                    <div class="label">
                        MOVEMENT INTELLIGENCE
                    </div>

                    <div class="value">
                        {movement}
                    </div>

                    <div class="label">
                        RISK
                    </div>

                    <div class="value">
                        {risk} · {risk_level}
                    </div>

                </div>
                """
            )


        # ====================================================
        # LIVE RISK INTELLIGENCE
        # ====================================================

        st.html(
            """
            <div class="section-title">
                LIVE RISK INTELLIGENCE
            </div>
            """
        )


        risk_col, intelligence_col = st.columns(
            [0.75, 1.25]
        )


        with risk_col:

            if analysis is None:

                risk_score = "--"

                risk_level = "MONITORING"

            else:

                risk_score = str(
                    analysis["risk"]["score"]
                )

                risk_level = (
                    analysis["risk"]["level"]
                )


            st.html(
                f"""
                <div class="panel">

                    <div class="label">
                        CURRENT RISK SCORE
                    </div>

                    <div class="risk-number">
                        {risk_score}
                    </div>

                    <div class="risk-level">
                        {risk_level}
                    </div>

                </div>
                """
            )


        with intelligence_col:

            if analysis is None:

                species_factor = "Waiting"

                crop_factor = crop.upper()

                movement_factor = "Waiting"

                intrusion = "--"

            else:

                species_factor = (

                    f'{analysis["detection"]["species"]} '

                    f'({analysis["detection"]["confidence"]:.1f}%)'

                )

                crop_factor = (

                    f'{crop.upper()} → '

                    f'{analysis["damage"]["severity"]}'

                )

                movement_factor = (

                    analysis["movement"]["status"]

                )

                intrusion = str(

                    analysis["movement"]
                    ["intrusion_score"]

                )


            st.html(
                f"""
                <div class="panel">

                    <div class="label">
                        SPECIES THREAT
                    </div>

                    <div class="value">
                        {species_factor}
                    </div>

                    <div class="label">
                        CROP VULNERABILITY
                    </div>

                    <div class="value">
                        {crop_factor}
                    </div>

                    <div class="label">
                        MOVEMENT
                    </div>

                    <div class="value">
                        {movement_factor}
                    </div>

                    <div class="label">
                        INTRUSION SCORE
                    </div>

                    <div class="value">
                        {intrusion}
                    </div>

                </div>
                """
            )


        # ====================================================
        # THREAT RESPONSE
        # ====================================================

        st.html(
            """
            <div class="section-title">
                THREAT RESPONSE
            </div>
            """
        )


        if st.session_state.alert_active:

            st.html(
                """
                <div class="alert-box">

                    <div class="alert-title">
                        ⚠ WILDLIFE THREAT DETECTED
                    </div>

                    <div class="alert-text">
                        HIGH / CRITICAL RISK CONDITION ACTIVE
                    </div>

                    <div class="alert-text">
                        EDITH RESPONSE PROTOCOL ENGAGED
                    </div>

                </div>
                """
            )


            if st.session_state.authority_notified:

                st.error(
                    "📨 SMS / EMAIL SENT TO RESPECTIVE "
                    "AUTHORITIES • DEMO NOTIFICATION"
                )


            if st.button(
                "🔇 TURN OFF ALERT",
                use_container_width=True
            ):

                st.session_state.alert_active = False

                st.session_state.alert_suppressed = True

                st.session_state.authority_notified = False

                st.rerun()


        else:

            st.html(
                """
                <div class="status-box">

                    <div class="status-value">
                        ✓ NO ACTIVE THREAT
                    </div>

                    <div class="status-label">
                        EDITH CONTINUES MONITORING
                    </div>

                </div>
                """
            )


    live_edith()


# ============================================================
# MP3 ALERT PLAYER
#
# IMPORTANT:
# This block is OUTSIDE the fragment.
#
# There is deliberately NO f-string here.
# Therefore JavaScript { } cannot cause Python syntax errors.
# ============================================================

if (
    st.session_state.alert_active
    and
    st.session_state.audio_armed
):

    if ALARM_BASE64 is not None:

        alarm_player = """
        <html>

        <body style="
            margin:0;
            padding:0;
            background:transparent;
            overflow:hidden;
        ">

            <audio
                id="edithAlarm"
                autoplay
                loop
                style="display:none;"
            >

                <source
                    src="data:audio/mpeg;base64,ALARM_DATA_HERE"
                    type="audio/mpeg"
                >

            </audio>

            <script>

                const alarm =
                    document.getElementById(
                        "edithAlarm"
                    );

                alarm.volume = 1.0;

                alarm.loop = true;

                alarm.play().catch(
                    function(error) {

                        console.log(
                            "EDITH audio autoplay blocked:",
                            error
                        );

                    }
                );

            </script>

        </body>

        </html>
        """

        alarm_player = alarm_player.replace(
            "ALARM_DATA_HERE",
            ALARM_BASE64
        )

        components.html(
            alarm_player,
            height=1,
            scrolling=False
        )

    else:

        st.error(
            "EDITH alarm file not found:\n"
            + ALARM_PATH
        )


# ============================================================
# RESPONSE CONTROL
# ============================================================

st.html(
    """
    <div class="section-title">
        RESPONSE CONTROL
    </div>
    """
)

r1, r2, r3 = st.columns(3)


with r1:

    if st.button(
        "◉ ALERT FARMER",
        use_container_width=True
    ):

        st.session_state.farmer_alert = True

        st.success(
            "Farmer alert module activated."
        )


with r2:

    if st.button(
        "◉ INFORM AUTHORITIES",
        use_container_width=True
    ):

        st.session_state.authority_alert = True

        st.success(
            "Authority notification queued."
        )


with r3:

    if st.button(
        "◉ ACTIVATE NON-HARMFUL DETERRENT",
        use_container_width=True
    ):

        st.session_state.deterrent_active = True

        st.info(
            "Non-harmful deterrent module activated."
        )


# ============================================================
# EDITH ENGINE
# ============================================================

st.html(
    """
    <div class="section-title">
        EDITH ENGINE
    </div>
    """
)

st.html(
    """
    <div class="panel">

        <div class="label">
            VISION MODEL
        </div>

        <div class="value">
            CUSTOM YOLO · best.pt
        </div>

        <div class="label">
            WILDLIFE CLASSES
        </div>

        <div class="small">
            BEAR · DEER · ELEPHANT · LEOPARD ·
            MONKEY · TIGER · WILD BOAR
        </div>

        <div class="label">
            INTELLIGENCE
        </div>

        <div class="small">
            RISK ENGINE · CROP DAMAGE ·
            MOVEMENT INTELLIGENCE
        </div>

        <div class="label">
            RESPONSE
        </div>

        <div class="small">
            FARMER ALERT · AUTHORITY ALERT ·
            NON-HARMFUL DETERRENT
        </div>

    </div>
    """
)


# ============================================================
# FOOTER
# ============================================================

st.html(
    """
    <div style="
        text-align:center;
        color:#405457;
        font-size:0.45rem;
        letter-spacing:2px;
        margin-top:30px;
    ">

        EDITH.ai · WILDLIFE CONFLICT INTELLIGENCE

    </div>
    """
)