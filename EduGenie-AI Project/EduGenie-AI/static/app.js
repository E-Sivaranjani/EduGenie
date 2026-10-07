/* =====================================================
   EDUGENIE FRONTEND
   Connects frontend with FastAPI backend
===================================================== */


/* =====================================================
   ELEMENTS
===================================================== */

const taskCards =
    document.querySelectorAll(".task-card");

const mainInput =
    document.getElementById("mainInput");

const contextInput =
    document.getElementById("context");

const levelSelect =
    document.getElementById("level");

const questionCount =
    document.getElementById("questionCount");

const weeksSelect =
    document.getElementById("weeks");

const submitButton =
    document.getElementById("submitButton");

const submitText =
    document.getElementById("submitText");

const loadingSpinner =
    document.getElementById("loadingSpinner");

const clearButton =
    document.getElementById("clearButton");

const resultSection =
    document.getElementById("resultSection");

const resultContainer =
    document.getElementById("resultContainer");

const resultTitle =
    document.getElementById("resultTitle");

const errorMessage =
    document.getElementById("errorMessage");

const errorText =
    document.getElementById("errorText");

const copyButton =
    document.getElementById("copyButton");

const characterCount =
    document.getElementById("characterCount");

const inputTitle =
    document.getElementById("inputTitle");

const inputDescription =
    document.getElementById("inputDescription");

const inputLabel =
    document.getElementById("inputLabel");

const questionCountGroup =
    document.getElementById("questionCountGroup");

const weeksGroup =
    document.getElementById("weeksGroup");

const contextGroup =
    document.getElementById("contextGroup");


/* =====================================================
   CURRENT TASK
===================================================== */

let currentTask = "qa";


/* =====================================================
   TASK INFORMATION
===================================================== */

const taskInformation = {

    qa: {

        title: "Ask your question",

        description:
            "Ask EduGenie anything about your studies.",

        label:
            "Your Question",

        placeholder:
            "Example: What is photosynthesis?",

        button:
            "Ask EduGenie",

        resultTitle:
            "Answer"

    },


    explain: {

        title:
            "Explain a concept",

        description:
            "Get a simple explanation of a difficult topic.",

        label:
            "Topic",

        placeholder:
            "Example: Explain Object-Oriented Programming",

        button:
            "Explain Concept",

        resultTitle:
            "Explanation"

    },


    quiz: {

        title:
            "Generate a quiz",

        description:
            "Paste study material and create multiple-choice questions.",

        label:
            "Study Material",

        placeholder:
            "Paste your study material here...",

        button:
            "Generate Quiz",

        resultTitle:
            "Generated Quiz"

    },


    summary: {

        title:
            "Summarize study material",

        description:
            "Convert long study material into simple revision notes.",

        label:
            "Study Material",

        placeholder:
            "Paste the text you want to summarize...",

        button:
            "Summarize",

        resultTitle:
            "Summary"

    },


    "learning-path": {

        title:
            "Create a learning path",

        description:
            "Create a personalized roadmap for learning a topic.",

        label:
            "Learning Topic",

        placeholder:
            "Example: Machine Learning",

        button:
            "Create Learning Path",

        resultTitle:
            "Personalized Learning Path"

    }

};


/* =====================================================
   SELECT TASK
===================================================== */

taskCards.forEach((card) => {

    card.addEventListener("click", () => {

        const task =
            card.dataset.task;

        selectTask(task);

    });

});


function selectTask(task) {

    currentTask = task;


    /* Remove active state */

    taskCards.forEach((card) => {

        card.classList.remove("active");

    });


    /* Add active state */

    const selectedCard =
        document.querySelector(
            `.task-card[data-task="${task}"]`
        );

    if (selectedCard) {

        selectedCard.classList.add("active");

    }


    /* Get information */

    const information =
        taskInformation[task];


    inputTitle.textContent =
        information.title;

    inputDescription.textContent =
        information.description;

    inputLabel.textContent =
        information.label;

    mainInput.placeholder =
        information.placeholder;

    submitText.textContent =
        information.button;


    /* Hide optional controls */

    questionCountGroup.style.display =
        "none";

    weeksGroup.style.display =
        "none";

    contextGroup.style.display =
        "none";


    /* Quiz */

    if (task === "quiz") {

        questionCountGroup.style.display =
            "block";

    }


    /* Learning Path */

    if (task === "learning-path") {

        weeksGroup.style.display =
            "block";

    }


    /* Explanation */

    if (task === "explain") {

        contextGroup.style.display =
            "block";

    }


    /* Reset old result */

    hideResult();

    hideError();

}


