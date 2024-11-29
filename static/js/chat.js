export async function fetchData(url, options = {}) {
    try {
        const response = await fetch(url, options);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching data:', error);
        return null;
    }
}

function sendMessage() {
    let input = document.getElementById('chat_input_message');
    let inputText = input.value
    if (inputText === undefined || inputText === '') {
        return
    }
    let content = document.getElementById("chat_message_content");
    let message = createChatMessage(0, inputText)
    content.appendChild(message)
    fetchData('/chat/send', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            message: inputText
        })
    }).then(resp => {
        if (resp.code === 0 && resp.data) {
            replyMessage(resp.data.reply_message)
        } else {
            console.log("send message error, ", resp)
        }
    })
    console.log("发送消息：" + inputText)
    input.value = ''
}

function replyMessage(text) {
    console.log('回复消息:' + text)
    let content = document.getElementById("chat_message_content");
    let message = createChatMessage(1, text)
    content.appendChild(message)
}

function createMessageAvatar(className, srcUrl) {
    let avatar = document.createElement('img')
    avatar.setAttribute('class', className)
    avatar.setAttribute('src', srcUrl)
    avatar.setAttribute('alt', className)
    return avatar
}

/**
 * fromRole: 0 发送者 1回复者
 */
function createChatMessage(fromRole, messageText) {
    let message = document.createElement('div')
    let avatar;
    if (fromRole === 0) {
        message.setAttribute('class', 'send_message')
        avatar = createMessageAvatar('from_avatar', '../static/meta/sender_avatar.png');
    } else {
        message.setAttribute('class', 'reply_message')
        avatar = createMessageAvatar('to_avatar', '../static/meta/healer_avatar.png');
    }
    let inputText = document.createElement('div')
    inputText.setAttribute('class', 'message_bubble')
    inputText.append(messageText)
    message.appendChild(avatar)
    message.appendChild(inputText)
    return message
}
