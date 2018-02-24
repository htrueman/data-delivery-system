export default class XhrSetup {
    /*
    Main class for XMLHttp requests.
     */
    constructor (method, path, isAsync=true) {
        this.method = method;
        this.path = path;
        this.isAsync = isAsync;

        this.xhr = new XMLHttpRequest();
        this.xhr.open(this.method, this.path, this.isAsync);
        this.setupCsrfToken();

        // send body template
        this.defaultBody = {
            data: '', // request data
            success: function (e) {}, // calls on request success
            error: function (e) {} // calls on request error
        };
    }
    send (body=this.defaultBody) {
        this.xhr.onload = function (progressEvent) {
            if (body.hasOwnProperty('success')) {
                body.success(progressEvent.target);
            }
        };
        this.xhr.onerror = function (progressEvent) {
            if (body.hasOwnProperty('error')) {
                body.error(progressEvent.target);
            }
        };

        this.xhr.send(body.data);
    }
    setRequestHeader (headerKey, headerValue) {
        this.xhr.setRequestHeader(headerKey, headerValue);
    }
    setupCsrfToken () {
        // From django docs

        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie != '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        const csrftoken = getCookie('csrftoken');

        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }

        function sameOrigin(url) {
            // test that a given url is a same-origin URL
            // url could be relative or scheme relative or absolute
            let host = document.location.host; // host + port
            let protocol = document.location.protocol;
            let sr_origin = '//' + host;
            let origin = protocol + sr_origin;
            // Allow absolute or scheme relative URLs to same origin
            return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
                (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
                // or any other URL that isn't scheme relative or absolute i.e relative.
                !(/^(\/\/|http:|https:).*/.test(url));
        }

        if (!csrfSafeMethod(this.method) && sameOrigin(this.path)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            this.xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
}
