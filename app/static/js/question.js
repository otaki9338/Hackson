import { CameraHandler } from "./cameraHandler.js";

class Questionnaire {
    constructor(standardQuestions, customQuestionsNum, groupName, showStandardQuestions, customQuestionChoices) {
        this.standardQuestions = standardQuestions; // 質問の配列
        this.standardQuestionNum = standardQuestions.length; // 質問の数
        this.standardQuestionsInput = new Array(this.standardQuestionNum); // 入力された値を保持する配列(質問の数で固定)
        this.customQuestionsNum = customQuestionsNum; // 追加質問の数
        this.customQuestions = new Array(customQuestionsNum); // 追加質問の配列（質問数で固定）
        this.customQuestionsInput = new Array(customQuestionsNum); // 追加質問の入力値を保持する配列
        this.groupName = groupName; // グループ名
        this.showStandardQuestions = showStandardQuestions; // 表示する質問の配列
        this.customQuestionChoices = customQuestionChoices; // 追加質問の配列
        this.customQuestionSelected = Array(customQuestionChoices.length).fill(false); // 追加質問が選択されたかどうかを保持する配列

        this.currentQuestionIndex = 0; // 現在の質問のインデックス

        this.questionsContainer = document.getElementById('questions-container'); // 質問を表示するコンテナ
        this.nextButton = document.getElementById('next-button'); // 次へボタン
        this.nextButton.disabled = true; // 初期状態では「次へ」ボタンを無効にする
        this.finishMessage = document.getElementById('finish-message'); // 終了メッセージ
        this.cameraContainer = document.getElementById('camera-container'); // カメラキャプチャ画面

        this.cameraHandler = new CameraHandler('video', 'canvas', 'captured-image'); // カメラハンドラーのインスタンスを作成

        this.showStandardQuestion(this.currentQuestionIndex); // 最初の質問を表示
    }

    // 質問を表示するメソッド
    showStandardQuestion(index) {
        this.questionsContainer.innerHTML = ''; // コンテナをクリア

        if (this.standardQuestions[index] === 'image') {
            this.showCameraCapture(index);
        } else if (this.standardQuestions[index] === 'country' || this.standardQuestions[index] === 'mbti') {
            this.selectChoices(index);
        } else {
            // 新たなdiv要素を作成（グループ化するため）
            const questionDiv = document.createElement('div');
            questionDiv.className = 'question';

            // 新たなlabel要素を作成（質問文を表示するため）
            const questionLabel = document.createElement('label');
            questionLabel.textContent = `${this.showStandardQuestions[index]}:`;
            questionLabel.setAttribute('for', `answer-${index}`);

            // 新たなinput要素を作成（回答を入力するため）
            const questionInput = document.createElement('input');
            questionInput.type = 'text';
            questionInput.id = `answer-${index}`;
            questionInput.name = `answer-${index}`;

            // 入力フィールドにイベントリスナーを追加
            questionInput.addEventListener('input', () => this.checkInput(questionInput));

            // div要素に追加
            questionDiv.appendChild(questionLabel);
            questionDiv.appendChild(document.createElement('br'));
            questionDiv.appendChild(questionInput);
            this.questionsContainer.appendChild(questionDiv);
        }
    }

