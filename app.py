<<<<<<< HEAD
from flask import Flask, render_template, request, jsonify, session
import re, uuid, random, json, os, urllib.request
from datetime import datetime

app = Flask(__name__)
app.secret_key = "acadbot_secret_2025"

# ── Persistent storage paths ──────────────────────────────────────────
DATA_DIR = os.path.join("/tmp", "acadbot_data")
HIST_FILE  = os.path.join(DATA_DIR, "chat_history.json")
STATS_FILE = os.path.join(DATA_DIR, "analytics.json")
os.makedirs(DATA_DIR, exist_ok=True)

# ── Knowledge Base ────────────────────────────────────────────────────
KNOWLEDGE_BASE = {
    "sem5_subjects": {
        "phrases": ["sem 5 subjects","semester 5 subjects","sem v subjects",
                    "5th sem subjects","fifth semester","subjects in sem 5",
                    "list of sem 5","sem 5 syllabus","semester v syllabus",
                    "what are sem 5","sem5"],
        "keywords": [],
        "responses": [
            "📚 **Semester V Subjects – B.Sc. IT (TY) 2025–26**\n\n"
            "**Major Mandatory:**\n"
            "• 25UBIT501 – Network Security (4 cr)\n"
            "• 25UBIT502 – Web Development Framework (2 cr)\n"
            "• 25UBIT503 – Software Engineering & Agile Methodologies (4 cr)\n\n"
            "**Minor:**\n"
            "• 25UBIT504 – Advanced Java (4 cr)\n\n"
            "**Elective (any 1 of 3):**\n"
            "• 25UBIT505 – Mobile App Development\n"
            "• 25UBIT506 – Functional & Reactive Programming\n"
            "• 25UBIT507 – Advanced Database Programming\n\n"
            "**Vocational/Skill:**\n"
            "• 25UBIT508 – Figma (2 cr)\n\n"
            "**Field Project:**\n"
            "• 25UBIT509 – Field Project (2 cr)\n\n"
            "📊 **Total Credits: 22**\n\nAsk me about any subject for full details!"
        ]
    },
    "sem6_subjects": {
        "phrases": ["sem 6 subjects","semester 6 subjects","sem vi subjects",
                    "6th sem subjects","sixth semester","subjects in sem 6",
                    "list of sem 6","sem 6 syllabus","semester vi syllabus",
                    "what are sem 6","sem6","subjects of semester 6"],
        "keywords": [],
        "responses": [
            "📚 **Semester VI Subjects – B.Sc. IT (TY) 2025–26**\n\n"
            "**Major Mandatory:**\n"
            "• 25UBIT601 – Full-Stack Web Development / MERN Stack (4 cr)\n"
            "• 25UBIT602 – Blockchain (2 cr)\n"
            "• 25UBIT603 – Internet of Things / IoT (4 cr)\n\n"
            "**Minor:**\n"
            "• 25UBIT604 – Software Testing (4 cr)\n\n"
            "**Elective (any 1 of 3):**\n"
            "• 25UBIT605 – Spring Boot\n"
            "• 25UBIT606 – Game Programming with Python\n"
            "• 25UBIT607 – AI-Driven Software Development\n\n"
            "**On Job Training:**\n"
            "• OJT – On Job Training (4 cr)\n\n"
            "📊 **Total Credits: 22**\n\nAsk me about any subject for full details!"
        ]
    },
    "all_subjects": {
        "phrases": ["all subjects","complete syllabus","full syllabus",
                    "both semesters","all semesters","tybscit subjects","ty bsc it subjects"],
        "keywords": [],
        "responses": [
            "📚 **B.Sc. IT (TY) – Complete Syllabus (AY 2025–26)**\n\n"
            "**── SEMESTER V ──**\n"
            "• 25UBIT501 – Network Security (4 cr)\n"
            "• 25UBIT502 – Web Dev Framework (2 cr)\n"
            "• 25UBIT503 – Software Engineering & Agile (4 cr)\n"
            "• 25UBIT504 – Advanced Java (4 cr)\n"
            "• 25UBIT505/06/07 – Elective (4 cr)\n"
            "• 25UBIT508 – Figma (2 cr)\n"
            "• 25UBIT509 – Field Project (2 cr)\n"
            "📊 Sem V Total: 22 credits\n\n"
            "**── SEMESTER VI ──**\n"
            "• 25UBIT601 – Full-Stack / MERN (4 cr)\n"
            "• 25UBIT602 – Blockchain (2 cr)\n"
            "• 25UBIT603 – Internet of Things (4 cr)\n"
            "• 25UBIT604 – Software Testing (4 cr)\n"
            "• 25UBIT605/06/07 – Elective (4 cr)\n"
            "• OJT – On Job Training (4 cr)\n"
            "📊 Sem VI Total: 22 credits\n\nType any subject name for detailed info!"
        ]
    },
    "network_security": {
        "phrases": ["network security","25ubit501","ubit501","netsec",
                    "about network security","network security subject",
                    "tell me about network security","network security details"],
        "keywords": [],
        "responses": [
            "🔐 **Network Security (25UBIT501)**\n\n"
            "• **Type:** Major Mandatory | **Credits:** 4 | **Total Marks:** 150\n"
            "• **Lectures/week:** 4 | **Focuses on:** Employability\n\n"
            "**Units:**\n"
            "1. Intro to Network Security & Threat Landscape – CIA Triad, malware, DoS/DDoS, ethical hacking\n"
            "2. Cryptography & Secure Communication – AES, RSA, TLS/SSL, digital signatures\n"
            "3. Network Security Technologies – Firewalls, VPNs, IDS/IPS, honeypots\n"
            "4. Wireless & Web Security – WPA3, OWASP Top 10, DNSSEC\n"
            "5. Monitoring, Logging & Legal – Wireshark, Nmap, IT Act, ISO 27001\n\n"
            "**Practicals:** Wireshark sniffing, AES in Python, firewall setup, Nmap, OWASP ZAP, Snort"
        ]
    },
    "web_dev_framework": {
        "phrases": ["web development framework","web dev framework","25ubit502","ubit502",
                    "web framework subject","about web development framework","tell me about web framework"],
        "keywords": [],
        "responses": [
            "🌐 **Web Development Framework (25UBIT502)**\n\n"
            "• **Type:** Major Mandatory | **Credits:** 2 | **Total Marks:** 150\n"
            "• **Focuses on:** Skill Development\n\n"
            "Covers modern frontend and backend frameworks, JavaScript ecosystem (React, Angular, Vue), "
            "REST API development, routing, state management, and deploying web apps.\n\n"
            "**Practicals:** Build a React component, REST API with Express, deploy on Vercel."
        ]
    },
    "software_engineering": {
        "phrases": ["software engineering","agile methodologies","25ubit503","ubit503",
                    "se subject","software engg","about software engineering",
                    "tell me about software engineering","scrum subject","devops subject"],
        "keywords": [],
        "responses": [
            "⚙️ **Software Engineering & Agile Methodologies (25UBIT503)**\n\n"
            "• **Type:** Major Mandatory | **Credits:** 4 | **Total Marks:** 150\n"
            "• **Lectures/week:** 4 | **Focuses on:** Skill Development\n\n"
            "**Units:**\n"
            "1. Foundations of SE – SDLC: Waterfall, Spiral, V-Model, Agile\n"
            "2. Requirements Engineering – SRS, UML diagrams (use case, class, activity, sequence)\n"
            "3. Software Design Principles – MVC, Microservices, Design Patterns\n"
            "4. Agile & DevOps – Scrum, Kanban, JIRA, Trello, CI/CD, Docker, Jenkins\n"
            "5. Testing & Maintenance – TDD, Selenium, JUnit, versioning, refactoring\n\n"
            "**Practicals:** SRS doc, UML diagrams, sprint plan on JIRA, Docker, GitHub Actions"
        ]
    },
    "advanced_java": {
        "phrases": ["advanced java","25ubit504","ubit504","adv java",
                    "about advanced java","tell me about advanced java","java subject"],
        "keywords": [],
        "responses": [
            "☕ **Advanced Java (25UBIT504)**\n\n"
            "• **Type:** Minor | **Credits:** 4 | **Total Marks:** 150\n"
            "• **Lectures/week:** 4 | **Focuses on:** Skill Development\n\n"
            "Covers JDBC, Servlets, JSP, Hibernate ORM, Spring framework basics, "
            "multithreading, collections, and enterprise Java application development.\n\n"
            "**Practicals:** CRUD with JDBC, Servlet login system, Hibernate entity mapping, Spring MVC mini app."
        ]
    },
    "mobile_app": {
        "phrases": ["mobile app development","mobile development","25ubit505","ubit505",
                    "app development subject","android subject",
                    "about mobile app","tell me about mobile app development"],
        "keywords": [],
        "responses": [
            "📱 **Mobile App Development (25UBIT505)**\n\n"
            "• **Type:** Elective | **Credits:** 4 | **Total Marks:** 150\n"
            "• **Lectures/week:** 4 | **Focuses on:** Employability\n\n"
            "Covers Android/cross-platform mobile development, activity lifecycle, fragments, "
            "UI components, REST API integration, Firebase, and app publishing.\n\n"
            "**Practicals:** Login app, REST API integration, Firebase auth, JUnit & Espresso testing."
        ]
    },
    "functional_reactive": {
        "phrases": ["functional programming","reactive programming","25ubit506","ubit506",
                    "functional reactive","rxjs subject",
                    "about functional programming","tell me about functional programming",
                    "tell me about reactive programming"],
        "keywords": [],
        "responses": [
            "🔄 **Functional & Reactive Programming (25UBIT506)**\n\n"
            "• **Type:** Elective | **Credits:** 4 | **Total Marks:** 150\n"
            "• **Lectures/week:** 4 | **Focuses on:** Employability\n\n"
            "**Units:**\n"
            "1. Fundamentals of FP – pure functions, immutability, recursion\n"
            "2. FP in JavaScript/Kotlin – closures, map/filter/reduce, higher-order functions\n"
            "3. Advanced FP Concepts – monads, functors, lazy evaluation, Redux\n"
            "4. Intro to Reactive Programming – RxJS/RxJava, Observables, Observer pattern\n"
            "5. Reactive System Dev – backpressure, Spring WebFlux, real-time dashboards\n\n"
            "**Practicals:** RxJS Observables, real-time search, Spring WebFlux + WebSockets"
        ]
    },
    "advanced_database": {
        "phrases": ["advanced database","database programming","25ubit507","ubit507",
                    "advanced db","about advanced database",
                    "tell me about advanced database programming"],
        "keywords": [],
        "responses": [
            "🗄️ **Advanced Database Programming (25UBIT507)**\n\n"
            "• **Type:** Elective | **Credits:** 4 | **Total Marks:** 150\n"
            "• **Lectures/week:** 4 | **Focuses on:** Employability\n\n"
            "Covers advanced SQL, stored procedures, triggers, indexing, transactions, "
            "NoSQL with MongoDB, and modern database optimization techniques.\n\n"
            "**Practicals:** Stored procedures in MySQL, MongoDB CRUD, query optimization, indexing."
        ]
    },
    "figma": {
        "phrases": ["figma","25ubit508","ubit508","figma subject",
                    "about figma","tell me about figma","ui ux subject",
                    "design tool subject","prototyping subject"],
        "keywords": [],
        "responses": [
            "🎨 **Figma (25UBIT508)**\n\n"
            "• **Type:** Vocational / Skill Enhancement | **Credits:** 2 | **Total Marks:** 100\n"
            "• **Focuses on:** Skill Development\n\n"
            "Covers UI/UX design using Figma – wireframing, prototyping, component libraries, "
            "design systems, auto-layout, and team collaboration.\n\n"
            "**Practicals:** Design a mobile app wireframe, build a design system, create interactive prototypes."
        ]
    },
    "mern_fullstack": {
        "phrases": ["mern stack","full stack web development","fullstack web",
                    "25ubit601","ubit601","mern subject",
                    "about mern","tell me about mern","tell me about full stack",
                    "full stack development subject"],
        "keywords": [],
        "responses": [
            "🌐 **Full-Stack Web Development – MERN Stack (25UBIT601)**\n\n"
            "• **Type:** Major Mandatory | **Credits:** 4 | **Total Marks:** 150\n"
            "• **Lectures/week:** 4 | **Focuses on:** Employability\n\n"
            "**MERN Stack:**\n"
            "• **M** – MongoDB (NoSQL database)\n"
            "• **E** – Express.js (backend framework)\n"
            "• **R** – React.js (frontend library)\n"
            "• **N** – Node.js (JavaScript runtime)\n\n"
            "Includes REST API design, JWT authentication, state management, deployment.\n\n"
            "**Practicals:** CRUD app, REST API with Express, React frontend, deploy on cloud."
        ]
    },
    "blockchain": {
        "phrases": ["blockchain","25ubit602","ubit602","blockchain subject",
                    "about blockchain","tell me about blockchain",
                    "smart contract","web3 subject"],
        "keywords": [],
        "responses": [
            "⛓️ **Blockchain (25UBIT602)**\n\n"
            "• **Type:** Major Mandatory | **Credits:** 2 | **Total Marks:** 150\n"
            "• **Focuses on:** Skill Development\n\n"
            "Covers blockchain fundamentals, distributed ledger technology, consensus mechanisms "
            "(Proof of Work, Proof of Stake), Ethereum, smart contracts (Solidity), "
            "and real-world blockchain applications.\n\n"
            "**Practicals:** Deploy a smart contract, simulate blockchain transactions, build a basic dApp."
        ]
    },
    "iot": {
        "phrases": ["internet of things","iot subject","25ubit603","ubit603",
                    "about iot","tell me about iot",
                    "iot subject details","what is iot subject"],
        "keywords": [],
        "responses": [
            "🔌 **Internet of Things – IoT (25UBIT603)**\n\n"
            "• **Type:** Major Mandatory | **Credits:** 4 | **Total Marks:** 150\n"
            "• **Lectures/week:** 4 | **Focuses on:** Skill Development\n\n"
            "**Units:**\n"
            "1. IoT Architecture & Ecosystem – layers, devices, gateways, cloud\n"
            "2. Sensors & Actuators – types, interfacing, data collection\n"
            "3. Microcontrollers – Arduino and Raspberry Pi programming\n"
            "4. IoT Protocols – MQTT, HTTP, CoAP, Zigbee, Bluetooth\n"
            "5. Cloud & Security – AWS IoT / Azure IoT, data analytics, IoT security\n\n"
            "**Practicals:** Arduino sensor interfacing, Raspberry Pi GPIO, MQTT pub/sub, "
            "smart home monitoring system."
        ]
    },
    "software_testing": {
        "phrases": ["software testing","25ubit604","ubit604",
                    "about software testing","tell me about software testing",
                    "testing subject","test cases subject"],
        "keywords": [],
        "responses": [
            "🧪 **Software Testing (25UBIT604)**\n\n"
            "• **Type:** Minor | **Credits:** 4 | **Total Marks:** 150\n"
            "• **Lectures/week:** 4 | **Focuses on:** Skill Development\n\n"
            "Covers black-box, white-box, unit, integration, system and acceptance testing, "
            "TDD, and automation testing with Selenium and JUnit.\n\n"
            "**Practicals:** Write test cases, automate with Selenium, JUnit unit testing, test reports."
        ]
    },
    "spring_boot": {
        "phrases": ["spring boot","25ubit605","ubit605","spring boot subject",
                    "about spring boot","tell me about spring boot","java spring subject"],
        "keywords": [],
        "responses": [
            "🍃 **Spring Boot (25UBIT605)**\n\n"
            "• **Type:** Elective | **Credits:** 4 | **Total Marks:** 150\n"
            "• **Lectures/week:** 4 | **Focuses on:** Employability\n\n"
            "Covers Spring Boot for Java web apps and REST APIs – Spring MVC, "
            "Spring Data JPA, Spring Security, Hibernate, and microservices with Spring Cloud.\n\n"
            "**Practicals:** Build REST APIs, MySQL with JPA, JWT security, create a microservice."
        ]
    },
    "game_programming": {
        "phrases": ["game programming","game development","25ubit606","ubit606",
                    "pygame subject","python game subject",
                    "about game programming","tell me about game programming",
                    "game programming with python"],
        "keywords": [],
        "responses": [
            "🎮 **Game Programming with Python (25UBIT606)**\n\n"
            "• **Type:** Elective | **Credits:** 4 | **Total Marks:** 150\n"
            "• **Lectures/week:** 4 | **Focuses on:** Employability\n\n"
            "Covers 2D game development using Python (Pygame) – game loop, sprites, "
            "collision detection, physics, scoring systems, AI opponents (Minimax), and level design.\n\n"
            "**Practicals:** Pong clone, Minimax AI for Tic-Tac-Toe, platformer game with levels."
        ]
    },
    "ai_software": {
        "phrases": ["ai driven software","ai software development","25ubit607","ubit607",
                    "ai subject","artificial intelligence subject",
                    "about ai driven","tell me about ai driven software",
                    "machine learning subject","ai development subject"],
        "keywords": [],
        "responses": [
            "🤖 **AI-Driven Software Development (25UBIT607)**\n\n"
            "• **Type:** Elective | **Credits:** 4 | **Total Marks:** 150\n"
            "• **Lectures/week:** 4 | **Focuses on:** Employability\n\n"
            "Covers integrating AI/ML into software – NLP pipelines, computer vision APIs, "
            "AI-assisted coding, ML model deployment with Flask/FastAPI, and building intelligent applications.\n\n"
            "**Practicals:** Build a chatbot, deploy ML model as API, use OpenAI API, "
            "image classification app."
        ]
    },
    "exam": {
        "phrases": ["exam schedule","exam dates","examination schedule","semester exam",
                    "when are exams","exam timetable","exam date",
                    "when is the exam","timetable of exam"],
        "keywords": ["exam","examination","timetable"],
        "responses": [
            "📅 **Exam Schedule – KES' Shroff College (2025–26)**\n\n"
            "**Odd Semesters (I, III, V):**\n"
            "• Unit Test: 18–21 Aug 2025\n"
            "• Additional Unit Test: 01–04 Sep 2025\n"
            "• **Semester Exam: 08–17 Oct 2025**\n\n"
            "**Even Semesters (II, IV, VI):**\n"
            "• Unit Test I: 28–31 Jan 2026\n"
            "• Additional Unit Test: 09–12 Feb 2026\n"
            "• **Semester Exam: 21 Mar – 04 Apr 2026**\n\n"
            "**Result Declaration (Sem II, IV, VI):** 20 Apr 2026\n\n"
            "⚠️ Always check the official notice board for any changes."
        ]
    },
    "internal": {
        "phrases": ["internal marks","internal assessment","continuous assessment",
                    "unit test marks","how are internal marks","internal marks breakdown",
                    "marks distribution","cia marks"],
        "keywords": ["internal","cia"],
        "responses": [
            "📊 **Internal Assessment Breakdown**\n\n"
            "• Attendance: **5 marks**\n"
            "• Assignments / Class Tests: **10 marks**\n"
            "• Unit Test: **10 marks**\n"
            "──────────────────\n"
            "**Total Internal: 25 marks per subject**\n\n"
            "**Unit Test Schedule (2025–26):**\n"
            "• Odd Sem Unit Test: 18–21 Aug 2025\n"
            "• Odd Sem Additional: 01–04 Sep 2025\n"
            "• Even Sem Unit Test: 28–31 Jan 2026\n"
            "• Even Sem Additional: 09–12 Feb 2026"
        ]
    },
    "attendance": {
        "phrases": ["attendance rule","attendance policy","attendance percentage",
                    "minimum attendance","how much attendance","attendance requirement",
                    "short attendance","proxy attendance"],
        "keywords": ["attendance","absent","bunk","proxy"],
        "responses": [
            "🎯 **Attendance Policy**\n\n"
            "• Minimum required: **75% attendance**\n"
            "• Below 75% → Detained from semester exams\n"
            "• Medical leave: Submit certificate within 3 days\n\n"
            "💡 **Tip:** Aim for 85%+ – attendance counts for 5 internal marks!"
        ]
    },
    "project": {
        "phrases": ["project guidelines","field project","project submission",
                    "project marks","project guide","ojt","on job training",
                    "project topic","about project","project details"],
        "keywords": ["project"],
        "responses": [
            "💻 **Project & OJT Guidelines**\n\n"
            "**Semester V – Field Project (25UBIT509)**\n"
            "• Type: CEP / Field Project | Credits: 2\n"
            "• Groups of 2–3 students\n"
            "• Synopsis submission: Week 4 of Sem V\n"
            "• Mid-review: Week 10 | Final viva: End of semester\n"
            "• Marks: 100 (50 internal + 50 external)\n\n"
            "**Semester VI – On Job Training (OJT)**\n"
            "• Industry internship or in-house live project\n"
            "• Credits: 4 | Submit OJT report + presentation\n"
            "• Marks: As per college evaluation rubrics"
        ]
    },
    "deadline": {
        "phrases": ["assignment deadline","submission deadline","last date",
                    "lecture ends","lectures end","due date","assignment due"],
        "keywords": ["deadline","submission"],
        "responses": [
            "⏰ **Key Academic Deadlines (2025–26)**\n\n"
            "**Odd Semester:**\n"
            "• Lectures End: 24 Sep 2025\n"
            "• Semester Exam: 08–17 Oct 2025\n\n"
            "**Even Semester:**\n"
            "• Lectures End (SY & TY): 07 Mar 2026\n"
            "• Semester Exam: 21 Mar – 04 Apr 2026\n"
            "• Lectures Begin (Sem IV, VI): 06 Nov 2025\n\n"
            "**ATKT Form Filling:**\n"
            "• Odd Sems: 26 May – 05 Jun 2025\n"
            "• Even Sems: 10 Dec 2025 – 20 Jan 2026"
        ]
    },
    "fees": {
        "phrases": ["fee payment","how to pay fees","fee structure",
                    "tuition fees","challan fee","scholarship"],
        "keywords": ["fees","fee","payment","scholarship","challan"],
        "responses": [
            "💰 **Fee & Payment Info**\n\n"
            "• Fee portal: College website → Student Login → Fee Portal\n"
            "• Scholarship applications: First month of the academic year\n"
            "• Late fee penalty: ₹50/day after due date\n"
            "• Fee receipts: Visit the accounts office\n\n"
            "Contact admin for scholarship and concession queries."
        ]
    },
    "rules": {
        "phrases": ["college rules","college regulations","code of conduct",
                    "discipline rules","dress code"],
        "keywords": ["rules","regulations","discipline"],
        "responses": [
            "📋 **College Rules & Regulations**\n\n"
            "• ID card mandatory on campus\n"
            "• Mobile phones on silent in classrooms\n"
            "• Formal dress code on exam days\n"
            "• Zero tolerance for ragging\n"
            "• Library books must be returned on time\n\n"
            "Full rulebook available at the college office."
        ]
    },
    "library": {
        "phrases": ["library timings","library hours","borrow book",
                    "library card","library fine","reference books"],
        "keywords": ["library","book","borrow","journals"],
        "responses": [
            "📖 **Library Information**\n\n"
            "• Timings: **9 AM – 6 PM** (Mon–Sat)\n"
            "• Borrow duration: **7 days** per book\n"
            "• Maximum: **2 books** at a time\n"
            "• Late return fine: ₹2 per day\n"
            "• Reference books & e-journals available\n\n"
            "Show your college ID card to borrow books."
        ]
    },
    "result": {
        "phrases": ["result date","result declaration","when will result come",
                    "how to check result","marksheet","revaluation",
                    "passing marks","atkt rule","cgpa"],
        "keywords": ["result","grade","scorecard","pass","fail","cgpa"],
        "responses": [
            "📈 **Results & Grading (2025–26)**\n\n"
            "• **Sem II, IV, VI Result:** 20 Apr 2026\n"
            "• Passing marks: **40% in each subject**\n"
            "• ATKT allowed in max 2 subjects\n"
            "• ATKT Exam (backlog): 10–20 Sep 2025\n"
            "• ATKT Form Filling (Even Sems): 10 Dec 2025 – 20 Jan 2026\n"
            "• Marksheet collection: College office after result\n\n"
            "For revaluation, apply within 15 days of result declaration."
        ]
    },
    "admission": {
        "phrases": ["admission process","how to take admission","first year admission",
                    "fy admission","new admission","admission form"],
        "keywords": ["admission","enroll","registration"],
        "responses": [
            "📝 **Admissions Info (2025–26)**\n\n"
            "• **FY Admission Window:** 27 May – 15 Jun 2025\n"
            "• **Academic Term Starts:** 09 Jun 2025\n"
            "• **FY Lectures Begin:** 16 Jun 2025\n"
            "• Merit-based admission\n"
            "• Documents: Previous marksheet, Aadhar card, passport photos\n\n"
            "Visit the college office or website for the online application form."
        ]
    },
    "holidays": {
        "phrases": ["diwali vacation","ganapati vacation","winter vacation",
                    "summer vacation","holiday list","college holidays",
                    "when is diwali break","vacation dates","holiday dates"],
        "keywords": ["holiday","vacation","break","ganapati","diwali"],
        "responses": [
            "🎉 **Official Holidays & Vacations (2025–26)**\n\n"
            "• 🐘 **Ganapati Vacation:** 27–31 Aug 2025\n"
            "• 🪔 **Diwali Vacation:** 20 Oct – 05 Nov 2025\n"
            "• ❄️ **Winter Vacation:** 26 Dec 2025 – 01 Jan 2026\n"
            "• ☀️ **Summer Vacation:** 23 Apr – 02 Jun 2026\n\n"
            "All dates from the official KES' Shroff College Academic Calendar 2025–26."
        ]
    },
    "academic_calendar": {
        "phrases": ["academic calendar","full calendar","important dates",
                    "all dates","college schedule","academic schedule"],
        "keywords": [],
        "responses": [
            "🗓️ **KES' Shroff College – Academic Calendar 2025–26**\n\n"
            "**Term 1 (Jun–Oct 2025)**\n"
            "• Academic Term Starts: 09 Jun 2025\n"
            "• FY Lectures Begin: 16 Jun 2025\n"
            "• Unit Test (Odd Sems): 18–21 Aug 2025\n"
            "• Ganapati Vacation: 27–31 Aug 2025\n"
            "• Additional Unit Test: 01–04 Sep 2025\n"
            "• ATKT Exam (backlog): 10–20 Sep 2025\n"
            "• Lectures End (Odd Sems): 24 Sep 2025\n"
            "• Sem Exam I, III, V: 08–17 Oct 2025\n"
            "• Diwali Vacation: 20 Oct – 05 Nov 2025\n\n"
            "**Term 2 (Nov 2025–Apr 2026)**\n"
            "• Sem IV & VI Lectures Begin: 06 Nov 2025\n"
            "• Winter Vacation: 26 Dec 2025 – 01 Jan 2026\n"
            "• Unit Test I (Even Sems): 28–31 Jan 2026\n"
            "• Additional Unit Test: 09–12 Feb 2026\n"
            "• ATKT Exam: 02–18 Mar 2026\n"
            "• Lectures End (SY & TY): 07 Mar 2026\n"
            "• Sem Exam II, IV, VI: 21 Mar – 04 Apr 2026\n"
            "• Result Declaration: 20 Apr 2026\n"
            "• Summer Vacation: 23 Apr – 02 Jun 2026"
        ]
    },
    "faculty": {
        "phrases": ["contact teacher","faculty contact","teacher email",
                    "how to contact professor","hod contact"],
        "keywords": ["faculty","teacher","professor","lecturer","hod"],
        "responses": [
            "👩‍🏫 **Faculty Contact**\n\n"
            "• Faculty list: College website → Department → IT Faculty\n"
            "• Cabin numbers & office hours: Department notice board\n"
            "• Email format: firstname.lastname@college.edu\n\n"
            "For HOD appointments, contact the department office directly."
        ]
    },
    "greet": {
        "phrases": ["hello","hi","hey","good morning","good afternoon",
                    "good evening","hii","helo","hai"],
        "keywords": [],
        "responses": [
            "👋 Hello! I'm **AcadBot**, your academic assistant for **B.Sc. IT (TY)** at KES' Shroff College.\n\n"
            "I can help you with:\n"
            "• Sem V & VI subject details\n"
            "• Exam dates & schedules\n"
            "• Attendance rules\n"
            "• Project & OJT guidelines\n"
            "• Holidays & academic calendar\n"
            "• Fees, results & library info\n\n"
            "What would you like to know? 😊"
        ]
    },
    "thanks": {
        "phrases": ["thank you","thanks","thank u","thx","ty",
                    "great thanks","you are helpful","helpful bot"],
        "keywords": ["thank","helpful","awesome"],
        "responses": [
            "😊 You're welcome! Feel free to ask anything anytime. Good luck with your studies! 🎓",
            "🙌 Happy to help! Is there anything else you'd like to know?"
        ]
    },
    "bye": {
        "phrases": ["bye","goodbye","see you","cya","later","good bye"],
        "keywords": ["bye","quit","exit"],
        "responses": [
            "👋 Goodbye! Best of luck with your academics. Come back anytime! 🎓"
        ]
    }
}

