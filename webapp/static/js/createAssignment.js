window.addEventListener('load', () => {
    let questionsContainer = document.getElementById('questions'),
        addQuestionButton = document.getElementById('add-question'),
        tQuestion = Handlebars.compile(document.getElementById('question-template').innerHTML),
        tAnswer = Handlebars.compile(document.getElementById('answer-template').innerHTML),
        questions = [],
        nextIndex = 0;

    addQuestionButton.onclick = () => {
        nextIndex++;
        addQuestion(nextIndex);
    };

    addQuestion(0);

    function updateDebug() {
        document.getElementById('questionsDebug').textContent = JSON.stringify(questions);
    }

    function getQuestionIndex(e) {
        return parseInt(e.target.closest('.question').dataset.index);
    }

    function addQuestion(index) {
        let question = document.createElement('div');
        question.classList.add('box', 'columns', 'is-vcentered', 'question');
        question.dataset.index = index;
        let apparentPosition = questions.filter(x => x !== null).length + 1;
        question.innerHTML = tQuestion({n: apparentPosition, index});
        questionsContainer.appendChild(question);

        questions[index] = {question: '', answers: [], correct_answer: 0};

        document.getElementById(`question${index}`).onkeyup = questionTextChanged;
        document.getElementById(`delQ${index}`).onclick = deleteQuestion;

        updateDebug();
    }

    function questionTextChanged(e) {
        questions[getQuestionIndex(e)].question = e.target.value;
        updateDebug();
    }

    function deleteQuestion(e) {
        // confirm modal?
        questions[getQuestionIndex(e)] = null;
        let el = e.target.closest('.question');
        el.parentNode.removeChild(el);
        updateDebug();
    }
}, false);
