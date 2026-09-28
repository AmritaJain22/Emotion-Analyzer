async function analyzeEmotion() {

    // =====================================================
    // GET ELEMENTS
    // =====================================================

    const textInput =
        document.getElementById("textInput");

    const result =
        document.getElementById("result");

    const error =
        document.getElementById("error");

    const loading =
        document.getElementById("loading");

    const button =
        document.getElementById("analyzeButton");


    // =====================================================
    // GET TEXT
    // =====================================================

    const text =
        textInput.value.trim();


    // =====================================================
    // RESET
    // =====================================================

    result.classList.add("hidden");

    error.classList.add("hidden");


    // =====================================================
    // EMPTY INPUT CHECK
    // =====================================================

    if (!text) {

        error.textContent =
            "Please enter some text first.";

        error.classList.remove(
            "hidden"
        );

        return;
    }


    // =====================================================
    // SHOW LOADING
    // =====================================================

    loading.classList.remove(
        "hidden"
    );

    button.disabled = true;

    button.textContent =
        "Analyzing...";


    try {

        // =================================================
        // SEND REQUEST TO FASTAPI
        // =================================================

        const response =
            await fetch(
                "https://emotion-analyzer-nw3m.onrender.com/predict",
                {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        text: text
                    })

                }
            );


        // =================================================
        // CONVERT RESPONSE TO JSON
        // =================================================

        const data =
            await response.json();


        // =================================================
        // HIDE LOADING
        // =================================================

        loading.classList.add(
            "hidden"
        );

        button.disabled = false;

        button.textContent =
            "Analyze Emotion";


        // =================================================
        // ERROR RESPONSE
        // =================================================

        if (!response.ok) {

            throw new Error(
                "Server error"
            );

        }


        if (!data.success) {

            error.textContent =
                data.message;

            error.classList.remove(
                "hidden"
            );

            return;
        }


        // =================================================
        // DISPLAY EMOTION
        // =================================================

        document.getElementById(
            "emotion"
        ).textContent =
            data.emotion;


        // =================================================
        // DISPLAY CONFIDENCE
        // =================================================

        document.getElementById(
            "confidence"
        ).textContent =
            data.confidence;


        // =================================================
        // UPDATE PROGRESS BAR
        // =================================================

        document.getElementById(
            "progressBar"
        ).style.width =
            data.confidence + "%";


        // =================================================
        // DISPLAY PROCESSED TEXT
        // =================================================

        document.getElementById(
            "cleanedText"
        ).textContent =
            data.cleaned_text;


        // =================================================
        // SHOW RESULT
        // =================================================

        result.classList.remove(
            "hidden"
        );


    } catch (err) {

        // =================================================
        // HIDE LOADING
        // =================================================

        loading.classList.add(
            "hidden"
        );

        button.disabled = false;

        button.textContent =
            "Analyze Emotion";


        // =================================================
        // SHOW ERROR
        // =================================================

        error.textContent =
            "Unable to connect to the server. Please make sure FastAPI is running.";

        error.classList.remove(
            "hidden"
        );


        console.error(err);

    }

}