# ── Synonym Map ───────────────────────────────────────────────────────
# Maps common alternate words → canonical words used in phrases/keywords
SYNONYMS = {
    # semester
    "sem":       "semester",
    "trimester": "semester",
    "term":      "semester",
    # subjects
    "subject":   "subjects",
    "course":    "subjects",
    "courses":   "subjects",
    "paper":     "subjects",
    "papers":    "subjects",
    "topics":    "subjects",
    "topic":     "subjects",
    # exam
    "test":      "exam",
    "tests":     "exam",
    "examination":"exam",
    "exams":     "exam",
    "paper":     "exam",
    # attendance
    "presence":  "attendance",
    "absent":    "attendance",
    "bunking":   "attendance",
    "bunk":      "attendance",
    "skip":      "attendance",
    "leave":     "attendance",
    # marks / internal
    "marks":     "internal marks",
    "score":     "internal marks",
    "scores":    "internal marks",
    "grades":    "internal marks",
    "grade":     "internal marks",
    "cia":       "internal marks",
    # project
    "assignment": "project",
    "internship": "ojt",
    "training":   "ojt",
    # library
    "books":     "library",
    "borrow":    "library",
    # fees
    "fee":       "fees",
    "money":     "fees",
    "payment":   "fees",
    "tuition":   "fees",
    # result
    "result":    "result date",
    "results":   "result date",
    "marksheet": "result date",
    "cgpa":      "result date",
    # holiday
    "break":     "vacation",
    "off":       "holiday",
    "holiday":   "holiday dates",
    "holidays":  "holiday dates",
    # greet
    "wassup":    "hello",
    "sup":       "hello",
    "hiya":      "hello",
    "yo":        "hello",
    # subject aliases
    "netsec":    "network security",
    "cyber":     "network security",
    "networking":"network security",
    "react":     "mern stack",
    "node":      "mern stack",
    "nodejs":    "mern stack",
    "expressjs": "mern stack",
    "mongodb":   "mern stack",
    "iot":       "internet of things",
    "arduino":   "internet of things",
    "raspberry": "internet of things",
    "blockchain":"blockchain",
    "crypto":    "blockchain",
    "web3":      "blockchain",
    "java":      "advanced java",
    "android":   "mobile app development",
    "flutter":   "mobile app development",
    "kotlin":    "mobile app development",
    "agile":     "software engineering",
    "scrum":     "software engineering",
    "devops":    "software engineering",
    "sdlc":      "software engineering",
    "testing":   "software testing",
    "selenium":  "software testing",
    "junit":     "software testing",
    "spring":    "spring boot",
    "springboot":"spring boot",
    "pygame":    "game programming",
    "gaming":    "game programming",
    "ai":        "ai driven software",
    "ml":        "ai driven software",
    "figma":     "figma",
    "ui":        "figma",
    "ux":        "figma",
    "design":    "figma",
    "rxjs":      "functional programming",
    "reactive":  "reactive programming",
    "functional":"functional programming",
    "nosql":     "advanced database",
    "sql":       "advanced database",
    "database":  "advanced database",
}

# ── Fuzzy Matching Helpers ────────────────────────────────────────────
def levenshtein(s1, s2):
    """Fast edit-distance — O(n*m) but short strings only."""
=======
# =============================================================================
#  KES ACADBOT  —  Academic Chatbot for KES' Shroff College
#  Pure knowledge-base NLP (no external API required)
#  Clean, modular structure — easy to read and extend
# =============================================================================

from flask import Flask, render_template, request, jsonify, session
import re, uuid, random, json, os
from datetime import datetime, timedelta
from collections import Counter

app = Flask(__name__)
app.secret_key = "kes_acadbot_2025"

# ─────────────────────────────────────────────────────────────────────────────
#  FILE PATHS  —  all persistent data lives in the /data folder
# ─────────────────────────────────────────────────────────────────────────────
DATA_DIR   = os.path.join(os.path.dirname(__file__), "data")
HIST_FILE  = os.path.join(DATA_DIR, "history.json")
STATS_FILE = os.path.join(DATA_DIR, "stats.json")
os.makedirs(DATA_DIR, exist_ok=True)


# =============================================================================
#  SECTION 1 — KNOWLEDGE BASE
#
#  Structure of each intent:
#    "intent_name": {
#        "phrases"  : list of multi-word strings (matched with high priority)
#        "keywords" : list of single words     (matched as fallback)
#        "response" : the reply string
#    }
#
#  To ADD a new topic:
#    1. Add a new key to KNOWLEDGE_BASE below
#    2. Fill in phrases, keywords, and response
#    That's it — the NLP engine picks it up automatically.
# =============================================================================

