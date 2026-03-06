document.addEventListener('DOMContentLoaded', () => {
    const promptInput = document.getElementById('prompt-input');
    const generateBtn = document.getElementById('generate-btn');
    const btnText = document.querySelector('.btn-text');
    const iconRegular = document.querySelector('.icon-regular');
    const iconLoading = document.querySelector('.icon-loading');
    const errorMessage = document.getElementById('error-message');

    const placeholderWrapper = document.getElementById('image-placeholder');
    const resultWrapper = document.getElementById('image-result');
    const generatedImg = document.getElementById('generated-img');
    const downloadBtn = document.getElementById('download-btn');

    // Make generate button clickable on Cmd/Ctrl + Enter
    promptInput.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            generateImage();
        }
    });

    generateBtn.addEventListener('click', generateImage);

    async function generateImage() {
        const prompt = promptInput.value.trim();

        if (!prompt) {
            showError("Vui lòng nhập mô tả cho bức ảnh (Please enter a prompt).");
            promptInput.focus();
            return;
        }

        // Reset UI
        hideError();
        setLoadingState(true);

        try {
            // Call our Local FastAPI backend
            const response = await fetch('http://127.0.0.1:8001/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ prompt: prompt })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || "Failed to generate image.");
            }

            // Get the image blob
            const imageBlob = await response.blob();
            const imageUrl = URL.createObjectURL(imageBlob);

            // Display Image
            displayImage(imageUrl);

        } catch (error) {
            console.error('Error generating image:', error);
            showError(`Lỗi (Error): ${error.message} \nĐảm bảo backend Local đang chạy và đã tải xong Model (Make sure local model is loaded).`);
            setLoadingState(false);
        }
    }

    function setLoadingState(isLoading) {
        if (isLoading) {
            promptInput.disabled = true;
            generateBtn.disabled = true;
            btnText.textContent = "Đang tạo... (Generating)";
            iconRegular.style.display = "none";
            iconLoading.style.display = "inline-block";

            // Add pulse animation to placeholder
            if (placeholderWrapper.style.display !== 'none') {
                placeholderWrapper.style.opacity = '0.5';
                placeholderWrapper.style.animation = 'pulse 1.5s infinite';
            }

            // If regenerating, hide old image and show placeholder
            if (resultWrapper.style.display === 'flex') {
                resultWrapper.style.display = 'none';
                placeholderWrapper.style.display = 'flex';
                placeholderWrapper.style.opacity = '0.5';
                placeholderWrapper.style.animation = 'pulse 1.5s infinite';
            }

        } else {
            promptInput.disabled = false;
            generateBtn.disabled = false;
            btnText.textContent = "Generate Image";
            iconRegular.style.display = "inline-block";
            iconLoading.style.display = "none";

            placeholderWrapper.style.opacity = '1';
            placeholderWrapper.style.animation = 'none';
        }
    }

    function displayImage(url) {
        generatedImg.src = url;

        // Hide placeholder, show image wrapper
        placeholderWrapper.style.display = 'none';
        resultWrapper.style.display = 'flex';

        // Setup download button
        downloadBtn.onclick = () => {
            const a = document.createElement('a');
            a.href = url;
            a.download = `dreamforge-${Date.now()}.jpg`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        };

        setLoadingState(false);
    }

    function showError(msg) {
        errorMessage.textContent = msg;
        errorMessage.style.display = 'block';
        setTimeout(() => {
            errorMessage.style.display = 'none';
        }, 8000);
    }

    function hideError() {
        errorMessage.style.display = 'none';
    }
});

// Add pulse animation dynamic style
const style = document.createElement('style');
style.innerHTML = `
    @keyframes pulse {
        0% { transform: scale(0.98); opacity: 0.5; }
        50% { transform: scale(1); opacity: 0.8; }
        100% { transform: scale(0.98); opacity: 0.5; }
    }
`;
document.head.appendChild(style);
