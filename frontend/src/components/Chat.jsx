import { useEffect, useRef, useState } from "react";
import axios from "axios";
import { ClipLoader } from "react-spinners";
import Message from "./Message";

function Chat({ selectedFiles }) {

    const [question, setQuestion] = useState("");

    const [messages, setMessages] = useState([]);

    const [loading, setLoading] = useState(false);

    const bottomRef = useRef(null);

    useEffect(() => {

        bottomRef.current?.scrollIntoView({
            behavior: "smooth"
        });

    }, [messages, loading]);

    const askQuestion = async () => {

        if (question.trim() === "")
            return;

        const currentQuestion = question;

        setMessages(prev => [

            ...prev,

            {
                role: "user",
                content: currentQuestion
            }

        ]);

        setQuestion("");

        setLoading(true);

        try {

            const response = await axios.post(

                "http://localhost:8000/ask",

                {

                    question: currentQuestion,

                    filenames: selectedFiles

                }

            );

            setMessages(prev => [

                ...prev,

                {

                    role: "assistant",

                    content: response.data.answer,

                    sources: response.data.sources

                }

            ]);

        }

        catch (error) {

            setMessages(prev => [

                ...prev,

                {

                    role: "assistant",

                    content:

                        error.response?.data?.detail ||

                        "Unable to connect."

                }

            ]);

        }

        setLoading(false);

    };

    return (

        <div className="chat">

            <div className="messages">

                {

                    messages.length === 0 && (

                        <div className="welcome">

                            <h1>📚 StudyGPT</h1>

                            <p>

                                Upload your PDFs and ask anything.

                            </p>

                        </div>

                    )

                }

                {

                    messages.map((message, index) => (

                        <Message

                            key={index}

                            message={message}

                        />

                    ))

                }

                {

                    loading && (

                        <div className="thinking">

                            <ClipLoader size={22} />

                            <span>

                                StudyGPT is thinking...

                            </span>

                        </div>

                    )

                }

                <div ref={bottomRef}></div>

            </div>

            <div className="chat-input">

                <input

                    placeholder="Ask anything from your notes..."

                    value={question}

                    onChange={(e) =>

                        setQuestion(e.target.value)

                    }

                    onKeyDown={(e) => {

                        if (e.key === "Enter" && !loading)

                            askQuestion();

                    }}

                />

                <button

                    disabled={loading}

                    onClick={askQuestion}

                >

                    Send

                </button>

            </div>

        </div>

    );

}

export default Chat;