KNOWLEDGE_BASE = {

    # ─── COLLEGE OVERVIEW ────────────────────────────────────────────────────

    "college_overview": {
        "phrases": [
            "about kes college", "about kes shroff college", "about the college",
            "college information", "college details", "tell me about this college",
            "what is kes shroff", "history of college", "college established",
            "naac grade", "iso certified", "autonomous college", "affiliated university",
        ],
        "keywords": ["naac", "autonomous", "affiliated", "accreditation", "iso"],
        "response": (
            "KES' Shroff College — College Overview\n\n"
            "Full Name  : KES' B.K. Shroff College of Arts & M.H. Shroff College of Commerce\n"
            "Location   : Bhulabhai Desai Road, Kandivali (W), Mumbai – 400067\n"
            "Founded    : 1989\n"
            "Status     : NAAC 'A' Grade | ISO 9001:2015 Certified | Autonomous College\n"
            "Affiliated : University of Mumbai\n\n"
            "Contact:\n"
            "• Phone   : 022-41914500\n"
            "• Email   : office@kessc.edu.in\n"
            "• Website : kessc.edu.in"
        )
    },

    "courses_offered": {
        "phrases": [
            "all courses", "courses offered", "list of courses",
            "what courses does kes offer", "programs available",
            "which degree can i take", "all programs", "departments",
        ],
        "keywords": ["courses", "programs", "departments", "degree", "stream"],
        "response": (
            "KES' Shroff College — All Courses Offered\n\n"
            "SCIENCE & IT:\n"
            "• B.Sc. IT  (Information Technology)\n"
            "• B.Sc.     (Data Science)\n"
            "• B.Sc.     (Artificial Intelligence)\n\n"
            "COMPUTER APPLICATIONS:\n"
            "• BCA       (Bachelor of Computer Applications)\n\n"
            "COMMERCE:\n"
            "• B.Com     (General Commerce)\n"
            "• BAF       (Accounting & Finance)\n"
            "• BBI       (Banking & Insurance)\n"
            "• BFM       (Financial Markets)\n"
            "• B.Com     (International Accounting)\n"
            "• B.Com     (Fintech)\n\n"
            "MANAGEMENT:\n"
            "• BMS       (Management Studies)\n"
            "• BBA       (Business Administration)\n\n"
            "ARTS & MEDIA:\n"
            "• BMM       (Mass Media)\n"
            "• BATM      (Arts in Tourism Management)\n"
            "• B.A.      (Economics & other streams)\n\n"
            "POSTGRADUATE:\n"
            "• M.Com     (Accountancy)\n"
            "• M.Com     (Management)\n"
            "• M.A.      (Economics)\n\n"
            "Duration: UG = 3 years (6 semesters) | PG = 2 years (4 semesters)\n"
            "Ask me about any specific course for full details!"
        )
    },

    # ─── ADMISSIONS ──────────────────────────────────────────────────────────

    "admission": {
        "phrases": [
            "admission process", "how to get admission", "how to apply",
            "admission form", "first year admission", "fy admission",
            "admission for bsc it", "admission for bcom", "admission for bms",
            "admission eligibility", "when does admission start",
            "admission 2025", "new admission", "apply for admission",
        ],
        "keywords": ["admission", "apply", "enroll", "registration", "eligibility"],
        "response": (
            "Admission Process — KES' Shroff College\n\n"
            "HOW TO APPLY:\n"
            "• Online portal : enrollonline.co.in/Registration/Apply/kessc\n"
            "• University portal : muugadmission.samarth.edu.in\n\n"
            "TIMELINE 2025:\n"
            "• FY Admission window : 27 May – 15 Jun 2025\n"
            "• Academic year starts : 09 Jun 2025\n"
            "• FY lectures begin    : 16 Jun 2025\n\n"
            "ELIGIBILITY:\n"
            "• B.Sc. IT / BCA / BMS / BBA : HSC pass with 45% minimum\n"
            "• B.Com / BAF / BBI / BFM    : HSC pass (any stream)\n"
            "• BMM / BATM / B.A.           : HSC pass\n"
            "• M.Com                       : B.Com with 45% minimum\n\n"
            "DOCUMENTS NEEDED:\n"
            "• HSC / Degree marksheet\n"
            "• Aadhar card\n"
            "• School leaving certificate\n"
            "• Caste certificate (if applicable)\n"
            "• Passport-size photographs\n"
            "• Bank account details\n\n"
            "Admission is merit-based as per University of Mumbai norms."
        )
    },

    # ─── B.Sc. IT ─────────────────────────────────────────────────────────────

    "bscit_overview": {
        "phrases": [
            "bsc it course", "b.sc it details", "about bsc it",
            "bsc information technology", "bsc it eligibility",
            "bsc it duration", "bsc it program",
        ],
        "keywords": ["bscit", "b.sc it"],
        "response": (
            "B.Sc. IT — Bachelor of Science in Information Technology\n\n"
            "Duration   : 3 years (6 semesters)\n"
            "Eligibility: HSC pass with minimum 45% (any stream)\n"
            "Credits    : 22 per semester\n"
            "Affiliation: University of Mumbai (Autonomous)\n\n"
            "FOCUS AREAS:\n"
            "• Programming (Python, Java, JavaScript)\n"
            "• Networking & Cyber Security\n"
            "• Web & Mobile Development\n"
            "• Cloud Computing & IoT\n"
            "• AI / ML & Data Science\n"
            "• Blockchain & FinTech\n\n"
            "CAREER OPTIONS:\n"
            "• Software Developer / Web Developer\n"
            "• Network Engineer / Cyber Security Analyst\n"
            "• Data Analyst / AI Engineer\n"
            "• System Administrator\n"
            "• IT Consultant\n\n"
            "Ask me about Sem 5 or Sem 6 subjects for detailed syllabus!"
        )
    },

    "bscit_sem5": {
        "phrases": [
            "bsc it sem 5", "bsc it semester 5", "sem 5 subjects",
            "semester 5 subjects", "sem v subjects", "5th sem subjects",
            "sem 5 syllabus", "subjects in sem 5", "sem5",
        ],
        "keywords": [],
        "response": (
            "B.Sc. IT — Semester V Subjects (2025-26)\n\n"
            "MAJOR MANDATORY:\n"
            "• 25UBIT501 — Network Security               (4 cr)\n"
            "• 25UBIT502 — Web Development Framework      (2 cr)\n"
            "• 25UBIT503 — Software Engineering & Agile   (4 cr)\n\n"
            "MINOR:\n"
            "• 25UBIT504 — Advanced Java                  (4 cr)\n\n"
            "ELECTIVE (choose any 1):\n"
            "• 25UBIT505 — Mobile App Development\n"
            "• 25UBIT506 — Functional & Reactive Programming\n"
            "• 25UBIT507 — Advanced Database Programming\n\n"
            "VOCATIONAL / SKILL:\n"
            "• 25UBIT508 — Figma                          (2 cr)\n\n"
            "FIELD PROJECT:\n"
            "• 25UBIT509 — Field Project                  (2 cr)\n\n"
            "Total Credits: 22"
        )
    },

    "bscit_sem6": {
        "phrases": [
            "bsc it sem 6", "bsc it semester 6", "sem 6 subjects",
            "semester 6 subjects", "sem vi subjects", "6th sem subjects",
            "sem 6 syllabus", "subjects in sem 6", "sem6",
            "subjects of semester 6",
        ],
        "keywords": [],
        "response": (
            "B.Sc. IT — Semester VI Subjects (2025-26)\n\n"
            "MAJOR MANDATORY:\n"
            "• 25UBIT601 — Full-Stack Web Dev / MERN      (4 cr)\n"
            "• 25UBIT602 — Blockchain                     (2 cr)\n"
            "• 25UBIT603 — Internet of Things (IoT)       (4 cr)\n\n"
            "MINOR:\n"
            "• 25UBIT604 — Software Testing               (4 cr)\n\n"
            "ELECTIVE (choose any 1):\n"
            "• 25UBIT605 — Spring Boot\n"
            "• 25UBIT606 — Game Programming with Python\n"
            "• 25UBIT607 — AI-Driven Software Development\n\n"
            "ON JOB TRAINING:\n"
            "• OJT       — On Job Training                (4 cr)\n\n"
            "Total Credits: 22"
        )
    },

    # ─── INDIVIDUAL B.Sc. IT SUBJECTS ────────────────────────────────────────

    "network_security": {
        "phrases": [
            "network security", "25ubit501", "ubit501",
            "tell me about network security", "network security subject",
        ],
        "keywords": ["netsec"],
        "response": (
            "Network Security (25UBIT501)\n\n"
            "Type: Major Mandatory | Credits: 4 | Marks: 150\n\n"
            "UNITS:\n"
            "1. Intro & Threats       — CIA Triad, malware, DoS/DDoS\n"
            "2. Cryptography          — AES, RSA, TLS/SSL, digital signatures\n"
            "3. Security Technologies — Firewalls, VPNs, IDS/IPS\n"
            "4. Wireless & Web Sec    — WPA3, OWASP Top 10\n"
            "5. Monitoring & Law      — Wireshark, Nmap, IT Act\n\n"
            "PRACTICALS: Wireshark analysis, AES in Python, Nmap scanning, OWASP ZAP"
        )
    },

    "mern_stack": {
        "phrases": [
            "mern stack", "full stack web development", "25ubit601",
            "tell me about mern", "fullstack subject",
        ],
        "keywords": ["mern", "fullstack"],
        "response": (
            "Full-Stack Web Development — MERN Stack (25UBIT601)\n\n"
            "Type: Major Mandatory | Credits: 4 | Marks: 150\n\n"
            "MERN STACK:\n"
            "• M — MongoDB   (NoSQL database)\n"
            "• E — Express.js (backend framework)\n"
            "• R — React.js   (frontend library)\n"
            "• N — Node.js    (JavaScript runtime)\n\n"
            "Topics: REST APIs, JWT auth, state management, deployment, CI/CD"
        )
    },

    "iot": {
        "phrases": [
            "internet of things", "iot subject", "25ubit603",
            "tell me about iot", "iot details",
        ],
        "keywords": [],
        "response": (
            "Internet of Things — IoT (25UBIT603)\n\n"
            "Type: Major Mandatory | Credits: 4 | Marks: 150\n\n"
            "UNITS:\n"
            "1. IoT Architecture  — layers, devices, gateways, cloud\n"
            "2. Sensors           — types, interfacing, data collection\n"
            "3. Microcontrollers  — Arduino & Raspberry Pi\n"
            "4. Protocols         — MQTT, HTTP, CoAP, Zigbee\n"
            "5. Cloud & Security  — AWS IoT, Azure IoT, IoT security\n\n"
            "PRACTICALS: Arduino wiring, Raspberry Pi GPIO, MQTT pub/sub"
        )
    },

    "blockchain": {
        "phrases": [
            "blockchain", "25ubit602", "tell me about blockchain",
            "smart contract subject", "blockchain subject",
        ],
        "keywords": ["web3"],
        "response": (
            "Blockchain (25UBIT602)\n\n"
            "Type: Major Mandatory | Credits: 2 | Marks: 150\n\n"
            "Topics:\n"
            "• Distributed ledger technology\n"
            "• Consensus mechanisms — PoW, PoS\n"
            "• Ethereum & smart contracts (Solidity basics)\n"
            "• Real-world blockchain applications & DeFi"
        )
    },

    "software_testing": {
        "phrases": [
            "software testing", "25ubit604", "tell me about software testing",
            "testing subject",
        ],
        "keywords": ["selenium", "junit"],
        "response": (
            "Software Testing (25UBIT604)\n\n"
            "Type: Minor | Credits: 4 | Marks: 150\n\n"
            "Topics:\n"
            "• Black-box & white-box testing\n"
            "• Unit, integration, system, acceptance testing\n"
            "• Test-driven development (TDD)\n"
            "• Automation with Selenium & JUnit\n"
            "• Test case design & quality assurance"
        )
    },

    "advanced_java": {
        "phrases": [
            "advanced java", "25ubit504", "tell me about advanced java",
            "java subject",
        ],
        "keywords": [],
        "response": (
            "Advanced Java (25UBIT504)\n\n"
            "Type: Minor | Credits: 4 | Marks: 150\n\n"
            "Topics: JDBC, Servlets, JSP, Hibernate ORM,\n"
            "Spring framework, multithreading, enterprise Java.\n\n"
            "Practicals: CRUD with JDBC, Servlet login, Spring MVC mini app."
        )
    },

    "software_engineering": {
        "phrases": [
            "software engineering", "25ubit503", "agile methodologies",
            "tell me about software engineering", "se subject",
        ],
        "keywords": ["sdlc", "scrum", "agile", "devops"],
        "response": (
            "Software Engineering & Agile Methodologies (25UBIT503)\n\n"
            "Type: Major Mandatory | Credits: 4 | Marks: 150\n\n"
            "UNITS:\n"
            "1. SDLC Models    — Waterfall, Spiral, V-Model, Agile\n"
            "2. Requirements   — SRS, UML diagrams\n"
            "3. Design         — MVC, Microservices, Design Patterns\n"
            "4. Agile & DevOps — Scrum, Kanban, JIRA, Docker, CI/CD\n"
            "5. Testing        — TDD, Selenium, JUnit, versioning"
        )
    },

    "mobile_app": {
        "phrases": [
            "mobile app development", "25ubit505", "android subject",
            "tell me about mobile app",
        ],
        "keywords": ["android", "flutter", "kotlin"],
        "response": (
            "Mobile App Development (25UBIT505)\n\n"
            "Type: Elective | Credits: 4 | Marks: 150\n\n"
            "Topics: Android/cross-platform development,\n"
            "activity lifecycle, REST API integration, Firebase,\n"
            "UI components, app publishing on Play Store."
        )
    },

    "spring_boot": {
        "phrases": [
            "spring boot", "25ubit605", "tell me about spring boot",
            "spring boot subject",
        ],
        "keywords": ["spring"],
        "response": (
            "Spring Boot (25UBIT605)\n\n"
            "Type: Elective | Credits: 4 | Marks: 150\n\n"
            "Topics: Spring MVC, Spring Data JPA, Spring Security,\n"
            "Hibernate integration, microservices with Spring Cloud,\n"
            "building and securing REST APIs."
        )
    },

    "game_programming": {
        "phrases": [
            "game programming", "game programming with python", "25ubit606",
            "tell me about game programming", "pygame subject",
        ],
        "keywords": ["pygame", "gaming"],
        "response": (
            "Game Programming with Python (25UBIT606)\n\n"
            "Type: Elective | Credits: 4 | Marks: 150\n\n"
            "Topics: Pygame library, game loop, sprites, collision detection,\n"
            "physics simulation, scoring systems, AI opponents (Minimax algorithm),\n"
            "level design."
        )
    },

    "ai_driven_software": {
        "phrases": [
            "ai driven software", "25ubit607", "tell me about ai driven software",
            "ai software subject", "machine learning subject",
        ],
        "keywords": [],
        "response": (
            "AI-Driven Software Development (25UBIT607)\n\n"
            "Type: Elective | Credits: 4 | Marks: 150\n\n"
            "Topics: Integrating AI/ML into applications,\n"
            "NLP pipelines, computer vision APIs, AI-assisted coding,\n"
            "ML model deployment with Flask/FastAPI."
        )
    },

    "web_dev_framework": {
        "phrases": [
            "web development framework", "25ubit502", "web framework subject",
            "tell me about web development framework",
        ],
        "keywords": [],
        "response": (
            "Web Development Framework (25UBIT502)\n\n"
            "Type: Major Mandatory | Credits: 2 | Marks: 150\n\n"
            "Topics: Frontend frameworks (React, Angular, Vue),\n"
            "backend with Node/Express, REST API development,\n"
            "state management, deployment."
        )
    },




    # ─── BCA ─────────────────────────────────────────────────────────────────


    # ─── B.COM ───────────────────────────────────────────────────────────────

    "bcom": {
        "phrases": [
            "bcom course", "b.com details", "about bcom",
            "bachelor of commerce", "bcom subjects", "bcom syllabus",
            "bcom eligibility", "bcom duration", "general commerce",
            "what is bcom",
        ],
        "keywords": ["bcom", "b.com", "commerce"],
        "response": (
            "B.Com — Bachelor of Commerce\n\n"
            "Duration   : 3 years (6 semesters)\n"
            "Eligibility: HSC pass (any stream)\n"
            "Affiliation: University of Mumbai\n\n"
            "CORE SUBJECTS:\n"
            "• Financial Accounting & Bookkeeping\n"
            "• Cost Accounting & Management Accounting\n"
            "• Business Economics & Statistics\n"
            "• Business Law & Company Law\n"
            "• Direct & Indirect Taxation\n"
            "• Auditing & Assurance\n"
            "• Commerce & Business Management\n"
            "• Foundation of IT\n\n"
            "SEMESTER-WISE TOPICS:\n"
            "• Sem I & II : Basics of accounting, economics, law\n"
            "• Sem III & IV: Cost accounting, taxation, auditing\n"
            "• Sem V & VI : Advanced accounting, management, project\n\n"
            "CAREER OPTIONS:\n"
            "• Accountant / Tax Consultant / Auditor\n"
            "• Banking & Finance sector\n"
            "• Government exams (CA, CMA, CS preparation)\n"
            "• MBA / M.Com higher studies"
        )
    },

    "bcom_sem1": {
        "phrases": [
            "bcom sem 1", "b.com semester 1", "bcom first semester",
            "bcom sem 1 subjects", "b.com sem 1 syllabus",
        ],
        "keywords": [],
        "response": (
            "B.Com — Semester I Subjects\n\n"
            "• Financial Accounting — I\n"
            "• Business Economics   — I\n"
            "• Business Communication\n"
            "• Foundation Course — I (Environmental Studies)\n"
            "• Mathematical & Statistical Techniques — I\n"
            "• Commerce — I (Business Environment)\n\n"
            "Passing marks: 40% per subject"
        )
    },

    "bcom_sem2": {
        "phrases": [
            "bcom sem 2", "b.com semester 2", "bcom second semester",
            "bcom sem 2 subjects", "b.com sem 2 syllabus",
        ],
        "keywords": [],
        "response": (
            "B.Com — Semester II Subjects\n\n"
            "• Financial Accounting — II\n"
            "• Business Economics   — II\n"
            "• Business Law         — I\n"
            "• Foundation Course    — II (Social Awareness)\n"
            "• Mathematical & Statistical Techniques — II\n"
            "• Commerce — II (Insurance & Risk Management)\n\n"
            "Passing marks: 40% per subject"
        )
    },

    "bcom_sem3": {
        "phrases": [
            "bcom sem 3", "b.com semester 3", "bcom third semester",
            "bcom sem 3 subjects", "bcom sy sem 3",
        ],
        "keywords": [],
        "response": (
            "B.Com — Semester III Subjects\n\n"
            "• Financial Accounting — III\n"
            "• Cost Accounting — I\n"
            "• Business Law — II (Company Law basics)\n"
            "• Commerce — III (Export Marketing)\n"
            "• IT in Accounting — I\n"
            "• Foundation Course — III\n\n"
            "Passing marks: 40% per subject"
        )
    },

    "bcom_sem4": {
        "phrases": [
            "bcom sem 4", "b.com semester 4", "bcom fourth semester",
            "bcom sem 4 subjects", "bcom sy sem 4",
        ],
        "keywords": [],
        "response": (
            "B.Com — Semester IV Subjects\n\n"
            "• Financial Accounting — IV\n"
            "• Cost Accounting — II\n"
            "• Direct Tax\n"
            "• Commerce — IV (Entrepreneurship)\n"
            "• IT in Accounting — II\n"
            "• Research Methodology (Optional)\n\n"
            "Passing marks: 40% per subject"
        )
    },

    "bcom_sem5": {
        "phrases": [
            "bcom sem 5", "b.com semester 5", "bcom fifth semester",
            "bcom sem 5 subjects", "bcom ty sem 5",
        ],
        "keywords": [],
        "response": (
            "B.Com — Semester V Subjects\n\n"
            "• Financial Accounting — V (Advanced)\n"
            "• Management Accounting\n"
            "• Indirect Tax (GST)\n"
            "• Auditing & Assurance — I\n"
            "• Commerce — V (Operations Management)\n"
            "• Elective (Investment Analysis / Export Management)\n\n"
            "Passing marks: 40% per subject"
        )
    },

    "bcom_sem6": {
        "phrases": [
            "bcom sem 6", "b.com semester 6", "bcom sixth semester",
            "bcom sem 6 subjects", "bcom ty sem 6",
        ],
        "keywords": [],
        "response": (
            "B.Com — Semester VI Subjects\n\n"
            "• Financial Accounting — VI (Advanced)\n"
            "• Management Accounting — II\n"
            "• Indirect Tax — II\n"
            "• Auditing & Assurance — II\n"
            "• Commerce — VI (Strategic Management)\n"
            "• Project Work\n\n"
            "Passing marks: 40% per subject"
        )
    },

    # ─── BAF ─────────────────────────────────────────────────────────────────

    "baf": {
        "phrases": [
            "baf course", "bachelor of accounting and finance",
            "about baf", "baf details", "baf eligibility",
            "baf subjects", "baf syllabus", "accounting and finance",
            "baf duration", "what is baf",
        ],
        "keywords": ["baf", "accountancy", "finance course"],
        "response": (
            "BAF — Bachelor of Accounting & Finance\n\n"
            "Duration   : 3 years (6 semesters)\n"
            "Eligibility: HSC pass (any stream), min 45% preferred\n"
            "Affiliation: University of Mumbai\n\n"
            "CORE SUBJECTS:\n"
            "• Financial Accounting (Advanced)\n"
            "• Cost Accounting & Management Accounting\n"
            "• Direct Tax & Indirect Tax (GST)\n"
            "• Auditing & Assurance\n"
            "• Corporate Finance & Financial Management\n"
            "• Company Law & Securities Regulation\n"
            "• Investment Analysis & Portfolio Management\n"
            "• Financial Services & Markets\n\n"
            "SEMESTER-WISE FOCUS:\n"
            "• Sem I & II : Accounting basics, Business Law, Economics\n"
            "• Sem III & IV: Cost Accounting, Taxation, Auditing\n"
            "• Sem V & VI : Advanced Finance, Portfolio Mgmt, Project\n\n"
            "CAREER OPTIONS:\n"
            "• Chartered Accountant (CA) preparation\n"
            "• Cost & Management Accountant (CMA)\n"
            "• Finance Manager / CFO track\n"
            "• Investment Analyst / Equity Researcher\n"
            "• Banking & Insurance sector\n\n"
            "BAF is ideal for students aiming for CA, CMA, CS professional courses."
        )
    },

    "baf_sem_subjects": {
        "phrases": [
            "baf sem 1", "baf sem 2", "baf sem 3", "baf sem 4",
            "baf sem 5", "baf sem 6", "baf semester subjects", "baf syllabus semester",
        ],
        "keywords": [],
        "response": (
            "BAF — Semester-wise Subjects\n\n"
            "SEM I & II (Foundation):\n"
            "• Financial Accounting I & II\n"
            "• Business Law, Economics, Statistics\n"
            "• Cost Accounting basics\n\n"
            "SEM III & IV (Core):\n"
            "• Advanced Accounting\n"
            "• Taxation (Direct & Indirect)\n"
            "• Auditing & Company Law\n"
            "• Corporate Finance\n\n"
            "SEM V & VI (Advanced):\n"
            "• Investment Analysis & Portfolio Management\n"
            "• Advanced Taxation\n"
            "• Financial Reporting\n"
            "• Project Work\n\n"
            "Ask me for specific semester subjects if needed!"
        )
    },

    # ─── BBI ─────────────────────────────────────────────────────────────────

    "bbi": {
        "phrases": [
            "bbi course", "bachelor of banking and insurance",
            "about bbi", "bbi details", "bbi subjects",
            "bbi syllabus", "banking and insurance course",
            "what is bbi",
        ],
        "keywords": ["bbi", "banking insurance"],
        "response": (
            "BBI — Bachelor of Banking & Insurance\n\n"
            "Duration   : 3 years (6 semesters)\n"
            "Eligibility: HSC pass (any stream)\n"
            "Affiliation: University of Mumbai\n\n"
            "CORE SUBJECTS:\n"
            "• Principles of Banking & Bank Management\n"
            "• Banking Law & Practice\n"
            "• Principles of Insurance (Life & Non-Life)\n"
            "• Risk Management & Underwriting\n"
            "• Financial Accounting & Taxation\n"
            "• Business Economics & Statistics\n"
            "• Information Technology in Banking\n"
            "• Claims & Settlements\n\n"
            "CAREER OPTIONS:\n"
            "• Bank PO / Bank Clerk (IBPS exams)\n"
            "• Insurance Officer / Underwriter\n"
            "• Risk Manager\n"
            "• Financial Advisor\n"
            "• IRDA / RBI regulated roles"
        )
    },

    # ─── BFM ─────────────────────────────────────────────────────────────────

    # ─── BMS ─────────────────────────────────────────────────────────────────

    "bms": {
        "phrases": [
            "bms course", "bachelor of management studies",
            "about bms", "bms details", "bms eligibility",
            "bms subjects", "bms syllabus", "bms duration",
            "management studies course", "what is bms",
        ],
        "keywords": ["bms", "management studies"],
        "response": (
            "BMS — Bachelor of Management Studies\n\n"
            "Duration   : 3 years (6 semesters)\n"
            "Eligibility: HSC pass with minimum 45%\n"
            "Affiliation: University of Mumbai\n\n"
            "CORE SUBJECTS:\n"
            "• Principles of Management\n"
            "• Business Communication & Soft Skills\n"
            "• Business Economics (Micro & Macro)\n"
            "• Financial Management & Accounting\n"
            "• Human Resource Management (HRM)\n"
            "• Marketing Management\n"
            "• Operations Management\n"
            "• Strategic Management\n"
            "• International Business\n"
            "• Entrepreneurship Development\n"
            "• Research Methodology & Project\n\n"
            "SEMESTER-WISE FOCUS:\n"
            "• Sem I & II : Foundation — Management basics, economics, law\n"
            "• Sem III & IV: Core — HR, Marketing, Finance, Operations\n"
            "• Sem V & VI : Advanced — Strategy, International business, Project\n\n"
            "CAREER OPTIONS:\n"
            "• Business Manager / Management Trainee\n"
            "• HR Manager / Recruiter\n"
            "• Marketing Executive / Brand Manager\n"
            "• Operations Manager\n"
            "• Entrepreneur\n"
            "• MBA / PGDM (higher studies)"
        )
    },

    "bms_sem_subjects": {
        "phrases": [
            "bms sem 1", "bms sem 2", "bms sem 3", "bms sem 4",
            "bms sem 5", "bms sem 6", "bms semester subjects",
            "bms syllabus semester",
        ],
        "keywords": [],
        "response": (
            "BMS — Semester-wise Subjects\n\n"
            "SEM I & II (Foundation):\n"
            "• Principles of Management\n"
            "• Business Communication\n"
            "• Business Economics I & II\n"
            "• Business Law, Statistics\n\n"
            "SEM III & IV (Core):\n"
            "• Financial Management & Accounting\n"
            "• HRM & Organisational Behaviour\n"
            "• Marketing Management\n"
            "• Operations & Production Management\n\n"
            "SEM V & VI (Advanced):\n"
            "• Strategic Management\n"
            "• International Business & Export-Import\n"
            "• Entrepreneurship Development\n"
            "• Research Methodology & Project Work\n\n"
            "Ask me for any specific BMS subject details!"
        )
    },

    # ─── BBA ─────────────────────────────────────────────────────────────────

    "bba": {
        "phrases": [
            "bba course", "bachelor of business administration",
            "about bba", "bba details", "bba eligibility",
            "bba subjects", "bba syllabus", "business administration",
            "what is bba",
        ],
        "keywords": ["bba", "business administration"],
        "response": (
            "BBA — Bachelor of Business Administration\n\n"
            "Duration   : 3 years (6 semesters)\n"
            "Eligibility: HSC pass with minimum 45%\n"
            "Affiliation: University of Mumbai\n\n"
            "CORE SUBJECTS:\n"
            "• Business Management & Leadership\n"
            "• Business Communication\n"
            "• Financial Accounting & Corporate Finance\n"
            "• Marketing & Digital Marketing\n"
            "• Human Resource Management\n"
            "• Operations & Supply Chain Management\n"
            "• Business Analytics & IT\n"
            "• Business Ethics & Corporate Governance\n"
            "• Entrepreneurship & Innovation\n"
            "• International Business\n\n"
            "CAREER OPTIONS:\n"
            "• Business Development Executive\n"
            "• Marketing Manager\n"
            "• HR Executive\n"
            "• Operations Analyst\n"
            "• Entrepreneur\n"
            "• MBA (higher studies)"
        )
    },

    # ─── BMM ─────────────────────────────────────────────────────────────────

    "bmm": {
        "phrases": [
            "bmm course", "bachelor of mass media",
            "about bmm", "bmm details", "bmm eligibility",
            "bmm subjects", "bmm syllabus", "mass media course",
            "what is bmm", "journalism course",
        ],
        "keywords": ["bmm", "mass media", "journalism", "advertising"],
        "response": (
            "BMM — Bachelor of Mass Media\n\n"
            "Duration   : 3 years (6 semesters)\n"
            "Eligibility: HSC pass (any stream)\n"
            "Affiliation: University of Mumbai\n\n"
            "CORE SUBJECTS:\n"
            "• Print Journalism & Feature Writing\n"
            "• Broadcast Media (TV & Radio)\n"
            "• Digital Journalism & Social Media\n"
            "• Advertising & Brand Communication\n"
            "• Public Relations & Corporate Communication\n"
            "• Photography & Videography\n"
            "• Film Studies & Scriptwriting\n"
            "• Media Laws & Ethics\n"
            "• Research Methods in Media\n\n"
            "SPECIALIZATIONS (Sem V & VI):\n"
            "• Advertising, Journalism, or Public Relations\n\n"
            "CAREER OPTIONS:\n"
            "• Journalist / Reporter / Editor\n"
            "• Copywriter / Content Writer\n"
            "• PR Executive / Brand Manager\n"
            "• Film & Television Production\n"
            "• Social Media Manager\n"
            "• Digital Marketing Specialist"
        )
    },

    # ─── M.COM ───────────────────────────────────────────────────────────────

    "mcom": {
        "phrases": [
            "mcom course", "master of commerce", "m.com details",
            "about mcom", "mcom eligibility", "mcom subjects",
            "mcom syllabus", "mcom duration", "postgraduate commerce",
            "what is mcom", "pg course",
        ],
        "keywords": ["mcom", "m.com", "postgraduate", "pg commerce"],
        "response": (
            "M.Com — Master of Commerce\n\n"
            "Duration       : 2 years (4 semesters)\n"
            "Eligibility    : B.Com / BAF / BBI / BFM with minimum 45%\n"
            "Specializations: Accountancy | Management\n"
            "Affiliation    : University of Mumbai\n\n"
            "M.COM (ACCOUNTANCY) SUBJECTS:\n"
            "• Advanced Financial Accounting\n"
            "• Advanced Cost Accounting & Costing\n"
            "• Advanced Direct & Indirect Taxation\n"
            "• Auditing & Assurance (Advanced)\n"
            "• Financial Reporting & Analysis\n"
            "• Research Methodology & Project\n\n"
            "M.COM (MANAGEMENT) SUBJECTS:\n"
            "• Strategic Management\n"
            "• International Business Management\n"
            "• Financial Management (Advanced)\n"
            "• Human Resource Development\n"
            "• Marketing Management (Advanced)\n"
            "• Research Methodology & Dissertation\n\n"
            "CAREER OPTIONS:\n"
            "• Lecturer / Professor (after NET/SET)\n"
            "• Senior Accountant / CFO track\n"
            "• CA / CMA / CS (professional exams)\n"
            "• PhD / Research"
        )
    },

    # ─── B.Sc. DATA SCIENCE & AI ─────────────────────────────────────────────

    "data_science": {
        "phrases": [
            "data science course", "bsc data science",
            "about data science", "data science details",
            "data science eligibility", "data science subjects",
        ],
        "keywords": ["data science"],
        "response": (
            "B.Sc. Data Science\n\n"
            "Duration   : 3 years (6 semesters)\n"
            "Eligibility: HSC pass with Mathematics, min 45%\n"
            "Affiliation: University of Mumbai\n\n"
            "CORE SUBJECTS:\n"
            "• Python Programming & Statistics\n"
            "• Data Wrangling & Visualization\n"
            "• Machine Learning Algorithms\n"
            "• Deep Learning & Neural Networks\n"
            "• Big Data Analytics (Hadoop, Spark)\n"
            "• Database Systems (SQL & NoSQL)\n"
            "• Natural Language Processing (NLP)\n"
            "• Data Mining & Warehousing\n\n"
            "CAREER OPTIONS:\n"
            "• Data Analyst / Data Scientist\n"
            "• ML Engineer / AI Researcher\n"
            "• Business Intelligence Analyst\n"
            "• Data Engineer"
        )
    },

    "ai_course": {
        "phrases": [
            "artificial intelligence course", "bsc artificial intelligence",
            "about ai course", "ai course details", "ai course eligibility",
            "bsc ai subjects",
        ],
        "keywords": [],
        "response": (
            "B.Sc. Artificial Intelligence\n\n"
            "Duration   : 3 years (6 semesters)\n"
            "Eligibility: HSC pass with Mathematics, min 45%\n"
            "Affiliation: University of Mumbai\n\n"
            "CORE SUBJECTS:\n"
            "• Python & Programming Fundamentals\n"
            "• Mathematics for AI (Calculus, Linear Algebra)\n"
            "• Machine Learning & Deep Learning\n"
            "• Computer Vision & Image Processing\n"
            "• Natural Language Processing\n"
            "• Robotics & Automation basics\n"
            "• AI Ethics & Governance\n"
            "• Capstone Project\n\n"
            "CAREER OPTIONS:\n"
            "• AI Engineer / ML Engineer\n"
            "• Computer Vision Engineer\n"
            "• NLP Engineer\n"
            "• AI Researcher"
        )
    },

    # ─── BCA SEMESTER SUBJECTS ────────────────────────────────────────────────

    "bca_sem_subjects": {
        "phrases": [
            "bca sem 1", "bca sem 2", "bca sem 3", "bca sem 4",
            "bca sem 5", "bca sem 6", "bca semester subjects",
            "bca syllabus semester", "bca first year subjects",
            "bca second year subjects", "bca third year subjects",
        ],
        "keywords": [],
        "response": (
            "BCA — Semester-wise Subjects\n\n"
            "SEM I (Foundation):\n"
            "• Programming in C\n"
            "• Mathematical Foundations\n"
            "• Digital Electronics\n"
            "• Communication Skills\n"
            "• Office Automation Tools\n\n"
            "SEM II:\n"
            "• C++ Programming\n"
            "• Discrete Mathematics\n"
            "• Operating Systems\n"
            "• Accounting & Finance Basics\n\n"
            "SEM III:\n"
            "• Data Structures using C\n"
            "• Database Management Systems\n"
            "• Java Programming\n"
            "• Computer Networks\n\n"
            "SEM IV:\n"
            "• Advanced Java\n"
            "• Software Engineering\n"
            "• Web Technologies (HTML, CSS, JS)\n"
            "• Linux & Open Source\n\n"
            "SEM V:\n"
            "• Python Programming\n"
            "• Android App Development\n"
            "• Cyber Security Fundamentals\n"
            "• Elective (AI / Cloud / Data Science)\n\n"
            "SEM VI:\n"
            "• Full Stack Development\n"
            "• Project Work (Major)\n"
            "• Emerging Technologies\n"
            "Passing marks: 40% per subject"
        )
    },

    # ─── BFM ─────────────────────────────────────────────────────────────────

    "bfm": {
        "phrases": [
            "bfm course", "bachelor of financial markets",
            "about bfm", "bfm details", "bfm eligibility",
            "bfm subjects", "bfm syllabus", "financial markets course",
            "what is bfm", "stock market course",
        ],
        "keywords": ["bfm", "financial markets", "stock market course"],
        "response": (
            "BFM — Bachelor of Financial Markets\n\n"
            "Duration   : 3 years (6 semesters)\n"
            "Eligibility: HSC pass (any stream)\n"
            "Affiliation: University of Mumbai\n\n"
            "CORE SUBJECTS:\n"
            "• Financial Markets & Capital Markets\n"
            "• Equity, Debt & Derivative Markets\n"
            "• Mutual Funds & Portfolio Management\n"
            "• Securities Analysis & Valuation\n"
            "• Financial Planning & Wealth Management\n"
            "• Corporate Finance & Investment Banking\n"
            "• Financial Risk Management\n"
            "• Commodity Markets & Foreign Exchange\n"
            "• NISM / NCFM Certification preparation\n\n"
            "CAREER OPTIONS:\n"
            "• Stock Broker / Equity Analyst\n"
            "• Mutual Fund Advisor / Wealth Manager\n"
            "• Investment Banker\n"
            "• Risk Analyst / Compliance Officer\n"
            "• Financial Planner (CFP)\n\n"
            "BFM is ideal for students interested in stock markets and investments."
        )
    },

    "bfm_sem_subjects": {
        "phrases": [
            "bfm sem 1", "bfm sem 2", "bfm sem 3", "bfm sem 4",
            "bfm sem 5", "bfm sem 6", "bfm semester subjects",
            "bfm syllabus semester",
        ],
        "keywords": [],
        "response": (
            "BFM — Semester-wise Subjects\n\n"
            "SEM I & II (Foundation):\n"
            "• Introduction to Financial Markets\n"
            "• Financial Accounting I & II\n"
            "• Business Economics, Business Law\n"
            "• Foundation of Commerce\n\n"
            "SEM III & IV (Core):\n"
            "• Equity & Debt Markets\n"
            "• Derivatives & Commodity Markets\n"
            "• Cost Accounting, Taxation\n"
            "• Securities Law & SEBI Regulations\n\n"
            "SEM V & VI (Advanced):\n"
            "• Mutual Fund & Portfolio Management\n"
            "• Investment Banking & Corporate Finance\n"
            "• Financial Risk Management\n"
            "• Forex & International Finance\n"
            "• Project Work\n\n"
            "Ask for a specific semester if you need more detail!"
        )
    },

    # ─── BBI SEMESTER SUBJECTS ────────────────────────────────────────────────

    "bbi_sem_subjects": {
        "phrases": [
            "bbi sem 1", "bbi sem 2", "bbi sem 3", "bbi sem 4",
            "bbi sem 5", "bbi sem 6", "bbi semester subjects",
            "bbi syllabus semester",
        ],
        "keywords": [],
        "response": (
            "BBI — Semester-wise Subjects\n\n"
            "SEM I & II (Foundation):\n"
            "• Principles of Banking\n"
            "• Financial Accounting I & II\n"
            "• Business Economics, Business Law\n"
            "• Introduction to Insurance\n\n"
            "SEM III & IV (Core):\n"
            "• Commercial Banking Operations\n"
            "• Life Insurance & General Insurance\n"
            "• Cost Accounting, Taxation\n"
            "• Banking Regulation & Compliance\n\n"
            "SEM V & VI (Advanced):\n"
            "• Investment Banking\n"
            "• Risk Management in Banking & Insurance\n"
            "• Treasury Operations\n"
            "• Project Work\n\n"
            "Ask for a specific semester if you need more detail!"
        )
    },

    # ─── BBA SEMESTER SUBJECTS ────────────────────────────────────────────────

    "bba_sem_subjects": {
        "phrases": [
            "bba sem 1", "bba sem 2", "bba sem 3", "bba sem 4",
            "bba sem 5", "bba sem 6", "bba semester subjects",
            "bba syllabus semester",
        ],
        "keywords": [],
        "response": (
            "BBA — Semester-wise Subjects\n\n"
            "SEM I & II (Foundation):\n"
            "• Principles of Management\n"
            "• Business Communication\n"
            "• Business Economics I & II\n"
            "• Accounting & Finance Basics\n"
            "• Business Law\n\n"
            "SEM III & IV (Core):\n"
            "• Marketing Management\n"
            "• Human Resource Management\n"
            "• Operations Management\n"
            "• Financial Management\n"
            "• Organizational Behaviour\n\n"
            "SEM V & VI (Advanced):\n"
            "• Strategic Management\n"
            "• International Business\n"
            "• Business Analytics & IT\n"
            "• Entrepreneurship & Innovation\n"
            "• Project Work / Internship\n\n"
            "Passing marks: 40% per subject"
        )
    },

    # ─── BMM SEMESTER SUBJECTS ────────────────────────────────────────────────

    "bmm_sem_subjects": {
        "phrases": [
            "bmm sem 1", "bmm sem 2", "bmm sem 3", "bmm sem 4",
            "bmm sem 5", "bmm sem 6", "bmm semester subjects",
            "bmm syllabus semester",
        ],
        "keywords": [],
        "response": (
            "BMM — Semester-wise Subjects\n\n"
            "SEM I & II (Foundation):\n"
            "• Introduction to Mass Communication\n"
            "• Reporting & Writing for Media\n"
            "• Media History & Theory\n"
            "• Photography & Visual Communication\n\n"
            "SEM III & IV (Core):\n"
            "• Print Journalism & Magazine Writing\n"
            "• Broadcast Media (TV & Radio)\n"
            "• Digital Journalism & Social Media\n"
            "• Advertising Basics & Brand Communication\n"
            "• PR & Corporate Communication\n\n"
            "SEM V & VI (Specialization):\n"
            "Choose: Advertising | Journalism | Public Relations\n"
            "• Advanced electives in chosen specialization\n"
            "• Media Laws & Ethics\n"
            "• Research & Project Work\n\n"
            "Passing marks: 40% per subject"
        )
    },

    # ─── BATM ─────────────────────────────────────────────────────────────────

    "batm": {
        "phrases": [
            "batm course", "bachelor of arts tourism management",
            "about batm", "batm details", "batm eligibility",
            "batm subjects", "tourism management course",
            "what is batm", "tourism course",
        ],
        "keywords": ["batm", "tourism", "travel management"],
        "response": (
            "BATM — Bachelor of Arts in Tourism Management\n\n"
            "Duration   : 3 years (6 semesters)\n"
            "Eligibility: HSC pass (any stream)\n"
            "Affiliation: University of Mumbai\n\n"
            "CORE SUBJECTS:\n"
            "• Introduction to Tourism & Travel Industry\n"
            "• Geography of Tourism\n"
            "• Hotel & Hospitality Management\n"
            "• Tour Operations & Travel Agency Management\n"
            "• Airline & Transport Management\n"
            "• Event Management\n"
            "• Cultural Tourism & Heritage Studies\n"
            "• Tourism Marketing & Digital Promotion\n"
            "• Foreign Language (basic)\n\n"
            "CAREER OPTIONS:\n"
            "• Travel Agent / Tour Operator\n"
            "• Hotel & Hospitality Manager\n"
            "• Airline Staff / Airport Ground Services\n"
            "• Event Coordinator\n"
            "• Tourism Marketing Executive\n"
            "• Government Tourism Department"
        )
    },

    # ─── M.COM SEMESTER SUBJECTS ─────────────────────────────────────────────

    "mcom_sem_subjects": {
        "phrases": [
            "mcom sem 1", "mcom sem 2", "mcom sem 3", "mcom sem 4",
            "mcom semester subjects", "mcom syllabus semester",
            "m.com subjects", "postgraduate commerce subjects",
        ],
        "keywords": [],
        "response": (
            "M.Com — Semester-wise Subjects\n\n"
            "M.COM ACCOUNTANCY:\n"
            "Sem I: Advanced Financial Accounting, Business Finance, Statistics\n"
            "Sem II: Advanced Cost Accounting, Auditing, Tax Planning\n"
            "Sem III: Financial Reporting, Advanced Taxation, Corporate Law\n"
            "Sem IV: Research Methodology, Dissertation / Project\n\n"
            "M.COM MANAGEMENT:\n"
            "Sem I: Strategic Management, Financial Management, Marketing (Advanced)\n"
            "Sem II: HRD, Operations Management, International Business\n"
            "Sem III: Business Ethics, Entrepreneurship, Elective\n"
            "Sem IV: Research Methodology, Dissertation / Project\n\n"
            "Passing marks: 40% per subject | Dissertation compulsory in Sem IV"
        )
    },

    # ─── SCHOLARSHIP ─────────────────────────────────────────────────────────

    "scholarship": {
        "phrases": [
            "scholarship", "scholarship eligibility", "how to get scholarship",
            "freeship", "merit scholarship", "government scholarship",
            "ebc scholarship", "obc scholarship", "sc st scholarship",
            "scholarship amount", "scholarship documents", "minority scholarship",
        ],
        "keywords": ["scholarship", "freeship", "concession"],
        "response": (
            "Scholarships & Freeship — KES' Shroff College\n\n"
            "GOVERNMENT SCHOLARSHIPS:\n"
            "• EBC Freeship : For families with income < Rs 1 lakh/year\n"
            "• OBC / SBC Scholarship : For eligible caste categories\n"
            "• SC / ST / NT / DT Scholarship : Post-matric scholarship\n"
            "• Minority Scholarship : For notified minority communities\n"
            "• Central Sector Scholarship : 80th percentile HSC students\n\n"
            "COLLEGE-LEVEL:\n"
            "• Merit scholarships for first-class distinction students\n"
            "• Sports & Cultural achievement-based fee concessions\n\n"
            "HOW TO APPLY:\n"
            "• Apply online at mahadbt.maharashtra.gov.in (state schemes)\n"
            "• Apply during admission — first month of academic year\n"
            "• Submit income certificate, caste certificate, marksheet\n\n"
            "CONTACT:\n"
            "• Visit the college office or scholarship helpdesk\n"
            "• Phone: 022-41914500"
        )
    },

    # ─── NAAC & RECOGNITION ──────────────────────────────────────────────────

    "naac": {
        "phrases": [
            "naac accreditation", "naac grade", "college naac",
            "iqac", "quality certification", "iso certification",
            "autonomous college meaning", "university affiliation",
            "about naac", "college recognition", "college grade",
        ],
        "keywords": ["naac", "iqac", "autonomous", "accreditation"],
        "response": (
            "NAAC & Accreditation — KES' Shroff College\n\n"
            "• NAAC Grade    : 'A' Grade (Accredited by NAAC)\n"
            "• ISO Status    : ISO 9001:2015 Quality Certified\n"
            "• College Type  : Autonomous College\n"
            "• Affiliated to : University of Mumbai\n\n"
            "WHAT AUTONOMOUS MEANS FOR STUDENTS:\n"
            "• College sets its own exam papers (not Mumbai University)\n"
            "• More flexible and updated syllabus\n"
            "• Industry-relevant curriculum\n"
            "• College issues its own exam and marksheets under UoM\n\n"
            "IQAC (Internal Quality Assurance Cell):\n"
            "• Monitors teaching quality and student outcomes\n"
            "• Organizes workshops, seminars, faculty development\n"
            "• Maintains quality benchmarks for accreditation renewal\n\n"
            "The 'A' grade NAAC status reflects high academic standards,\n"
            "infrastructure, and student outcomes."
        )
    },

    # ─── COLLEGE RULES & DISCIPLINE ──────────────────────────────────────────

    "college_rules": {
        "phrases": [
            "college rules", "college regulations", "discipline rules",
            "code of conduct", "dress code", "mobile phone rules",
            "ragging", "anti ragging", "college discipline",
            "student rules", "campus rules",
        ],
        "keywords": ["rules", "regulations", "conduct", "discipline"],
        "response": (
            "College Rules & Code of Conduct\n\n"
            "GENERAL RULES:\n"
            "• College ID card must be worn on campus at all times\n"
            "• Maintain silence in library, corridors, and examination halls\n"
            "• Mobile phones must be on silent mode inside classrooms\n"
            "• No use of mobile phones during lectures\n\n"
            "DRESS CODE:\n"
            "• Formal/semi-formal attire expected on campus\n"
            "• Formal dress compulsory on exam days and viva days\n\n"
            "ANTI-RAGGING:\n"
            "• Strict zero-tolerance policy on ragging\n"
            "• Anti-ragging committee and helpline active\n"
            "• Any form of ragging leads to suspension/expulsion\n\n"
            "LIBRARY:\n"
            "• No talking or food inside the library\n"
            "• Return books on time to avoid fines\n\n"
            "EXAMINATIONS:\n"
            "• Hall ticket mandatory for appearing in exams\n"
            "• No copying or malpractice — leads to cancellation of paper\n\n"
            "For the full rulebook, visit the college office."
        )
    },

    # ─── ATKT / BACKLOG ──────────────────────────────────────────────────────

    "atkt": {
        "phrases": [
            "atkt", "atkt rules", "backlog exam", "how to clear atkt",
            "failed subject", "failed in exam", "atkt form filling",
            "atkt exam date", "allowed to keep terms", "kt exam",
        ],
        "keywords": ["atkt", "backlog", "failed", "kt"],
        "response": (
            "ATKT — Allowed To Keep Terms\n\n"
            "ATKT RULES:\n"
            "• You can appear for higher semester exams even if you failed\n"
            "  in the previous semester, subject to conditions\n"
            "• Maximum 2 subjects in ATKT allowed to proceed to next semester\n"
            "• Students with ATKT must clear it within the allowed attempts\n\n"
            "ATKT EXAM SCHEDULE (2025-26):\n"
            "• Odd Sem ATKT (backlog): 10–20 Sep 2025\n"
            "• Even Sem ATKT Form Filling: 10 Dec 2025 – 20 Jan 2026\n"
            "• Even Sem ATKT Exam: 02–18 Mar 2026\n\n"
            "ATKT FORM FILLING:\n"
            "• Odd Sems Form Filling: 26 May – 05 Jun 2025\n"
            "• Forms available at college exam office\n\n"
            "IMPORTANT:\n"
            "• Passing marks: 40% per subject\n"
            "• For exact ATKT rules per course, check with the exam office\n"
            "• Phone: 022-41914500"
        )
    },

    # ─── REVALUATION ─────────────────────────────────────────────────────────

    "revaluation": {
        "phrases": [
            "revaluation", "rechecking marks", "how to apply revaluation",
            "revaluation process", "photocopy of answer sheet",
            "result wrong", "marks wrong", "apply for rechecking",
        ],
        "keywords": ["revaluation", "rechecking", "photocopy answer"],
        "response": (
            "Revaluation / Rechecking — KES' Shroff College\n\n"
            "PROCESS:\n"
            "• Apply for revaluation within 15 days of result declaration\n"
            "• Fill the revaluation form at the examination office\n"
            "• Pay the prescribed revaluation fee per subject\n\n"
            "TYPES AVAILABLE:\n"
            "• Revaluation : Full re-checking of the answer paper\n"
            "• Photocopy   : You can request a photocopy of your answer sheet\n"
            "  first to check before applying for full revaluation\n\n"
            "RESULT:\n"
            "• Revaluation result declared within 30–45 days\n"
            "• If marks increase, original fee is refunded\n\n"
            "CONTACT:\n"
            "• Visit the Examination Office during office hours\n"
            "• 9 AM – 5 PM, Monday to Saturday\n"
            "• Phone: 022-41914500"
        )
    },

    # ─── CAREER GUIDANCE ─────────────────────────────────────────────────────

    "career_guidance": {
        "phrases": [
            "career after bcom", "career after bms", "career after baf",
            "career after bscit", "career after bca", "career after bmm",
            "career after bbi", "career after bfm", "career after batm",
            "career after mcom", "career options", "what to do after",
            "job opportunities", "scope after degree", "further studies",
            "higher studies after bcom", "which course has better scope",
        ],
        "keywords": ["career", "job", "scope", "future", "higher studies"],
        "response": (
            "Career Guide — After Your Degree from KES Shroff College\n\n"
            "B.Sc. IT / BCA:\n"
            "• Software Developer, Web Developer, AI/ML Engineer\n"
            "• Higher studies: MCA, M.Sc. IT, MBA Tech\n\n"
            "B.Com / BAF / BBI / BFM:\n"
            "• Accountant, Tax Consultant, Banker, Investment Analyst\n"
            "• Professional exams: CA, CMA, CS, CFA, FRM\n"
            "• Higher studies: M.Com, MBA Finance\n\n"
            "BMS / BBA:\n"
            "• Business Manager, HR Manager, Marketing Executive\n"
            "• Higher studies: MBA / PGDM (top B-Schools)\n\n"
            "BMM:\n"
            "• Journalist, Content Writer, PR Executive, Digital Marketer\n"
            "• Higher studies: MA in Mass Communication, PG Diploma\n\n"
            "BATM:\n"
            "• Travel Agent, Hotel Manager, Airline Staff, Event Coordinator\n"
            "• Higher studies: PG Diploma in Hospitality / MBA Tourism\n\n"
            "M.Com:\n"
            "• Professor / Lecturer (after NET/SET), CFO track, Research / PhD\n\n"
            "Ask me about a specific course for detailed career info!"
        )
    },

    # ─── COURSE COMPARISON ───────────────────────────────────────────────────

    "course_comparison": {
        "phrases": [
            "difference between bcom and baf", "bcom vs baf",
            "difference between bms and bba", "bms vs bba",
            "difference between bscit and bca", "bscit vs bca",
            "difference between bbi and bfm", "bbi vs bfm",
            "which is better bcom or baf", "which course should i choose",
            "bcom or bms which is better", "baf or bbi",
        ],
        "keywords": ["difference between", "vs", "which is better", "compare courses"],
        "response": (
            "Course Comparison — KES' Shroff College\n\n"
            "B.COM vs BAF:\n"
            "• B.Com: General commerce — broader, good for all roles\n"
            "• BAF  : Specialised in Accounting & Finance — ideal for CA/CMA\n\n"
            "BMS vs BBA:\n"
            "• BMS: Management Studies — more research and theory focused\n"
            "• BBA: Business Administration — more practical, industry-ready\n"
            "• Both lead to MBA. BMS is University of Mumbai specific.\n\n"
            "B.Sc. IT vs BCA:\n"
            "• B.Sc. IT: More focused on IT/tech — networks, security, AI\n"
            "• BCA     : Broader computer applications — development focused\n"
            "• Both lead to software careers. B.Sc. IT is slightly more technical.\n\n"
            "BBI vs BFM:\n"
            "• BBI: Banking & Insurance operations\n"
            "• BFM: Stock markets, investments, and financial planning\n\n"
            "Still unsure? Visit the college and speak to the counsellor!\n"
            "Phone: 022-41914500"
        )
    },

    # ─── SPORTS & EXTRA-CURRICULAR ────────────────────────────────────────────

    "sports_activities": {
        "phrases": [
            "sports facilities", "sports at kes college", "college sports",
            "extra curricular activities", "clubs at college", "cultural fest",
            "nss", "ncc", "student council", "college events",
            "co curricular", "annual day", "college festival",
        ],
        "keywords": ["sports", "club", "nss", "ncc", "cultural", "fest", "event"],
        "response": (
            "Sports & Extra-Curricular Activities — KES' Shroff College\n\n"
            "SPORTS:\n"
            "• Cricket, Football, Basketball, Volleyball courts\n"
            "• Table Tennis, Carrom, Chess available\n"
            "• Inter-college and university-level tournaments\n"
            "• Sports scholarship for outstanding athletes\n\n"
            "SOCIAL ACTIVITIES:\n"
            "• NSS (National Service Scheme) — community service\n"
            "• NCC (National Cadet Corps) — defence oriented\n\n"
            "CLUBS & COMMITTEES:\n"
            "• Student Council (elected representatives)\n"
            "• Drama & Theatre Club\n"
            "• Music & Dance Club\n"
            "• Literary Club & Debating Society\n"
            "• IT & Coding Club (TechShroff)\n"
            "• Finance & Investment Club\n"
            "• Entrepreneurship Cell\n\n"
            "ANNUAL EVENTS:\n"
            "• Annual Cultural Fest (semester 2)\n"
            "• Annual Prize Distribution Day\n"
            "• Sports Day\n"
            "• Intercollegiate competitions throughout the year"
        )
    },

    # ─── CANTEEN & FOOD ───────────────────────────────────────────────────────

    "canteen": {
        "phrases": [
            "canteen", "college canteen", "food at college",
            "cafeteria", "mess", "tiffin", "food facility",
            "eating at college", "canteen timing",
        ],
        "keywords": ["canteen", "cafeteria", "food", "mess"],
        "response": (
            "Canteen — KES' Shroff College\n\n"
            "• Canteen is located on the ground floor of the college building\n"
            "• Timings: 8:30 AM – 5:30 PM (Monday to Saturday)\n"
            "• Serves snacks, meals, beverages, and daily specials\n"
            "• Hygienic and affordable pricing for students\n"
            "• Seating available inside and outside the canteen area\n\n"
            "For specific menu or pricing queries, visit the canteen directly."
        )
    },

    # ─── TRANSPORT / HOSTEL ──────────────────────────────────────────────────

    "transport_hostel": {
        "phrases": [
            "hostel facility", "hostel available", "accommodation",
            "college hostel", "transport facility", "bus service",
            "how to reach college", "college transport",
            "train station near college", "nearest station",
        ],
        "keywords": ["hostel", "accommodation", "transport", "bus"],
        "response": (
            "Transport & Accommodation — KES' Shroff College\n\n"
            "HOSTEL:\n"
            "• The college does not have an attached hostel facility\n"
            "• Students can explore private PG/hostel options near Kandivali\n\n"
            "HOW TO REACH COLLEGE:\n"
            "• Nearest Railway Station: Kandivali (W) — Western Railway Line\n"
            "  (5-10 minute walk from station to college)\n"
            "• Bus: BEST buses stop near Bhulabhai Desai Road\n"
            "• Auto / Cab: Available from Kandivali station\n\n"
            "ADDRESS:\n"
            "KES' Shroff College, Bhulabhai Desai Rd,\n"
            "Kandivali (W), Mumbai – 400067\n\n"
            "Google Maps: Search 'KES Shroff College Kandivali'"
        )
    },

    # ─── INTERNAL COMPLAINT / GRIEVANCE ──────────────────────────────────────

    "grievance": {
        "phrases": [
            "grievance cell", "complaint", "file complaint",
            "anti sexual harassment", "posh committee",
            "students grievance", "internal complaint committee",
            "how to raise complaint", "complaint against teacher",
        ],
        "keywords": ["grievance", "complaint", "harassment", "posh"],
        "response": (
            "Grievance & Complaint — KES' Shroff College\n\n"
            "STUDENT GRIEVANCE CELL:\n"
            "• Handles academic and non-academic grievances\n"
            "• Submit written complaint to the Principal's office\n"
            "• Also available: suggestion/complaint box at college entrance\n\n"
            "ANTI-SEXUAL HARASSMENT (POSH):\n"
            "• Internal Complaints Committee (ICC) is active\n"
            "• Any form of sexual harassment must be reported to ICC\n"
            "• Complaints are treated with strict confidentiality\n\n"
            "ANTI-RAGGING:\n"
            "• Anti-ragging committee handles all ragging complaints\n"
            "• You can also report at: antiragging.in\n\n"
            "CONTACT:\n"
            "• Principal's Office: 022-41914500\n"
            "• Email: principal@kessc.edu.in"
        )
    },

    # ─── EXAM HALL TICKET ─────────────────────────────────────────────────────

    "hall_ticket": {
        "phrases": [
            "hall ticket", "admit card", "exam admit card",
            "how to get hall ticket", "exam hall pass",
            "when will hall ticket come", "hall ticket download",
        ],
        "keywords": ["hall ticket", "admit card"],
        "response": (
            "Hall Ticket / Admit Card — KES' Shroff College\n\n"
            "• Hall tickets are issued before semester exams\n"
            "• Distributed through the college examination office\n"
            "• Also available on the college website (kessc.edu.in)\n"
            "• Usually released 7–10 days before exam date\n\n"
            "CONDITIONS TO GET HALL TICKET:\n"
            "• Minimum 75% attendance is mandatory\n"
            "• All college fees must be paid up to date\n"
            "• Library books must be returned / no pending dues\n\n"
            "IMPORTANT:\n"
            "• Carry hall ticket + college ID on every exam day\n"
            "• Examinees without hall ticket will NOT be allowed to write exam\n\n"
            "For issues contact: Examination Office, 022-41914500"
        )
    },

    # ─── INTERNSHIP OPPORTUNITIES ─────────────────────────────────────────────

    "internship": {
        "phrases": [
            "internship", "summer internship", "internship opportunities",
            "how to find internship", "college internship support",
            "internship portal", "paid internship", "industrial training",
        ],
        "keywords": ["internship"],
        "response": (
            "Internships — KES' Shroff College\n\n"
            "• Training & Placement Cell assists students in finding internships\n"
            "• Companies regularly visit campus for internship offers\n"
            "• Internship portals: Internshala, LinkedIn, Naukri, Indeed\n\n"
            "COURSE-SPECIFIC:\n"
            "• B.Sc. IT / BCA: Tech companies, IT firms, startups\n"
            "• BMS / BBA     : Management consultancy, FMCG, marketing firms\n"
            "• BAF / B.Com   : CA firms, banks, finance companies\n"
            "• BMM           : Media houses, advertising agencies, digital firms\n"
            "• BFM           : Broking firms, banks, wealth management\n\n"
            "OJT (On Job Training) in Sem VI:\n"
            "• Mandatory for B.Sc. IT students\n"
            "• 4 credits | Submit OJT report at end of semester\n\n"
            "Contact: Placement Cell, KES' Shroff College, 022-41914500"
        )
    },


    "attendance": {
        "phrases": [
            "minimum attendance", "how much attendance required",
            "short attendance", "attendance requirement",
            "what happens if attendance is low",
        ],
        "keywords": ["attendance", "absent", "bunk", "proxy"],
        "response": (
            "Attendance Policy — All Courses\n\n"
            "• Minimum required : 75% attendance in each subject\n"
            "• Below 75%        : Detained from semester exams\n"
            "• Medical leave    : Submit medical certificate within 3 days\n\n"
            "INTERNAL MARKS IMPACT:\n"
            "• Attendance contributes 5 marks to internal assessment\n"
            "• 85%+ attendance = full 5 marks\n\n"
            "Monthly defaulter lists are displayed on the notice board.\n"
            "Tip: Aim for 85%+ to be safe and score full internal marks!"
        )
    },

    "internal_marks": {
        "phrases": [
            "internal marks", "internal assessment", "cia marks",
            "internal marks breakdown", "how are internal marks calculated",
            "unit test marks", "marks distribution",
        ],
        "keywords": ["internal", "cia"],
        "response": (
            "Internal Assessment Breakdown — All Courses\n\n"
            "• Attendance              : 5 marks\n"
            "• Assignments / Tests     : 10 marks\n"
            "• Unit Test               : 10 marks\n"
            "Total Internal            : 25 marks per subject\n\n"
            "UNIT TEST SCHEDULE 2025-26:\n"
            "Odd Semesters (I, III, V):\n"
            "• Unit Test         : 18–21 Aug 2025\n"
            "• Additional Test   : 01–04 Sep 2025\n\n"
            "Even Semesters (II, IV, VI):\n"
            "• Unit Test         : 28–31 Jan 2026\n"
            "• Additional Test   : 09–12 Feb 2026"
        )
    },

    "exam_schedule": {
        "phrases": [
            "exam schedule", "exam dates", "examination dates",
            "when are exams", "semester exam dates", "exam timetable",
            "when is the exam", "exam 2025", "exam 2026",
        ],
        "keywords": ["exam", "examination", "timetable"],
        "response": (
            "Exam Schedule — KES' Shroff College (2025-26)\n\n"
            "ODD SEMESTERS (I, III, V) — All Courses:\n"
            "• Unit Test           : 18–21 Aug 2025\n"
            "• Additional Unit Test: 01–04 Sep 2025\n"
            "• Lectures End        : 24 Sep 2025\n"
            "• Semester Exam       : 08–17 Oct 2025\n\n"
            "EVEN SEMESTERS (II, IV, VI) — All Courses:\n"
            "• Unit Test           : 28–31 Jan 2026\n"
            "• Additional Unit Test: 09–12 Feb 2026\n"
            "• Lectures End (SY/TY): 07 Mar 2026\n"
            "• Semester Exam       : 21 Mar – 04 Apr 2026\n\n"
            "• Result Declaration  : 20 Apr 2026\n"
            "• ATKT Exam (backlog) : 10–20 Sep 2025\n\n"
            "Always check the official college notice board for last-minute changes."
        )
    },

    "results_grading": {
        "phrases": [
            "result date", "result declaration", "when will result come",
            "how to check result", "marksheet", "revaluation",
            "passing marks", "atkt rule", "cgpa grading",
            "how results are declared",
        ],
        "keywords": ["result", "pass", "fail", "cgpa", "atkt", "marksheet"],
        "response": (
            "Results & Grading — All Courses\n\n"
            "• Result Declaration (Even Sems II, IV, VI) : 20 Apr 2026\n"
            "• Passing Marks      : 40% per subject (internal + external)\n"
            "• ATKT               : Allowed if failing max 2 subjects\n"
            "• ATKT Exam          : 10–20 Sep 2025 (backlog students)\n"
            "• ATKT Form Filling  : 10 Dec 2025 – 20 Jan 2026\n\n"
            "HOW TO CHECK RESULTS:\n"
            "• University website : mu.ac.in\n"
            "• College website    : kessc.edu.in/results\n\n"
            "REVALUATION:\n"
            "Apply within 15 days of result declaration.\n"
            "Fee as prescribed by University of Mumbai."
        )
    },

    "academic_calendar": {
        "phrases": [
            "academic calendar", "college schedule", "important dates",
            "all dates", "full academic calendar", "college calendar 2025",
        ],
        "keywords": [],
        "response": (
            "Academic Calendar 2025-26 — KES' Shroff College\n\n"
            "TERM 1  (Jun – Nov 2025):\n"
            "• 27 May – 05 Jun : ATKT Form Filling (Odd Sems)\n"
            "• 09 Jun          : Academic Year Starts\n"
            "• 10 Jun          : II & III year lectures begin\n"
            "• 16 Jun          : FY lectures begin\n"
            "• 18–21 Aug       : Unit Test (Odd Sems)\n"
            "• 27–31 Aug       : Ganapati Vacation\n"
            "• 01–04 Sep       : Additional Unit Test (Odd Sems)\n"
            "• 10–20 Sep       : ATKT Exam (backlog students)\n"
            "• 24 Sep          : Lectures End (Odd Sems)\n"
            "• 08–17 Oct       : Semester Exam (I, III, V)\n"
            "• 20 Oct – 05 Nov : Diwali Vacation\n\n"
            "TERM 2  (Nov 2025 – Jun 2026):\n"
            "• 06 Nov          : Sem IV & VI lectures begin\n"
            "• 02–10 Dec       : Certificate Course Registration (Term II)\n"
            "• 10 Dec – 20 Jan : ATKT Form Filling (Even Sems)\n"
            "• 26 Dec – 01 Jan : Winter Vacation\n"
            "• 28–31 Jan       : Unit Test I (Even Sems)\n"
            "• 09–12 Feb       : Additional Unit Test (Even Sems)\n"
            "• 02–18 Mar       : ATKT Exam (UG & PG)\n"
            "• 07 Mar          : Lectures End (SY & TY)\n"
            "• 21 Mar – 04 Apr : Semester Exam (II, IV, VI)\n"
            "• 20 Apr          : Result Declaration\n"
            "• 23 Apr – 02 Jun : Summer Vacation"
        )
    },

    "holidays": {
        "phrases": [
            "holiday list", "college holidays", "vacation dates",
            "diwali vacation", "ganapati vacation", "winter vacation",
            "summer vacation", "when is diwali break", "holiday dates",
        ],
        "keywords": ["holiday", "vacation", "break", "ganapati", "diwali"],
        "response": (
            "Official Holidays & Vacations (2025-26)\n\n"
            "• Ganapati Vacation : 27–31 Aug 2025  (5 days)\n"
            "• Diwali Vacation   : 20 Oct – 05 Nov 2025  (16 days)\n"
            "• Winter Vacation   : 26 Dec 2025 – 01 Jan 2026  (7 days)\n"
            "• Summer Vacation   : 23 Apr – 02 Jun 2026  (~6 weeks)\n\n"
            "Additional public holidays as per Government of Maharashtra.\n"
            "Check the college notice board for exact holiday declarations."
        )
    },

    # ─── FEES ─────────────────────────────────────────────────────────────────

    "fees": {
        "phrases": [
            "fee structure", "fees for bscit", "fees for bcom", "fees for bms",
            "fees for baf", "fees for bca", "college fees",
            "how much is the fee", "how to pay fees",
            "fee payment", "scholarship", "tuition fee",
        ],
        "keywords": ["fee", "fees", "tuition", "scholarship", "challan", "payment"],
        "response": (
            "Fees & Payments — KES' Shroff College\n\n"
            "FEE PAYMENT:\n"
            "• Portal  : College website → Student Login → Fee Portal\n"
            "• Mode    : Online (preferred) or challan at accounts office\n"
            "• Late fee: Rs 50 per day after due date\n\n"
            "SCHOLARSHIPS & CONCESSIONS:\n"
            "• Apply in the first month of academic year\n"
            "• Government scholarships (SC/ST/OBC/EBC) available\n"
            "• Merit scholarships for top academic performers\n"
            "• Minority scholarships available\n\n"
            "FEE STRUCTURE:\n"
            "• Fee varies by course and is set by University of Mumbai\n"
            "• Exact fee chart available at college admin office\n"
            "• Contact: 022-41914500 | office@kessc.edu.in\n\n"
            "Fee receipts: Visit the accounts office in person."
        )
    },

    # ─── FACILITIES ──────────────────────────────────────────────────────────

    "facilities": {
        "phrases": [
            "college facilities", "labs in college", "library facilities",
            "canteen", "sports", "gym", "wifi campus",
            "computer lab", "auditorium", "seminar hall",
            "what facilities does kes have",
        ],
        "keywords": ["facilities", "lab", "canteen", "sports", "wifi", "hostel"],
        "response": (
            "Facilities — KES' Shroff College\n\n"
            "ACADEMIC:\n"
            "• State-of-the-art Computer Labs (IT & BCA departments)\n"
            "• Central Library with e-resources & online journals\n"
            "• Seminar Halls & Auditorium\n"
            "• Language Lab\n\n"
            "CAMPUS LIFE:\n"
            "• Wi-Fi enabled campus\n"
            "• Student Canteen\n"
            "• Sports facilities (indoor & outdoor)\n"
            "• Student Activity Room\n\n"
            "SUPPORT SERVICES:\n"
            "• Training & Placement Cell\n"
            "• CCTV surveillance for safety\n"
            "• Grievance Redressal Cell\n"
            "• Anti-ragging Committee\n"
            "• Student Counselling Cell\n\n"
            "Note: Hostel facility is NOT available on campus."
        )
    },

    "library": {
        "phrases": [
            "library timings", "library hours", "library information",
            "borrow books", "library card", "library fine",
            "how to use library", "library resources",
        ],
        "keywords": ["library", "book", "borrow", "journals", "opac"],
        "response": (
            "Library — KES' Shroff College\n\n"
            "• Timings         : 9:00 AM – 6:00 PM  (Monday to Saturday)\n"
            "• Books allowed   : 2 books at a time\n"
            "• Loan period     : 7 days per book\n"
            "• Late return fine: Rs 2 per day\n"
            "• Reference books : Available for reading inside library only\n"
            "• E-resources     : Online journals & e-books available\n"
            "• OPAC catalogue  : Search books online on college website\n\n"
            "Bring your college ID card to borrow books."
        )
    },

    # ─── PLACEMENT ───────────────────────────────────────────────────────────

    "placement": {
        "phrases": [
            "placement cell", "campus placement", "job placement",
            "companies visiting", "placement record", "internship",
            "job opportunities", "placement in kes college",
            "how is placement in kes",
        ],
        "keywords": ["placement", "job", "recruit", "campus", "internship"],
        "response": (
            "Training & Placement — KES' Shroff College\n\n"
            "• Active Training & Placement Cell on campus\n"
            "• Campus recruitment drives organized every year\n\n"
            "SECTORS THAT RECRUIT:\n"
            "• IT & Software companies  (for B.Sc. IT, BCA)\n"
            "• Banking & Finance firms  (for BAF, BBI, BFM, B.Com)\n"
            "• Management companies     (for BMS, BBA)\n"
            "• Media & Advertising      (for BMM)\n\n"
            "TRAINING PROVIDED:\n"
            "• Aptitude & reasoning workshops\n"
            "• Group discussion & interview preparation\n"
            "• Resume writing & LinkedIn profile building\n"
            "• Soft skills & communication training\n\n"
            "For placement queries contact the placement office directly."
        )
    },

    # ─── PROJECT & OJT ───────────────────────────────────────────────────────

    "project_ojt": {
        "phrases": [
            "project guidelines", "field project", "project submission",
            "project marks", "ojt", "on job training",
            "project details", "how to submit project",
            "project evaluation", "project for bscit",
        ],
        "keywords": ["project", "ojt"],
        "response": (
            "Project & OJT Guidelines — B.Sc. IT\n\n"
            "SEMESTER V — Field Project (25UBIT509):\n"
            "• Type          : CEP / Field Project\n"
            "• Credits       : 2\n"
            "• Group size    : 2–3 students\n"
            "• Synopsis      : Submit by Week 4 of Sem V\n"
            "• Mid-review    : Week 10 of Sem V\n"
            "• Final viva    : End of Semester V\n"
            "• Marks         : 100  (50 internal + 50 external)\n\n"
            "SEMESTER VI — On Job Training (OJT):\n"
            "• Type          : Industry internship or live in-house project\n"
            "• Credits       : 4\n"
            "• Submission    : OJT report + presentation\n"
            "• Marks         : As per college evaluation rubrics\n\n"
            "Both projects require a faculty guide to be assigned."
        )
    },

    # ─── CONTACT ─────────────────────────────────────────────────────────────

    "contact": {
        "phrases": [
            "college contact", "college phone number", "college email",
            "college address", "how to contact kes college",
            "principal contact", "office contact",
        ],
        "keywords": ["contact", "phone", "email", "address", "principal"],
        "response": (
            "Contact — KES' Shroff College\n\n"
            "• Address : Bhulabhai Desai Road, Kandivali (W), Mumbai – 400067\n"
            "• Phone   : 022-41914500\n"
            "• Email   : principal@kessc.edu.in\n"
            "            office@kessc.edu.in\n"
            "• Website : kessc.edu.in\n\n"
            "Office hours: Monday to Saturday, 9:00 AM – 5:00 PM\n\n"
            "For specific departments, visit the college website."
        )
    },

    # ─── CONVERSATION ────────────────────────────────────────────────────────

    "greet": {
        "phrases": ["hello", "hi", "hey", "good morning", "good afternoon",
                    "good evening", "hii", "helo", "hai"],
        "keywords": [],
        "response": (
            "Hello! I'm KES AcadBot, the official AI assistant for KES' Shroff College.\n\n"
            "I can help you with information about:\n"
            "• All Courses  : B.Sc. IT, BCA, B.Com, BAF, BBI, BFM, BMS, BBA, BMM, M.Com\n"
            "• Admissions   : Process, eligibility, important dates\n"
            "• Academics    : Subjects, exams, attendance, results\n"
            "• Campus       : Library, facilities, placement, fees\n\n"
            "What would you like to know?"
        )
    },

    "thanks": {
        "phrases": ["thank you", "thanks", "thank u", "thx", "ty", "helpful", "great"],
        "keywords": ["thank", "helpful", "awesome"],
        "response": "You're welcome! Feel free to ask anything anytime."
    },

    # ─── BCA OVERVIEW ────────────────────────────────────────────────────────

    "bca": {
        "phrases": [
            "bca course", "bachelor of computer applications",
            "about bca", "bca details", "bca eligibility",
            "bca subjects", "bca syllabus", "bca duration",
            "what is bca", "computer applications course",
        ],
        "keywords": ["bca"],
        "response": (
            "BCA — Bachelor of Computer Applications\n\n"
            "Duration   : 3 years (6 semesters)\n"
            "Eligibility: HSC pass with Mathematics or Statistics\n"
            "Affiliation: University of Mumbai\n\n"
            "FOCUS AREAS:\n"
            "• Programming (C, C++, Java, Python)\n"
            "• Data Structures & Algorithms\n"
            "• Database Management Systems (DBMS)\n"
            "• Computer Networks & Cyber Security\n"
            "• Web Development (HTML, CSS, PHP, JS)\n"
            "• Software Engineering\n"
            "• Mobile Application Development\n"
            "• Emerging Tech (AI, Cloud, Data Science)\n\n"
            "CAREER OPTIONS:\n"
            "• Software Developer / Web Developer\n"
            "• Database Administrator\n"
            "• Network / System Administrator\n"
            "• IT Support Specialist\n"
            "• Higher studies: MCA, M.Sc. IT, MBA Tech\n\n"
            "Ask me about BCA semester-wise subjects for full details!"
        )
    },

    # ─── FIGMA & REMAINING BSCIT SUBJECTS ─────────────────────────────────────

    "figma": {
        "phrases": [
            "figma", "25ubit508", "tell me about figma",
            "ui ux subject", "design subject", "figma subject",
        ],
        "keywords": ["figma", "ui", "ux", "design"],
        "response": (
            "Figma (25UBIT508)\n\n"
            "Type: Vocational / Skill Enhancement | Credits: 2 | Marks: 100\n\n"
            "Topics:\n"
            "• UI/UX design fundamentals\n"
            "• Wireframing and prototyping\n"
            "• Component libraries and design systems\n"
            "• Auto-layout and responsive design\n"
            "• Team collaboration and handoff\n\n"
            "Practicals: Design a mobile app wireframe, build an interactive prototype"
        )
    },

    "functional_reactive": {
        "phrases": [
            "functional programming", "reactive programming", "25ubit506",
            "tell me about functional programming",
            "functional reactive programming",
        ],
        "keywords": ["rxjs", "functional"],
        "response": (
            "Functional & Reactive Programming (25UBIT506)\n\n"
            "Type: Elective | Credits: 4 | Marks: 150\n\n"
            "Units:\n"
            "1. Fundamentals of FP — pure functions, immutability, recursion\n"
            "2. FP in JavaScript/Kotlin — map, filter, reduce, closures\n"
            "3. Advanced FP — monads, functors, lazy evaluation, Redux\n"
            "4. Reactive Programming — RxJS/RxJava, Observables\n"
            "5. Reactive Systems — Spring WebFlux, real-time dashboards\n\n"
            "Practicals: RxJS Observables, real-time search, Spring WebFlux"
        )
    },

    "advanced_database": {
        "phrases": [
            "advanced database", "25ubit507", "tell me about advanced database",
            "database programming subject",
        ],
        "keywords": ["nosql"],
        "response": (
            "Advanced Database Programming (25UBIT507)\n\n"
            "Type: Elective | Credits: 4 | Marks: 150\n\n"
            "Topics:\n"
            "• Advanced SQL — stored procedures, triggers, indexing\n"
            "• NoSQL with MongoDB — CRUD, aggregation, indexing\n"
            "• Database transactions and concurrency\n"
            "• Query optimization techniques\n"
            "• Modern database design patterns\n\n"
            "Practicals: MySQL stored procedures, MongoDB operations, query tuning"
        )
    },

    "bye": {
        "phrases": ["bye", "goodbye", "see you", "cya", "later", "good bye"],
        "keywords": ["bye", "quit", "exit"],
        "response": "Goodbye! Best of luck with your academics. Come back anytime!"
    },

}  # ── END OF KNOWLEDGE_BASE ─────────────────────────────────────────────────