/* =====================================================
   CHARACTER COUNT
===================================================== */

mainInput.addEventListener(
    "input",
    () => {

        characterCount.textContent =
            mainInput.value.length;

    }
);


/* =====================================================
   CLEAR
===================================================== */

clearButton.addEventListener(
    "click",
    () => {

        mainInput.value = "";

        contextInput.value = "";

        characterCount.textContent = "0";

        hideResult();

        hideError();

    }
);


/* =====================================================
   SUBMIT
===================================================== */

submitButton.addEventListener(
    "click",
    handleSubmit
);


async function handleSubmit() {

    hideError();


    const input =
        mainInput.value.trim();


    /* Validate input */

    if (!input) {

        showError(
            "Please enter some content before submitting."
        );

        mainInput.focus();

        return;

    }


    /* Start loading */

    setLoading(true);


    try {

        let result;


        /* =============================================
           Q&A
        ============================================= */

        if (currentTask === "qa") {

            result =
                await callAPI(
                    "/qa",
                    {
                        question: input,

                        level:
                            levelSelect.value
                    }
                );

            displayTextResult(
                result.result,

                "Answer"
            );

        }


        /* =============================================
           EXPLAIN
        ============================================= */

        else if (currentTask === "explain") {

            result =
                await callAPI(
                    "/explain",
                    {
                        topic: input,

                        level:
                            levelSelect.value,

                        context:
                            contextInput.value.trim()
                    }
                );

            displayTextResult(
                result.result,

                "Explanation"
            );

        }


        /* =============================================
           QUIZ
        ============================================= */

        else if (currentTask === "quiz") {

            if (input.length < 20) {

                throw new Error(
                    "Please enter at least 20 characters of study material."
                );

            }


            result =
                await callAPI(
                    "/quiz",
                    {
                        text: input,

                        level:
                            levelSelect.value,

                        question_count:
                            Number(
                                questionCount.value
                            )
                    }
                );


            displayQuiz(result);

        }


        /* =============================================
           SUMMARY
        ============================================= */

        else if (currentTask === "summary") {

            if (input.length < 30) {

                throw new Error(
                    "Please enter at least 30 characters of study material."
                );

            }


            result =
                await callAPI(
                    "/summarize",
                    {
                        text: input,

                        level:
                            levelSelect.value,

                        max_words: 120
                    }
                );


            displayTextResult(
                result.result,

                "Summary"
            );

        }


        /* =============================================
           LEARNING PATH
        ============================================= */

        else if (
            currentTask === "learning-path"
        ) {

            result =
                await callAPI(
                    "/learn/recommendations",
                    {
                        topic: input,

                        level:
                            levelSelect.value,

                        weeks:
                            Number(
                                weeksSelect.value
                            )
                    }
                );


            displayLearningPath(result);

        }

    }

    catch (error) {

        console.error(error);

        showError(
            error.message ||
            "Unable to process your request."
        );

    }

    finally {

        setLoading(false);

    }

}


/* =====================================================
   API CALL
===================================================== */

async function callAPI(
    endpoint,
    data
) {

    const response =
        await fetch(
            endpoint,
            {

                method: "POST",

                headers: {

                    "Content-Type":
                        "application/json"

                },

                body:
                    JSON.stringify(data)

            }
        );


    let responseData;


    try {

        responseData =
            await response.json();

    }

    catch {

        throw new Error(
            "The server returned an invalid response."
        );

    }


    if (!response.ok) {

        let message =
            "Request failed.";

        if (
            responseData &&
            responseData.detail
        ) {

            if (
                Array.isArray(
                    responseData.detail
                )
            ) {

                message =
                    responseData.detail
                        .map(
                            item =>
                                item.msg
                        )
                        .join(", ");

            }

            else {

                message =
                    responseData.detail;

            }

        }

        throw new Error(message);

    }


    return responseData;

}


