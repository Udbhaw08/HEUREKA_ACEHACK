const ELEVEN_API_KEY = import.meta.env.VITE_ELEVEN_API_KEY;
const VOICE_ID = "21m00Tcm4TlvDq8ikWAM"; // Rachel - Professional/Calm

export async function generateVoice(text) {
    if (!ELEVEN_API_KEY) {
        console.error("ElevenLabs API Key Missing");
        return null;
    }

    try {
        const response = await fetch(
            `https://api.elevenlabs.io/v1/text-to-speech/${VOICE_ID}`,
            {
                method: "POST",
                headers: {
                    "xi-api-key": ELEVEN_API_KEY,
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    text: text,
                    model_id: "eleven_multilingual_v2",
                    voice_settings: {
                        stability: 0.5,
                        similarity_boost: 0.75,
                    }
                }),
            }
        );

        if (!response.ok) {
            throw new Error(`ElevenLabs API error: ${response.statusText}`);
        }

        const audioBlob = await response.blob();
        return URL.createObjectURL(audioBlob);
    } catch (error) {
        console.error("Error generating voice:", error);
        return null;
    }
}
