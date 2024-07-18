document.getElementById('tts-form').addEventListener('submit', async function (e) {
    e.preventDefault();
    const text = document.getElementById('text-input').value;
    
    const response = await fetch('/tts', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text })
    });

    if (response.ok) {
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        const audio = document.getElementById('audio');
        audio.src = url;
        audio.play();
    } else {
        console.error('Failed to generate speech');
    }
});
