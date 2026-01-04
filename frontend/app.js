const API = "";
let sid = null;

const MOODS = {
    welcome: "Greetings, seeker. I am the SkillPath Oracle. To find your destiny, I must first understand your baseline...",
    thinking: ["Fascinating logic...", "Scanning potential futures...", "A pattern emerges in your data...", "Calculating career trajectory...", "The ether responds to your choice..."],
    end: "The calculation is absolute. Behold your path."
};

function type(text, id) {
    const el = document.getElementById(id);
    if (!el) return;
    el.innerHTML = "";
    let i = 0;
    const speed = 15;
    
    function writer() {
        if (i < text.length) {
            el.innerHTML += text.charAt(i);
            i++;
            setTimeout(writer, speed);
        }
    }
    writer();
}

function showSetup() {
    // Hide Domain, Show Setup
    document.getElementById("domain-screen").classList.add("hidden");
    document.getElementById("setup-screen").classList.remove("hidden");
    
    // Trigger Character Message
    type(MOODS.welcome, "oracle-msg-setup");
}

async function start(level) {
    try {
        const res = await fetch(`${API}/start`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ familiarity: level })
        });
        const data = await res.json();
        sid = data.session_id;
        
        document.getElementById("setup-screen").classList.add("hidden");
        document.getElementById("quiz-screen").classList.remove("hidden");
        
        processStep(data.next_question);
    } catch (e) {
        alert("Connection Error: Is the FastAPI server running?");
    }
}

function processStep(step) {
    if (step.type === "result") {
        showResult(step);
        return;
    }

    // AI Personality Reaction
    const moodText = MOODS.thinking[Math.floor(Math.random() * MOODS.thinking.length)];
    type(`${moodText} \n\n ${step.question}`, "q-text");

    const container = document.getElementById("btns");
    container.innerHTML = "";
    
    // Scale Labels
    const labels = step.options[1] === 1 ? ["No", "Yes"] : ["No", "Somewhat", "Definitely"];
    
    labels.forEach((text, i) => {
        const btn = document.createElement("button");
        btn.className = "action-btn";
        btn.innerHTML = `<strong>${text}</strong>`;
        btn.onclick = () => submitAnswer(step.feature, i);
        container.appendChild(btn);
    });
}

async function submitAnswer(feature, value) {
    const res = await fetch(`${API}/submit`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ session_id: sid, feature, value })
    });
    const data = await res.json();
    processStep(data);
}

function showResult(data) {
    document.getElementById("quiz-screen").classList.add("hidden");
    document.getElementById("result-screen").classList.remove("hidden");
    
    const podium = document.getElementById("podium");
    podium.innerHTML = data.top_matches.map((m, i) => `
        <div class="result-item rank-${i}">
            <div class="result-info">
                <span class="rank-tag">${m.rank_label}</span>
                <div class="career-name">${m.career}</div>
            </div>
            <div class="conf-percent">${m.confidence}%</div>
        </div>
    `).join("");

    document.getElementById("reasons-list").innerHTML = data.reasons.map(r => `
        <div class="reason-bullet">✦ ${r}</div>
    `).join("");
}