    showCustomQuestion(customIndex) {
        this.questionsContainer.innerHTML = ''; // コンテナをクリア
        this.cameraContainer.innerHTML = ''; // カメラコンテナをクリア
        this.cameraContainer.style.display = 'none'; // カメラコンテナを隠す
        this.questionsContainer.style.display = 'block'; // 質問コンテナを表示

        // 新たなdiv要素を作成（グループ化するため）
        const questionDiv = document.createElement('div');
        questionDiv.className = 'question';

        // 新たなlabel要素を作成（質問文を表示するため）
        const questionLabel = document.createElement('label');
        questionLabel.textContent = `New Question${customIndex + 1}:`;
        questionLabel.setAttribute('for', `custom-question-${customIndex}`);

        // 新たなselect要素を作成（選択式の質問）
        const questionSelect = document.createElement('select');
        questionSelect.id = `custom-question-${customIndex}`;
        questionSelect.name = `custom-question-${customIndex}`;

        // 選択肢を追加
        this.customQuestionChoices.forEach((choice, index) => {
            if (!this.customQuestionSelected[index]) {
                const option = document.createElement('option');
                option.value = choice;
                option.textContent = choice;
                questionSelect.appendChild(option);
            }
        });

        // 新たなlabel要素を作成（回答欄を表示するため）
        const answerLabel = document.createElement('label');
        answerLabel.textContent = `Answer${customIndex + 1}:`;
        answerLabel.setAttribute('for', `custom-answer-${customIndex}`);

        // 新たなinput要素を作成（回答を入力するため）
        const answerInput = document.createElement('input');
        answerInput.type = 'text';
        answerInput.id = `custom-answer-${customIndex}`;
        answerInput.name = `custom-answer-${customIndex}`;

        // 入力フィールドにイベントリスナーを追加
        answerInput.addEventListener('input', () => this.checkInput(answerInput));


        // div要素に追加
        questionDiv.appendChild(questionLabel);
        questionDiv.appendChild(questionSelect);
        questionDiv.appendChild(document.createElement('br'));
        questionDiv.appendChild(document.createElement('br'));
        questionDiv.appendChild(answerLabel);
        questionDiv.appendChild(answerInput);
        questionDiv.appendChild(document.createElement('br'));
        this.questionsContainer.appendChild(questionDiv);
    }


    // 次の質問に進むメソッド
    showNextQuestion() {
        this.nextButton.disabled = true;

         // カメラ起動中ならば，カメラを停止
         if (this.cameraHandler.cameraRunning){
            this.cameraHandler.stopCamera();
        }

        // 通常の質問時
        if (this.currentQuestionIndex < this.standardQuestionNum) {
            // 入力された値を取得し，保存
            if (this.standardQuestions[this.currentQuestionIndex] !== 'image') {
                const currentInput = document.getElementById(`answer-${this.currentQuestionIndex}`);
                // this.standardQuestionsInput.push(currentInput.value);
                this.standardQuestionsInput[this.currentQuestionIndex] = currentInput.value
            }

            // 現在の質問インデックスをインクリメント
            this.currentQuestionIndex++;

            // 次の質問がある場合
            if (this.currentQuestionIndex < this.standardQuestionNum) {
                // 次の質問を表示
                this.showStandardQuestion(this.currentQuestionIndex);
            }
            else {
                // 最初の追加質問を表示
                this.showCustomQuestion(0);
            }
        // 追加質問時
        } else {
            // 入力された値を取得し，保存
            const customIndex = this.currentQuestionIndex - this.standardQuestionNum;
            const customQuestion = document.getElementById(`custom-question-${customIndex}`);
            const customAnswer = document.getElementById(`custom-answer-${customIndex}`);
            this.customQuestions[customIndex] = customQuestion.value;

            this.customQuestionsInput[customIndex] = customAnswer.value;

            // 選択された質問がself.customQuestionChoiceのどのインデックスにあるかを特定
            const selectedQuestionIndex = this.customQuestionChoices.indexOf(customQuestion.value);

            // 質問を表示済みに設定
            if (selectedQuestionIndex !== -1) {
                this.customQuestionSelected[selectedQuestionIndex] = true;
            }

            this.currentQuestionIndex++;

            if (this.currentQuestionIndex - this.standardQuestionNum < this.customQuestionsNum) {
                this.showCustomQuestion(this.currentQuestionIndex - this.standardQuestionNum);
            } else {
                this.showFinishMessage();
            }
        }
    }