# =============================================================================
#  SECTION 2 — SYNONYM MAP
#  Maps informal / alternate words → canonical words used in phrases/keywords
#  To ADD synonyms: just add more key:value pairs below
# =============================================================================

SYNONYMS = {
    # ── General academic terms ────────────────────────────────────────────────
    "sem":              "semester",
    "course":           "subjects",
    "courses":          "subjects",
    "subject":          "subjects",
    "paper":            "subjects",
    "papers":           "subjects",
    "test":             "exam",
    "tests":            "exam",
    "exams":            "exam",
    "timetable":        "exam schedule",
    "marks":            "internal marks",
    "score":            "internal marks",
    "grades":           "internal marks",
    "grade":            "internal marks",
    "cia":              "internal marks",
    "holiday":          "holiday dates",
    "holidays":         "holiday dates",
    "break":            "vacation",
    "fee":              "fees",
    "tuition":          "fees",
    "payment":          "fees",
    "books":            "library",
    "borrow":           "library",
    "job":              "placement",
    "training":         "ojt",
    "result":           "result date",
    "results":          "result date",
    "marksheet":        "result date",
    "cgpa":             "result date",
    "gpa":              "result date",
    "backlog":          "atkt",
    "kt":               "atkt",
    "recheck":          "revaluation",
    "rechecking":       "revaluation",

    # ── Greeting variations ───────────────────────────────────────────────────
    "wassup":           "hello",
    "sup":              "hello",
    "yo":               "hello",
    "hiya":             "hello",

    # ── B.Sc. IT subject shortcuts ────────────────────────────────────────────
    "netsec":           "network security",
    "cyber":            "network security",
    "react":            "mern stack",
    "node":             "mern stack",
    "nodejs":           "mern stack",
    "iot":              "internet of things",
    "arduino":          "internet of things",
    "raspberry":        "internet of things",
    "blockchain":       "blockchain",
    "crypto":           "blockchain",
    "web3":             "blockchain",
    "java":             "advanced java",
    "android":          "mobile app development",
    "flutter":          "mobile app development",
    "agile":            "software engineering",
    "scrum":            "software engineering",
    "devops":           "software engineering",
    "sdlc":             "software engineering",
    "selenium":         "software testing",
    "junit":            "software testing",
    "spring":           "spring boot",
    "pygame":           "game programming",
    "rxjs":             "functional programming",
    "nosql":            "advanced database",
    "mongodb":          "advanced database",

    # ── Course name shortcuts ─────────────────────────────────────────────────
    "bscit":            "bsc it",
    "b.sc it":          "bsc it",
    "commerce":         "b.com",
    "bcom":             "b.com",
    "management":       "bms",
    "it course":        "bsc it",
    "accountancy":      "baf",
    "banking":          "bbi",
    "insurance":        "bbi",
    "stock market":     "bfm",
    "financial market": "bfm",
    "mass media":       "bmm",
    "journalism":       "bmm",
    "advertising":      "bmm",
    "tourism":          "batm",
    "travel":           "batm",
    "postgraduate":     "mcom",
    "pg":               "mcom",
    "masters":          "mcom",

    # ── Question type shortcuts ───────────────────────────────────────────────
    "scope":            "career options",
    "future":           "career options",
    "after degree":     "career options",
    "admit":            "hall ticket",
    "admit card":       "hall ticket",
    "scholarship":      "scholarship",
    "freeship":         "scholarship",
    "concession":       "scholarship",
    "complaint":        "grievance",
    "harassment":       "grievance",
    "ragging":          "college rules",
    "hostel":           "transport hostel",
    "accommodation":    "transport hostel",
    "canteen":          "canteen",
    "food":             "canteen",
    "sports":           "sports activities",
    "nss":              "sports activities",
    "ncc":              "sports activities",
    "festival":         "sports activities",
    "fest":             "sports activities",
    "naac":             "naac",
    "iqac":             "naac",
    "autonomous":       "naac",
}


