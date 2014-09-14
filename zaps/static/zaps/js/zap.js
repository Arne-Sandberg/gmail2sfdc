$(document).ready(function(){
    $("#gmail").click(function() {
        var authPopup = window.open('/auth/gmail-oauth', '_blank', 'width=500, height=500');
        pollPopupClose(authPopup)
    });

    $("#sfdc").click(function() {
        var authPopup = window.open('/auth/sfdc-oauth', '_blank', 'width=700, height=450');
        pollPopupClose(authPopup)
    });

    getMessages();
})

/*
 * as soon as the popup is closed, we need to refresh 'connect app' page to reflect changes
 * if user is giving permission for first time, popup redirects to gmail/salesforce site
 * due to cross domain, we can't detect window.unload in that case, so manually
 * polling oAuthPopUp close
 */
function pollPopupClose(popupWin) {
    var interval = window.setInterval(function () {
        if (popupWin == null || popupWin.closed) {
            window.clearInterval(interval);
            location.reload();
        }
    }, 1000);
}

//global list of messages
var msgList;

/**
 * gets all messages and renders on UI
 */
function getMessages() {
    $('.loader').removeClass('hide')
    $("#msgList").html('');
    $("#msgBody").html('');
    $("#msgAttachments").html('');
    var requestData = {
        query: $("#query").val()
    }
    $.getJSON('/zap/list', requestData, function(data) {
        $('.loader').addClass('hide')
        $("#msgList").html('');
        msgList = [];
        var msgIndex = 0;
        $.each(data, function(index, val) {
            var messages = val.messages;
            if (messages.length > 1) {
                // show first message in thread as heading
                // show reply messages indented under heading
                var threadHead = messages[0]
                msgList.push(threadHead)
                renderMessage(threadHead, msgIndex++)
                for(var i=1; i<messages.length; i++) {
                    msgList.push(messages[i])
                    renderSubMessage(messages[i], msgIndex++)
                }
            } else if (messages.length == 1){
                var message = messages[0];
                msgList.push(message)
                renderMessage(message, msgIndex++)
            }
        });
        if (msgList.length > 0) {
            showMessageContent(0);
        }

    })
    .fail(function(data) {
        //TODO: handle error. Timeout eems common if the query fetches too many results
    })
}

/**
 * renders the message on UI
 * @param message
 * @param index - index of the message in msgList
 */
function renderMessage(message, index) {
    var subject = getMessageHeaders(message)['Subject']
    if (subject) {
        var msgLink = "<br><a href='#' onclick='showMessageContent("+index+")'>"+subject+"</a><br>"
        $("#msgList").append(msgLink)
    }
    // subject will be undefined for chat messages, ignoring them for now
}

/**
 * renders the reply message on UI, indented under main message
 * @param message
 * @param index - index of the message in msgList
 */
function renderSubMessage(message, index) {
    var subject = getMessageHeaders(message)['Subject']
    if (subject) {
        var msgLink = "<a href='#' style='margin-left: 10px' onclick='showMessageContent(" + index + ")'>- " + subject + "</a><br>"
        $("#msgList").append(msgLink)
    }
    // subject will be undefined for chat messages, ignoring them for now
}

/**
 * returns a map of message headers
 * @param message
 * @return {{}}
 */
function getMessageHeaders(message) {
    var headers = {};
    $.each(message.headers, function(ix, header) {
        headers[header.name] = header.value;
    });
    return headers;
}

/**
 * showa message body and attachment in right pane
 * @param index
 */
function showMessageContent(index) {
    $("#msgBody").css('max-height', '')
    var message = msgList[index]
    //show body
    var content = message.content
    //first, try to get the html body
    var body = content.html_content
    //if html body is not present, show text body
    if (!body) {
        body = content.text_content
    }
    $("#msgBody").html(body)

    //show attachments
    $("#msgAttachments").html('');
    var attachments = content.attachments
    if (attachments && attachments.length > 0) {
        $("#msgBody").css('max-height', '300px')
        $("#msgAttachments").append("<br><br><b>Attachments:</b>")
        $.each(attachments, function(ix, att) {
            var dwnldParams = "id="+att.id+"&msgId="+message.id+"&fileName="+att.filename
            var attHtml = "<br><br>"+att.filename+"&nbsp;&nbsp;&nbsp;<a href='#' onClick='uploadAttachment(event, \"" +
                att.id+"\",\""+message.id+"\",\""+att.filename+"\")'>Upload to Salesforce</a>"
            $("#msgAttachments").append(attHtml)
        });
    }
}

function uploadAttachment(e, attId, msgId, fileName) {
    $(e.target).html('uploading...')
    var requestData = {
        'att_id': attId,
        'msg_id': msgId,
        'file_name': fileName
    }
    $.get('/zap/sfupload', requestData, function (data) {
        if (data == 'success') {
            $(e.target).html('uploaded')
        }
    })
    .fail(function(data) {
        $(e.target).html('Failed. Please try agan!!')
    })
}

