const ws = new WebSocket(
    'ws:/127.0.0.1:8001/ws/check-git-clone-status?subscribe-broadcast');

ws.onmessage = (message) => {
    console.log("Received: " + message.data);
    ws.close();
};

ws.onerror = (error) => {
    console.error(error);
};
