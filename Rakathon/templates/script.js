// Get elements
const cameraIcon = document.getElementById('camera-icon');
const popupContainer = document.getElementById('popup-container');
const closePopupButton = document.getElementById('close-popup');
const uploadImageButton = document.getElementById('upload-image');
const generateImageButton = document.getElementById('generate-image');
const generateImageOptions = document.getElementById('generate-image-options');
const fileInput = document.createElement('input'); // Create a file input element

// Set the file input type to 'file'
fileInput.type = 'file';

// Create a function to show a success message
function showSuccessMessage(message) {
    const successMessage = document.createElement('p');
    successMessage.textContent = message;
    successMessage.style.color = '#4CAF50'; // Green color for success
    generateImageOptions.appendChild(successMessage);

    // Remove the success message after a delay (e.g., 3 seconds)
    setTimeout(() => {
        generateImageOptions.removeChild(successMessage);
    }, 3000); // 3000 milliseconds (3 seconds)
}

// Function to handle image upload
function handleImageUpload() {
    // Trigger the file input when the "Upload Image" button is clicked
    fileInput.click();
}

// Add click event listener to camera icon
cameraIcon.addEventListener('click', () => {
    // Show the popup
    popupContainer.style.display = 'flex';

    // Add animation class
    popupContainer.classList.add('popup-animation');
});

// Add click event listener to close button
closePopupButton.addEventListener('click', () => {
    // Hide the popup
    popupContainer.style.display = 'none';

    // Remove animation class (for future animations)
    popupContainer.classList.remove('popup-animation');
});

// Add click event listener to generate image button
generateImageButton.addEventListener('click', () => {
    // Show the generate image options
    generateImageOptions.style.display = 'block';
});

// Add click event listener to upload image button
uploadImageButton.addEventListener('click', handleImageUpload);

// Add change event listener to the file input
fileInput.addEventListener('change', (event) => {
    // Handle the selected file here (e.g., upload or process the image)
    const selectedFile = event.target.files[0];
    if (selectedFile) {
        // Display a success message when the image is uploaded
        showSuccessMessage('Image uploaded successfully!');
        // You can perform further actions with the selected file, such as uploading it to a server or processing it.
    }
});