/* =====================================================
   DISPLAY TEXT RESULT
===================================================== */

function displayTextResult(
    text,
    title
) {

    resultTitle.textContent =
        title;


    resultContainer.innerHTML = "";


    const resultText =
        document.createElement("div");

    resultText.className =
        "result-text";


    resultText.textContent =
        text;


    resultContainer.appendChild(
        resultText
    );


    showResult();

}


/* =====================================================
   DISPLAY QUIZ
===================================================== */

function displayQuiz(data) {

    resultTitle.textContent =
        "Generated Quiz";


    resultContainer.innerHTML = "";


    if (
        !data.questions ||
        !Array.isArray(data.questions)
    ) {

        throw new Error(
            "Invalid quiz response received."
        );

    }


    const quizWrapper =
        document.createElement("div");

    quizWrapper.className =
        "quiz-wrapper";


    data.questions.forEach(
        (question, index) => {

            const questionBox =
                document.createElement("div");

            questionBox.className =
                "quiz-question";


            /* Number */

            const number =
                document.createElement("div");

            number.className =
                "quiz-number";

            number.textContent =
                `Question ${index + 1}`;


            /* Question */

            const questionTitle =
                document.createElement("div");

            questionTitle.className =
                "quiz-question-title";

            questionTitle.textContent =
                question.question;


            /* Options */

            const options =
                document.createElement("div");

            options.className =
                "quiz-options";


            question.options.forEach(
                (option) => {

                    const optionElement =
                        document.createElement("div");

                    optionElement.className =
                        "quiz-option";


                    if (
                        option ===
                        question.correct_answer
                    ) {

                        optionElement.classList.add(
                            "correct-answer"
                        );

                    }


                    optionElement.textContent =
                        option;


                    options.appendChild(
                        optionElement
                    );

                }
            );


            /* Explanation */

            const explanation =
                document.createElement("div");

            explanation.className =
                "quiz-explanation";


            const explanationLabel =
                document.createElement("strong");

            explanationLabel.textContent =
                "Explanation: ";


            const explanationText =
                document.createTextNode(
                    question.explanation
                );


            explanation.appendChild(
                explanationLabel
            );

            explanation.appendChild(
                explanationText
            );


            /* Add everything */

            questionBox.appendChild(
                number
            );

            questionBox.appendChild(
                questionTitle
            );

            questionBox.appendChild(
                options
            );

            questionBox.appendChild(
                explanation
            );


            quizWrapper.appendChild(
                questionBox
            );

        }
    );


    resultContainer.appendChild(
        quizWrapper
    );


    showResult();

}


/* =====================================================
   DISPLAY LEARNING PATH
===================================================== */

