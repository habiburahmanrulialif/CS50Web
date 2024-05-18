document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

  // use button to send email
  document.querySelector('#compose-form').addEventListener('submit', sending_email);
});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#open-email').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#open-email').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  //fetch mailbox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      // Loop through enails and create a div for each
      emails.forEach(email => {

        console.log(email)

        // Create div for each email
        const newEmail = document.createElement('div');
        newEmail.innerHTML = `
        <div class="col-2 my-auto"><h6>Sender: ${email.sender}</h6></div>
        <div class="col-8 text-center my-auto"><h5>Subject: ${email.subject}</h5></div>
        <div class="col-2 my-auto"><p>${email.timestamp}</p></div>
        `;
        newEmail.className = "my-2 border row py-3 border"
        newEmail.className += email.read ? " read" : " unread"
        // Add click event to view email
        newEmail.addEventListener('click', function() {
          open_email(email.id)
        });
        document.querySelector('#emails-view').append(newEmail);
      });
  });
}

function open_email(id){
    // Show the email and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#open-email').style.display = 'block';

    // Checking if there's already an email open
    const test = document.querySelector('#email');
    if (test){
      // Clear window first before opening new email
      test.remove();
    }

    // fetch email base on id
    fetch(`emails/${id}`)
    .then(res => res.json())
    .then(email => {
      // Check archive status
      let archive_status = "";
      if (!email.archived){
        archive_status = "Archive";
      }
      else{
        archive_status = "Unarchive";
      }
      // Check if the sender the same as current user
      const currentUser = email.user;
      const archiveButton = currentUser === email.sender ? '' : `<button id="archive">${archive_status}</button>`;

      const newEmail =  document.createElement("div");
      newEmail.innerHTML = `
        <div class = ""><h3>${email.subject.toUpperCase()}</h3></div>
        <div class = ""><strong>Sender: ${email.sender}</strong></br>&nbsp&nbsp&nbsp&nbsp&nbsp Recepient: ${email.recipients}</br>&nbsp&nbsp&nbsp&nbsp&nbsp ${email.timestamp}<hr></div>
        <div class = "mx-auto" id="body">${email.body}</div>
        ${archiveButton}
        <button id="reply">Replay</button>
      `;
      newEmail.id = "email";
      document.querySelector('#open-email').append(newEmail);

      // Change email read
      if (!email.read){
        fetch(`emails/${id}`, {
          method: 'PUT',
          body: JSON.stringify({
              read: true
          })
        })
      }

      document.querySelector('#reply').addEventListener('click', () => {
        compose_email();

        document.querySelector('#compose-recipients').value = email['sender'];
        let subject = email['subject'];
        console.log(subject.split(" ", 1)[0]);
        if (subject.split(" ", 1)[0] != "Re:") {
          subject = "Re: " + subject;
        }

        document.querySelector('#compose-subject').value = subject;
        let body = `
          On ${email['timestamp']}, ${email['sender']} wrote: ${email['body']}
        `;
        document.querySelector('#compose-body').value = body;
      })

      document.querySelector('#archive').addEventListener('click', () => {
        if (email.archived){
          fetch(`emails/${id}`, {
            method: 'PUT',
            body: JSON.stringify({
              archived: false
            })
          })
        }
        else{
          fetch(`emails/${id}`, {
            method: 'PUT',
            body: JSON.stringify({
              archived: true
            })
          })
        }
        

        load_mailbox('inbox');
      })
    });
}

function sending_email(event){
  // Prevent submit even to send request to server
  event.preventDefault();

  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  // Posting email to server using API
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        "recipients": recipients,
        "subject": subject,
        "body": body
    }),
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
      load_mailbox('sent')
  });
}
