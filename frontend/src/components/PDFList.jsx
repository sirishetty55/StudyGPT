import { useState } from "react";
import axios from "axios";
import { FaTrash } from "react-icons/fa";
import toast from "react-hot-toast";

function PDFList({
    files,
    refreshFiles,
    selectedFiles,
    setSelectedFiles
}) {

    const [search, setSearch] = useState("");

    const deleteFile = async (filename) => {

        if (!window.confirm(`Delete ${filename}?`))
            return;

        await axios.delete(
            `http://localhost:8000/files/${filename}`
        );

        refreshFiles();

        setSelectedFiles(prev =>
            prev.filter(file => file !== filename)
        );

    };

    const filteredFiles = files.filter(file =>
        file.toLowerCase().includes(
            search.toLowerCase()
        )
    );

    return (

        <>

            <input

                className="pdf-search"

                placeholder="🔍 Search PDFs..."

                value={search}

                onChange={(e)=>

                    setSearch(e.target.value)

                }

            />

            {

                filteredFiles.map(file=>(

                    <div

                        key={file}

                        className={
                            selectedFiles.includes(file)
                                ? "pdf-item selected"
                                : "pdf-item"
                        }

                        onClick={()=>{

                            if(selectedFiles.includes(file)){

                                setSelectedFiles(

                                    prev=>prev.filter(

                                        x=>x!==file

                                    )

                                );

                            }

                            else{

                                setSelectedFiles(

                                    prev=>[...prev,file]

                                );

                            }

                        }}

                    >

                        <span>

                            {file}

                        </span>

                        <FaTrash

                            className="delete-icon"

                            onClick={(e)=>{

                                e.stopPropagation();

                                deleteFile(file);

                            }}

                        />

                    </div>

                ))

            }

        </>

    );

}

export default PDFList;