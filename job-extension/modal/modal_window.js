
showLoadingModal = function () {
    document.getElementById("ai-loading-toast")?.remove();

    document.body.insertAdjacentHTML("beforeend", `
        <div id="ai-loading-toast" style="
            position: fixed;
            bottom: 20px;
            left: 20px;
            z-index: 999999;
            background: #fff;
            padding: 18px 24px;
            border-left: 5px solid #0073b1;
            border-radius: 12px;
            box-shadow: 0 8px 24px rgba(0,0,0,.2);
            font: 600 18px Arial, sans-serif;
        ">
            🤖 Analyzing Job...
        </div>
    `);
};



function showAnalysisModal() {
    document.getElementById("ai-loading-toast")?.remove();
    document.getElementById("ai-modal")?.remove();

    document.body.insertAdjacentHTML("beforeend", `
        <div id="ai-modal" style="
            position: fixed;
            inset: 0;
            z-index: 999999;
            background: rgba(0, 0, 0, 0.55);
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        ">
            <div id="ai-modal-content" style="
                position: relative;
                width: min(700px, 95vw);
                max-height: 85vh;
                overflow-y: auto;
                background: white;
                border-radius: 16px;
                padding: 28px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.35);
                font-family: Arial, sans-serif;
            ">
                <button id="ai-modal-close" style="
                    position: absolute;
                    top: 12px;
                    right: 14px;
                    border: none;
                    background: transparent;
                    font-size: 28px;
                    cursor: pointer;
                    color: #444;
                ">
                    ×
                </button>

                <h2 style="
                    margin: 0 40px 20px 0;
                    color: #0073b1;
                    font-size: 26px;
                ">
                    🤖 AI Job Analysis
                </h2>

                <pre id="ai-stream-output" style="
                    margin: 0;
                    white-space: pre-wrap;
                    overflow-wrap: anywhere;
                    font-family: Arial, sans-serif;
                    font-size: 18px;
                    line-height: 1.6;
                    color: #222;
                "></pre>

                <div id="ai-processing-time" style="
                    margin-top: 22px;
                    padding-top: 15px;
                    border-top: 1px solid #ddd;
                    font-size: 15px;
                    color: #666;
                ">
                    Generating analysis...
                </div>
            </div>
        </div>
    `);

    const modal = document.getElementById("ai-modal");
    const closeButton =
        document.getElementById("ai-modal-close");

    closeButton?.addEventListener("click", () => {
        modal?.remove();
    });

    modal?.addEventListener("click", event => {
        if (event.target === modal) {
            modal.remove();
        }
    });
}