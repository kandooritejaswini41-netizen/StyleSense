document.getElementById("uploadForm").onsubmit = async function(e) {
    e.preventDefault();

    const formData = new FormData(this);

    const res = await fetch("/analyze", {
        method: "POST",
        body: formData
    });

    const data = await res.json();

    document.getElementById("result").innerHTML = `
        <h3>Skin Tone: ${data.skin_tone}</h3>
        <p>RGB: ${data.rgb}</p>
        <pre>${data.recommendations}</pre>
    `;
};
