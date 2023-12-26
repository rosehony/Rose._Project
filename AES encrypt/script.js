async function processFile(operation) {
    const fileInput = document.getElementById("fileInput");
    const encryptionKey = document.getElementById("encryptionKey");
    const statusMessage = document.getElementById("statusMessage");
    const loadingSpinner = document.getElementById("loadingSpinner");

    const file = fileInput.files[0];
    const key = encryptionKey.value;

    if (file && key) {
        loadingSpinner.style.display = "block";
        statusMessage.innerText = "";

        try {
            const response = await fetch(`/${operation}`, {
                method: "POST",
                body: createFormData(file, key),
            });

            if (!response.ok) {
                throw new Error(`${capitalize(operation)} failed: ${response.statusText}`);
            }

            const blob = await response.blob();
            downloadFile(blob, `${operation}_file.${getFileExtension(file)}`);
            statusMessage.innerText = `${capitalize(operation)} successful`;
        } catch (error) {
            statusMessage.innerText = `${capitalize(operation)} failed: ${error.message}`;
        } finally {
            loadingSpinner.style.display = "none";
        }
    } else {
        statusMessage.innerText = "Please select a file and enter an encryption key.";
    }
}

function createFormData(file, key) {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("key", key);
    return formData;
}

function downloadFile(blob, fileName) {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = fileName;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}

function getFileExtension(file) {
    const fileNameParts = file.name.split(".");
    return fileNameParts[fileNameParts.length - 1];
}

function capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

