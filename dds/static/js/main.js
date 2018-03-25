const ws = new WebSocket(
    'ws:/127.0.0.1:8001/ws/check-git-clone-status?subscribe-broadcast');

ws.onmessage = (message) => {
    console.log("Received: " + message.data);

    const messageData = JSON.parse(message.data);
    const linkToUpdate = document.getElementsByClassName(`repo-link-${ messageData.id }`)[0];
    const statusToUpdate = document.getElementsByClassName(`repo-cloning-status-${ messageData.id }`)[0];
    if (messageData.type === 'success') {
        const linkText = linkToUpdate.text();
        linkToUpdate.html(`
            <a href="${ repoManagerLinkBase.replace('0', messageData.id) }">
                ${ linkText }
            </a>
        `);
        statusToUpdate.html('<i class="fa fa-check" style="font-size:16px;color:green;"></i> Cloned');
    }
    else if (messageData.type === 'fail') {
        statusToUpdate.html('<i class="fa fa-close" style="font-size:16px;color:red;"></i> Cloning failed');
    }
    console.log('here');
    ws.close();
};

ws.onerror = (error) => {
    console.error(error);
};
