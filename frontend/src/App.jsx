import "./App.css";

import { useEffect, useState } from "react";
import axios from "axios";
import { Toaster } from "react-hot-toast";

import Sidebar from "./components/Sidebar";
import Chat from "./components/Chat";

function App() {

    const [files, setFiles] = useState([]);

    const [selectedFiles, setSelectedFiles] = useState([]);

    const refreshFiles = async () => {

        try {

            const response = await axios.get(
                "http://localhost:8000/files"
            );

            setFiles(response.data.files);

        }

        catch (error) {

            console.log(error);

        }

    };

    useEffect(() => {

        refreshFiles();

    }, []);

    return (

        <div className="app">

            <Toaster
                position="top-right"
                reverseOrder={false}
            />

            <Sidebar

                files={files}

                refreshFiles={refreshFiles}

                selectedFiles={selectedFiles}

                setSelectedFiles={setSelectedFiles}

            />

            <Chat

                selectedFiles={selectedFiles}

            />

        </div>

    );

}

export default App;