const ws = new WebSocket(
    'ws:/127.0.0.1:8001/ws/check-git-clone-status?subscribe-broadcast');

ws.onmessage = (message) => {
    console.log("Received: ", message);

    const messageData = JSON.parse(message.data);
    const linkToUpdate = document.getElementsByClassName(`repo-link-${ messageData.id }`)[0];
    const statusToUpdate = document.getElementsByClassName(`repo-cloning-status-${ messageData.id }`)[0];

    if (messageData.type === 'success' && linkToUpdate && statusToUpdate) {
        const linkText = linkToUpdate.innerHTML;
        linkToUpdate.innerHTML = `
            <a href="${ repoManagerLinkBase.replace('0', messageData.id) }">
                ${ linkText }
            </a>`;
        statusToUpdate.innerHTML = '<i class="fa fa-check" style="font-size:16px;color:green;"></i> Cloned';
    }
    else if (messageData.type === 'fail' && statusToUpdate) {
        statusToUpdate.innerHTML = '<i class="fa fa-close" style="font-size:16px;color:red;"></i> Cloning failed';
    }
};

ws.onerror = (error) => {
    console.error(error);
};
