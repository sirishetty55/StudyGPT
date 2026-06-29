import Upload from "./Upload";
import PDFList from "./PDFList";

function Sidebar({
    files,
    refreshFiles,
    selectedFiles,
    setSelectedFiles
}) {

    return (

        <div className="sidebar">

            <h2>📚 StudyGPT</h2>

            <Upload
                refreshFiles={refreshFiles}
            />

            <h3>Uploaded PDFs</h3>

            <PDFList

                files={files}

                refreshFiles={refreshFiles}

                selectedFiles={selectedFiles}

                setSelectedFiles={setSelectedFiles}

            />

        </div>

    );

}

export default Sidebar;