# =============================================================================
#  SECTION 3 — NLP ENGINE
#  Functions: preprocess → apply_synonyms → get_intent → get_response
#  No changes needed here unless you want to tune scoring weights
# =============================================================================

def preprocess(text: str) -> str:
    """Lowercase, strip punctuation, collapse whitespace."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", " ", text)
    return re.sub(r"\s+", " ", text)


def apply_synonyms(text: str) -> str:
    """Replace known synonyms with canonical forms."""
    tokens = text.split()
    result = []
    i = 0
    while i < len(tokens):
        # Try 2-word synonym first
        if i + 1 < len(tokens):
            pair = tokens[i] + " " + tokens[i + 1]
            if pair in SYNONYMS:
                result.extend(SYNONYMS[pair].split())
                i += 2
                continue
        # Single word synonym
        result.append(SYNONYMS.get(tokens[i], tokens[i]))
        i += 1
    return " ".join(result)


def levenshtein(s1: str, s2: str) -> int:
    """Edit distance between two short strings."""
>>>>>>> f763b2e (Refactor: clean structure with separate CSS and JS modules)
    if len(s1) > 30 or len(s2) > 30:
        return 999
    m, n = len(s1), len(s2)
    dp = list(range(n + 1))
    for i in range(1, m + 1):
<<<<<<< HEAD
        prev = dp[:]
        dp[0] = i
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[j] = prev[j-1]
            else:
                dp[j] = 1 + min(prev[j], dp[j-1], prev[j-1])
    return dp[n]

def fuzzy_score(token, target):
    """Return 0–1 similarity; 1 = exact, 0 = too distant."""
    if token == target:
        return 1.0
    dist = levenshtein(token, target)
    max_len = max(len(token), len(target), 1)
    sim = 1 - dist / max_len
    return sim if sim >= 0.80 else 0.0   # threshold: 80% similarity

# ── NLP Engine ────────────────────────────────────────────────────────
def preprocess(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text

def apply_synonyms(text):
    """Replace each token with its canonical form if a synonym exists."""
    tokens = text.split()
    out = []
    i = 0
    while i < len(tokens):
        # try 2-word synonym first
        if i + 1 < len(tokens):
            two = tokens[i] + " " + tokens[i+1]
            if two in SYNONYMS:
                out.extend(SYNONYMS[two].split())
                i += 2
                continue
        w = tokens[i]
        out.append(SYNONYMS.get(w, w))
        i += 1
    return " ".join(out)

def fuzzy_phrase_in_text(phrase_tokens, text_tokens):
    """
    Check whether phrase_tokens appear (in order, roughly) in text_tokens
    using fuzzy per-token matching. Returns match_ratio (0–1).
    """
    if not phrase_tokens:
        return 0.0
    matched = 0
    t_idx = 0
    for p_tok in phrase_tokens:
        found = False
        while t_idx < len(text_tokens):
            sim = fuzzy_score(text_tokens[t_idx], p_tok)
            t_idx += 1
            if sim > 0:
                matched += sim
                found = True
                break
        if not found:
            pass  # partial credit still counts
    return matched / len(phrase_tokens)

def get_intent(user_input):
    processed  = preprocess(user_input)
    expanded   = apply_synonyms(processed)           # synonym expansion
    text_tokens = expanded.split()

    best_intent, best_score = None, 0.0
=======
        prev, dp[0] = dp[:], i
        for j in range(1, n + 1):
            dp[j] = (prev[j - 1] if s1[i - 1] == s2[j - 1]
                     else 1 + min(prev[j], dp[j - 1], prev[j - 1]))
    return dp[n]


def fuzzy_sim(a: str, b: str) -> float:
    """Return 0–1 similarity. Returns 0 if below 80% threshold."""
    if a == b:
        return 1.0
    sim = 1 - levenshtein(a, b) / max(len(a), len(b), 1)
    return sim if sim >= 0.80 else 0.0


def phrase_in_text(phrase_tokens: list, text_tokens: list) -> float:
    """Fuzzy sequential phrase matching. Returns match ratio 0–1."""
    if not phrase_tokens:
        return 0.0
    matched, t = 0.0, 0
    for pt in phrase_tokens:
        while t < len(text_tokens):
            s = fuzzy_sim(text_tokens[t], pt)
            t += 1
            if s > 0:
                matched += s
                break
    return matched / len(phrase_tokens)


def get_intent(user_input: str) -> str | None:
    """
    Score every intent and return the best match.

    Scoring weights:
      Exact phrase match   → 10 × word_count
      Fuzzy phrase match   →  8 × ratio × word_count   (if ratio ≥ 0.85)
      Exact keyword match  →  2 × word_count
      Fuzzy keyword match  →  1.5 × similarity
    """
    processed  = preprocess(user_input)
    expanded   = apply_synonyms(processed)
    text_toks  = expanded.split()

    best_intent = None
    best_score  = 0.0
>>>>>>> f763b2e (Refactor: clean structure with separate CSS and JS modules)

    for intent, data in KNOWLEDGE_BASE.items():
        score = 0.0

<<<<<<< HEAD
        # ── Phase 1: exact phrase match in expanded text (highest priority)
        for phrase in data.get("phrases", []):
            p = preprocess(phrase)
            p_exp = apply_synonyms(p)
            if p_exp in expanded:
                score += 10 * len(p_exp.split())
                continue
            # ── Phase 2: fuzzy phrase match
            p_tokens = p_exp.split()
            if len(p_tokens) >= 2:
                ratio = fuzzy_phrase_in_text(p_tokens, text_tokens)
                if ratio >= 0.85:           # 85% of phrase tokens matched
                    score += 8 * ratio * len(p_tokens)

        # ── Phase 3: keyword exact match (whole-word)
        for kw in data.get("keywords", []):
            k     = preprocess(kw)
            k_exp = apply_synonyms(k)
            if re.search(r'\b' + re.escape(k_exp) + r'\b', expanded):
                score += 2 * len(k_exp.split())
                continue
            # Phase 4: fuzzy keyword match (single tokens only)
            for t in text_tokens:
                sim = fuzzy_score(t, k_exp)
                if sim >= 0.82 and sim < 1.0:   # avoid double-counting exact
                    score += 1.5 * sim

        if score > best_score:
            best_score = score
=======
        for phrase in data.get("phrases", []):
            p = apply_synonyms(preprocess(phrase))

            if p in expanded:                          # exact phrase
                score += 10 * len(p.split())
                continue

            pt = p.split()
            if len(pt) >= 2:                           # fuzzy phrase
                ratio = phrase_in_text(pt, text_toks)
                if ratio >= 0.85:
                    score += 8 * ratio * len(pt)

        for kw in data.get("keywords", []):
            k = apply_synonyms(preprocess(kw))

            if re.search(r"\b" + re.escape(k) + r"\b", expanded):  # exact kw
                score += 2 * len(k.split())
                continue

            for tok in text_toks:                      # fuzzy keyword
                s = fuzzy_sim(tok, k)
                if 0 < s < 1.0:
                    score += 1.5 * s

        if score > best_score:
            best_score  = score
>>>>>>> f763b2e (Refactor: clean structure with separate CSS and JS modules)
            best_intent = intent

    return best_intent if best_score > 0 else None

<<<<<<< HEAD
# ── Gemini API ────────────────────────────────────────────────────────
GEMINI_API_KEY = ""
GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.0-flash:generateContent?key=" + GEMINI_API_KEY
)

GEMINI_SYSTEM_PROMPT = """You are AcadBot, an academic support chatbot for B.Sc. IT (TY) students at KES' Shroff College, Kandivali (W), Mumbai.