    // 終了メッセージを表示するメソッド
    showFinishMessage() {
        // 入力値確認（デバック用）
        console.log("通常の質問: ", this.standardQuestions)
        console.log("ユーザーが入力した値: ", this.standardQuestionsInput); // 全ての入力値を表示
        console.log("ユーザーが入力した追加質問: ", this.customQuestions); // 全ての追加質問を表示
        console.log("ユーザーが入力した追加質問の回答: ", this.customQuestionsInput); // 全ての追加質問の回答を表示

        this.nextButton.style.display = 'none'; // 次へボタンを隠す
        this.finishMessage.style.display = 'block'; // 終了メッセージを表示

        // Flaskにデータを送信
        this.sendQuestionnaire();
    }

    // Flaskに質問と回答をデータを送信するメソッド
    sendQuestionnaire() {
        // ローディングアクションを表示
        document.getElementById('loading-spinner').style.display = 'block';

        // 通常質問の質問と回答をオブジェクトに変換
        const standardQuestionsData = this.standardQuestions.reduce((acc, question, index) => {
            acc[question] = this.standardQuestionsInput[index] || ''; // 回答がない場合も空文字を設定
            return acc;
        }, {});

        // 追加質問の質問と回答をオブジェクトに変換
        const customQuestionsData = this.customQuestions.reduce((acc, question, index) => {
            acc[question] = this.customQuestionsInput[index] || ''; // 回答がない場合も空文字を設定
            return acc;
        }, {});

        // 最終的な送信データを構成
        const dataToSend = {
            group_name: this.groupName,
            ...standardQuestionsData,
            ...customQuestionsData
        };

        // コンソールに表示（デバッグ用）
        console.log("送信するデータ: ", dataToSend);

        // Flaskにデータを送信
        fetch('/questions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dataToSend)
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);

            // リダイレクト
            window.location.href = `/complete?name=${encodeURIComponent(data.name)}&group_name=${encodeURIComponent(data.group_name)}`;
        })
        .catch((error) => {
            console.error('Error:', error);
        })
        .finally(() => {
            // リダイレクト前にローディングスピナーを非表示にする（念のため）
            document.getElementById('loading-spinner').style.display = 'none';
        });
    }

    // カメラキャプチャ画面を表示するメソッド
    showCameraCapture(index) {
        // 質問コンテナをクリア
        this.questionsContainer.innerHTML = '';
        this.questionsContainer.style.display = 'none';

        this.cameraContainer.style.display = 'block';

        // Nextボタンを非表示にする
        this.nextButton.style.display = 'none';

        // キャプチャー画像を表示する要素を取得
        const capturedImage = document.getElementById('captured-image');
        capturedImage.style.display = 'none';

        // キャプチャー画像のラベルを取得し，非表示にする
        const capturedLabel = document.getElementById('captured-label');
        capturedLabel.style.display = 'none';
        

        // カメラを起動
        document.getElementById('onCamera-button').addEventListener('click', () => {
            this.cameraHandler.startCamera();
        });

        // 撮影後に次へボタンを表示する
        const nextButton = document.getElementById('next-button');
        nextButton.style.display = 'block';
        this.nextButton.disabled = true;

        // 撮影ボタンのクリックイベントリスナーを追加
        document.getElementById('capture-button').addEventListener('click', () => {
            const capturedDataUrl = this.cameraHandler.captureImage();
            // this.standardQuestionsInput.push(capturedDataUrl);
            this.standardQuestionsInput[index] = capturedDataUrl;
    
            // キャプチャー画像を表示する
            capturedImage.src = capturedDataUrl;
            capturedImage.style.display = 'block';

            // キャプチャー画像のラベルを表示する
            capturedLabel.style.display = 'block';

            this.nextButton.disabled = false; // 初期状態では「次へ」ボタンを無効にする
        });
    }

    selectChoices(index) {
        this.nextButton.disabled = false;

        // 新たなdiv要素を作成（グループ化するため）
        const questionDiv = document.createElement('div');
        questionDiv.className = 'question';

        // 新たなlabel要素を作成（質問文を表示するため）
        const questionLabel = document.createElement('label');
        questionLabel.textContent = `${this.showStandardQuestions[index]}:`;
        questionLabel.setAttribute('for', `answer-${index}`);

        // 新たなselect要素を作成（選択式の質問）
        const questionSelect = document.createElement('select');
        questionSelect.id = `answer-${index}`;
        questionSelect.name = `answer-${index}`;

        // 選択肢を追加
        let choices = [];
        if(this.standardQuestions[index] === 'country') {
            choices = ["Japan", "United States of America", "Canada", "Germany", "Australia", "India", "China", "United Kingdom"];
        } else if(this.standardQuestions[index] === 'mbti') {
            choices = ["INTJ", "INTP", "ENTJ", "ENTP", "INFJ", "INFP", "ENFJ", "ENFP", "ISTJ", "ISFJ", "ESTJ", "ESFJ", "ISTP", "ISFP", "ESTP", "ESFP"];
        }

        choices.forEach(choice => {
            const option = document.createElement('option');
            option.value = choice;
            option.textContent = choice;
            questionSelect.appendChild(option);
        });

        // div要素に追加
        questionDiv.appendChild(questionLabel);
        questionDiv.appendChild(document.createElement('br'));
        questionDiv.appendChild(questionSelect);
        this.questionsContainer.appendChild(questionDiv);
    }

    checkInput(currentInput) {
        // 現在表示されている質問のインデックスを取得
        // const currentQuestionId = `answer-${this.currentQuestionIndex}`;
        // const currentInput = document.getElementById(currentQuestionId);

        // 入力がある場合は「次へ」ボタンを有効にし、ない場合は無効にする
        if (currentInput && currentInput.value.trim() !== '') {
            this.nextButton.disabled = false;
        } else {
            this.nextButton.disabled = true;
        }
    }

}

