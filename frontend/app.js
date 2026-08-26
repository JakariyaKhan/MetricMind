/**
 * MetricMind - Conversational BI Client Application
 * Handles real-time SSE streaming, dynamic ECharts rendering,
 * and single-source-of-truth audit drawers ("View SQL" / "View API Call").
 */

let currentModalData = "";
let chartInstances = [];

document.addEventListener("DOMContentLoaded", () => {
    fetchSchemaMetadata();
    fetchTelemetry();
    
    // Auto-resize charts on window resize
    window.addEventListener("resize", () => {
        chartInstances.forEach(c => c.resize());
    });
});

async function fetchTelemetry() {
    try {
        const res = await fetch("/api/audit/stats");
        if (res.ok) {
            const stats = await res.json();
            document.getElementById("statQueries").textContent = stats.queries_processed;
            document.getElementById("statDiagnostics").textContent = stats.secondary_diagnostics_triggered;
        }
    } catch (e) {
        console.error("Error fetching telemetry:", e);
    }
}

async function fetchSchemaMetadata() {
    const explorer = document.getElementById("schemaExplorer");
    try {
        const res = await fetch("/api/semantic/meta");
        const data = await res.json();
        
        let html = "";
        (data.cubes || []).forEach(cube => {
            html += `
            <div class="cube-node">
                <div class="cube-header">
                    <span><i class="fa-solid fa-cube text-blue"></i> ${cube.name}</span>
                    <span class="member-type">${cube.measures.length}M / ${cube.dimensions.length}D</span>
                </div>
                <div class="cube-content">
                    <div style="font-size:0.7rem; color:var(--text-muted); margin-bottom:4px; font-weight:600;">MEASURES:</div>
                    ${cube.measures.map(m => `
                        <div class="member-row">
                            <span class="member-name text-green">${m.name}</span>
                            <span class="member-type">${m.format || m.type}</span>
                        </div>
                    `).join('')}
                    <div style="font-size:0.7rem; color:var(--text-muted); margin:6px 0 4px 0; font-weight:600;">DIMENSIONS:</div>
                    ${cube.dimensions.map(d => `
                        <div class="member-row">
                            <span class="member-name text-blue">${d.name}</span>
                            <span class="member-type">${d.type}</span>
                        </div>
                    `).join('')}
                </div>
            </div>
            `;
        });
        explorer.innerHTML = html;
    } catch (e) {
        explorer.innerHTML = `<div style="color:var(--color-red); padding:10px;">Failed to load schema catalog</div>`;
    }
}

function sendPrompt(text) {
    const input = document.getElementById("queryInput");
    input.value = text;
    document.getElementById("chatForm").dispatchEvent(new Event("submit", { cancelable: true }));
}

async function handleChatSubmit(e) {
    e.preventDefault();
    const input = document.getElementById("queryInput");
    const query = input.value.trim();
    if (!query) return;

    input.value = "";
    appendUserMessage(query);

    // Create assistant placeholder card
    const cardId = "msg-" + Date.now();
    const assistantCard = appendAssistantPlaceholder(cardId);
    const bodyContainer = assistantCard.querySelector(".message-markdown");
    const statusContainer = assistantCard.querySelector(".status-stream");

    try {
        const response = await fetch("/api/chat/stream", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query: query, stream: true })
        });

        if (!response.ok) {
            throw new Error(`Server returned HTTP ${response.status}`);
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let accumulatedText = "";
        let finalPayload = null;

        while (true) {
            const { value, done } = await reader.read();
            if (done) break;

            const rawChunk = decoder.decode(value);
            const lines = rawChunk.split("\n");

            for (const line of lines) {
                if (line.startsWith("data: ")) {
                    try {
                        const eventData = JSON.parse(line.slice(6));
                        
                        if (eventData.type === "status") {
                            statusContainer.innerHTML = `<i class="fa-solid fa-spinner fa-spin text-blue"></i> <em>${eventData.content}</em>`;
                            statusContainer.style.display = "block";
                        } else if (eventData.type === "token") {
                            statusContainer.style.display = "none";
                            accumulatedText += eventData.content;
                            bodyContainer.innerHTML = marked.parse(accumulatedText);
                            scrollToBottom();
                        } else if (eventData.type === "complete") {
                            finalPayload = eventData.payload;
                        }
                    } catch (err) {
                        // ignore malformed JSON chunk
                    }
                }
            }
        }

        if (finalPayload) {
            renderPayloadVisuals(assistantCard, finalPayload);
        }
        fetchTelemetry();

    } catch (err) {
        bodyContainer.innerHTML = `<div style="color:var(--color-red);"><i class="fa-solid fa-triangle-exclamation"></i> Error querying Semantic BI Engine: ${err.message}</div>`;
    }
}

