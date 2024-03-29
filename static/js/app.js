const fileUpload = document.querySelector("#file-upload")
const fileNameLabel = document.querySelector("#file-name")
fileUpload.addEventListener("change", function (e) {
    fileNameLabel.textContent = extractFilename(fileUpload.value)
})
function extractFilename(path) {
    if (path.substr(0, 12) == "C:\\fakepath\\")
        return path.substr(12); // modern browser
    var x;
    x = path.lastIndexOf('/');
    if (x >= 0) // Unix-based path
        return path.substr(x + 1);
    x = path.lastIndexOf('\\');
    if (x >= 0) // Windows-based path
        return path.substr(x + 1);
    return path; // just the filename
}