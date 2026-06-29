import ReactMarkdown from "react-markdown";
import { FaRobot, FaUser, FaFilePdf, FaCopy } from "react-icons/fa";

function Message({ message }) {

    const copyAnswer = () => {

        navigator.clipboard.writeText(message.content);

        alert("Copied!");

    };

    return (

        <div
            className={
                message.role === "user"
                    ? "user-message"
                    : "ai-message"
            }
        >

            {

                message.role === "assistant" && (

                    <div className="message-header">

                        <div className="ai-info">

                            <div className="avatar">

                                <FaRobot />

                            </div>

                            <div>

                                <strong>StudyGPT</strong>

                                <div className="time">

                                    {new Date().toLocaleTimeString([], {
                                        hour: "2-digit",
                                        minute: "2-digit"
                                    })}

                                </div>

                            </div>

                        </div>

                        <button
                            className="copy-btn"
                            onClick={copyAnswer}
                        >

                            <FaCopy />

                        </button>

                    </div>

                )

            }

            {

                message.role === "user" && (

                    <div className="message-header">

                        <div className="ai-info">

                            <div className="avatar user-avatar">

                                <FaUser />

                            </div>

                            <strong>You</strong>

                        </div>

                    </div>

                )

            }

            <ReactMarkdown>

                {message.content}

            </ReactMarkdown>

            {

                message.sources &&
                message.sources.length > 0 && (

                    <div className="source-container">

                        {

                            message.sources.map((file) => (

                                <div
                                    key={file}
                                    className="source-chip"
                                >

                                    <FaFilePdf />

                                    {file}

                                </div>

                            ))

                        }

                    </div>

                )

            }

        </div>

    );

}

export default Message;