function appendUserMessage(text) {
    const viewport = document.getElementById("messagesViewport");
    const card = document.createElement("div");
    card.className = "message-card user-card";
    card.innerHTML = `<div class="user-bubble">${escapeHtml(text)}</div>`;
    viewport.appendChild(card);
    scrollToBottom();
}

function appendAssistantPlaceholder(id) {
    const viewport = document.getElementById("messagesViewport");
    const card = document.createElement("div");
    card.className = "message-card assistant-card";
    card.id = id;
    card.innerHTML = `
        <div class="agent-avatar"><i class="fa-solid fa-brain-circuit"></i></div>
        <div class="message-body">
            <div class="agent-name">
                MetricMind Governed Engine
                <span class="governance-tag"><i class="fa-solid fa-lock"></i> Cube.dev Governed</span>
            </div>
            <div class="status-stream" style="font-size:0.8rem; color:var(--text-muted); margin-bottom:8px;">
                <i class="fa-solid fa-spinner fa-spin text-blue"></i> Connecting to Semantic Layer...
            </div>
            <div class="message-markdown"></div>
            <div class="charts-container"></div>
            <div class="audit-actions-bar" style="display:none;"></div>
        </div>
    `;
    viewport.appendChild(card);
    scrollToBottom();
    return card;
}

function renderPayloadVisuals(card, payload) {
    const chartsContainer = card.querySelector(".charts-container");
    const auditBar = card.querySelector(".audit-actions-bar");

    // 1. Render Apache ECharts
    if (payload.charts && payload.charts.length > 0) {
        chartsContainer.innerHTML = "";
        payload.charts.forEach((chartConfig, idx) => {
            const chartDiv = document.createElement("div");
            chartDiv.className = "chart-card";
            const echartId = "echart-" + Date.now() + "-" + idx;
            
            chartDiv.innerHTML = `
                <div class="chart-title"><i class="fa-solid fa-chart-line text-blue"></i> ${chartConfig.title}</div>
                <div class="echart-instance" id="${echartId}"></div>
            `;
            chartsContainer.appendChild(chartDiv);

            // Initialize ECharts instance
            setTimeout(() => {
                const chartDom = document.getElementById(echartId);
                if (chartDom) {
                    const myChart = echarts.init(chartDom, 'dark', { backgroundColor: 'transparent' });
                    myChart.setOption(chartConfig.option);
                    chartInstances.push(myChart);
                }
            }, 50);
        });
    }

    // 2. Build Transparency Modals ("View SQL" & "View API Call")
    if (payload.steps && payload.steps.length > 0) {
        auditBar.style.display = "flex";
        auditBar.innerHTML = "";

        payload.steps.forEach((step, idx) => {
            // View SQL Button
            const sqlBtn = document.createElement("button");
            sqlBtn.className = "btn-audit";
            sqlBtn.innerHTML = `<i class="fa-solid fa-terminal text-blue"></i> View SQL (Step ${idx+1})`;
            sqlBtn.onclick = () => openModal(`Compiled Snowflake/Lakehouse SQL (Step ${idx+1})`, step.compiled_sql);
            auditBar.appendChild(sqlBtn);

            // View API Call Button
            const apiBtn = document.createElement("button");
            apiBtn.className = "btn-audit";
            apiBtn.innerHTML = `<i class="fa-solid fa-code text-green"></i> View Cube API Payload (Step ${idx+1})`;
            apiBtn.onclick = () => openModal(`Cube.dev REST API Payload (Step ${idx+1})`, JSON.stringify(step.cube_query, null, 2));
            auditBar.appendChild(apiBtn);
        });
    }
    scrollToBottom();
}

function openModal(title, code) {
    document.getElementById("modalTitle").innerHTML = `<i class="fa-solid fa-file-code text-blue"></i> ${title}`;
    document.getElementById("modalCode").textContent = code;
    currentModalData = code;
    document.getElementById("auditModal").classList.add("open");
}

function closeModal(e) {
    document.getElementById("auditModal").classList.remove("open");
}

function copyModalCode() {
    navigator.clipboard.writeText(currentModalData).then(() => {
        alert("Copied to clipboard!");
    });
}

function scrollToBottom() {
    const vp = document.getElementById("messagesViewport");
    vp.scrollTop = vp.scrollHeight;
}

function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}
