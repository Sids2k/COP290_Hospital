// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', function() {
    // Get the question form element
    var questionForm = document.getElementById('question-form');

    // Add submit event listener to the question form
    questionForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent form submission

        // Get the question input value
        var questionInput = document.getElementById('question-input');
        var question = questionInput.value;

        // Clear the question input
        questionInput.value = '';

        // Create a new list item element to display the question
        var questionListItem = document.createElement('li');
        questionListItem.className = 'mb-3';
        questionListItem.textContent = question;

        // Append the question list item to the questions list
        var questionsList = document.getElementById('questions-list');
        questionsList.appendChild(questionListItem);
});
});