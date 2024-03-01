fetchGroup()

function getCSRFToken() {
    const selectElement = document.querySelector('input[name="csrfmiddlewaretoken"]');
    return selectElement.value;
}

function fetchGroup(){
    document.querySelector('#group-list').innerHTML = '';
    fetch('group', {
        method: 'GET',
        headers: {
        }
        })
    .then(response => response.json())
    .then(groups => {
        groups.forEach(group => {
            console.log(group)

        // Create div for each email
        const newGroup = document.createElement('div');

        const imagePath = '/static/chat/images/no-image.jpg';
        newGroup.innerHTML = `
        <div id="group-card">
            <div class="row g-0" id="group-content">
                <div class="col-md-2" id="group-image-container">
                    <img src="${imagePath}" id="group-image" alt="...">
                </div>
                <div class="col-md-10" id="group-info-container">
                    <h5 id="group-info-title">${group.group_name}</h5>
                    <p id="group-info-member">Member : </p>
                </div>
            </div>
        </div>
        `;

        // Selecting the group-info-member element
        const groupInfoMember = newGroup.querySelector('#group-info-member');
        
        // Iterate over group members and append them to group-info-member
        group.group_member.forEach((member, index) => {
            const memberElement = document.createElement('span');
            memberElement.textContent = member;
        
            // Add comma for non-last members
            if (index < group.group_member.length - 1) {
                memberElement.textContent += ', ';
            }
        
            groupInfoMember.appendChild(memberElement);
        });

        newGroup.addEventListener('click', function() {
            fetchChat(group.group_name);
            changeGroupName(group.group_name, group.group_member);
            });
        document.querySelector('#group-list').append(newGroup);

        });
    })
    .catch(error => console.error('Error:', error));
}

function fetchChat(groupName){
    fetch(`group/${groupName}`, {
        method: 'GET',
        headers: {
        }
        })
    .then(response => response.json())
    .then(chats => {
        const messageContainer = document.querySelector('#message-data');
        messageContainer.textContent= "";
        const firstChatNode = messageContainer.firstChild;
        chats.forEach(chat => {
            console.log(chat)
            const isCurrentUser = chat.sender === currentUser; // Change 'username' to the appropriate field if needed

            // Create div for each email
            const newChat = document.createElement('div');
            if (isCurrentUser) {
                newChat.classList.add('message-list-owner');
            } else {
                newChat.classList.add('message-list-not-owner');
            }
            newChat.innerHTML = `
                <div class="message-container">
                    <div class="message-sender">
                        ~ ${chat.sender}
                    </div>
                    <div class="message-content">
                        ${chat.message}
                    </div>
                </div>
            `;

            messageContainer.insertBefore(newChat, firstChatNode);
        });
    })
    .catch(error => console.error('Error:', error));
}

function changeGroupName(groupName, groupMember){
    const groupTitle = document.getElementById("group-title");
    const group_Member = document.getElementById("group-member");
    group_Member.textContent = "";
    changeSendBtn(groupName);
    groupTitle.textContent = groupName;

    groupMember.forEach((member, index) => {
        const memberElement = document.createElement('span');
        memberElement.textContent = member;
    
        // Add comma for non-last members
        if (index < groupMember.length - 1) {
            memberElement.textContent += ', ';
        }
    
        group_Member.appendChild(memberElement);
    });
}

function clearForm(){
    document.getElementById("groupNameInput").value = '';
    const newMessage = document.getElementById("message-form-text").value = '';
}

function openForm(){
    document.getElementById("myForm").style.display = "block";
    clearForm();
}

function closeForm(){
    document.getElementById("myForm").style.display = "none";
    clearForm();
}

function newGroup(){
    const groupNameInput = document.getElementById("groupNameInput").value;
    var data = {
        group_name : groupNameInput
    }

    fetch("group/create", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        clearForm();
        if (response.ok) {
            // Handle success response
            console.log("Group created successfully.");
            closeForm();
            fetchGroup();
            // You can redirect or show a success message here
        } else {
            // Handle error response
            console.error("Error creating group.");
            // You can display an error message here
        }
        clearForm()
    })
    .catch(error => {
        console.error("Error:", error);
    });
}

function sendMessage(groupName){
    const newMessage = document.getElementById("message-form-text").value;
    var data = {
        content : newMessage
    }
    fetch(`group/${groupName}/newMessage`, {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()
        },
        body: JSON.stringify(data)
        })
        .then(response => {
            clearForm();
            if (response.ok) {
                // Handle success response
                console.log("Group created successfully.");
                closeForm();
                fetchGroup();
                // You can redirect or show a success message here
            } else {
                // Handle error response
                console.error("Error creating group.");
                // You can display an error message here
            }
            clearForm()
        })
        .catch(error => {
            console.error("Error:", error);
        });
}

function changeSendBtn(groupName) {
    const formBtn = document.getElementById("message-form-button");

    // Remove any existing click event listener
    formBtn.removeEventListener('click', formBtn.clickEvent);

    // Add a new click event listener
    formBtn.clickEvent = function() {
        sendMessage(groupName);
    };

    formBtn.addEventListener('click', formBtn.clickEvent);
}