// 質問の配列を定義
const STANDARD_QUESTIONS = [
    "name",
    "age",
    "country",
    "favorite_things",
    "mbti",
    "image"
];

const SHOW_STANDARD_QUESTIONS = [
    "Name",
    "Age",
    "Country",
    "Favorite Things",
    "MBTI"
];

const CUSTOM_QUESTION_CHOICES_ENG = [
    "How would you describe your personality in one word?",
    "If today were your last day, what would you do?",
    "Where would you like to travel?",
    "What's your favorite scent?",
    "If you could be any animal, what would you be?",
    "What would you do if you suddenly became a billionaire?",
    "Who is a famous person you admire?",
    "What's the biggest mistake you've ever made?",
    "What color represents you?",
    "When was the happiest moment of your life?",
    "When did you cry the most in your life?",
    "What would you want for your last meal?"
]

const CUSTOM_QUESTION_CHOICES = [
    "自分の性格を一言で表すと？",
    "もし今日が人生最後の日なら何をしますか？",
    "旅行するならどこがいい？",
    "好きな香りは何ですか？",
    "どんな動物に生まれ変わりたいですか？",
    "突然億万長者になったら何をしますか？",
    "尊敬する有名人は？",
    "人生で一番やらかしたことは何ですか？",
    "自分を色で例えると何ですか？",
    "人生で一番幸せだと感じた瞬間は？",
    "人生で一番泣いた出来事は？",
    "最後の晩餐は？"
    ];

const CUSTOM_QUESTIONS_NUM = 3; // 追加質問の数

// Questionnaireクラスのインスタンスを作成
const questionnaire = new Questionnaire(STANDARD_QUESTIONS, CUSTOM_QUESTIONS_NUM, GROUP_NAME, SHOW_STANDARD_QUESTIONS, CUSTOM_QUESTION_CHOICES);

// 次へボタンのクリックイベントリスナーを追加
document.getElementById('next-button').addEventListener('click', () => {
    questionnaire.showNextQuestion();
});