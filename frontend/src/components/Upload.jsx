import { useState } from "react";
import axios from "axios";
import { FaUpload } from "react-icons/fa";
import toast from "react-hot-toast";

function Upload({ refreshFiles }) {

    const [dragging, setDragging] = useState(false);

    const uploadFile = async (file) => {

        if (!file) return;

        const formData = new FormData();

        formData.append("file", file);

        try {

            const response = await axios.post(

                "http://localhost:8000/upload-pdf",

                formData,

                {

                    headers: {

                        "Content-Type": "multipart/form-data"

                    }

                }

            );

            toast.success(

                response.data.message ||

                "PDF Uploaded Successfully!"

            );

            refreshFiles();

        }

        catch (error) {

            console.log("UPLOAD ERROR:", error);

            console.log("RESPONSE:", error.response);

            console.log("DATA:", error.response?.data);

            toast.error(

                error.response?.data?.message ||

                error.message ||

                "Upload Failed"

            );

        }

    };

    const handleDrop = (e) => {

        e.preventDefault();

        setDragging(false);

        const file = e.dataTransfer.files[0];

        uploadFile(file);

    };

    return (

        <div

            className={

                dragging

                    ? "upload-card dragging"

                    : "upload-card"

            }

            onDragOver={(e) => {

                e.preventDefault();

                setDragging(true);

            }}

            onDragLeave={() => {

                setDragging(false);

            }}

            onDrop={handleDrop}

        >

            <label

                htmlFor="pdf-upload"

                style={{

                    cursor: "pointer",

                    width: "100%",

                    display: "block",

                    textAlign: "center"

                }}

            >

                <FaUpload size={38} />

                <h3>Upload PDF</h3>

                <p>Click or Drag & Drop</p>

            </label>

            <input

                id="pdf-upload"

                hidden

                type="file"

                accept=".pdf"

                onChange={(e) =>

                    uploadFile(e.target.files[0])

                }

            />

        </div>

    );

}

export default Upload;