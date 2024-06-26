const promptInput = document.getElementById('prompt');
const sendBtn = document.getElementById('send-btn');
let planData;

// View re-loaded plans
document.querySelectorAll('.plan').forEach(function(planBtn) {
    planBtn.addEventListener('click', function() {
        const planID = planBtn.id.replace('plan', '');
        const modal = document.getElementById('modal' + planID);
        openModal(modal);
    });
});



// Add an input event listener to the input field
promptInput.addEventListener('input', function() {
    // Enable or disable the send button based on whether the input field has text
    if (promptInput.value.trim() !== '') {
        sendBtn.disabled = false;
    } else {
        sendBtn.disabled = true;
    }
});


function sendMessage() {
    var prompt = document.getElementById('prompt').value;
    addMessage('user', prompt);

    fetch('/home/openai', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({prompt: prompt})
    })
    .then(response => response.text())
    .then(data => {
        planData = data;
        addMessage('bot', data);
    })
    .catch(error => console.error('Error:', error));

    document.getElementById('prompt').value = '';
}


// Allows user to send message using 'Enter' key
document.getElementById('prompt').addEventListener('keydown', function(event) {
    if (event.keyCode === 13) {
        event.preventDefault();
        sendMessage();
    }
});


function addMessage(sender, message) {
    const chatContainer = document.getElementById('message-container');
    const messageElement = document.createElement('div');
    messageElement.classList.add('chat-message');
    messageElement.classList.add(sender + '-message');
    messageElement.innerText = message;

    if (sender == 'bot') {
        const bookmarkBtn = document.createElement('button');
        bookmarkBtn.classList.add('bookmark-btn');
        bookmarkBtn.innerText = 'Save';
        messageElement.appendChild(bookmarkBtn);

        bookmarkBtn.addEventListener('click', function() {
            const planContainer = document.getElementById('plan-container');
            const plan = document.createElement('button');
            plan.classList.add('plan');

            const modal = document.createElement('div');
            modal.classList.add('modal');

            plan.addEventListener('click', function() {
                openModal(modal);
            });

            const closeBtn = document.createElement('button');
            closeBtn.classList.add('close-btn');
            closeBtn.innerHTML = '&times;';
            closeBtn.addEventListener('click', function() {
                closeModal(modal);
            });

            const modalContent = document.createElement('div');
            modalContent.classList.add('modal-content');
            modalContent.innerText = message;

            modalContent.appendChild(closeBtn);
            modal.appendChild(modalContent);
            planContainer.appendChild(plan);
            planContainer.appendChild(modal);

            fetch('/dbapi/plans', {
                method: 'POST',  // Ensure this is set to 'POST'
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    courses: planData,
                    userID: '<firebase_user_id>'
                })
            })
            .then(response => response.text())
            .then(data => {
                console.log(data);
            })
            .catch(error => console.error('Error:', error));            
            
        });
    }
    chatContainer.appendChild(messageElement);
}


function openModal(modal) {
    modal.style.display = 'block';
}

function closeModal(modal) {
    modal.style.display = 'none';
}

window.onclick = function(event) {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(function(modal) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });
}