function displayLearningPath(
    data
) {

    resultTitle.textContent =
        "Personalized Learning Path";


    resultContainer.innerHTML = "";


    /* Topic heading */

    const topicHeading =
        document.createElement("h3");

    topicHeading.textContent =
        `${data.topic} - ${data.weeks} Weeks`;


    resultContainer.appendChild(
        topicHeading
    );


    /* Roadmap */

    const roadmap =
        document.createElement("div");

    roadmap.className =
        "learning-roadmap";


    if (
        data.roadmap &&
        Array.isArray(data.roadmap)
    ) {

        data.roadmap.forEach(
            (item) => {

                const roadmapItem =
                    document.createElement("div");

                roadmapItem.className =
                    "roadmap-item";


                /* Stage */

                const stage =
                    document.createElement("div");

                stage.className =
                    "roadmap-stage";

                stage.textContent =
                    item.stage;


                /* Duration */

                const duration =
                    document.createElement("span");

                duration.className =
                    "roadmap-duration";

                duration.textContent =
                    item.duration;


                /* Topics */

                const topicsTitle =
                    document.createElement("h4");

                topicsTitle.textContent =
                    "Topics";


                const topicsList =
                    document.createElement("ul");


                if (
                    Array.isArray(item.topics)
                ) {

                    item.topics.forEach(
                        topic => {

                            const li =
                                document.createElement("li");

                            li.textContent =
                                topic;

                            topicsList.appendChild(
                                li
                            );

                        }
                    );

                }


                /* Resources */

                const resourcesTitle =
                    document.createElement("h4");

                resourcesTitle.textContent =
                    "Resources";


                const resourcesList =
                    document.createElement("ul");


                if (
                    Array.isArray(
                        item.resources
                    )
                ) {

                    item.resources.forEach(
                        resource => {

                            const li =
                                document.createElement("li");

                            li.textContent =
                                resource;

                            resourcesList.appendChild(
                                li
                            );

                        }
                    );

                }


                /* Practice */

                const practiceTitle =
                    document.createElement("h4");

                practiceTitle.textContent =
                    "Practice";


                const practice =
                    document.createElement("p");

                practice.textContent =
                    item.practice;


                /* Add */

                roadmapItem.appendChild(
                    stage
                );

                roadmapItem.appendChild(
                    duration
                );

                roadmapItem.appendChild(
                    topicsTitle
                );

                roadmapItem.appendChild(
                    topicsList
                );

                roadmapItem.appendChild(
                    resourcesTitle
                );

                roadmapItem.appendChild(
                    resourcesList
                );

                roadmapItem.appendChild(
                    practiceTitle
                );

                roadmapItem.appendChild(
                    practice
                );


                roadmap.appendChild(
                    roadmapItem
                );

            }
        );

    }


    resultContainer.appendChild(
        roadmap
    );


    /* Study tips */

    if (
        data.study_tips &&
        Array.isArray(data.study_tips)
    ) {

        const tips =
            document.createElement("div");

        tips.className =
            "study-tips";


        const title =
            document.createElement("h3");

        title.textContent =
            "Study Tips";


        const list =
            document.createElement("ul");


        data.study_tips.forEach(
            tip => {

                const li =
                    document.createElement("li");

                li.textContent =
                    tip;

                list.appendChild(
                    li
                );

            }
        );


        tips.appendChild(
            title
        );

        tips.appendChild(
            list
        );


        resultContainer.appendChild(
            tips
        );

    }


    showResult();

}


/* =====================================================
   SHOW RESULT
===================================================== */

function showResult() {

    resultSection.style.display =
        "block";


    resultSection.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });

}


/* =====================================================
   HIDE RESULT
===================================================== */

function hideResult() {

    resultSection.style.display =
        "none";

    resultContainer.innerHTML =
        "";

}


/* =====================================================
   ERROR
===================================================== */

function showError(message) {

    errorText.textContent =
        message;

    errorMessage.style.display =
        "block";


    errorMessage.scrollIntoView({
        behavior: "smooth",
        block: "center"
    });

}


function hideError() {

    errorMessage.style.display =
        "none";

    errorText.textContent =
        "";

}


/* =====================================================
   LOADING
===================================================== */

function setLoading(isLoading) {

    submitButton.disabled =
        isLoading;


    if (isLoading) {

        loadingSpinner.style.display =
            "inline-block";

        submitText.textContent =
            "Generating...";

    }

    else {

        loadingSpinner.style.display =
            "none";

        submitText.textContent =
            taskInformation[
                currentTask
            ].button;

    }

}


/* =====================================================
   COPY RESULT
===================================================== */

copyButton.addEventListener(
    "click",
    async () => {

        try {

            const text =
                resultContainer.innerText;


            await navigator.clipboard.writeText(
                text
            );


            copyButton.textContent =
                "✓ Copied";


            setTimeout(
                () => {

                    copyButton.textContent =
                        "📋 Copy";

                },
                1500
            );

        }

        catch (error) {

            console.error(error);

            showError(
                "Unable to copy the result."
            );

        }

    }
);


/* =====================================================
   INITIALIZE
===================================================== */

selectTask("qa");