Your knowledge covers:
- Semester V subjects: Network Security, Web Dev Framework, Software Engineering & Agile, Advanced Java, Mobile App Dev, Functional & Reactive Programming, Advanced Database Programming, Figma, Field Project
- Semester VI subjects: Full-Stack Web Dev (MERN), Blockchain, IoT, Software Testing, Spring Boot, Game Programming with Python, AI-Driven Software Development, OJT
- Academic Calendar 2025-26: Term starts June 9 2025, Ganapati vacation Aug 27-31, Diwali vacation Oct 20 - Nov 5, Odd sem exams Oct 8-17, Even sem exams Mar 21 - Apr 4 2026, Results Apr 20 2026
- Attendance: Minimum 75% required, below 75% detained from exams
- Internal marks: 25 total (5 attendance + 10 assignments + 10 unit test)
- Project: Field Project Sem V (2 credits), OJT Sem VI (4 credits)
- Library: 9AM-6PM Mon-Sat, 2 books max, 7 days, Rs 2/day fine

IMPORTANT FORMATTING RULES:
1. Use plain text only — NO markdown asterisks (**), NO hash headers (#), NO backticks
2. Use clean bullet points with • symbol
3. Use clear line breaks between sections
4. Keep responses concise and student-friendly
5. If asked something outside college academics, politely say you only cover academic topics
6. Always respond in English"""

def call_gemini(user_input):
    """Call Gemini API and return clean text response."""
    try:
        payload = {
            "system_instruction": {
                "parts": [{"text": GEMINI_SYSTEM_PROMPT}]
            },
            "contents": [
                {"role": "user", "parts": [{"text": user_input}]}
            ],
            "generationConfig": {
                "temperature": 0.3,
                "maxOutputTokens": 400,
                "topP": 0.8,
            }
        }
        req = urllib.request.Request(
            GEMINI_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=8) as resp:
            result = json.loads(resp.read().decode("utf-8"))
        text = result["candidates"][0]["content"]["parts"][0]["text"].strip()
        # Clean up any residual markdown asterisks or hashes
        text = re.sub(r'\*{1,3}(.*?)\*{1,3}', r'\1', text)
        text = re.sub(r'^#{1,4}\s+', '', text, flags=re.MULTILINE)
        text = re.sub(r'`{1,3}', '', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()
    except Exception as e:
        return None

def get_response(user_input):
    """
    Hybrid response:
    1. Try predefined NLP knowledge base first (fast, accurate for known topics)
    2. If no intent matched → call Gemini for intelligent fallback
    3. If Gemini fails → return friendly error message
    """
    intent = get_intent(user_input)

    # ── Known intent: return predefined response ──
    if intent:
        reply = random.choice(KNOWLEDGE_BASE[intent]["responses"])
        # Strip markdown bold markers from predefined responses for consistency
        clean = re.sub(r'\*\*(.*?)\*\*', r'\1', reply)
        return clean, intent, "predefined"

    # ── Unknown intent: try Gemini ──
    gemini_reply = call_gemini(user_input)
    if gemini_reply:
        return gemini_reply, "gemini", "gemini"

    # ── Both failed: fallback message ──
    fallback = (
        "I couldn't understand your query.\n\n"
        "Try asking things like:\n"
        "• What are Sem 6 subjects?\n"
        "• Tell me about IoT subject\n"
        "• When are the exams?\n"
        "• What is the attendance rule?\n"
        "• Tell me about MERN stack\n"
        "• Show me the academic calendar"
    )
    return fallback, "invalid", "predefined"

# ── Persistent Storage Helpers ────────────────────────────────────────
def load_json(path, default):
    try:
        if os.path.exists(path):
            with open(path, 'r') as f:
=======

INVALID_RESPONSE = (
    "I couldn't understand your query.\n\n"
    "Try asking things like:\n"
    "• What are B.Com subjects?\n"
    "• Tell me about BMS course\n"
    "• What is BAF course?\n"
    "• Sem 6 B.Sc. IT subjects\n"
    "• When are the exams?\n"
    "• Admission process\n"
    "• College fees\n"
    "• Library timings\n\n"
    "Or type 'all courses' to see everything KES Shroff College offers."
)


def get_response(user_input: str) -> tuple:
    """
    Returns (reply_text, intent_name, source)
    source is always 'predefined' since we use no external API.
    """
    intent = get_intent(user_input)

    if intent:
        return KNOWLEDGE_BASE[intent]["response"], intent, "predefined"

    return INVALID_RESPONSE, "invalid", "predefined"


# =============================================================================
#  SECTION 4 — STORAGE HELPERS
#  Simple JSON file read/write. Easy to swap for a database later.
# =============================================================================

def read_json(path: str, default):
    try:
        if os.path.exists(path):
            with open(path) as f:
>>>>>>> f763b2e (Refactor: clean structure with separate CSS and JS modules)
                return json.load(f)
    except Exception:
        pass
    return default

<<<<<<< HEAD
def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

def load_history():
    return load_json(HIST_FILE, {})

def save_history(h):
    save_json(HIST_FILE, h)

def load_stats():
    default = {
        "total_messages": 0,
        "matched": 0,
        "unmatched": 0,
        "intent_counts": {},
        "daily_counts": {},
        "first_use": None,
        "unique_users": [],          # list of session IDs seen
        "user_messages": [],         # list of raw user messages (last 500)
    }
    return load_json(STATS_FILE, default)

def save_stats(s):
    save_json(STATS_FILE, s)

# ── Routes ────────────────────────────────────────────────────────────
=======

def write_json(path: str, data) -> None:
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def load_history() -> dict:
    return read_json(HIST_FILE, {})


def load_stats() -> dict:
    defaults = {
        "total_messages": 0,
        "matched":        0,
        "unmatched":      0,
        "intent_counts":  {},
        "daily_counts":   {},
        "first_use":      None,
        "unique_users":   [],
        "user_messages":  [],
    }
    return read_json(STATS_FILE, defaults)


# =============================================================================
#  SECTION 5 — FLASK ROUTES
# =============================================================================

>>>>>>> f763b2e (Refactor: clean structure with separate CSS and JS modules)
@app.route("/")
def index():
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())
    return render_template("index.html")

<<<<<<< HEAD
=======

>>>>>>> f763b2e (Refactor: clean structure with separate CSS and JS modules)
@app.route("/analytics")
def analytics_page():
    return render_template("analytics.html")

<<<<<<< HEAD
@app.route("/chat", methods=["POST"])
def chat():
=======

@app.route("/chat", methods=["POST"])
def chat():
    """Receive a user message, return bot reply + update history & stats."""
>>>>>>> f763b2e (Refactor: clean structure with separate CSS and JS modules)
    data     = request.get_json()
    user_msg = data.get("message", "").strip()
    if not user_msg:
        return jsonify({"error": "Empty message"}), 400

<<<<<<< HEAD
    sid     = session.get("session_id", str(uuid.uuid4()))
    ts      = datetime.now().strftime("%I:%M %p")
    today   = datetime.now().strftime("%Y-%m-%d")

    # History
    history = load_history()
    if sid not in history:
        history[sid] = []
    history[sid].append({"role": "user", "message": user_msg, "time": ts})

    # Hybrid NLP + Gemini
    bot_reply, intent, source = get_response(user_msg)

    history[sid].append({
        "role": "bot", "message": bot_reply,
        "intent": intent, "source": source, "time": ts
    })
    save_history(history)

    # Analytics
    stats = load_stats()
    if stats["first_use"] is None:
        stats["first_use"] = today
    stats["total_messages"] += 1

    if "unique_users" not in stats:
        stats["unique_users"] = []
    if sid not in stats["unique_users"]:
        stats["unique_users"].append(sid)

    if "user_messages" not in stats:
        stats["user_messages"] = []
=======
    sid   = session.get("session_id", str(uuid.uuid4()))
    ts    = datetime.now().strftime("%I:%M %p")
    today = datetime.now().strftime("%Y-%m-%d")

    # — Save user message to history —
    history = load_history()
    history.setdefault(sid, [])
    history[sid].append({"role": "user", "message": user_msg, "time": ts})

    # — Get bot reply —
    reply, intent, source = get_response(user_msg)
    history[sid].append({"role": "bot", "message": reply,
                          "intent": intent, "source": source, "time": ts})
    write_json(HIST_FILE, history)

    # — Update analytics stats —
    stats = load_stats()
    stats["first_use"] = stats["first_use"] or today
    stats["total_messages"] += 1

    if sid not in stats["unique_users"]:
        stats["unique_users"].append(sid)

>>>>>>> f763b2e (Refactor: clean structure with separate CSS and JS modules)
    stats["user_messages"].append(user_msg)
    if len(stats["user_messages"]) > 500:
        stats["user_messages"] = stats["user_messages"][-500:]

<<<<<<< HEAD
    # Track gemini vs predefined
    if "gemini_count" not in stats:
        stats["gemini_count"] = 0
    if source == "gemini":
        stats["gemini_count"] += 1

    if intent not in ("invalid",):
=======
    if intent != "invalid":
>>>>>>> f763b2e (Refactor: clean structure with separate CSS and JS modules)
        stats["matched"] += 1
        stats["intent_counts"][intent] = stats["intent_counts"].get(intent, 0) + 1
    else:
        stats["unmatched"] += 1
<<<<<<< HEAD
    stats["daily_counts"][today] = stats["daily_counts"].get(today, 0) + 1
    save_stats(stats)

    return jsonify({"reply": bot_reply, "intent": intent, "source": source, "time": ts})

@app.route("/history", methods=["GET"])
def get_history():
    sid     = session.get("session_id", "")
    history = load_history()
    return jsonify({"history": history.get(sid, [])})

@app.route("/clear", methods=["POST"])
def clear():
    sid     = session.get("session_id", "")
    history = load_history()
    history[sid] = []
    save_history(history)
    return jsonify({"status": "cleared"})

@app.route("/api/analytics", methods=["GET"])
def api_analytics():
    from datetime import timedelta
    from collections import Counter

    stats     = load_stats()
    history   = load_history()
    total     = stats["total_messages"]
    matched   = stats["matched"]
    unmatched = stats["unmatched"]
    accuracy  = round((matched / total * 100), 1) if total > 0 else 0

    # Top intents
    top = sorted(stats["intent_counts"].items(), key=lambda x: x[1], reverse=True)[:10]

    # Daily last 7 days
    daily = []
    for i in range(6, -1, -1):
        d = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        daily.append({"date": d, "count": stats["daily_counts"].get(d, 0)})

    # Unique users
    unique_users = len(stats.get("unique_users", []))

    # Most asked questions — top 10 from raw messages
    raw_msgs = stats.get("user_messages", [])
    # normalise: lowercase + strip
    normalised = [m.lower().strip() for m in raw_msgs if m.strip()]
    counter = Counter(normalised)
    most_asked = counter.most_common(10)

    # Sessions = unique session IDs in history file
    sessions = len(history)

    return jsonify({
        "total_messages":  total,
        "matched":         matched,
        "unmatched":       unmatched,
        "accuracy":        accuracy,
        "top_intents":     top,
        "daily":           daily,
        "sessions":        sessions,
        "unique_users":    unique_users,
        "most_asked":      most_asked,
        "first_use":       stats.get("first_use", "N/A"),
        "gemini_count":    stats.get("gemini_count", 0),
    })

=======

    stats["daily_counts"][today] = stats["daily_counts"].get(today, 0) + 1
    write_json(STATS_FILE, stats)

    return jsonify({"reply": reply, "intent": intent, "source": source, "time": ts})


@app.route("/history")
def get_history():
    sid = session.get("session_id", "")
    return jsonify({"history": load_history().get(sid, [])})


@app.route("/clear", methods=["POST"])
def clear_history():
    sid     = session.get("session_id", "")
    history = load_history()
    history[sid] = []
    write_json(HIST_FILE, history)
    return jsonify({"status": "cleared"})


@app.route("/api/analytics")
def api_analytics():
    """Return all analytics data as JSON for the analytics dashboard."""
    stats = load_stats()
    hist  = load_history()

    total    = stats["total_messages"]
    matched  = stats["matched"]
    unmatched= stats["unmatched"]
    accuracy = round(matched / total * 100, 1) if total else 0

    # Top 10 intents by usage
    top_intents = sorted(
        stats["intent_counts"].items(),
        key=lambda x: x[1], reverse=True
    )[:10]

    # Daily message counts for last 7 days
    daily = [
        {
            "date":  (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d"),
            "count": stats["daily_counts"].get(
                        (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d"), 0)
        }
        for i in range(6, -1, -1)
    ]

    # Most asked raw questions (top 10)
    raw_msgs   = stats.get("user_messages", [])
    most_asked = Counter(m.lower().strip() for m in raw_msgs if m.strip()).most_common(10)

    return jsonify({
        "total_messages": total,
        "matched":        matched,
        "unmatched":      unmatched,
        "accuracy":       accuracy,
        "top_intents":    top_intents,
        "daily":          daily,
        "sessions":       len(hist),
        "unique_users":   len(stats.get("unique_users", [])),
        "most_asked":     most_asked,
        "first_use":      stats.get("first_use", "N/A"),
        "gemini_count":   0,   # no Gemini used — pure KB
        "total_intents":  len(KNOWLEDGE_BASE),
    })


# =============================================================================
#  ENTRY POINT
# =============================================================================

>>>>>>> f763b2e (Refactor: clean structure with separate CSS and JS modules)
if __name__ == "__main__":
    app.run(debug=True, port=5000)
