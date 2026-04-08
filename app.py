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
    if len(s1) > 30 or len(s2) > 30:
        return 999
    m, n = len(s1), len(s2)
    dp = list(range(n + 1))
    for i in range(1, m + 1):
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

    for intent, data in KNOWLEDGE_BASE.items():
        score = 0.0

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
            best_intent = intent

    return best_intent if best_score > 0 else None

# ── Gemini API ────────────────────────────────────────────────────────
GEMINI_API_KEY = "AIzaSyDpVOJ1CBwbc1ynsGskpHIeshUK8D6t8uE"
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
                return json.load(f)
    except Exception:
        pass
    return default

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
@app.route("/")
def index():
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())
    return render_template("index.html")

@app.route("/analytics")
def analytics_page():
    return render_template("analytics.html")

@app.route("/chat", methods=["POST"])
def chat():
    data     = request.get_json()
    user_msg = data.get("message", "").strip()
    if not user_msg:
        return jsonify({"error": "Empty message"}), 400

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
    stats["user_messages"].append(user_msg)
    if len(stats["user_messages"]) > 500:
        stats["user_messages"] = stats["user_messages"][-500:]

    # Track gemini vs predefined
    if "gemini_count" not in stats:
        stats["gemini_count"] = 0
    if source == "gemini":
        stats["gemini_count"] += 1

    if intent not in ("invalid",):
        stats["matched"] += 1
        stats["intent_counts"][intent] = stats["intent_counts"].get(intent, 0) + 1
    else:
        stats["unmatched"] += 1
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

if __name__ == "__main__":
    app.run(debug=True, port=5000)
